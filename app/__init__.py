from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.models import db

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 注册蓝图
    from app.blueprints.oa import bp as oa_bp
    app.register_blueprint(oa_bp, url_prefix='/oa')
    
    from app.blueprints.board import bp as board_bp
    app.register_blueprint(board_bp, url_prefix='/board')
    
    # 注册主页路由
    @app.route('/')
    def index():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>办公系统</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                .links {
                    margin-top: 30px;
                }
                .links a {
                    display: inline-block;
                    margin: 10px;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }
                .links a:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>办公自动化系统</h1>
                <div class="links">
                    <a href="/oa">办公系统</a>
                    <a href="/board">公告栏</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    return app 