# 办公自动化系统

基于Flask的办公自动化系统，包含文档管理和公告栏功能。

## 功能特点

- **文档管理**：
  - 支持上传、查看和搜索文档
  - 按年份筛选文档
  - 自定义每页显示行数
  - CSV批量导入文档数据
  
- **公告栏**：
  - 支持添加、编辑、删除和搜索公告
  - 支持标记重要公告
  - 公告详情查看
  - **附件上传与管理**：支持PDF、Word、Excel等格式
  - **PDF在线预览**：直接在页面中查看PDF附件

- **系统功能**：
  - **友好的错误处理**：自定义404页面和错误跳转
  - **系统日志查看**：管理员可查看系统运行日志
  - **README文档在线查看**：系统使用说明随时可查
  - **MQTT数据监控**：实时监控电压数据，以音量柱形式动态显示

- **响应式设计**：适配各种设备屏幕

## 技术栈

- **后端**：Flask + SQLAlchemy + Flask-Migrate
- **前端**：Bootstrap 5 + Jinja2模板 + Bootstrap Icons
- **数据处理**：Pandas (用于CSV处理)
- **通信协议**：MQTT (用于实时数据监控)
- **部署**：Docker + Gunicorn

## 安装与运行

### 使用Docker

1. 克隆仓库
   ```
   git clone <仓库地址>
   cd pro_office
   ```

2. 使用Docker Compose构建并运行
   ```
   docker-compose up -d
   ```

3. 访问应用
   在浏览器中访问 http://localhost:8080

### 本地开发

1. 克隆仓库
   ```
   git clone <仓库地址>
   cd pro_office
   ```

2. 创建虚拟环境并安装依赖
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 初始化数据库
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. 运行应用
   ```
   flask run
   ```

5. 访问应用
   在浏览器中访问 http://localhost:5000

## Docker维护指令

### 基本操作

1. **启动容器**
   ```
   docker-compose up -d
   ```

2. **停止容器**
   ```
   docker-compose down
   ```

3. **查看容器状态**
   ```
   docker-compose ps
   ```

4. **查看容器日志**
   ```
   docker-compose logs -f
   ```

### 数据维护

1. **导入CSV数据**
   ```
   # 将CSV文件放入data目录，然后执行：
   docker-compose exec web python -c "from update_data import update_from_directory; update_from_directory()"
   ```

2. **备份数据库**
   ```
   # 使用备份脚本（推荐）
   ./backup_db.sh
   
   # 或者手动执行以下命令：
   # 创建备份目录（如果不存在）
   mkdir -p backups
   
   # 在容器内创建数据库备份
   docker-compose exec web sh -c "cp /app/database/app.db /app/database/app.db.backup"
   
   # 将备份文件复制到宿主机
   docker cp pro_office_web_1:/app/database/app.db.backup ./backups/app.db.backup.$(date +%Y%m%d%H%M%S)
   ```

3. **恢复数据库**
   ```
   # 使用恢复脚本（推荐）
   ./restore_db.sh ./backups/app.db.backup.YYYYMMDDHHMMSS
   
   # 或者手动执行以下命令：
   # 选择要恢复的备份文件
   BACKUP_FILE=./backups/app.db.backup.YYYYMMDDHHMMSS
   
   # 将备份文件复制到容器
   docker cp $BACKUP_FILE pro_office_web_1:/app/database/app.db.backup
   
   # 在容器内恢复数据库
   docker-compose exec web sh -c "cp /app/database/app.db.backup /app/database/app.db"
   
   # 重启容器以应用更改
   docker-compose restart web
   ```

4. **数据库迁移**
   ```
   # 生成迁移脚本（在修改模型后执行）
   docker-compose exec web flask db migrate -m "描述更改的消息"
   
   # 应用迁移
   docker-compose exec web flask db upgrade
   
   # 回滚迁移
   docker-compose exec web flask db downgrade
   ```

### 系统维护

1. **重新构建容器**
   ```
   docker-compose down
   docker-compose up -d --build
   ```

2. **更新代码后重启**
   ```
   docker-compose restart web
   ```

3. **查看容器资源使用情况**
   ```
   docker stats pro_office_web_1
   ```

4. **进入容器内部**
   ```
   docker-compose exec web bash
   ```

5. **清理未使用的Docker资源**
   ```
   docker system prune -a
   ```

6. **查看系统日志**
   ```
   # 通过Web界面访问：
   http://localhost:8080/log
   ```

## 数据导入

