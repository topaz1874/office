#!/bin/bash

# 创建备份目录（如果不存在）
mkdir -p backups

# 获取当前时间戳
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_FILE="app.db.backup.$TIMESTAMP"

echo "开始备份数据库..."

# 在容器内创建数据库备份
docker-compose exec -T web sh -c "cp /app/database/app.db /app/database/app.db.backup"

# 将备份文件复制到宿主机
docker cp pro_office_web_1:/app/database/app.db.backup ./backups/$BACKUP_FILE

echo "数据库备份完成: ./backups/$BACKUP_FILE"
echo "备份大小: $(du -h ./backups/$BACKUP_FILE | cut -f1)" 