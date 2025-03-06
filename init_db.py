from app import create_app
from app.models import db, Announcement

app = create_app()

with app.app_context():
    # 创建所有表
    db.create_all()
    print("数据库表已创建")
    
    # 添加一个测试公告
    if Announcement.query.count() == 0:
        announcement = Announcement(
            title="测试公告",
            content="这是一个测试公告，用于测试附件功能。",
            author="管理员",
            is_important=True
        )
        db.session.add(announcement)
        db.session.commit()
        print("已添加测试公告")
    else:
        print("已有公告存在，跳过添加测试公告") 