系统支持通过CSV文件导入文档数据。CSV文件应包含以下列：
- 登记时间
- 文号
- 标题
- 来文单位（可选）
- 原文号（可选）
- 密级（可选）
- 移交部门（可选）
- 业务类型（可选）
- 跟踪/公文状态（可选）

## 系统使用说明

### 文档管理

1. **浏览文档**：访问`/oa/documents`页面
2. **按年份筛选**：点击顶部的年份选项卡
3. **调整每页显示行数**：使用右上角的下拉菜单
4. **搜索文档**：使用搜索框按标题搜索
5. **查看文档详情**：点击文档行中的"查看"按钮

### 公告栏

1. **浏览公告**：访问`/board`页面
2. **添加公告**：点击左侧的"添加公告"按钮
3. **编辑公告**：在公告详情页点击"编辑"按钮
4. **删除公告**：在公告详情页点击"删除"按钮
5. **标记重要公告**：添加或编辑公告时勾选"标记为重要公告"
6. **上传附件**：添加或编辑公告时可上传附件文件
7. **查看附件**：在公告详情页可查看和下载附件，PDF文件可直接在页面中预览

### 系统功能

1. **查看系统日志**：访问`/log`页面（仅管理员可用）
2. **查看系统说明**：访问`/readme`页面
3. **错误处理**：访问不存在的页面时会显示友好的错误页面
4. **电压监控**：访问`/mqtt/voltage`页面，查看实时电压数据
   - 支持音量柱动态显示
   - 支持鼠标滚轮缩放
   - 根据电压值大小自动变色（低值红色-中值黄色-高值绿色）

## 树莓派部署指南

要在局域网的树莓派上部署本系统，请按照以下步骤操作：

### 1. 准备工作

- 一台安装了Raspberry Pi OS的树莓派（建议使用Raspberry Pi 4，至少2GB内存）
- 树莓派已连接到局域网并能访问互联网
- 树莓派上已安装Docker和Docker Compose

### 2. 安装Docker和Docker Compose

如果尚未安装Docker和Docker Compose，请执行以下命令：

```bash
# 安装Docker
curl -sSL https://get.docker.com | sh

# 将当前用户添加到docker组（免sudo运行docker）
sudo usermod -aG docker $USER
```

### 3. 配置Docker国内镜像源

为了加快Docker镜像拉取速度，强烈建议配置Docker国内镜像源：

```bash
# 创建或修改daemon.json文件
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://mirror.baidubce.com",
    "https://mirrors.ustc.edu.cn/dockerhub/",
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF

# 重启Docker服务
sudo systemctl restart docker
```

验证镜像是否配置成功：

```bash
# 查看Docker信息，确认registry-mirrors已经生效
docker info | grep "Registry Mirrors" -A 5
```

如果您使用的是Docker Compose，还可以在`docker-compose.yml`文件中直接指定镜像源：

```yaml
version: '3'
services:
  web:
    build:
      context: .
      args:
        # 使用国内PyPI镜像源
        PIP_INDEX_URL: https://mirrors.aliyun.com/pypi/simple/
        PIP_TRUSTED_HOST: mirrors.aliyun.com
    # 其他配置...
```

安装Docker Compose（如果遇到`externally-managed-environment`错误，请使用以下方法之一）：

**方法1：使用apt安装（推荐）**
```bash
sudo apt-get update
sudo apt-get install -y docker-compose
```

**方法2：使用Python虚拟环境**
```bash
# 安装Python虚拟环境
sudo apt-get update
sudo apt-get install -y python3-venv

# 创建虚拟环境
python3 -m venv ~/docker-compose-env

# 激活虚拟环境
source ~/docker-compose-env/bin/activate

# 在虚拟环境中安装docker-compose
pip install docker-compose

# 创建符号链接使docker-compose全局可用
sudo ln -s ~/docker-compose-env/bin/docker-compose /usr/local/bin/docker-compose
```

**方法3：使用--break-system-packages参数（不推荐）**
```bash
sudo apt-get update
sudo apt-get install -y python3-pip
sudo pip3 install docker-compose --break-system-packages
```

安装完成后重启树莓派：

```bash
sudo reboot
```

### 4. 配置Git国内镜像源

为了加快代码克隆和更新速度，建议配置Git国内镜像源：

```bash
# 全局配置使用gitee镜像
git config --global url."https://gitee.com/".insteadOf "https://github.com/"

# 或者配置特定仓库使用国内镜像
# 中国科学技术大学镜像
git config --global url."https://mirrors.ustc.edu.cn/".insteadOf "https://"

# 清华大学镜像
# git config --global url."https://mirrors.tuna.tsinghua.edu.cn/git/".insteadOf "https://"
```

