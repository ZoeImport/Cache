"""
VAE 实战: 从零实现 Variational Autoencoder 并在 MNIST 上训练
(VAE in Action: Implementing Variational Autoencoder from Scratch on MNIST)
================================================================================
依赖 (Dependencies): torch>=2.1.0, torchvision>=0.16.0, matplotlib>=3.7.0, numpy>=1.24.0

涵盖 (Covers):
  1. VAE 模型: Encoder -> Reparameterize -> Decoder
  2. 完整训练循环与逐 epoch 日志
  3. 重建损失 + KL 损失的分量可视化
  4. 2D 潜在空间可视化 (按数字类别着色)
  5. 潜在空间插值 (在两个随机样本之间线性过渡)
  6. 从先验 N(0, I) 采样生成新图像

数学核心 (Mathematical Core):
  ELBO = E_q[log p(x|z)] - KL(q(z|x) || p(z))
  Reparameterization: z = mu + sigma * eps, eps ~ N(0, I)
  KL(N(mu, sigma^2) || N(0, 1)) = 0.5 * (mu^2 + sigma^2 - log(sigma^2) - 1)

运行 (Usage):
  python vae.py                  # 默认训练 20 个 epoch
  python vae.py --epochs 10      # 训练 10 个 epoch
  python vae.py --latent-dim 2   # 2 维潜在空间 (便于可视化)
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# ============================================================
# 0. 全局设置 (Global Settings)
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")
print(f"PyTorch version: {torch.__version__}")
print()

# ============================================================
# 1. VAE 模型定义 (VAE Model Definition)
# ============================================================
class Encoder(nn.Module):
    """编码器: 将图像 x 映射为潜在分布的参数 mu, logvar.

    Encoder: maps image x to latent distribution parameters mu, logvar.

    架构 (Architecture):
        Input (1x28x28)
            -> Flatten (784)
            -> Linear(784, 400) + ReLU
            -> Linear(400, 2 * latent_dim) -> mu, logvar
    """

    def __init__(self, latent_dim: int = 2):
        super().__init__()
        self.fc1 = nn.Linear(784, 400)
        self.fc_mu = nn.Linear(400, latent_dim)
        self.fc_logvar = nn.Linear(400, latent_dim)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Forward pass of encoder.

        Args:
            x: shape (B, 1, 28, 28)
        Returns:
            mu:     shape (B, latent_dim)
            logvar: shape (B, latent_dim)
        """
        h = x.view(x.size(0), -1)  # (B, 784)
        h = F.relu(self.fc1(h))
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar


class Decoder(nn.Module):
    """解码器: 从潜在编码 z 重建图像 x.

    Decoder: reconstructs image x from latent code z.

    架构 (Architecture):
        Input (latent_dim)
            -> Linear(latent_dim, 400) + ReLU
            -> Linear(400, 784) + Sigmoid
            -> Reshape (1x28x28)
    """

    def __init__(self, latent_dim: int = 2):
        super().__init__()
        self.fc1 = nn.Linear(latent_dim, 400)
        self.fc2 = nn.Linear(400, 784)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        """Decode latent code to image.

        Args:
            z: shape (B, latent_dim)
        Returns:
            x_recon: shape (B, 1, 28, 28)
        """
        h = F.relu(self.fc1(z))
        x_recon = torch.sigmoid(self.fc2(h))
        return x_recon.view(-1, 1, 28, 28)


