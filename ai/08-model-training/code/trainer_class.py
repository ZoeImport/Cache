#!/usr/bin/env python3
"""
trainer_class.py — Reusable Training Loop Template

A complete, production-style Trainer class demonstrating:
  1. Standard training loop (epoch + batch)
  2. Checkpoint save / resume
  3. Gradient accumulation
  4. Gradient clipping
  5. Mixed precision training (AMP)
  6. Experiment tracking (TensorBoard / WandB ready)
  7. Full CIFAR-10 demo with a small CNN

Usage:
  python trainer_class.py                         # full demo
  python trainer_class.py --amp                   # force AMP on
  python trainer_class.py --no-amp                # force AMP off
  python trainer_class.py --accum 4               # gradient accumulation steps
  python trainer_class.py --resume checkpoint.pth # resume training

Requirements:
  torch>=2.1.0, torchvision, numpy, matplotlib
"""

import os
import sys
import time
import math
import argparse
from copy import deepcopy
from collections import defaultdict

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.amp import autocast, GradScaler
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


# ╔══════════════════════════════════════════════════════════════════╗
# ║  1.  Model Definition — Simple CNN for CIFAR-10                ║
# ╚══════════════════════════════════════════════════════════════════╝

class SimpleCNN(nn.Module):
    """A small CNN for CIFAR-10. ~1.2M parameters, fast to train."""

    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            # Conv block 1: 3 -> 64
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 32 -> 16

            # Conv block 2: 64 -> 128
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 16 -> 8

            # Conv block 3: 128 -> 256
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # 8 -> 4
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(512, num_classes),
        )

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


# ╔══════════════════════════════════════════════════════════════════╗
# ║  2.  Data Preparation — CIFAR-10 Loaders                       ║
# ╚══════════════════════════════════════════════════════════════════╝

def get_cifar10_loaders(
    batch_size: int = 64,
    num_workers: int = 4,
    data_dir: str = "./data",
) -> tuple[DataLoader, DataLoader]:
    """Return (train_loader, val_loader) for CIFAR-10 with standard aug."""

    # Training: random crop + horizontal flip + normalization
    train_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.4914, 0.4822, 0.4465],
            std=[0.2470, 0.2435, 0.2616],
        ),
    ])
    # Validation: just resize + normalize
    val_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.4914, 0.4822, 0.4465],
            std=[0.2470, 0.2435, 0.2616],
        ),
    ])

    train_dataset = datasets.CIFAR10(
        root=data_dir, train=True, download=True, transform=train_transform,
    )
    val_dataset = datasets.CIFAR10(
        root=data_dir, train=False, download=True, transform=val_transform,
    )

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=True,
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size * 2, shuffle=False,
        num_workers=num_workers, pin_memory=True,
    )

    return train_loader, val_loader


# ╔══════════════════════════════════════════════════════════════════╗
# ║  3.  Trainer Class — Reusable Template                          ║
# ╚══════════════════════════════════════════════════════════════════╝

