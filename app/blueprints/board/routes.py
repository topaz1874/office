from flask import render_template, request, redirect, url_for, flash, current_app, send_from_directory
from app.blueprints.board import bp
from app.models import Announcement, db
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'}

def allowed_file(filename):
    """检查文件类型是否允许上传"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    """安全地获取文件扩展名"""
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

@bp.route('/')
def index():
    """公告栏首页"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 支持按标题搜索
    search = request.args.get('search', '')
    if search:
        pagination = Announcement.query.filter(Announcement.title.like(f'%{search}%')).order_by(
            Announcement.publish_date.desc()).paginate(page=page, per_page=per_page)
    else:
        pagination = Announcement.query.order_by(Announcement.publish_date.desc()).paginate(
            page=page, per_page=per_page)
    
    return render_template('board/index.html', title='公告栏', 
                           pagination=pagination, search=search)

@bp.route('/announcement/<int:id>')
def announcement_detail(id):
    """公告详情页面"""
    announcement = Announcement.query.get_or_404(id)
    return render_template('board/announcement_detail.html', title=announcement.title, announcement=announcement)

@bp.route('/add', methods=['GET', 'POST'])
def add_announcement():
    """添加公告"""
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        author = request.form.get('author', '')
        is_important = 'is_important' in request.form
        
        if not title:
            flash('标题不能为空', 'error')
            return render_template('board/add_announcement.html', title='添加公告')
            
        if not content:
            flash('内容不能为空', 'error')
            return render_template('board/add_announcement.html', title='添加公告')
        
        # 创建公告对象
        announcement = Announcement(
            title=title,
            content=content,
            author=author,
            is_important=is_important,
            publish_date=datetime.now()
        )
        
        # 处理附件上传
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '':
                # 检查文件是否有扩展名
                file_extension = get_file_extension(file.filename)
                if not file_extension:
                    flash('文件必须有扩展名', 'error')
                    return render_template('board/add_announcement.html', title='添加公告')
                
                # 检查文件类型是否允许
                if file_extension not in ALLOWED_EXTENSIONS:
                    flash('不支持的文件类型', 'error')
                    return render_template('board/add_announcement.html', title='添加公告')
                
                try:
                    # 生成安全的文件名
                    original_filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
                    
                    # 确保上传目录存在
                    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'attachments')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # 保存文件
                    file_path = os.path.join(upload_folder, unique_filename)
                    file.save(file_path)
                    
                    # 更新公告对象
                    announcement.attachment_filename = original_filename
                    announcement.attachment_path = os.path.join('attachments', unique_filename)
                    announcement.attachment_type = file_extension
                except Exception as e:
                    current_app.logger.error(f"文件处理错误: {str(e)}")
                    flash('文件处理过程中出错', 'error')
                    return render_template('board/add_announcement.html', title='添加公告')
        
        # 保存到数据库
        db.session.add(announcement)
        db.session.commit()
        
        flash('公告添加成功', 'success')
        return redirect(url_for('board.index'))
    
    return render_template('board/add_announcement.html', title='添加公告')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_announcement(id):
    """编辑公告"""
    announcement = Announcement.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        author = request.form.get('author', '')
        is_important = 'is_important' in request.form
        
        if not title:
            flash('标题不能为空', 'error')
            return render_template('board/edit_announcement.html', title='编辑公告', announcement=announcement)
            
        if not content:
            flash('内容不能为空', 'error')
            return render_template('board/edit_announcement.html', title='编辑公告', announcement=announcement)
        
        # 更新公告信息
        announcement.title = title
        announcement.content = content
        announcement.author = author
        announcement.is_important = is_important
        
        # 处理附件上传
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '':
                # 检查文件是否有扩展名
                file_extension = get_file_extension(file.filename)
                if not file_extension:
                    flash('文件必须有扩展名', 'error')
                    return render_template('board/edit_announcement.html', title='编辑公告', announcement=announcement)
                
                # 检查文件类型是否允许
                if file_extension not in ALLOWED_EXTENSIONS:
                    flash('不支持的文件类型', 'error')
                    return render_template('board/edit_announcement.html', title='编辑公告', announcement=announcement)
                
                try:
                    # 如果已有附件，删除旧文件
                    if announcement.attachment_path:
                        old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], announcement.attachment_path)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    
                    # 生成安全的文件名
                    original_filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
                    
                    # 确保上传目录存在
                    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'attachments')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # 保存文件
                    file_path = os.path.join(upload_folder, unique_filename)
                    file.save(file_path)
                    
                    # 更新公告对象
                    announcement.attachment_filename = original_filename
                    announcement.attachment_path = os.path.join('attachments', unique_filename)
                    announcement.attachment_type = file_extension
                except Exception as e:
                    current_app.logger.error(f"文件处理错误: {str(e)}")
                    flash('文件处理过程中出错', 'error')
                    return render_template('board/edit_announcement.html', title='编辑公告', announcement=announcement)
        
        # 保存到数据库
        db.session.commit()
        
        flash('公告更新成功', 'success')
        return redirect(url_for('board.announcement_detail', id=announcement.id))
    
    return render_template('board/edit_announcement.html', title='编辑公告', announcement=announcement)

@bp.route('/delete/<int:id>')
def delete_announcement(id):
    """删除公告"""
    announcement = Announcement.query.get_or_404(id)
    
    # 如果有附件，删除附件文件
    if announcement.attachment_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], announcement.attachment_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(announcement)
    db.session.commit()
    
    flash('公告已删除', 'success')
    return redirect(url_for('board.index'))

@bp.route('/attachment/<int:id>')
def get_attachment(id):
    """获取附件"""
    announcement = Announcement.query.get_or_404(id)
    
    if not announcement.attachment_path:
        flash('该公告没有附件', 'error')
        return redirect(url_for('board.announcement_detail', id=id))
    
    directory = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.dirname(announcement.attachment_path))
    filename = os.path.basename(announcement.attachment_path)
    
    return send_from_directory(directory, filename, 
                              as_attachment=request.args.get('download', '0') == '1',
                              download_name=announcement.attachment_filename)

# 注册错误处理函数
@bp.app_errorhandler(404)
def page_not_found(e):
    """处理404错误"""
    # 检查请求路径是否与公告相关
    if request.path.startswith('/board/announcement/') or request.path.startswith('/board/edit/') or request.path.startswith('/board/delete/') or request.path.startswith('/board/attachment/'):
        flash('您访问的公告不存在或已被删除', 'error')
        return redirect(url_for('board.index'))
    
    # 对于其他404错误，返回通用的404页面
    return render_template('404.html'), 404 