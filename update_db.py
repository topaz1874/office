from app import create_app
from app.models import db
import sqlalchemy as sa

app = create_app()

with app.app_context():
    # 检查表是否存在
    inspector = sa.inspect(db.engine)
    tables = inspector.get_table_names()
    
    if 'announcement' in tables:
        # 检查列是否已存在
        columns = [col['name'] for col in inspector.get_columns('announcement')]
        
        # 添加附件字段
        with db.engine.begin() as conn:
            if 'attachment_filename' not in columns:
                conn.execute(sa.text('ALTER TABLE announcement ADD COLUMN attachment_filename VARCHAR(255)'))
                print("添加了 attachment_filename 列")
                
            if 'attachment_path' not in columns:
                conn.execute(sa.text('ALTER TABLE announcement ADD COLUMN attachment_path VARCHAR(255)'))
                print("添加了 attachment_path 列")
                
            if 'attachment_type' not in columns:
                conn.execute(sa.text('ALTER TABLE announcement ADD COLUMN attachment_type VARCHAR(50)'))
                print("添加了 attachment_type 列")
        
        print("数据库更新完成")
    else:
        print("announcement 表不存在") 