class Trainer:
    """
    A reusable training loop template.

    Features:
      - Epoch-based training / validation loop
      - Checkpoint save & resume (model, optimizer, scheduler, scaler, metrics)
      - Gradient accumulation (simulate larger batch size)
      - Gradient clipping (prevent exploding gradients)
      - Mixed precision (AMP) with GradScaler
      - Learning rate scheduling (CosineAnnealing)
      - Best model tracking and saving
      - Optional WandB / TensorBoard logging (configurable)

    Usage:
      trainer = Trainer(model, train_loader, val_loader, ...)
      trainer.train()

      # Resume from checkpoint:
      trainer = Trainer(..., resume_path="checkpoint.pth")
      trainer.train()
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        epochs: int = 30,
        lr: float = 0.01,
        weight_decay: float = 5e-4,
        momentum: float = 0.9,
        accumulation_steps: int = 1,
        max_grad_norm: float | None = 1.0,
        use_amp: bool = True,
        use_wandb: bool = False,
        use_tensorboard: bool = False,
        log_interval: int = 50,
        checkpoint_dir: str = "./checkpoints",
        resume_path: str | None = None,
        device: str | None = None,
    ):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.epochs = epochs
        self.lr = lr
        self.accumulation_steps = max(1, accumulation_steps)
        self.max_grad_norm = max_grad_norm
        self.use_amp = use_amp and torch.cuda.is_available()
        self.log_interval = log_interval
        self.checkpoint_dir = checkpoint_dir

        # Device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        self.model = self.model.to(self.device)

        # Loss & optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(
            self.model.parameters(),
            lr=lr,
            momentum=momentum,
            weight_decay=weight_decay,
        )

        # LR scheduler
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=epochs,
        )

        # AMP scaler
        self.scaler = GradScaler("cuda", enabled=self.use_amp)

        # Training state
        self.start_epoch = 0
        self.best_acc = 0.0
        self.best_model_state = None
        self.train_losses: list[float] = []
        self.val_losses: list[float] = []
        self.val_accs: list[float] = []
        self.epoch_times: list[float] = []

        # Logging
        self.use_wandb = use_wandb
        self.use_tensorboard = use_tensorboard
        self._setup_logging()

        # Create checkpoint directory
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        # Resume from checkpoint if specified
        if resume_path is not None:
            self._load_checkpoint(resume_path)

        # Print config
        self._print_config()

    def _setup_logging(self):
        """Initialize experiment tracking backends."""
        if self.use_wandb:
            try:
                import wandb
                wandb.init(project="trainer-demo", config=self._get_config_dict())
                self.wandb = wandb
            except ImportError:
                print("[Warning] wandb not installed. Falling back to console logging.")
                self.use_wandb = False
        if self.use_tensorboard:
            try:
                from torch.utils.tensorboard import SummaryWriter
                self.tb_writer = SummaryWriter(log_dir=os.path.join(
                    self.checkpoint_dir, "tensorboard",
                ))
            except ImportError:
                print("[Warning] tensorboard not installed. Falling back to console logging.")
                self.use_tensorboard = False

    def _get_config_dict(self) -> dict:
        """Return trainer config as a flat dict for logging."""
        return {
            "epochs": self.epochs,
            "lr": self.lr,
            "accumulation_steps": self.accumulation_steps,
            "max_grad_norm": self.max_grad_norm,
            "use_amp": self.use_amp,
            "model_params": sum(p.numel() for p in self.model.parameters()),
        }

    def _print_config(self):
        """Print a summary of the trainer configuration."""
        n_params = sum(p.numel() for p in self.model.parameters())
        print(f"[Device] {self.device}")
        print(f"[Model] {self.model.__class__.__name__} (parameters: {n_params:,})")
        print(f"[AMP] {'ON' if self.use_amp else 'OFF'}")
        print(f"[Accumulation Steps] {self.accumulation_steps}")
        print(f"[Max Grad Norm] {self.max_grad_norm}")
        print(f"[Checkpoint Dir] {self.checkpoint_dir}")
        print()

    def _get_lr(self) -> float:
        """Return the current learning rate."""
        return self.optimizer.param_groups[0]["lr"]

    # ── Public API ──────────────────────────────────────────────

    def train(self):
        """Run the full training loop (start_epoch -> epochs)."""
        print(f"{'='*60}")
        print(f" Training started  |  Epochs: {self.start_epoch} -> {self.epochs}")
        print(f"{'='*60}\n")

        total_start_time = time.time()

        for epoch in range(self.start_epoch, self.epochs):
            epoch_start = time.time()

            # Train one epoch
            train_loss = self._train_epoch(epoch)

            # Validate
            val_loss, val_acc = self._validate(epoch)

            # LR scheduler step
            self.scheduler.step()

            # Store metrics
            self.train_losses.append(train_loss)
            self.val_losses.append(val_loss)
            self.val_accs.append(val_acc)
            epoch_time = time.time() - epoch_start
            self.epoch_times.append(epoch_time)

            # Log
            self._log_epoch(epoch, train_loss, val_loss, val_acc, epoch_time)

            # Save checkpoint
            self._save_checkpoint(epoch, val_acc)

            # Save best model
            if val_acc > self.best_acc:
                self.best_acc = val_acc
                self.best_model_state = deepcopy(self.model.state_dict())
                best_path = os.path.join(self.checkpoint_dir, "best_model.pth")
                torch.save(self.model.state_dict(), best_path)
                print(f"  * New best model! Acc: {val_acc:.2f}% -> {best_path}")

        total_time = time.time() - total_start_time
        self._print_summary(total_time)

        # Restore best model
        if self.best_model_state is not None:
            self.model.load_state_dict(self.best_model_state)

        return self.val_accs

    # ── Training Epoch ──────────────────────────────────────────

    def _train_epoch(self, epoch: int) -> float:
        """Run one training epoch. Returns average loss."""
        self.model.train()
        total_loss = 0.0
        num_batches = len(self.train_loader)

        # Zero gradients at the start of the epoch
        self.optimizer.zero_grad()

        for batch_idx, (inputs, targets) in enumerate(self.train_loader):
            inputs = inputs.to(self.device, non_blocking=True)
            targets = targets.to(self.device, non_blocking=True)

            # ── Forward (with autocast if AMP enabled) ──
            with autocast("cuda", enabled=self.use_amp):
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)

                # Scale loss for gradient accumulation
                loss = loss / self.accumulation_steps

            # ── Backward ──
            self.scaler.scale(loss).backward()

            total_loss += loss.item() * self.accumulation_steps

            # ── Gradient accumulation check ──
            if (batch_idx + 1) % self.accumulation_steps == 0:
                # Unscale gradients before clipping
                if self.max_grad_norm is not None:
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), self.max_grad_norm,
                    )

                # Step & zero grad
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad()

            # ── Logging ──
            if batch_idx % self.log_interval == 0 and batch_idx > 0:
                avg_loss = total_loss / (batch_idx + 1)
                print(f"  [{self._elapsed_str(batch_idx, num_batches)}] "
                      f"Epoch {epoch+1:>3}/{self.epochs} | "
                      f"Batch {batch_idx:>4}/{num_batches} | "
                      f"Loss: {avg_loss:.4f} | "
                      f"LR: {self._get_lr():.5f}")

        # Handle remainder batch
        total_batches_seen = len(self.train_loader)
        if total_batches_seen % self.accumulation_steps != 0:
            if self.max_grad_norm is not None:
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(), self.max_grad_norm,
                )
            self.scaler.step(self.optimizer)
            self.scaler.update()
            self.optimizer.zero_grad()

        return total_loss / num_batches

    # ── Validation ──────────────────────────────────────────────

    @torch.no_grad()
    def _validate(self, epoch: int) -> tuple[float, float]:
        """Run validation. Returns (avg_loss, accuracy%)."""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        for inputs, targets in self.val_loader:
            inputs = inputs.to(self.device, non_blocking=True)
            targets = targets.to(self.device, non_blocking=True)

            with autocast("cuda", enabled=self.use_amp):
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        avg_loss = total_loss / len(self.val_loader)
        accuracy = 100.0 * correct / total
        return avg_loss, accuracy

    # ── Checkpoint Save / Resume ────────────────────────────────

    def _save_checkpoint(self, epoch: int, val_acc: float):
        """Save a full training checkpoint."""
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scheduler_state_dict": self.scheduler.state_dict(),
            "scaler_state_dict": self.scaler.state_dict(),
            "best_acc": self.best_acc,
            "val_acc": val_acc,
            "train_losses": self.train_losses,
            "val_losses": self.val_losses,
            "val_accs": self.val_accs,
            "config": self._get_config_dict(),
        }
        path = os.path.join(self.checkpoint_dir, f"checkpoint_epoch_{epoch+1}.pth")
        torch.save(checkpoint, path)

        # Also save a 'latest' for easy resume
        latest_path = os.path.join(self.checkpoint_dir, "latest.pth")
        torch.save(checkpoint, latest_path)

    def _load_checkpoint(self, path: str):
        """Load a training checkpoint and restore all states."""
        if not os.path.exists(path):
            print(f"[Warning] Checkpoint not found: {path}. Starting from scratch.")
            return

        checkpoint = torch.load(path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        if "scheduler_state_dict" in checkpoint:
            self.scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
        if "scaler_state_dict" in checkpoint:
            self.scaler.load_state_dict(checkpoint["scaler_state_dict"])

        self.start_epoch = checkpoint.get("epoch", 0) + 1
        self.best_acc = checkpoint.get("best_acc", 0.0)
        self.train_losses = checkpoint.get("train_losses", [])
        self.val_losses = checkpoint.get("val_losses", [])
        self.val_accs = checkpoint.get("val_accs", [])

        print(f"\n[Resume] Loaded checkpoint: {path}")
        print(f"         Resuming from epoch {self.start_epoch}")
        print(f"         Previous best acc: {self.best_acc:.2f}%\n")

    # ── Logging ─────────────────────────────────────────────────

    def _log_epoch(
        self, epoch: int, train_loss: float, val_loss: float,
        val_acc: float, epoch_time: float,
    ):
        """Log epoch-level metrics to all configured backends."""
        lr = self._get_lr()
        print(
            f"[{self._format_time(epoch_time):>6}] "
            f"Epoch {epoch+1:>3}/{self.epochs} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Val Loss: {val_loss:.4f} | "
            f"Val Acc: {val_acc:.2f}% | "
            f"LR: {lr:.5f}"
        )

        if self.use_wandb:
            self.wandb.log({
                "epoch": epoch + 1,
                "train/loss": train_loss,
                "val/loss": val_loss,
                "val/acc": val_acc,
                "lr": lr,
                "time": epoch_time,
            })
        if self.use_tensorboard:
            step = epoch + 1
            self.tb_writer.add_scalar("train/loss", train_loss, step)
            self.tb_writer.add_scalar("val/loss", val_loss, step)
            self.tb_writer.add_scalar("val/acc", val_acc, step)
            self.tb_writer.add_scalar("lr", lr, step)

    def _print_summary(self, total_time: float):
        """Print a final training summary."""
        print(f"\n{'='*60}")
        print(f" Training completed in {self._format_time(total_time)}")
        print(f"{'='*60}")
        print(f"  Best Val Acc:  {self.best_acc:.2f}%")
        print(f"  Final Val Acc: {self.val_accs[-1]:.2f}%")
        if self.val_accs:
            best_epoch = int(np.argmax(self.val_accs)) if self.val_accs else -1
            print(f"  Best Epoch:    {best_epoch + 1}")
        print(f"  Avg epoch time: {self._format_time(float(np.mean(self.epoch_times)))}")
        print(f"  Checkpoints:    {self.checkpoint_dir}/")
        print(f"{'='*60}\n")

    # ── Helpers ─────────────────────────────────────────────────

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds into MM:SS or HH:MM:SS."""
        seconds = int(seconds)
        h, remainder = divmod(seconds, 3600)
        m, s = divmod(remainder, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

    def _elapsed_str(self, batch_idx: int, total: int) -> str:
        """Return a progress indicator showing batch position."""
        pct = 100.0 * (batch_idx + 1) / total
        return f"{pct:5.1f}%"


# ╔══════════════════════════════════════════════════════════════════╗
# ║  4.  Demo Functions                                             ║
# ╚══════════════════════════════════════════════════════════════════╝

def demo_speed_comparison(args):
    """
    Run two training sessions (AMP ON / AMP OFF) and compare speed + accuracy.
    """
    print("\n" + "#" * 60)
    print("#  AMP SPEED COMPARISON")
    print("#" * 60 + "\n")

    results = {}

    for use_amp in [True, False]:
        amp_label = "ON" if use_amp else "OFF"
        print(f"\n{'-'*50}")
        print(f"  Training with AMP = {amp_label}")
        print(f"{'-'*50}\n")

        train_loader, val_loader = get_cifar10_loaders(
            batch_size=64, data_dir=args.data_dir,
        )
        model = SimpleCNN()
        trainer = Trainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=args.epochs,
            lr=args.lr,
            accumulation_steps=args.accum,
            max_grad_norm=args.clip,
            use_amp=use_amp,
            checkpoint_dir=os.path.join(args.checkpoint_dir, f"amp_{amp_label.lower()}"),
            resume_path=None,
        )
        val_accs = trainer.train()
        results[amp_label] = {
            "acc": val_accs[-1] if val_accs else 0.0,
            "time": sum(trainer.epoch_times),
            "best_acc": trainer.best_acc,
        }

    # Print comparison
    print(f"\n{'='*60}")
    print("  AMP SPEED COMPARISON RESULTS")
    print(f"{'='*60}")
    time_on = results["ON"]["time"]
    time_off = results["OFF"]["time"]
    speedup = time_off / time_on if time_on > 0 else 0
    print(f"  AMP ON:   {results['ON']['best_acc']:.2f}%  |  "
          f"Time: {Trainer._format_time(time_on)}")
    print(f"  AMP OFF:  {results['OFF']['best_acc']:.2f}%  |  "
          f"Time: {Trainer._format_time(time_off)}")
    print(f"  Speedup:  {speedup:.2f}x  "
          f"(AMP ON is {speedup:.1f}x faster)")