您也可以直接使用国内Git平台（如Gitee）上的项目镜像：

```bash
# 使用Gitee上的镜像仓库
git clone https://gitee.com/yourusername/pro_office.git
```

### 5. 获取项目代码

```bash
# 克隆项目代码
git clone https://github.com/yourusername/pro_office.git
git clone https://ghfast.top/https://github.com/topaz1874/office.git

cd pro_office
```

### 6. 修改MQTT配置

编辑`app/blueprints/mqtt/routes.py`文件，将MQTT代理地址修改为您局域网中MQTT服务器的地址：

```python
# MQTT配置
MQTT_BROKER = "192.168.1.xxx"  # 替换为您的MQTT服务器IP
MQTT_PORT = 1883
MQTT_TOPIC = "voltage"
```

### 7. 构建和启动容器

```bash
# 构建并启动容器
docker-compose up -d
```

### 8. 初始化数据库

```bash
# 初始化数据库
docker-compose exec web python /app/init_db.py
```

### 9. 访问系统

现在您可以通过树莓派的IP地址和端口访问系统：

```
http://树莓派IP:5000
```

例如：`http://192.168.1.xxx:5000`

### 10. 设置开机自启动

创建systemd服务文件：

```bash
sudo nano /etc/systemd/system/pro-office.service
```

添加以下内容：

```
[Unit]
Description=Pro Office System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pro_office
ExecStart=/usr/local/bin/docker-compose up
ExecStop=/usr/local/bin/docker-compose down
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable pro-office.service
sudo systemctl start pro-office.service
```

### 11. 故障排除

- 如果无法访问系统，请检查树莓派防火墙设置，确保5000端口已开放
- 检查Docker容器状态：`docker-compose ps`
- 查看日志：`docker-compose logs -f web`
- 如果树莓派资源有限，可以修改`docker-compose.yml`文件，减少容器的资源限制

#### Docker服务启动失败问题

如果遇到Docker服务无法启动的问题（例如日志中显示"docker.service: Failed with result 'exit-code'"），请尝试以下解决方法：

1. **检查Docker配置文件**

   首先检查Docker配置文件是否有语法错误：
   
   ```bash
   sudo cat /etc/docker/daemon.json
   ```
   
   确保JSON格式正确，没有多余的逗号或引号。

2. **修复配置文件**

   如果配置文件有问题，可以重新创建：
   
   ```bash
   # 备份原配置文件
   sudo mv /etc/docker/daemon.json /etc/docker/daemon.json.bak
   
   # 创建新的配置文件
   sudo tee /etc/docker/daemon.json <<-'EOF'
   {
     "registry-mirrors": [
       "https://mirror.baidubce.com"
     ]
   }
   EOF
   ```
   
   先使用最简单的配置，确保Docker能够启动。

3. **重置Docker服务**

   ```bash
   # 停止Docker服务
   sudo systemctl stop docker
   
   # 重置Docker服务状态
   sudo systemctl reset-failed docker.service
   
   # 启动Docker服务
   sudo systemctl start docker
   
   # 查看Docker服务状态
   sudo systemctl status docker
   ```

4. **检查系统日志**

   如果Docker仍然无法启动，查看详细日志：
   
   ```bash
   # 查看Docker服务日志
   sudo journalctl -u docker.service --no-pager
   
   # 或者查看最近的系统日志
   sudo dmesg | tail -n 50
   ```

5. **检查存储空间**

   确保系统有足够的存储空间：
   
   ```bash
   df -h
   ```
   
   如果存储空间不足，清理一些不需要的文件。

6. **重新安装Docker**

   如果以上方法都不能解决问题，可以尝试重新安装Docker：
   
   ```bash
   # 卸载Docker
   sudo apt-get purge docker-ce docker-ce-cli containerd.io
   
   # 删除Docker数据目录
   sudo rm -rf /var/lib/docker
   
   # 重新安装Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

#### Docker Compose连接错误问题

如果在使用Docker Compose时遇到类似以下错误：

```
OSError: [Errno 5] Input/output error
urllib3.exceptions.ProtocolError: ('Connection aborted.', OSError(5, 'Input/output error'))
requests.exceptions.ConnectionError: ('Connection aborted.', OSError(5, 'Input/output error'))
```

这通常是由于Docker守护进程通信问题或资源限制导致的，请尝试以下解决方法：

1. **重启Docker服务**

   ```bash
   sudo systemctl restart docker
   ```

2. **增加树莓派的交换空间**

   如果是内存不足导致的问题，可以增加交换空间：
   
   ```bash
   # 检查当前交换空间
   free -h
   
   # 增加交换空间（例如增加到2GB）
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # 修改CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

