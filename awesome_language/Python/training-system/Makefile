.PHONY: up down train shell logs clean

# 启动所有服务 (DB, MLflow, Trainer容器)
up:
	docker-compose -f deploy/docker-compose.yml up -d --build

# 停止服务
down:
	docker-compose -f deploy/docker-compose.yml down

# 进入训练容器 (类似 ssh 进去)
shell:
	docker exec -it llm_trainer_1650 /bin/bash

# 执行一次训练 (在容器外直接触发)
train:
	docker exec llm_trainer_1650 python main.py

# 往数据库塞一条测试数据 (方便调试)
seed_data:
	docker exec llm_db psql -U postgres -d llm_training_db -c 	"INSERT INTO training_data (instruction, output, status) VALUES ('Hello 1650', 'I am Qwen 1.5B running on GTX 1650!', 'pending');"

# 查看日志
logs:
	docker-compose -f deploy/docker-compose.yml logs -f