class VAE(nn.Module):
    """变分自编码器 (Variational Autoencoder).

    核心操作 (Core Operations):
        1. Encode:    x -> mu, logvar
        2. Reparam:   z = mu + exp(0.5 * logvar) * eps
        3. Decode:    z -> x_recon
    """

    def __init__(self, latent_dim: int = 2):
        super().__init__()
        self.latent_dim = latent_dim
        self.encoder = Encoder(latent_dim)
        self.decoder = Decoder(latent_dim)

    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        """重参数化技巧: z = mu + sigma * eps.

        Reparameterization trick: z = mu + sigma * eps, eps ~ N(0, I).

        Args:
            mu:     mean of the latent distribution, shape (B, latent_dim)
            logvar: log-variance of the latent distribution, shape (B, latent_dim)
        Returns:
            z: sampled latent code, shape (B, latent_dim)
        """
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std, device=std.device)
        return mu + std * eps

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """前向传播 (Forward pass).

        Args:
            x: input images, shape (B, 1, 28, 28)
        Returns:
            x_recon: reconstructed images, shape (B, 1, 28, 28)
            mu:      latent means, shape (B, latent_dim)
            logvar:  latent log-variances, shape (B, latent_dim)
        """
        mu, logvar = self.encoder(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decoder(z)
        return x_recon, mu, logvar


# ============================================================
# 2. 损失函数 (Loss Function)
# ============================================================
def vae_loss(
    x_recon: torch.Tensor,
    x: torch.Tensor,
    mu: torch.Tensor,
    logvar: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """计算 VAE 损失: Reconstruction Loss + KL Loss.

    VAE Loss = Reconstruction Loss + KL Loss

    重建损失 (Reconstruction Loss): BCE between x and x_recon
    KL 损失 (KL Loss): KL(N(mu, sigma^2) || N(0, 1))
        = 0.5 * sum(mu^2 + sigma^2 - log(sigma^2) - 1)

    Args:
        x_recon: reconstructed images, shape (B, 1, 28, 28)
        x:       original images, shape (B, 1, 28, 28)
        mu:      latent means, shape (B, latent_dim)
        logvar:  latent log-variances, shape (B, latent_dim)
    Returns:
        total_loss:       total VAE loss (scalar Tensor)
        recon_loss:       reconstruction loss (scalar Tensor)
        kl_loss:          KL divergence loss (scalar Tensor)
    """
    # Reconstruction loss: BCE (Binary Cross-Entropy)
    recon_loss = F.binary_cross_entropy(x_recon, x, reduction="sum")

    # KL divergence: KL(N(mu, sigma^2) || N(0, 1))
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    total_loss = recon_loss + kl_loss

    # Normalize to per-sample average (for logging)
    batch_size = x.size(0)
    return total_loss / batch_size, recon_loss / batch_size, kl_loss / batch_size


# ============================================================
# 3. 可视化工具 (Visualization Utilities)
# ============================================================
def plot_latent_space(
    model: VAE,
    dataloader: DataLoader,
    epoch: int,
    save_dir: Path,
) -> None:
    """绘制 2D 潜在空间，按数字类别着色。

    Plot the 2D latent space, colored by digit class.
    """
    model.eval()
    mus = []
    labels = []
    with torch.no_grad():
        for images, lbls in dataloader:
            images = images.to(DEVICE)
            mu, _ = model.encoder(images)
            mus.append(mu.cpu().numpy())
            labels.append(lbls.numpy())
    mus = np.concatenate(mus, axis=0)
    labels = np.concatenate(labels, axis=0)

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(mus[:, 0], mus[:, 1], c=labels, cmap="tab10", alpha=0.6, s=8)
    ax.set_title(f"Latent Space (epoch {epoch})", fontsize=14)
    ax.set_xlabel("z1", fontsize=12)
    ax.set_ylabel("z2", fontsize=12)
    cbar = fig.colorbar(scatter, ax=ax, ticks=range(10))
    cbar.set_label("Digit Label", fontsize=12)
    fig.tight_layout()
    fig.savefig(save_dir / f"latent_space_epoch_{epoch:03d}.png", dpi=150)
    plt.close(fig)


def plot_interpolation(
    model: VAE,
    save_dir: Path,
    num_steps: int = 10,
) -> None:
    """在潜在空间中两个随机点之间插值，生成过渡图像。

    Interpolate between two random points in latent space.
    """
    model.eval()
    with torch.no_grad():
        z1 = torch.randn(1, model.latent_dim, device=DEVICE)
        z2 = torch.randn(1, model.latent_dim, device=DEVICE)
        alphas = np.linspace(0, 1, num_steps)
        zs = torch.stack([
            (1 - alpha) * z1 + alpha * z2 for alpha in alphas
        ]).squeeze(1)
        decoded = model.decoder(zs)

    fig, axes = plt.subplots(1, num_steps, figsize=(num_steps * 1.5, 2))
    for i in range(num_steps):
        img = decoded[i].cpu().squeeze().numpy()
        axes[i].imshow(img, cmap="gray")
        axes[i].axis("off")
        axes[i].set_title(f"a={alphas[i]:.1f}", fontsize=9)
    fig.suptitle("Latent Space Interpolation", fontsize=14, y=1.05)
    fig.tight_layout()
    fig.savefig(save_dir / "interpolation.png", dpi=150)
    plt.close(fig)


def plot_generated_samples(
    model: VAE,
    save_dir: Path,
    num_samples: int = 25,
) -> None:
    """从先验 N(0, I) 采样并解码生成新图像。

    Sample from the prior N(0, I) and decode.
    """
    model.eval()
    with torch.no_grad():
        z = torch.randn(num_samples, model.latent_dim, device=DEVICE)
        samples = model.decoder(z).cpu()

    grid = torchvision.utils.make_grid(samples, nrow=5, padding=2)
    grid_img = grid.permute(1, 2, 0).numpy()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid_img, cmap="gray")
    ax.set_title("Generated Samples from Prior N(0, I)", fontsize=14)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(save_dir / "generated_samples.png", dpi=150)
    plt.close(fig)


def plot_reconstructions(
    model: VAE,
    dataloader: DataLoader,
    save_dir: Path,
) -> None:
    """展示原始图像与重建图像的对比。

    Show original vs. reconstruction side by side.
    """
    model.eval()
    images, _ = next(iter(dataloader))
    images = images.to(DEVICE)
    with torch.no_grad():
        recon, _, _ = model(images)

    images = images.cpu()
    recon = recon.cpu()

    n = min(8, images.size(0))
    fig, axes = plt.subplots(2, n, figsize=(n * 1.5, 3))
    for i in range(n):
        axes[0, i].imshow(images[i].squeeze(), cmap="gray")
        axes[0, i].axis("off")
        if i == 0:
            axes[0, i].set_ylabel("Original", fontsize=10)
        axes[1, i].imshow(recon[i].squeeze(), cmap="gray")
        axes[1, i].axis("off")
        if i == 0:
            axes[1, i].set_ylabel("Recon", fontsize=10)
    fig.suptitle("Original vs. Reconstruction", fontsize=14)
    fig.tight_layout()
    fig.savefig(save_dir / "reconstructions.png", dpi=150)
    plt.close(fig)


def plot_loss_curves(
    recon_losses: list[float],
    kl_losses: list[float],
    total_losses: list[float],
    save_dir: Path,
) -> None:
    """绘制训练损失曲线。

    Plot training loss curves.
    """
    epochs = range(1, len(total_losses) + 1)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    axes[0].plot(epochs, total_losses, "b-", linewidth=2)
    axes[0].set_title("Total Loss", fontsize=13)
    axes[0].set_xlabel("Epoch", fontsize=11)
    axes[0].set_ylabel("Loss", fontsize=11)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(epochs, recon_losses, "r-", linewidth=2)
    axes[1].set_title("Recon Loss (BCE)", fontsize=13)
    axes[1].set_xlabel("Epoch", fontsize=11)
    axes[1].set_ylabel("Loss", fontsize=11)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(epochs, kl_losses, "g-", linewidth=2)
    axes[2].set_title("KL Loss", fontsize=13)
    axes[2].set_xlabel("Epoch", fontsize=11)
    axes[2].set_ylabel("Loss", fontsize=11)
    axes[2].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_dir / "loss_curves.png", dpi=150)
    plt.close(fig)


