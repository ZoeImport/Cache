"""
training_techniques.py
======================
Compare weight initialization, optimizers, and learning rate schedules
on a 2-layer MLP trained on MNIST.

Usage:
    python training_techniques.py

Requirements:
    torch>=2.1.0, torchvision, matplotlib, tqdm
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import time
import math
import os

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
INPUT_DIM = 784
HIDDEN_DIM = 256
NUM_CLASSES = 10
EPOCHS = 10
BATCH_SIZE = 64
LR = 1e-3
SUBSET_SIZE = 2000

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {DEVICE}\n")


# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────
def get_mnist_loaders(batch_size=64, subset_size=2000):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])
    train_full = datasets.MNIST(
        "/tmp/mnist", train=True, download=True, transform=transform
    )
    test_full = datasets.MNIST(
        "/tmp/mnist", train=False, download=True, transform=transform
    )
    rng = np.random.RandomState(42)
    train_idx = rng.choice(len(train_full), subset_size, replace=False)
    train_set = Subset(train_full, train_idx)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_full, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


# ─────────────────────────────────────────────
# Model
# ─────────────────────────────────────────────
class MLP(nn.Module):
    """2-layer MLP: 784 -> 256 -> 10"""

    def __init__(self, init_method: str = "xavier", depth: int = 1):
        super().__init__()
        self.fc1 = nn.Linear(INPUT_DIM, HIDDEN_DIM)
        self.fc2 = nn.Linear(HIDDEN_DIM, NUM_CLASSES)
        self._init_weights(init_method, depth)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def _init_weights(self, method: str, depth: int = 1):
        for name, param in self.named_parameters():
            if "weight" not in name:
                continue
            if method == "xavier":
                nn.init.xavier_uniform_(param)
            elif method == "kaiming":
                nn.init.kaiming_uniform_(param, mode="fan_in", nonlinearity="relu")
            elif method == "llama":
                nn.init.normal_(param, mean=0.0, std=0.02 / math.sqrt(2 * depth))
            else:
                pass
        print(f"  [Init] Using {method} initialization")


# ─────────────────────────────────────────────
# Training helpers
# ─────────────────────────────────────────────
def train_epoch(model, loader, optimizer, criterion, scheduler=None):
    model.train()
    total_loss = 0.0
    total_correct = 0
    total_samples = 0
    for data, target in loader:
        data, target = data.to(DEVICE), target.to(DEVICE)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data.size(0)
        total_correct += (output.argmax(dim=1) == target).sum().item()
        total_samples += data.size(0)
    if scheduler is not None:
        scheduler.step()
    return total_loss / total_samples, total_correct / total_samples


@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_samples = 0
    for data, target in loader:
        data, target = data.to(DEVICE), target.to(DEVICE)
        output = model(data)
        loss = criterion(output, target)
        total_loss += loss.item() * data.size(0)
        total_correct += (output.argmax(dim=1) == target).sum().item()
        total_samples += data.size(0)
    return total_loss / total_samples, total_correct / total_samples


# ─────────────────────────────────────────────
# LR Schedules
# ─────────────────────────────────────────────
def get_scheduler(optimizer, name: str, epochs: int):
    if name == "none":
        return None
    elif name == "cosine":
        return optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    elif name == "step":
        return optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)
    elif name == "warmup_cosine":
        def lr_lambda(epoch):
            warmup_epochs = 2
            if epoch < warmup_epochs:
                return (epoch + 1) / warmup_epochs
            else:
                progress = (epoch - warmup_epochs) / max(epochs - warmup_epochs, 1)
                return 0.5 * (1.0 + math.cos(math.pi * progress))
        return optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
    else:
        return None


# ─────────────────────────────────────────────
# Experiment 1: Compare Weight Initializations
# ─────────────────────────────────────────────
def experiment_init(train_loader, test_loader):
    print("\n" + "=" * 60)
    print("Experiment 1: Weight Initialization Comparison")
    print("=" * 60)
    print(f"{'Init':>10} | {'Epoch':>6} | {'Train Loss':>10} | {'Train Acc':>9} | {'Test Acc':>8}")
    print("-" * 60)

    criterion = nn.CrossEntropyLoss()
    results = {}

    for init_name in ["xavier", "kaiming", "llama"]:
        model = MLP(init_method=init_name).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=LR)
        scheduler = get_scheduler(optimizer, "warmup_cosine", EPOCHS)
        train_losses, test_accs = [], []
        for epoch in range(1, EPOCHS + 1):
            train_loss, train_acc = train_epoch(
                model, train_loader, optimizer, criterion, scheduler
            )
            _, test_acc = evaluate(model, test_loader, criterion)
            train_losses.append(train_loss)
            test_accs.append(test_acc)
            if epoch == EPOCHS:
                print(f"{init_name:>10} | {epoch:>6d} | {train_loss:>10.4f} | {train_acc:>9.4f} | {test_acc:>8.4f}")
        results[init_name] = (train_losses, test_accs)

    print("\nFinal Test Accuracy by Initialization:")
    print(f"{'Init':>10} | {'Test Acc':>10}")
    print("-" * 25)
    for name in results:
        print(f"{name:>10} | {results[name][1][-1]:>10.4f}")
    return results


# ─────────────────────────────────────────────
# Experiment 2: Compare Optimizers
# ─────────────────────────────────────────────
def experiment_optimizer(train_loader, test_loader):
    print("\n" + "=" * 60)
    print("Experiment 2: Optimizer Comparison")
    print("=" * 60)
    print(f"{'Optimizer':>12} | {'Epoch':>6} | {'Train Loss':>10} | {'Train Acc':>9} | {'Test Acc':>8}")
    print("-" * 60)

    criterion = nn.CrossEntropyLoss()
    results = {}

    optim_configs = {
        "SGD":       (lambda p: optim.SGD(p, lr=LR), "warmup_cosine"),
        "Momentum":  (lambda p: optim.SGD(p, lr=LR, momentum=0.9), "warmup_cosine"),
        "Adam":      (lambda p: optim.Adam(p, lr=LR), "warmup_cosine"),
        "AdamW":     (lambda p: optim.AdamW(p, lr=LR, weight_decay=1e-4), "warmup_cosine"),
    }

    for opt_name, (opt_fn, sched_name) in optim_configs.items():
        model = MLP(init_method="kaiming").to(DEVICE)
        optimizer = opt_fn(model.parameters())
        scheduler = get_scheduler(optimizer, sched_name, EPOCHS)
        train_losses, test_accs = [], []
        for epoch in range(1, EPOCHS + 1):
            train_loss, train_acc = train_epoch(
                model, train_loader, optimizer, criterion, scheduler
            )
            _, test_acc = evaluate(model, test_loader, criterion)
            train_losses.append(train_loss)
            test_accs.append(test_acc)
            if epoch == EPOCHS:
                print(f"{opt_name:>12} | {epoch:>6d} | {train_loss:>10.4f} | {train_acc:>9.4f} | {test_acc:>8.4f}")
        results[opt_name] = (train_losses, test_accs)

    print("\nFinal Test Accuracy by Optimizer:")
    print(f"{'Optimizer':>12} | {'Test Acc':>10}")
    print("-" * 25)
    for name in results:
        print(f"{name:>12} | {results[name][1][-1]:>10.4f}")
    return results


# ─────────────────────────────────────────────
# Experiment 3: Compare LR Schedules
# ─────────────────────────────────────────────
def experiment_scheduler(train_loader, test_loader):
    print("\n" + "=" * 60)
    print("Experiment 3: Learning Rate Schedule Comparison")
    print("=" * 60)
    print(f"{'Scheduler':>14} | {'Epoch':>6} | {'Train Loss':>10} | {'Train Acc':>9} | {'Test Acc':>8}")
    print("-" * 60)

    criterion = nn.CrossEntropyLoss()
    results = {}

    for sched_name in ["none", "cosine", "step", "warmup_cosine"]:
        model = MLP(init_method="kaiming").to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=LR)
        scheduler = get_scheduler(optimizer, sched_name, EPOCHS)
        train_losses, test_accs = [], []
        for epoch in range(1, EPOCHS + 1):
            train_loss, train_acc = train_epoch(
                model, train_loader, optimizer, criterion, scheduler
            )
            _, test_acc = evaluate(model, test_loader, criterion)
            train_losses.append(train_loss)
            test_accs.append(test_acc)
            if epoch == EPOCHS:
                print(f"{sched_name:>14} | {epoch:>6d} | {train_loss:>10.4f} | {train_acc:>9.4f} | {test_acc:>8.4f}")
        results[sched_name] = (train_losses, test_accs)

    print("\nFinal Test Accuracy by LR Schedule:")
    print(f"{'Scheduler':>14} | {'Test Acc':>10}")
    print("-" * 28)
    for name in results:
        print(f"{name:>14} | {results[name][1][-1]:>10.4f}")
    return results


# ─────────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────────
def plot_results(init_results, opt_results, sched_results, save_path="training_techniques.png"):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    ax = axes[0]
    for name, (losses, accs) in init_results.items():
        ax.plot(losses, label=f"{name} (acc={accs[-1]:.3f})", linewidth=2)
    ax.set_title("Weight Initialization", fontsize=14)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Train Loss")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    for name, (losses, accs) in opt_results.items():
        ax.plot(losses, label=f"{name} (acc={accs[-1]:.3f})", linewidth=2)
    ax.set_title("Optimizer", fontsize=14)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Train Loss")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    for name, (losses, accs) in sched_results.items():
        label = name if name != "none" else "Constant LR"
        ax.plot(losses, label=f"{label} (acc={accs[-1]:.3f})", linewidth=2)
    ax.set_title("Learning Rate Schedule", fontsize=14)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Train Loss")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.suptitle("Training Techniques on MNIST (2-Layer MLP)", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"\n[Plot] Loss curves saved to {save_path}")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Training Techniques Comparison on MNIST")
    print("=" * 60)
    print(f"Device: {DEVICE}  |  Epochs: {EPOCHS}  |  Subset: {SUBSET_SIZE}  |  LR: {LR}")

    train_loader, test_loader = get_mnist_loaders(BATCH_SIZE, SUBSET_SIZE)
    print(f"Train batches: {len(train_loader)}  |  Test batches: {len(test_loader)}")

    results_init = experiment_init(train_loader, test_loader)
    results_opt = experiment_optimizer(train_loader, test_loader)
    results_sched = experiment_scheduler(train_loader, test_loader)

    plot_results(results_init, results_opt, results_sched)

    print("\n" + "=" * 60)
    print("All experiments completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
