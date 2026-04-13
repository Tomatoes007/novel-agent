# Novel Agent Backend

一个面向中文网文创作的后端项目骨架，技术栈为：FastAPI + MySQL + Redis + Milvus + OpenAI-compatible API。

## 已包含的能力

- 小说项目创建 / 查询
- 立项方案生成
- 世界观生成 / 保存
- 角色卡生成 / 保存
- 卷纲与章节纲生成 / 保存
- 单章节生成
- 章节生成后的记忆写回
- Redis 热缓存
- Milvus 语义记忆写入与检索
- 简单的一致性审校

## 目录说明

- `app/core`: 基础设施，配置、MySQL、Redis、Milvus、LLM 客户端
- `app/models`: SQLAlchemy ORM 模型
- `app/schemas`: Pydantic 请求/响应模型
- `app/repositories`: 数据访问层
- `app/services`: 业务服务层
- `app/agents`: Agent 工作流与上下文编排
- `app/prompts`: Prompt 模板
- `app/api/v1`: FastAPI 路由

## 启动方式

1. 复制环境变量

```bash
cp .env.example .env
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 启动服务

```bash
uvicorn app.main:app --reload
```

启动时会自动执行 `Base.metadata.create_all` 创建 MySQL 表。
Milvus collection 会在第一次调用向量写入/检索时自动创建。

## 推荐联调顺序

1. 创建项目
2. 生成立项方案
3. 生成世界观
4. 生成角色卡
5. 生成第一卷大纲
6. 生成某一章正文
7. 查看 foreshadowings / timeline / memory 检索结果