# ============================================================
# 4. 数据加载 (Data Loading)
# ============================================================
def load_mnist(batch_size: int = 128) -> tuple[DataLoader, DataLoader]:
    """加载 MNIST 数据集。

    Load MNIST dataset with normalization to [0, 1].

    Returns:
        train_loader, test_loader
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    train_dataset = torchvision.datasets.MNIST(
        root=str(OUTPUT_DIR.parent / "data"),
        train=True,
        transform=transform,
        download=True,
    )
    test_dataset = torchvision.datasets.MNIST(
        root=str(OUTPUT_DIR.parent / "data"),
        train=False,
        transform=transform,
        download=True,
    )

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=2
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False, num_workers=2
    )
    return train_loader, test_loader


# ============================================================
# 5. 训练循环 (Training Loop)
# ============================================================
def train_one_epoch(
    model: VAE,
    dataloader: DataLoader,
    optimizer: optim.Optimizer,
) -> tuple[float, float, float]:
    """训练一个 epoch。

    Returns:
        (avg_total_loss, avg_recon_loss, avg_kl_loss)
    """
    model.train()
    total_loss_sum = 0.0
    recon_loss_sum = 0.0
    kl_loss_sum = 0.0
    num_batches = 0

    for images, _ in dataloader:
        images = images.to(DEVICE)
        optimizer.zero_grad()

        x_recon, mu, logvar = model(images)
        total_loss, recon_loss, kl_loss = vae_loss(x_recon, images, mu, logvar)

        total_loss.backward()
        optimizer.step()

        total_loss_sum += total_loss.item()
        recon_loss_sum += recon_loss.item()
        kl_loss_sum += kl_loss.item()
        num_batches += 1

    avg_total = total_loss_sum / num_batches
    avg_recon = recon_loss_sum / num_batches
    avg_kl = kl_loss_sum / num_batches
    return avg_total, avg_recon, avg_kl


def evaluate(
    model: VAE,
    dataloader: DataLoader,
) -> tuple[float, float, float]:
    """在测试集上评估模型。

    Returns:
        (avg_total_loss, avg_recon_loss, avg_kl_loss)
    """
    model.eval()
    total_loss_sum = 0.0
    recon_loss_sum = 0.0
    kl_loss_sum = 0.0
    num_batches = 0

    with torch.no_grad():
        for images, _ in dataloader:
            images = images.to(DEVICE)
            x_recon, mu, logvar = model(images)
            total_loss, recon_loss, kl_loss = vae_loss(x_recon, images, mu, logvar)

            total_loss_sum += total_loss.item()
            recon_loss_sum += recon_loss.item()
            kl_loss_sum += kl_loss.item()
            num_batches += 1

    avg_total = total_loss_sum / num_batches
    avg_recon = recon_loss_sum / num_batches
    avg_kl = kl_loss_sum / num_batches
    return avg_total, avg_recon, avg_kl


# ============================================================
# 6. 主函数 (Main)
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Train a VAE on MNIST and visualize latent space."
    )
    parser.add_argument("--epochs", type=int, default=20, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=128, help="Batch size")
    parser.add_argument("--latent-dim", type=int, default=2, help="Latent dimension")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    args = parser.parse_args()

    print("=" * 60)
    print("VAE Training on MNIST")
    print("=" * 60)
    print(f"  Epochs:        {args.epochs}")
    print(f"  Batch size:    {args.batch_size}")
    print(f"  Latent dim:    {args.latent_dim}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Device:        {DEVICE}")
    print("=" * 60)
    print()

    # Data
    train_loader, test_loader = load_mnist(args.batch_size)
    print(f"Train samples: {len(train_loader.dataset)}")
    print(f"Test samples:  {len(test_loader.dataset)}")
    print()

    # Model
    model = VAE(latent_dim=args.latent_dim).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {total_params:,}")
    print()

    # Training
    train_total_losses: list[float] = []
    train_recon_losses: list[float] = []
    train_kl_losses: list[float] = []
    test_total_losses: list[float] = []

    print("Starting training...")
    print("-" * 72)
    print(f"{'Epoch':>6} | {'Train Total':>12} | {'Train Recon':>12} | {'Train KL':>12} | {'Test Total':>12}")
    print("-" * 72)

    for epoch in range(1, args.epochs + 1):
        train_total, train_recon, train_kl = train_one_epoch(
            model, train_loader, optimizer
        )
        test_total, _, _ = evaluate(model, test_loader)

        train_total_losses.append(train_total)
        train_recon_losses.append(train_recon)
        train_kl_losses.append(train_kl)
        test_total_losses.append(test_total)

        print(
            f"{epoch:>6} | {train_total:>12.2f} | {train_recon:>12.2f} "
            f"| {train_kl:>12.2f} | {test_total:>12.2f}"
        )

        # Visualization every 5 epochs
        if epoch % 5 == 0 or epoch == 1:
            plot_latent_space(model, test_loader, epoch, OUTPUT_DIR)

    print("-" * 72)
    print("Training complete!")
    print()

    # Final visualizations
    print("Generating visualizations...")
    plot_latent_space(model, test_loader, args.epochs, OUTPUT_DIR)
    plot_interpolation(model, OUTPUT_DIR)
    plot_generated_samples(model, OUTPUT_DIR)
    plot_reconstructions(model, test_loader, OUTPUT_DIR)
    plot_loss_curves(
        train_recon_losses, train_kl_losses, train_total_losses, OUTPUT_DIR
    )
    print(f"All figures saved to {OUTPUT_DIR}/")
    print()

    # Show final losses
    print("=" * 60)
    print("Final Results")
    print("=" * 60)
    print(f"  Train Total Loss:  {train_total_losses[-1]:.2f}")
    print(f"  Train Recon Loss:  {train_recon_losses[-1]:.2f}")
    print(f"  Train KL Loss:     {train_kl_losses[-1]:.2f}")
    print(f"  Test Total Loss:   {test_total_losses[-1]:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
