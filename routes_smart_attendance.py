"""
Intelligent attendance routes - Smart face recognition attendance
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from models import db, AttendanceRecord, User, TeacherStudent
from jwt_utils import token_required
from face_recognition_module import get_face_engine
import uuid

# Create blueprint
smart_attendance_bp = Blueprint('smart_attendance', __name__, url_prefix='/api/smart-attendance')

# Configuration
UPLOAD_FOLDER = 'uploads/classroom_photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

# Create upload folder
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@smart_attendance_bp.route('/upload-and-recognize', methods=['POST'])
@token_required
def upload_and_recognize(payload):
    """
    Upload classroom photo and perform face recognition
    
    Request:
    - file: Image file
    - class_id: (optional) Class ID for attendance
    - date: (optional) Attendance date
    
    Response:
    {
        "code": 200,
        "message": "Recognition completed",
        "data": {
            "total_faces": 5,
            "recognized_count": 4,
            "recognition_rate": 80.0,
            "students": [
                {
                    "student_id": 1,
                    "student_name": "John Doe",
                    "confidence": 95.5
                },
                ...
            ],
            "image_url": "/path/to/result/image.jpg"
        }
    }
    """
    try:
        teacher_id = payload.get('user_id')
        
        # Check if file is uploaded
        if 'file' not in request.files:
            return jsonify({
                'code': 400,
                'message': 'No image file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'code': 400,
                'message': 'No image file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'code': 400,
                'message': 'File type not allowed. Use png, jpg, jpeg, or bmp'
            }), 400
        
        # Save uploaded file
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Get face recognition engine
        face_engine = get_face_engine()
        
        # Perform recognition
        recognition_result = face_engine.recognize_faces_in_image(filepath)
        
        if recognition_result['status'] != 'success':
            return jsonify({
                'code': 500,
                'message': recognition_result['message']
            }), 500
        
        # Draw result image
        result_image_path = face_engine.draw_recognition_result(
            filepath,
            recognition_result,
            os.path.join(UPLOAD_FOLDER, f"result_{uuid.uuid4()}.jpg")
        )
        
        # Prepare response
        students_data = []
        for student_info in recognition_result['recognized_students']:
            students_data.append({
                'student_id': student_info['student_id'],
                'student_name': student_info['student_name'],
                'confidence': student_info['confidence']
            })
        
        return jsonify({
            'code': 200,
            'message': 'Recognition completed',
            'data': {
                'total_faces': recognition_result['face_count'],
                'recognized_count': recognition_result['recognized_count'],
                'recognition_rate': recognition_result['recognition_rate'],
                'students': students_data,
                'image_url': f"/uploads/classroom_photos/{os.path.basename(result_image_path)}" if result_image_path else None,
                'original_image': f"/uploads/classroom_photos/{filename}"
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Error: {str(e)}'
        }), 500


@smart_attendance_bp.route('/record-attendance', methods=['POST'])
@token_required
def record_attendance(payload):
    """
    Record attendance based on recognition results
    
    Request:
    {
        "students": [
            {
                "student_id": 1,
                "attendance_status": "present" or "absent",
                "confidence": 95.5
            },
            ...
        ],
        "class_id": 1,
        "attendance_date": "2025-12-07",
        "notes": "Recorded via smart attendance"
    }
    """
    try:
        teacher_id = payload.get('user_id')
        data = request.get_json() or {}
        
        students = data.get('students', [])
        class_id = data.get('class_id')
        attendance_date = data.get('attendance_date', datetime.now().strftime('%Y-%m-%d'))
        notes = data.get('notes', 'Smart face recognition attendance')
        
        if not students:
            return jsonify({
                'code': 400,
                'message': 'No students provided'
            }), 400
        
        # Validate students
        recorded_data = []
        for student_data in students:
            try:
                student_id = student_data.get('student_id')
                status = student_data.get('attendance_status', 'present')
                confidence = student_data.get('confidence', 0)
                
                # Check if student belongs to teacher
                relationship = TeacherStudent.query.filter_by(
                    teacher_id=teacher_id,
                    student_id=student_id,
                    deleted_at=None
                ).first()
                
                if relationship:
                    # Get student info
                    student = User.query.get(student_id)
                    if student:
                        recorded_data.append({
                            'student_id': student_id,
                            'student_name': student.fullname,
                            'status': status,
                            'confidence': confidence,
                            'attendance_date': attendance_date,
                            'notes': f"{notes} (Confidence: {confidence}%)"
                        })
            except Exception as e:
                print(f"Error processing student {student_data.get('student_id')}: {str(e)}")
                continue
        
        return jsonify({
            'code': 200,
            'message': f'Attendance data collected for {len(recorded_data)} students',
            'data': {
                'recorded_count': len(recorded_data),
                'total_count': len(students),
                'attendance_records': recorded_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Error: {str(e)}'
        }), 500


@smart_attendance_bp.route('/add-student-face', methods=['POST'])
@token_required
def add_student_face(payload):
    """
    Add student face to recognition database
    
    Request:
    - file: Image file containing student's face
    - student_id: Student ID
    - student_name: Student name (optional)
    """
    try:
        teacher_id = payload.get('user_id')
        
        if 'file' not in request.files:
            return jsonify({
                'code': 400,
                'message': 'No image file provided'
            }), 400
        
        file = request.files['file']
        student_id = request.form.get('student_id')
        student_name = request.form.get('student_name')
        
        if not student_id or not student_name:
            return jsonify({
                'code': 400,
                'message': 'student_id and student_name are required'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'code': 400,
                'message': 'File type not allowed'
            }), 400
        
        # Verify student belongs to teacher
        relationship = TeacherStudent.query.filter_by(
            teacher_id=teacher_id,
            student_id=int(student_id),
            deleted_at=None
        ).first()
        
        if not relationship:
            return jsonify({
                'code': 403,
                'message': 'Student does not belong to this teacher'
            }), 403
        
        # Save temporary file
        filename = secure_filename(f"temp_{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Add to face database
        face_engine = get_face_engine()
        success = face_engine.add_student_face(int(student_id), student_name, filepath)
        
        # Clean up temporary file
        try:
            os.remove(filepath)
        except:
            pass
        
        if success:
            return jsonify({
                'code': 200,
                'message': f'Face added for {student_name}'
            }), 200
        else:
            return jsonify({
                'code': 500,
                'message': 'Failed to add face'
            }), 500
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Error: {str(e)}'
        }), 500


@smart_attendance_bp.route('/statistics', methods=['GET'])
@token_required
def get_smart_attendance_statistics(payload):
    """
    Get smart attendance statistics for teacher
    """
    try:
        teacher_id = payload.get('user_id')
        
        # Get attendance statistics
        total_records = AttendanceRecord.query.filter_by(
            teacher_id=teacher_id
        ).count()
        
        present_count = AttendanceRecord.query.filter_by(
            teacher_id=teacher_id,
            status='present'
        ).count()
        
        absent_count = AttendanceRecord.query.filter_by(
            teacher_id=teacher_id,
            status='absent'
        ).count()
        
        late_count = AttendanceRecord.query.filter_by(
            teacher_id=teacher_id,
            status='late'
        ).count()
        
        return jsonify({
            'code': 200,
            'message': 'Statistics retrieved',
            'data': {
                'total_records': total_records,
                'present_count': present_count,
                'absent_count': absent_count,
                'late_count': late_count,
                'attendance_rate': round(present_count / total_records * 100, 2) if total_records > 0 else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Error: {str(e)}'
        }), 500


@smart_attendance_bp.route('/attendance-records', methods=['GET'])
@token_required
def get_attendance_records(payload):
    """
    Get attendance records for teacher
    """
    try:
        teacher_id = payload.get('user_id')
        
        records = AttendanceRecord.query.filter_by(
            teacher_id=teacher_id
        ).order_by(AttendanceRecord.created_at.desc()).limit(100).all()
        
        records_data = []
        for record in records:
            student = User.query.get(record.student_id)
            records_data.append({
                'id': record.id,
                'student_id': record.student_id,
                'student_name': student.fullname if student else 'Unknown',
                'status': record.status,
                'confidence': record.notes.split('Confidence: ')[-1].replace('%)', '') if 'Confidence:' in (record.notes or '') else None,
                'created_at': record.created_at.isoformat() if record.created_at else None
            })
        
        return jsonify({
            'code': 200,
            'message': 'Records retrieved',
            'data': records_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Error: {str(e)}'
        }), 500


@smart_attendance_bp.route('/student-faces/<int:student_id>', methods=['GET'])
@token_required
def get_student_faces(payload, student_id):
    """
    Get all face images for a specific student
    """
    try:
        teacher_id = payload.get('user_id')
        
        # Verify student belongs to teacher
        relationship = TeacherStudent.query.filter_by(
            teacher_id=teacher_id,
            student_id=student_id,
            deleted_at=None
        ).first()
        
        if not relationship:
            return jsonify({
                'code': 403,
                'message': 'Student does not belong to this teacher'
            }), 403
        
        # Get face images from face engine
        face_engine = get_face_engine()
        
        faces_data = []
        if student_id in face_engine.known_faces:
            for face_info in face_engine.known_faces[student_id]:
                face_path = face_info.get('face_path', '')
                if os.path.exists(face_path):
                    # Convert absolute path to relative URL
                    relative_path = face_path.replace('\\', '/').replace('face_database/', '')
                    faces_data.append({
                        'student_id': student_id,
                        'student_name': face_info.get('student_name', ''),
                        'image_url': f'/face_database/{relative_path}',
                        'face_path': face_path,  # 保留原始路径用于删除
                        'added_at': face_info.get('added_at', '')
                    })
        
        return jsonify({
            'code': 200,
            'message': 'Face images retrieved',
            'data': faces_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Error: {str(e)}'
        }), 500


@smart_attendance_bp.route('/delete-student-face', methods=['POST'])
@token_required
def delete_student_face(payload):
    """
    Delete a student's face image
    
    Request:
    {
        "student_id": 1,
        "face_path": "face_database/1/student_name_timestamp.jpg"
    }
    """
    try:
        teacher_id = payload.get('user_id')
        data = request.get_json() or {}
        
        print(f"🔍 Delete face request data: {data}")  # 调试日志
        
        student_id = data.get('student_id')
        face_path = data.get('face_path')
        
        print(f"🔍 student_id: {student_id}, face_path: {face_path}")  # 调试日志
        
        # 确保student_id和face_path都存在且不为空
        if student_id is None or face_path is None or student_id == '' or face_path == '':
            print(f"❌ 参数验证失败: student_id={student_id}, face_path={face_path}")  # 调试日志
            return jsonify({
                'code': 400,
                'message': 'student_id and face_path are required'
            }), 400
        
        # Verify student belongs to teacher
        relationship = TeacherStudent.query.filter_by(
            teacher_id=teacher_id,
            student_id=int(student_id),
            deleted_at=None
        ).first()
        
        if not relationship:
            return jsonify({
                'code': 403,
                'message': 'Student does not belong to this teacher'
            }), 403
        
        # Delete face file
        if os.path.exists(face_path):
            try:
                os.remove(face_path)
                # Find and delete corresponding pickle file
                pkl_dir = os.path.dirname(face_path)
                for pkl_file in os.listdir(pkl_dir):
                    if pkl_file.endswith('.pkl'):
                        pkl_path = os.path.join(pkl_dir, pkl_file)
                        try:
                            os.remove(pkl_path)
                        except:
                            pass
                
                # Reload face database
                face_engine = get_face_engine()
                face_engine.load_known_faces()
                
                return jsonify({
                    'code': 200,
                    'message': 'Face deleted successfully'
                }), 200
            except Exception as e:
                return jsonify({
                    'code': 500,
                    'message': f'Failed to delete face: {str(e)}'
                }), 500
        else:
            return jsonify({
                'code': 404,
                'message': 'Face file not found'
            }), 404
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'Error: {str(e)}'
        }), 500
