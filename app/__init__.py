from flask import Flask, render_template
from flask_migrate import Migrate
from config import Config
from app.models import db
import os
import markdown
import logging
from logging.handlers import RotatingFileHandler

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 设置日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/pro_office.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('办公系统启动')
    
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
                    <a href="/readme">系统说明</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    # 添加日志查看路由
    @app.route('/log')
    def view_log():
        try:
            with open('logs/pro_office.log', 'r') as f:
                log_content = f.read().splitlines()
                # 最多显示最近的1000行日志
                log_content = log_content[-1000:] if len(log_content) > 1000 else log_content
            return render_template('log.html', log_content=log_content)
        except Exception as e:
            app.logger.error(f"查看日志出错: {str(e)}")
            return render_template('log.html', log_content=["无法读取日志文件"])
    
    # 添加README查看路由
    @app.route('/readme')
    def view_readme():
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read()
                # 将Markdown转换为HTML
                html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
            return render_template('readme.html', content=html_content)
        except Exception as e:
            app.logger.error(f"查看README出错: {str(e)}")
            return render_template('readme.html', content="<p>无法读取README文件</p>")
    
    # 注册全局错误处理函数
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    return app 