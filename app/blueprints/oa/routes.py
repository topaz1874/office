from flask import render_template, request, redirect, url_for, flash, current_app
from app.blueprints.oa import bp
from app.models import Document, db
import pandas as pd
from datetime import datetime
import os

@bp.route('/')
def index():
    """OA系统首页"""
    # 获取最近的10个文档
    documents = Document.query.order_by(Document.register_time.desc()).limit(10).all()
    return render_template('oa/index.html', title='办公系统', documents=documents)

@bp.route('/documents')
def documents():
    """文档列表页面"""
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)
    
    # 获取搜索参数
    search = request.args.get('search', '')
    
    # 获取年份筛选参数
    selected_year = request.args.get('year', '')
    
    # 构建查询
    query = Document.query
    
    # 应用搜索条件
    if search:
        query = query.filter(Document.title.like(f'%{search}%'))
    
    # 应用年份筛选
    if selected_year and selected_year != 'all':
        year = int(selected_year)
        query = query.filter(
            db.extract('year', Document.register_time) == year
        )
    
    # 获取所有可用年份
    years_query = db.session.query(
        db.extract('year', Document.register_time).label('year')
    ).distinct().order_by(db.desc('year'))
    
    available_years = [int(year[0]) for year in years_query.all() if year[0] is not None]
    
    # 执行分页查询
    pagination = query.order_by(Document.register_time.desc()).paginate(
        page=page, per_page=per_page
    )
    
    # 可选的每页显示行数
    per_page_options = [10, 15, 20, 30, 50, 100]
    
    return render_template('oa/documents.html', 
                          title='文档列表', 
                          pagination=pagination, 
                          search=search,
                          selected_year=selected_year,
                          available_years=available_years,
                          per_page=per_page,
                          per_page_options=per_page_options)

@bp.route('/documents/<int:id>')
def document_detail(id):
    """文档详情页面"""
    document = Document.query.get_or_404(id)
    return render_template('oa/document_detail.html', title=document.title, document=document)

@bp.route('/upload', methods=['GET', 'POST'])
def upload_documents():
    """上传文档CSV文件"""
    if request.method == 'POST':
        # 检查是否有文件
        if 'file' not in request.files:
            flash('未选择文件', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        
        # 如果用户未选择文件
        if file.filename == '':
            flash('未选择文件', 'error')
            return redirect(request.url)
            
        if file and file.filename.endswith('.csv'):
            # 保存文件
            filename = 'documents_upload.csv'
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            # 确保上传目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            file.save(file_path)
            
            # 处理CSV文件
            success = process_csv_file(file_path)
            
            if success:
                flash('文件上传并处理成功', 'success')
            else:
                flash('文件处理失败', 'error')
                
            return redirect(url_for('oa.documents'))
    
    return render_template('oa/upload.html', title='上传文档')

def process_csv_file(file_path):
    """处理上传的CSV文件"""
    try:
        # 尝试不同的编码读取CSV
        try:
            df = pd.read_csv(file_path, dtype=str)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, dtype=str, encoding='gbk')
        
        # 清理列名
        df.columns = [col.strip().replace(' ', '').replace('\t', '').replace('\n', '') for col in df.columns]
        
        # 列名映射字典
        column_mapping = {
            '登记时间': 'register_time',
            '文号': 'doc_number',
            '来文单位': 'source_unit',
            '原文号': 'original_number',
            '密级': 'security_level',
            '标题': 'title',
            '移交部门': 'transfer_dept',
            '业务类型': 'business_type',
            '跟踪': 'tracking',
            '公文状态': 'tracking'
        }
        
        # 重命名列
        df = df.rename(columns=column_mapping)
        
        # 检查必要的列是否存在
        required_columns = ['register_time', 'doc_number', 'title']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            current_app.logger.error(f"CSV文件缺少必要的列: {missing_columns}")
            return False
        
        # 处理日期格式
        df['register_time'] = pd.to_datetime(df['register_time'], errors='coerce')

        # 将DataFrame转换为文档对象列表
        documents = []
        for _, row in df.iterrows():
            # 处理 tracking 字段
            tracking_value = ''
            if '跟踪' in row:
                tracking_value = clean_string(row['跟踪'])
            if not tracking_value and '公文状态' in row:
                tracking_value = clean_string(row['公文状态'])

            doc = Document(
                register_time=row['register_time'].to_pydatetime() if pd.notnull(row['register_time']) else None,
                doc_number=clean_string(row['doc_number']),
                source_unit=clean_string(row['source_unit']),
                original_number=clean_string(row['original_number']),
                security_level=clean_string(row['security_level']),
                title=clean_string(row['title']),
                transfer_dept=clean_string(row['transfer_dept']),
                business_type=clean_string(row['business_type']),
                tracking=tracking_value
            )
            documents.append(doc)

        # 批量添加到数据库
        db.session.bulk_save_objects(documents)
        db.session.commit()
        
        return True
        
    except Exception as e:
        current_app.logger.error(f"处理CSV文件时出错: {str(e)}")
        db.session.rollback()
        return False

def clean_string(value):
    """清理字符串值，将None和NaN转换为空字符串"""
    if pd.isna(value) or value is None:
        return ''
    value = str(value).strip()
    return value if value != 'nan' else '' 