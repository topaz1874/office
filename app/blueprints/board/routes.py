from flask import render_template, request, redirect, url_for, flash
from app.blueprints.board import bp
from app.models import Announcement, db
from datetime import datetime

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
        
        announcement = Announcement(
            title=title,
            content=content,
            author=author,
            is_important=is_important,
            publish_date=datetime.now()
        )
        
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
        
        announcement.title = title
        announcement.content = content
        announcement.author = author
        announcement.is_important = is_important
        
        db.session.commit()
        
        flash('公告更新成功', 'success')
        return redirect(url_for('board.announcement_detail', id=announcement.id))
    
    return render_template('board/edit_announcement.html', title='编辑公告', announcement=announcement)

@bp.route('/delete/<int:id>')
def delete_announcement(id):
    """删除公告"""
    announcement = Announcement.query.get_or_404(id)
    
    db.session.delete(announcement)
    db.session.commit()
    
    flash('公告已删除', 'success')
    return redirect(url_for('board.index')) 