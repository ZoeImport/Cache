# LLM Engineering Template (GTX 1650 Edition)

这是一套专为 4GB 显存显卡设计的、符合工程化规范的大模型持续训练系统。

## 1. 目录结构

```text
├── configs/             # [配置中心] Hydra YAML (类似 Viper)
├── src/
│   ├── schema/          # [DTO] Pydantic 定义 (类似 Go Struct)
│   ├── database/        # [DAO] SQLAlchemy ORM (类似 Gorm)
│   └── engine/          # [Service] Unsloth 训练逻辑
├── deploy/              # [部署] Dockerfile & Compose
├── outputs/             # [产物] LoRA 权重保存位置
├── Makefile             # [命令] 快捷操作
└── main.py              # [入口] 依赖注入与流程编排
```

## 2. 框架选型与 Go 对比

| 组件 | Python 选型 | Go 类比 | 理由 |
| :--- | :--- | :--- | :--- |
| **配置** | **Hydra** | `Viper` | 支持分层配置、命令行动态覆盖 (args parsing) |
| **数据校验** | **Pydantic** | `Struct` + `Validator` | 强类型检查，拒绝 Dict 裸奔 |
| **ORM** | **SQLAlchemy** | `Gorm` / `Ent` | 数据库抽象层，通过 Object 操作 DB |
| **引擎** | **Unsloth** | (无直接类比) | 当前最快、最省显存的微调库 (适配 1650 关键) |
| **监控** | **MLflow** | `Prometheus` + `Grafana` | 记录每一次实验的 Loss 曲线和参数 |

## 3. 快速开始 (调试方法)

### 第一步：启动环境
```bash
make up
```
这将拉起 Postgres, MLflow 和 配置好环境的 Trainer 容器。

### 第二步：注入测试数据
我们先往数据库里塞一条数据，否则没有数据可练。
```bash
make seed_data
```
*(你也可以用 Navicat/DBeaver 连接 localhost:5432 只有 user/pass 填对即可)*

### 第三步：运行训练
```bash
make train
```
你将看到日志输出：
1. 从 PG 获取 pending 数据
2. 加载 Qwen-1.5B (4bit)
3. 开始训练
4. 保存 LoRA 到 `outputs/`
5. 更新 PG 数据状态为 trained

### 第四步：查看监控
打开浏览器访问 `http://localhost:5000`，你可以看到 MLflow 的面板，里面有刚才训练的 Loss 图表。

## 4. 调试技巧

1. **进入容器调试**:
   如果你想修改代码并立即测试，不用重启容器（因为挂载了目录）。
   ```bash
   make shell
   # 进去后直接运行
   python main.py
   ```

2. **PDB 断点**:
   在代码里插入 `import pdb; pdb.set_trace()`，然后在容器内运行，即可单步调试。

3. **显存监控**:
   在宿主机新开一个终端运行 `watch -n 1 nvidia-smi`，观察 1650 的显存是否爆掉。

