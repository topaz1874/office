FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建上传目录
RUN mkdir -p app/static/uploads

# 不在构建时初始化数据库，而是在容器启动时进行
# 移除: RUN flask db init && flask db migrate && flask db upgrade

EXPOSE 5000

# 使用启动脚本
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# 修改CMD命令，使用正确的模块路径
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"] 