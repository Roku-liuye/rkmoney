# rkmoney 后端

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

```bash
uvicorn main:app --reload
```

### 数据库迁移

```bash
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

## API 端点

- `POST /api/assets` - 创建资产
- `GET /api/assets` - 获取资产列表
- `GET /api/assets/{id}` - 获取单个资产
- `PUT /api/assets/{id}` - 更新资产
- `DELETE /api/assets/{id}` - 删除资产
- `POST /api/assets/{id}/sell` - 售出资产
- `GET /api/assets/{id}/prices` - 获取资产价格记录
- `POST /api/assets/{id}/prices` - 添加价格记录
- `POST /api/calculate-daily-value` - 计算日均价值
