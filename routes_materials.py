"""
资料管理路由 - 处理文件上传和自动分类
使用Jieba进行文本分析、关键词提取和智能分类
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import mimetypes
from models import db, Document, User
from jwt_utils import token_required
from nlp_utils import AutoClassifier

# 创建蓝图
materials_bp = Blueprint('materials', __name__, url_prefix='/api/materials')

# 配置
UPLOAD_FOLDER = 'uploads/documents'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'pptx', 'txt', 'xls', 'xlsx'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# 创建上传文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 初始化分类器
auto_classifier = AutoClassifier()


def allowed_file(filename):
    """检查文件扩展名"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@materials_bp.route('/upload', methods=['POST'])
@token_required
def upload_document(payload):
    """
    上传文档
    请求体: 
    {
        "file": 二进制文件,
        "title": "文档标题",
        "description": "文档描述"
    }
    """
    try:
        teacher_id = payload.get('user_id')
        
        # 检查文件是否存在
        if 'file' not in request.files:
            return jsonify({'code': 400, 'message': '没有找到文件'}), 400
        
        file = request.files['file']
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        
        if file.filename == '':
            return jsonify({'code': 400, 'message': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'code': 400,
                'message': '不支持的文件类型，允许: ' + ', '.join(ALLOWED_EXTENSIONS)
            }), 400
        
        # 检查文件大小
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'code': 400, 'message': '文件过大，最大50MB'}), 400
        
        # 保存文件
        # 在secure_filename之前先提取扩展名，以保留原始扩展名
        if '.' not in file.filename:
            return jsonify({
                'code': 400,
                'message': '文件必须有扩展名'
            }), 400
        
        # 分离文件名和扩展名
        original_parts = file.filename.rsplit('.', 1)
        original_name_without_ext = original_parts[0]
        file_ext = original_parts[1].lower()
        
        # 对文件名部分进行安全处理，但保留扩展名
        safe_name = secure_filename(original_name_without_ext)
        if not safe_name:
            safe_name = 'document'
        
        # 重新组合文件名
        original_filename = f"{safe_name}.{file_ext}"
        
        # 如果没有手动输入标题，则使用原始文件名作为标题
        if not title:
            title = safe_name
        
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        new_filename = f"{teacher_id}_{timestamp}_{original_filename}"
        filepath = os.path.join(UPLOAD_FOLDER, new_filename)
        
        file.save(filepath)
        
        # 读取文件内容用于分类（仅支持文本形式）
        file_content = ''
        if file_ext == 'txt':
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='gb2312') as f:
                        file_content = f.read()
                except:
                    file_content = ''
            except:
                file_content = ''
        
        # 使用NLP进行自动分类
        classification = auto_classifier.classify_document(
            file_content, 
            title=title, 
            description=description
        )
        
        # 置信度乘以3，但不超过100%
        confidence_score = min(classification['confidence_score'] * 15, 1.0)
        
        # 如果没有手动输入标题，则使用原始文件名作为标题
        if not title:
            title = safe_name
        
        # 创建数据库记录
        document = Document(
            teacher_id=teacher_id,
            filename=new_filename,
            original_name=original_filename,
            file_path=filepath,
            file_size=file_size,
            file_type=file_ext,
            title=title,
            description=description,
            category=classification['category'],
            sub_category=classification['sub_category'],
            confidence_score=confidence_score,
            is_auto_classified=True
        )
        
        # 设置关键词和标签
        document.set_keywords(classification['keywords'])
        document.set_tags([classification['category'], classification['sub_category']])
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '文件上传成功',
            'data': {
                'document_id': document.id,
                'filename': original_filename,
                'category': document.category,
                'sub_category': document.sub_category,
                'confidence_score': document.confidence_score,
                'keywords': document.get_keywords(),
                'is_auto_classified': document.is_auto_classified
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': 500,
            'message': f'上传失败: {str(e)}'
        }), 500


@materials_bp.route('/list', methods=['GET'])
@token_required
def list_documents(payload):
    """
    获取所有文档列表（所有教师可见）
    查询参数:
    - category: 按分类筛选
    - page: 页码（默认1）
    - per_page: 每页数量（默认10）
    """
    try:
        category = request.args.get('category', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 构建查询
        query = Document.query.filter_by(deleted_at=None)
        
        if category:
            query = query.filter_by(category=category)
        
        # 分页
        paginated = query.order_by(Document.created_at.desc()).paginate(
            page=page,
            per_page=per_page
        )
        
        documents = [doc.to_dict() for doc in paginated.items]
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'documents': documents,
                'total': paginated.total,
                'pages': paginated.pages,
                'current_page': page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取文档列表失败: {str(e)}'
        }), 500


@materials_bp.route('/detail/<int:document_id>', methods=['GET'])
@token_required
def get_document_detail(payload, document_id):
    """获取文档详情"""
    try:
        document = Document.query.get(document_id)
        
        if not document or document.deleted_at:
            return jsonify({'code': 404, 'message': '文档不存在'}), 404
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': document.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取文档失败: {str(e)}'
        }), 500


