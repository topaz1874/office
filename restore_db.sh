#!/bin/bash

# 检查是否提供了备份文件参数
if [ $# -eq 0 ]; then
    echo "错误: 未指定备份文件"
    echo "用法: $0 <备份文件>"
    echo "示例: $0 ./backups/app.db.backup.20250306220044"
    exit 1
fi

BACKUP_FILE=$1

# 检查备份文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "错误: 备份文件 '$BACKUP_FILE' 不存在"
    exit 1
fi

echo "开始恢复数据库..."
echo "备份文件: $BACKUP_FILE"

# 将备份文件复制到容器
docker cp $BACKUP_FILE pro_office_web_1:/app/database/app.db.backup

# 在容器内恢复数据库
docker-compose exec -T web sh -c "cp /app/database/app.db.backup /app/database/app.db"

# 重启容器以应用更改
docker-compose restart web

echo "数据库恢复完成" 