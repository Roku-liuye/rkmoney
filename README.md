# rkmoney

资产价值管理应用

## 项目结构

```
rkmoney/
├── backend/          # FastAPI 后端
│   ├── main.py       # 主应用文件
│   ├── models.py     # 数据模型
│   ├── schemas.py    # Pydantic 模型
│   ├── crud.py       # 数据库操作
│   ├── database.py   # 数据库连接
│   ├── requirements.txt
│   └── .env
├── frontend/         # Vue 3 前端
│   └── src/
└── 开发计划/          # 开发文档
```

## 快速开始

### 前置要求

- Python 3.8+
- Node.js 20+
- SQLite (已包含在 Python 中)

### 安装和运行

#### 1. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并根据需要修改：

```bash
cp .env.example .env
```

#### 3. 运行后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

后端将在 http://localhost:8000 运行

#### 4. 安装前端依赖

```bash
cd frontend
npm install
```

#### 5. 运行前端

```bash
cd frontend
npm run dev
```

前端将在 http://localhost:5173 运行

## API 文档

后端运行后访问 http://localhost:8000/docs 查看自动生成的 API 文档

## 主要功能

- 资产管理（添加、编辑、删除、售出）
- 资产价格记录
- 日均价值计算
- 资产类型管理