@materials_bp.route('/reclassify/<int:document_id>', methods=['PUT'])
@token_required
def reclassify_document(payload, document_id):
    """
    重新分类文档
    请求体:
    {
        "category": "新分类",
        "keywords": ["关键词1", "关键词2"]
    }
    """
    try:
        teacher_id = payload.get('user_id')
        document = Document.query.get(document_id)
        
        if not document or document.deleted_at:
            return jsonify({'code': 404, 'message': '文档不存在'}), 404
        
        # 验证权限（只有上传者可以修改，或管理员）
        if document.teacher_id != teacher_id:
            return jsonify({'code': 403, 'message': '无权限修改此文档'}), 403
        
        data = request.get_json() or {}
        
        # 更新分类
        if 'category' in data:
            document.category = data['category']
            document.sub_category = auto_classifier._get_sub_category(data['category'])
        
        if 'keywords' in data:
            document.set_keywords(data['keywords'])
        
        if 'sub_category' in data:
            document.sub_category = data['sub_category']
        
        # 标记为手动修改
        document.is_auto_classified = False
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '重新分类成功',
            'data': document.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'重新分类失败: {str(e)}'
        }), 500


@materials_bp.route('/search', methods=['GET'])
@token_required
def search_documents(payload):
    """
    文档搜索（支持标题搜索和全文搜索）
    查询参数:
    - q: 搜索关键词
    - type: 搜索类型 ('title' 标题搜索 | 'fulltext' 全文搜索, 默认 'title')
    - category: 按分类筛选（可选）
    - page: 页码（默认1）
    - per_page: 每页数量（默认10）
    """
    try:
        query_text = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'title')  # 'title' 或 'fulltext'
        category = request.args.get('category', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if not query_text:
            return jsonify({
                'code': 400,
                'message': '搜索关键词不能为空'
            }), 400
        
        # 构建查询
        query = Document.query.filter_by(deleted_at=None)
        
        if search_type == 'fulltext':
            # 全文搜索：在文件名、标题、描述和关键词中搜索
            search_filter = db.or_(
                Document.original_name.ilike(f'%{query_text}%'),
                Document.title.ilike(f'%{query_text}%'),
                Document.description.ilike(f'%{query_text}%'),
                Document.keywords.ilike(f'%{query_text}%')
            )
        else:
            # 标题搜索：仅在标题中搜索
            search_filter = Document.title.ilike(f'%{query_text}%')
        
        query = query.filter(search_filter)
        
        # 按分类筛选
        if category:
            query = query.filter_by(category=category)
        
        # 分页
        paginated = query.order_by(Document.created_at.desc()).paginate(
            page=page,
            per_page=per_page
        )
        
        documents = []
        for doc in paginated.items:
            doc_dict = doc.to_dict()
            doc_dict['search_type'] = search_type
            
            # 对于全文搜索，提取上下文（包括文件内容）
            if search_type == 'fulltext':
                context = _extract_context(doc, query_text)
                doc_dict['context'] = context
            
            documents.append(doc_dict)
        
        return jsonify({
            'code': 200,
            'message': '搜索成功',
            'data': {
                'documents': documents,
                'total': paginated.total,
                'pages': paginated.pages,
                'current_page': page,
                'query': query_text,
                'search_type': search_type
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'搜索失败: {str(e)}'
        }), 500


def _extract_context(doc, keyword, context_length=60):
    """
    提取匹配关键词的上下文
    先从文件内容查找，再从元数据中查找
    """
    matched_context = None
    search_from = 'metadata'  # 标记搜索的来源
    
    # 首先尝试从文件内容查找（仅支持TXT格式）
    if doc.file_type == 'txt' and os.path.exists(doc.file_path):
        try:
            with open(doc.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
            
            # 在文件内容中查找
            match_pos = file_content.lower().find(keyword.lower())
            if match_pos != -1:
                # 计算上下文范围
                start = max(0, match_pos - context_length)
                end = min(len(file_content), match_pos + len(keyword) + context_length)
                
                context = file_content[start:end]
                matched_text = file_content[match_pos:match_pos + len(keyword)]
                
                # 标记上下文边界
                if start > 0:
                    context = '...' + context
                if end < len(file_content):
                    context = context + '...'
                
                return {
                    'text': matched_text,
                    'context': context,
                    'type': 'file_content'
                }
        except Exception as e:
            pass  # 如果文件读取失败，继续从元数据查找
    
    # 从元数据中查找
    text_to_search = doc.description or ''
    if not text_to_search and doc.title:
        text_to_search = doc.title
        search_from = 'title'
    else:
        search_from = 'description'
    
    if not text_to_search:
        return {'text': '', 'context': '', 'type': 'none'}
    
    # 查找匹配位置
    match_pos = text_to_search.lower().find(keyword.lower())
    if match_pos == -1:
        return {'text': '', 'context': '', 'type': 'none'}
    
    # 计算上下文范围
    start = max(0, match_pos - context_length)
    end = min(len(text_to_search), match_pos + len(keyword) + context_length)
    
    context = text_to_search[start:end]
    matched_text = text_to_search[match_pos:match_pos + len(keyword)]
    
    # 标记查找的位置
    if start > 0:
        context = '...' + context
    if end < len(text_to_search):
        context = context + '...'
    
    return {
        'text': matched_text,
        'context': context,
        'type': search_from
    }




@materials_bp.route('/download/<int:document_id>', methods=['GET'])
@token_required
def download_document(payload, document_id):
    """
    下载文档
    支持所有文件格式的下载
    """
    try:
        document = Document.query.get(document_id)
        
        if not document or document.deleted_at:
            return jsonify({'code': 404, 'message': '文档不存在'}), 404
        
        # 检查文件是否存在
        if not os.path.exists(document.file_path):
            return jsonify({'code': 404, 'message': '文件不存在'}), 404
        
        # 使用原始文件名下载
        return send_file(
            document.file_path,
            as_attachment=True,
            download_name=document.original_name,
            mimetype=mimetypes.guess_type(document.file_path)[0] or 'application/octet-stream'
        )
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'下载失败: {str(e)}'
        }), 500


@materials_bp.route('/open/<int:document_id>', methods=['GET'])
@token_required
def open_document(payload, document_id):
    """
    在线打开文档（TXT格式）
    返回文档的完整内容
    """
    try:
        document = Document.query.get(document_id)
        
        if not document or document.deleted_at:
            return jsonify({'code': 404, 'message': '文档不存在'}), 404
        
        # 只支持打开TXT文件
        if document.file_type != 'txt':
            return jsonify({
                'code': 400,
                'message': f'不支持打开{document.file_type}格式的文件，仅支持TXT格式'
            }), 400
        
        # 读取文件内容
        try:
            with open(document.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            with open(document.file_path, 'r', encoding='gb2312') as f:
                content = f.read()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'document_id': document.id,
                'filename': document.original_name,
                'title': document.title,
                'content': content,
                'file_type': document.file_type,
                'keywords': document.get_keywords(),
                'category': document.category,
                'sub_category': document.sub_category
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'打开文件失败: {str(e)}'
        }), 500