def demo_gradient_accumulation(args):
    """
    Compare training without vs. with gradient accumulation.
    """
    print("\n" + "#" * 60)
    print("#  GRADIENT ACCUMULATION EFFECT")
    print("#" * 60 + "\n")

    for accum, label in [(1, "Without accum (batch=64)"),
                         (args.accum, f"With accum (eff_batch={64 * args.accum})")]:
        print(f"\n{'-'*50}")
        print(f"  {label}")
        print(f"{'-'*50}\n")

        train_loader, val_loader = get_cifar10_loaders(
            batch_size=64, data_dir=args.data_dir,
        )
        model = SimpleCNN()
        trainer = Trainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=args.epochs,
            lr=args.lr,
            accumulation_steps=accum,
            max_grad_norm=args.clip,
            use_amp=args.amp,
            checkpoint_dir=os.path.join(args.checkpoint_dir, f"accum_{accum}"),
            resume_path=None,
        )
        val_accs = trainer.train()
        print(f"  -> Best accuracy: {trainer.best_acc:.2f}%")

    print(f"\n  Note: Larger effective batch size often provides slightly "
          f"more stable gradient estimates.")


def demo_checkpoint_resume(args):
    """
    Train for half the epochs, save a checkpoint, then resume and complete.
    Verify that the final accuracy matches expectations.
    """
    print("\n" + "#" * 60)
    print("#  CHECKPOINT RESUME DEMO")
    print("#" * 60 + "\n")

    half_epochs = max(2, args.epochs // 2)
    checkpoint_dir = os.path.join(args.checkpoint_dir, "resume_demo")

    # Phase 1: Train half epochs and save checkpoint
    print(f"\n{'-'*50}")
    print(f"  Phase 1: Train {half_epochs} epochs, save checkpoint")
    print(f"{'-'*50}\n")

    train_loader, val_loader = get_cifar10_loaders(
        batch_size=64, data_dir=args.data_dir,
    )
    model1 = SimpleCNN()
    trainer1 = Trainer(
        model=model1,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=half_epochs,
        lr=args.lr,
        accumulation_steps=args.accum,
        max_grad_norm=args.clip,
        use_amp=args.amp,
        checkpoint_dir=checkpoint_dir,
        resume_path=None,
    )
    trainer1.train()
    checkpoint_path = os.path.join(checkpoint_dir, "latest.pth")
    print(f"  Checkpoint saved to: {checkpoint_path}")

    # Phase 2: Resume and continue
    print(f"\n{'-'*50}")
    print(f"  Phase 2: Resume from checkpoint, train remaining epochs")
    print(f"{'-'*50}\n")

    train_loader2, val_loader2 = get_cifar10_loaders(
        batch_size=64, data_dir=args.data_dir,
    )
    model2 = SimpleCNN()
    trainer2 = Trainer(
        model=model2,
        train_loader=train_loader2,
        val_loader=val_loader2,
        epochs=args.epochs,
        lr=args.lr,
        accumulation_steps=args.accum,
        max_grad_norm=args.clip,
        use_amp=args.amp,
        checkpoint_dir=checkpoint_dir,
        resume_path=checkpoint_path,
    )
    trainer2.train()

    print(f"\n  {'='*40}")
    print(f"  Checkpoint Resume: SUCCESS")
    print(f"  Phase 1 best acc: {trainer1.best_acc:.2f}%")
    print(f"  Phase 2 final acc: {trainer2.best_acc:.2f}%")
    print(f"  {'='*40}\n")


def run_all_demos(args):
    """Run a single full training session with all features enabled."""
    print("\n" + "#" * 60)
    print("#  FULL TRAINING DEMO -- All Features Enabled")
    print("#" * 60 + "\n")

    train_loader, val_loader = get_cifar10_loaders(
        batch_size=64, data_dir=args.data_dir,
    )
    model = SimpleCNN()
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=args.epochs,
        lr=args.lr,
        accumulation_steps=args.accum,
        max_grad_norm=args.clip,
        use_amp=args.amp,
        checkpoint_dir=args.checkpoint_dir,
        resume_path=args.resume,
    )
    trainer.train()
    return trainer


