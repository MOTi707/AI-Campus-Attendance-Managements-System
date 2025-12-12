"""
Simplified Face Recognition Module using PIL
For classroom attendance through face recognition
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path
import pickle
from datetime import datetime
from typing import List, Dict
import random

class FaceRecognitionEngine:
    """Simplified face recognition engine"""
    
    def __init__(self, face_db_path='face_database'):
        """Initialize face recognition engine"""
        self.face_db_path = Path(face_db_path)
        self.face_db_path.mkdir(exist_ok=True)
        
        # Face data cache
        self.known_faces = {}
        self.load_known_faces()
    
    def add_student_face(self, student_id: int, student_name: str, image_path: str) -> bool:
        """Add student face to database"""
        try:
            # Read and validate image
            image = Image.open(image_path)
            image.verify()
            image = Image.open(image_path)  # Reopen after verify
            
            # Convert RGBA to RGB if necessary (for PNG with transparency)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create student directory
            student_dir = self.face_db_path / str(student_id)
            student_dir.mkdir(exist_ok=True)
            
            # Save image and create face record
            filename = f"{student_name}_{datetime.now().timestamp()}.jpg"
            face_path = student_dir / filename
            image.save(face_path, 'JPEG', quality=95)
            
            # Create metadata
            metadata = {
                'student_id': student_id,
                'student_name': student_name,
                'face_path': str(face_path),
                'added_at': datetime.now().isoformat()
            }
            
            metadata_file = student_dir / f"{student_name}_{datetime.now().timestamp()}.pkl"
            with open(metadata_file, 'wb') as f:
                pickle.dump(metadata, f)
            
            print(f"Added face for {student_name} (ID: {student_id})")
            self.load_known_faces()
            return True
            
        except Exception as e:
            print(f"Failed to add face: {str(e)}")
            return False
    
    def load_known_faces(self):
        """Load known faces from database"""
        self.known_faces = {}
        
        if not self.face_db_path.exists():
            return
        
        for student_dir in self.face_db_path.iterdir():
            if not student_dir.is_dir():
                continue
            
            try:
                student_id = int(student_dir.name)
                faces_list = []
                
                for pkl_file in student_dir.glob('*.pkl'):
                    with open(pkl_file, 'rb') as f:
                        metadata = pickle.load(f)
                        faces_list.append(metadata)
                
                if faces_list:
                    self.known_faces[student_id] = faces_list
                    
            except Exception as e:
                print(f"Error loading faces for {student_dir}: {str(e)}")
        
        print(f"Loaded {len(self.known_faces)} students with faces")
    
    def recognize_faces_in_image(self, image_path: str) -> Dict:
        """
        Simulate face recognition in image
        In production, use actual face recognition library
        """
        try:
            # Open image
            image = Image.open(image_path)
            width, height = image.size
            
            # Simulate detecting multiple faces
            num_faces = random.randint(3, 8)
            face_locations = []
            
            for i in range(num_faces):
                x1 = random.randint(50, width - 150)
                y1 = random.randint(50, height - 150)
                x2 = x1 + random.randint(80, 120)
                y2 = y1 + random.randint(100, 150)
                face_locations.append((y1, x2, y2, x1))
            
            # Match with known faces
            recognized_students_dict = {}  # 用于存储每个学生的最高置信度
            student_ids = list(self.known_faces.keys())
            
            for idx, face_location in enumerate(face_locations):
                if student_ids and random.random() < 0.75:  # 75% recognition rate
                    student_id = random.choice(student_ids)
                    student_info = self.known_faces[student_id][0]
                    confidence = round(random.uniform(85, 99), 2)
                    
                    # 只保留每个学生的最高置信度
                    if student_id not in recognized_students_dict or confidence > recognized_students_dict[student_id]['confidence']:
                        recognized_students_dict[student_id] = {
                            'student_id': student_id,
                            'student_name': student_info['student_name'],
                            'confidence': confidence,
                            'face_location': {
                                'top': int(face_location[0]),
                                'right': int(face_location[1]),
                                'bottom': int(face_location[2]),
                                'left': int(face_location[3])
                            }
                        }
            
            recognized_students = list(recognized_students_dict.values())
            
            return {
                'status': 'success',
                'message': 'Recognition complete',
                'recognized_students': recognized_students,
                'face_count': len(face_locations),
                'recognized_count': len(recognized_students),
                'recognition_rate': round(len(recognized_students) / len(face_locations) * 100, 2) if face_locations else 0
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Recognition failed: {str(e)}',
                'recognized_students': [],
                'face_count': 0,
                'recognized_count': 0
            }
    
    def draw_recognition_result(self, image_path: str, recognition_result: Dict, output_path: str = None) -> str:
        """Draw recognition result on image"""
        try:
            from PIL import ImageFont
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            
            # Try to load font for better text rendering
            try:
                # Windows Chinese font
                font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = None  # Use default font
            
            # Draw boxes for recognized faces
            for student in recognition_result.get('recognized_students', []):
                loc = student['face_location']
                top, right, bottom, left = loc['top'], loc['right'], loc['bottom'], loc['left']
                
                # Draw rectangle (green color, thicker line)
                draw.rectangle([left, top, right, bottom], outline='#00FF00', width=3)
                
                # Draw text label
                label = f"{student['student_name']} ({student['confidence']}%)"
                
                # Calculate text size
                if font:
                    bbox = draw.textbbox((0, 0), label, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                else:
                    text_width = len(label) * 10
                    text_height = 20
                
                # Draw text background
                text_bg_top = max(0, top - text_height - 10)
                draw.rectangle(
                    [left, text_bg_top, left + text_width + 10, top],
                    fill='#00FF00'
                )
                
                # Draw text
                if font:
                    draw.text((left + 5, text_bg_top + 5), label, fill='white', font=font)
                else:
                    draw.text((left + 5, text_bg_top + 5), label, fill='white')
            
            # Save result
            if output_path is None:
                output_dir = Path('temp_recognition_results')
                output_dir.mkdir(exist_ok=True)
                output_path = str(output_dir / f"recognition_{datetime.now().timestamp()}.jpg")
            
            image.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Failed to draw result: {str(e)}")
            return None


# Global instance
face_engine = None

def get_face_engine():
    """Get global face recognition engine instance"""
    global face_engine
    if face_engine is None:
        face_engine = FaceRecognitionEngine()
    return face_engine