3. **检查并修复Docker套接字权限**

   ```bash
   # 确保当前用户在docker组中
   sudo usermod -aG docker $USER
   
   # 修复套接字权限
   sudo chmod 666 /var/run/docker.sock
   ```

4. **使用较低版本的Docker Compose**

   有时较新版本的Docker Compose在树莓派上可能不稳定：
   
   ```bash
   # 卸载当前版本
   sudo apt-get remove docker-compose
   
   # 安装特定版本
   sudo pip3 install docker-compose==1.29.2 --break-system-packages
   ```

5. **检查存储设备健康状况**

   SD卡或USB存储设备问题也可能导致I/O错误：
   
   ```bash
   # 检查磁盘健康状况
   sudo apt-get install smartmontools
   sudo smartctl -a /dev/mmcblk0  # 对于SD卡
   
   # 检查文件系统错误
   sudo fsck -f /dev/mmcblk0p2  # 请根据实际分区调整
   ```

6. **降低Docker资源使用**

   修改docker-compose.yml文件，添加资源限制：
   
   ```yaml
   services:
     web:
       # 其他配置...
       deploy:
         resources:
           limits:
             cpus: '0.5'
             memory: 512M
   ```

7. **使用稳定的存储介质**

   考虑使用高质量的SD卡或外接SSD/USB存储，并将Docker数据目录移至该存储设备：
   
   ```bash
   # 停止Docker
   sudo systemctl stop docker
   
   # 创建新的Docker数据目录
   sudo mkdir -p /mnt/external/docker
   
   # 配置Docker使用新目录
   sudo tee /etc/docker/daemon.json <<-'EOF'
   {
     "registry-mirrors": ["https://mirror.baidubce.com"],
     "data-root": "/mnt/external/docker"
   }
   EOF
   
   # 启动Docker
   sudo systemctl start docker
   ``` 

## 树莓派5部署替代方案

如果您在树莓派5上使用Docker遇到困难，以下是一些更轻量级的替代部署方案：

### 1. 直接部署（无容器）

直接在树莓派上安装Python和依赖项，是最简单且资源消耗最少的方法：

```bash
# 安装Python和依赖
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# 克隆项目
git clone https://github.com/yourusername/pro_office.git
cd pro_office

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
flask db upgrade

# 使用Gunicorn运行（生产环境）
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app
```

设置开机自启动：
```bash
sudo nano /etc/systemd/system/pro-office.service
```

添加以下内容：
```
[Unit]
Description=Pro Office System
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/pro_office
ExecStart=/home/pi/pro_office/venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl enable pro-office.service
sudo systemctl start pro-office.service
```

### 2. 使用Supervisor管理Python应用

Supervisor是一个进程控制系统，可以更可靠地管理应用程序：

```bash
# 安装Supervisor
sudo apt-get install -y supervisor

# 创建配置文件
sudo nano /etc/supervisor/conf.d/pro-office.conf
```

添加以下内容：
```
[program:pro-office]
command=/home/pi/pro_office/venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app
directory=/home/pi/pro_office
user=pi
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

启用并启动服务：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start pro-office
```

### 3. 使用Nginx + uWSGI

这种组合提供了更好的性能和可靠性。以下是详细的部署步骤：

### 1. 安装必要的软件包

```bash
# 更新软件包列表
sudo apt-get update

# 安装Nginx、Python开发包和其他必要工具
sudo apt-get install -y nginx python3-dev python3-pip python3-venv build-essential
```

### 2. 创建Python虚拟环境

```bash
# 克隆项目代码
git clone https://github.com/yourusername/pro_office.git
cd pro_office

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装项目依赖
pip install -r requirements.txt

# 安装uWSGI
pip install uwsgi
```

### 3. 测试uWSGI是否能正确运行Flask应用

```bash
# 直接使用uWSGI运行应用进行测试
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```

如果能在浏览器中访问`http://树莓派IP:5000`并看到应用，说明uWSGI配置正确。按Ctrl+C停止测试服务器。

### 4. 创建uWSGI配置文件

```bash
# 在项目目录中创建uwsgi.ini文件
nano ~/pro_office/uwsgi.ini
```

添加以下内容：

