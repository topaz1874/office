from app import create_app, db
from app.models import Document, Announcement

# 创建应用实例 - 这个文件主要用于Flask CLI和本地开发
# 生产环境使用wsgi.py作为入口点
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Document': Document, 'Announcement': Announcement}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 