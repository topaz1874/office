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

- **响应式设计**：适配各种设备屏幕

## 技术栈

- **后端**：Flask + SQLAlchemy + Flask-Migrate
- **前端**：Bootstrap 5 + Jinja2模板
- **数据处理**：Pandas (用于CSV处理)
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
   docker-compose exec web sh -c "cp /app/app.db /app/app.db.backup"
   docker cp pro_office_web_1:/app/app.db.backup ./backups/
   ```

3. **恢复数据库**
   ```
   docker cp ./backups/app.db.backup pro_office_web_1:/app/
   docker-compose exec web sh -c "cp /app/app.db.backup /app/app.db"
   docker-compose restart web
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