```ini
[uwsgi]
# 基本配置
module = wsgi:app
master = true
processes = 2
threads = 2

# 套接字配置
socket = /tmp/pro-office.sock
chmod-socket = 666
vacuum = true
die-on-term = true

# 日志配置
logto = /var/log/uwsgi/%n.log

# 性能优化
harakiri = 30
max-requests = 5000
buffer-size = 32768

# 树莓派资源优化
cheaper = 1
cheaper-initial = 1
cheaper-step = 1
cheaper-algo = spare
cheaper-overload = 5
```

### 5. 创建系统服务文件

```bash
# 创建uWSGI服务文件
sudo nano /etc/systemd/system/pro-office.service
```

添加以下内容：

```
[Unit]
Description=uWSGI instance to serve Pro Office
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/pro_office
Environment="PATH=/home/pi/pro_office/venv/bin"
ExecStart=/home/pi/pro_office/venv/bin/uwsgi --ini uwsgi.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

### 6. 创建Nginx配置文件

```bash
# 创建Nginx站点配置
sudo nano /etc/nginx/sites-available/pro-office
```

添加以下内容：

```
server {
    listen 80;
    server_name _;  # 替换为您的域名或保留为通配符

    # 静态文件配置
    location /static {
        alias /home/pi/pro_office/app/static;
    }

    # 主应用配置
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/pro-office.sock;
        uwsgi_read_timeout 300s;
        uwsgi_send_timeout 300s;
        
        # 缓存配置
        uwsgi_buffering on;
        uwsgi_buffers 8 16k;
        uwsgi_buffer_size 32k;
    }

    # 日志配置
    access_log /var/log/nginx/pro-office-access.log;
    error_log /var/log/nginx/pro-office-error.log;
}
```

### 7. 启用Nginx配置并创建日志目录

```bash
# 创建uWSGI日志目录
sudo mkdir -p /var/log/uwsgi
sudo chown pi:pi /var/log/uwsgi

# 启用Nginx站点配置
sudo ln -s /etc/nginx/sites-available/pro-office /etc/nginx/sites-enabled
sudo rm -f /etc/nginx/sites-enabled/default  # 移除默认站点（可选）

# 测试Nginx配置
sudo nginx -t
```

### 8. 启动服务

```bash
# 重新加载systemd配置
sudo systemctl daemon-reload

# 启动uWSGI服务
sudo systemctl start pro-office
sudo systemctl enable pro-office

# 重启Nginx
sudo systemctl restart nginx
```

### 9. 验证部署

访问`http://树莓派IP`，您应该能看到应用正常运行。

### 10. 监控和故障排除

```bash
# 检查uWSGI服务状态
sudo systemctl status pro-office

# 查看uWSGI日志
sudo tail -f /var/log/uwsgi/pro-office.log

# 查看Nginx访问日志
sudo tail -f /var/log/nginx/pro-office-access.log

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/pro-office-error.log
```

### 11. 性能优化

#### 启用Nginx缓存

```bash
sudo nano /etc/nginx/sites-available/pro-office
```

添加以下内容到server块中：

```
# 静态文件缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 30d;
    add_header Cache-Control "public, no-transform";
}
```

#### 优化Nginx工作进程

```bash
sudo nano /etc/nginx/nginx.conf
```

修改为：

```
worker_processes 2;  # 设置为树莓派5的CPU核心数
worker_connections 1024;
```

#### 重启Nginx应用更改

```bash
sudo systemctl restart nginx
```

### 12. 安全加固

#### 配置防火墙

```bash
# 安装UFW
sudo apt-get install -y ufw

# 配置防火墙规则
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable
```

#### 设置HTTPS（可选）

```bash
# 安装Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 获取并配置SSL证书
sudo certbot --nginx -d yourdomain.com
```

### 13. 自动备份数据库

创建备份脚本：

```bash
sudo nano /home/pi/backup-db.sh
```

添加以下内容：

```bash
#!/bin/bash
DATE=$(date +%Y%m%d%H%M%S)
BACKUP_DIR="/home/pi/backups"

mkdir -p $BACKUP_DIR
cp /home/pi/pro_office/database/app.db $BACKUP_DIR/app.db.$DATE

# 保留最近10个备份
ls -t $BACKUP_DIR/app.db.* | tail -n +11 | xargs -r rm
```

设置权限并创建定时任务：

```bash
chmod +x /home/pi/backup-db.sh
crontab -e
```

添加以下内容：

```
0 2 * * * /home/pi/backup-db.sh
```

这个详细指南涵盖了使用Nginx + uWSGI在树莓派5上部署Flask应用的所有关键步骤，包括性能优化、安全加固和自动备份。这种部署方式比Docker更轻量级，更适合树莓派的资源限制，同时提供了生产级别的性能和可靠性。 