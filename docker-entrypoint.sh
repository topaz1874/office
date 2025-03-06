#!/bin/sh
set -e

echo "正在启动应用..."

# 安装依赖（确保所有依赖都已正确安装）
echo "检查依赖..."
pip install -r requirements.txt

# 初始化数据库
echo "初始化数据库..."
flask db init || echo "数据库已初始化，跳过init步骤"
flask db migrate || echo "数据库迁移失败，但将继续"
flask db upgrade || echo "数据库升级失败，但将继续"

# 检查应用是否可以导入
echo "检查应用..."
python -c "from wsgi import app; print('应用检查通过')" || echo "警告：应用导入测试失败"

# 执行传入的命令
echo "启动Web服务..."
exec "$@" 