@materials_bp.route('/preview/<int:document_id>', methods=['GET'])
@token_required
def preview_document(payload, document_id):
    """
    获取文档预览（前1000字符）
    用于快速查看文档内容
    """
    try:
        document = Document.query.get(document_id)
        
        if not document or document.deleted_at:
            return jsonify({'code': 404, 'message': '文档不存在'}), 404
        
        # 只支持TXT文件的预览
        if document.file_type != 'txt':
            return jsonify({
                'code': 400,
                'message': f'不支持预览{document.file_type}格式的文件'
            }), 400
        
        # 读取文件内容用于预览
        try:
            with open(document.file_path, 'r', encoding='utf-8') as f:
                preview_content = f.read(1000)
        except UnicodeDecodeError:
            with open(document.file_path, 'r', encoding='gb2312') as f:
                preview_content = f.read(1000)
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'document_id': document.id,
                'filename': document.original_name,
                'preview': preview_content + ('...' if len(preview_content) == 1000 else ''),
                'file_type': document.file_type,
                'keywords': document.get_keywords()[:5]  # 只显示前5个关键词
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取预览失败: {str(e)}'
        }), 500


@materials_bp.route('/categories', methods=['GET'])
@token_required
def get_categories(payload):
    """获取所有可用分类"""
    categories = [
        {'name': '数学', 'count': 0},
        {'name': '英语', 'count': 0},
        {'name': '物理', 'count': 0},
        {'name': '化学', 'count': 0},
        {'name': '生物', 'count': 0},
        {'name': '历史', 'count': 0},
        {'name': '地理', 'count': 0},
        {'name': '政治', 'count': 0},
        {'name': '经济', 'count': 0},
        {'name': '综合', 'count': 0}
    ]
    
    # 统计每个分类的文档数
    for cat in categories:
        count = Document.query.filter_by(
            category=cat['name'],
            deleted_at=None
        ).count()
        cat['count'] = count
    
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': categories
    }), 200


@materials_bp.route('/delete/<int:document_id>', methods=['DELETE'])
@token_required
def delete_document(payload, document_id):
    """删除文档（软删除）"""
    try:
        teacher_id = payload.get('user_id')
        document = Document.query.get(document_id)
        
        if not document or document.deleted_at:
            return jsonify({'code': 404, 'message': '文档不存在'}), 404
        
        # 验证权限
        if document.teacher_id != teacher_id:
            return jsonify({'code': 403, 'message': '无权限删除此文档'}), 403
        
        # 软删除
        document.deleted_at = datetime.utcnow()
        db.session.commit()
        
        # 删除物理文件
        try:
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
        except:
            pass
        
        return jsonify({
            'code': 200,
            'message': '删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'删除失败: {str(e)}'
        }), 500