# ╔══════════════════════════════════════════════════════════════════╗
# ║  5.  Main Entry Point                                          ║
# ╚══════════════════════════════════════════════════════════════════╝

def parse_args():
    parser = argparse.ArgumentParser(
        description="Trainer Class Demo -- Training Loop Mastery",
    )
    parser.add_argument("--epochs", type=int, default=5,
                        help="Number of epochs (default: 5)")
    parser.add_argument("--lr", type=float, default=0.01,
                        help="Learning rate (default: 0.01)")
    parser.add_argument("--batch-size", type=int, default=64,
                        help="Batch size (default: 64)")
    parser.add_argument("--accum", type=int, default=2,
                        help="Gradient accumulation steps (default: 2)")
    parser.add_argument("--clip", type=float, default=1.0,
                        help="Max gradient norm for clipping (default: 1.0)")
    parser.add_argument("--amp", action=argparse.BooleanOptionalAction,
                        default=True,
                        help="Enable/disable AMP (default: enabled)")
    parser.add_argument("--checkpoint-dir", type=str, default="./checkpoints",
                        help="Checkpoint directory (default: ./checkpoints)")
    parser.add_argument("--data-dir", type=str, default="./data",
                        help="Data directory (default: ./data)")
    parser.add_argument("--resume", type=str, default=None,
                        help="Path to checkpoint to resume from")
    parser.add_argument("--demo", type=str, default="full",
                        choices=["full", "amp-compare", "accum-compare",
                                 "resume-demo", "all"],
                        help="Which demo to run (default: full)")
    return parser.parse_args()


def main():
    args = parse_args()

    # Print header
    print()
    print("=" * 66)
    print("     Training Loop Mastery -- Reusable Trainer Class Demo")
    print("=" * 66)
    print(f"  PyTorch: {torch.__version__}  |  "
          f"Device: {'cuda' if torch.cuda.is_available() else 'cpu'}")

    if args.demo == "full":
        run_all_demos(args)
    elif args.demo == "amp-compare":
        demo_speed_comparison(args)
    elif args.demo == "accum-compare":
        demo_gradient_accumulation(args)
    elif args.demo == "resume-demo":
        demo_checkpoint_resume(args)
    elif args.demo == "all":
        run_all_demos(args)
        demo_speed_comparison(args)
        demo_gradient_accumulation(args)
        demo_checkpoint_resume(args)

    print("\nDone.\n")


if __name__ == "__main__":
    main()
