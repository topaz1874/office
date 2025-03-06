from app import create_app
from app.models import Document

app = create_app()

with app.app_context():
    count = Document.query.count()
    print(f"Total documents in database: {count}")
    
    # 显示最近的5条记录
    recent_docs = Document.query.order_by(Document.register_time.desc()).limit(5).all()
    print("\nRecent documents:")
    for doc in recent_docs:
        print(f"- {doc.title} ({doc.doc_number})") 