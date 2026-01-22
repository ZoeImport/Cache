import hydra
from datasets import Dataset
from src.database.connector import DBManager
from src.database.crud import Repository
from src.engine.trainer import ModelEngine

@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(cfg):
    # 1. DB Init
    db_url = f"postgresql://{cfg.db.user}:{cfg.db.password}@{cfg.db.host}:{cfg.db.port}/{cfg.db.name}"
    db = DBManager(db_url)
    db.init_db()
    repo = Repository(db)

    # 2. Get Data
    samples = repo.get_pending(limit=100)
    if not samples:
        print("💤 No pending data found.")
        return

    print(f"📦 Loaded {len(samples)} samples from PG.")
    
    # 3. Format Data
    # Go 程序员注意: 这里把 Struct 数组转换成了 HF 需要的 Dict Arrays
    hf_data = Dataset.from_dict({
        "text": [f"Instruction: {s.instruction}\nInput: {s.input_text}\nOutput: {s.output_text}" for s in samples]
    })

    # 4. Train
    engine = ModelEngine(cfg)
    engine.load()
    engine.train(hf_data)

    # 5. Commit Transaction
    repo.mark_trained([s.id for s in samples])
    print("✅ Done & DB Updated.")

if __name__ == "__main__":
    main()
