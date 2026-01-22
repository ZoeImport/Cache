from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
import mlflow

class ModelEngine:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = None
        self.tokenizer = None
    
    def load(self):
        print(f"🔄 Loading Base Model: {self.cfg.model.name}")
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name = self.cfg.model.name,
            max_seq_length = self.cfg.model.max_seq_length,
            load_in_4bit = self.cfg.model.load_in_4bit,
        )
        self.model = FastLanguageModel.get_peft_model(
            model, r = self.cfg.model.lora_rank,
            target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
            lora_alpha = 16, lora_dropout = 0, bias = "none",
        )
        self.tokenizer = tokenizer

    def train(self, dataset):
        mlflow.set_tracking_uri(self.cfg.mlflow.uri)
        mlflow.set_experiment(self.cfg.mlflow.experiment_name)
        
        args = TrainingArguments(
            output_dir=self.cfg.train.output_dir,
            per_device_train_batch_size=self.cfg.train.batch_size,
            gradient_accumulation_steps=self.cfg.train.gradient_accumulation_steps,
            max_steps=self.cfg.train.max_steps,
            learning_rate=self.cfg.train.learning_rate,
            logging_steps=1,
            fp16=True, # 1650 最好强制用 fp16
            optim="adamw_8bit",
            report_to="mlflow"
        )
        
        trainer = SFTTrainer(
            model=self.model, tokenizer=self.tokenizer,
            train_dataset=dataset, dataset_text_field="text",
            max_seq_length=self.cfg.model.max_seq_length, args=args
        )
        trainer.train()
        self.model.save_pretrained(f"{self.cfg.train.output_dir}/latest_lora")
