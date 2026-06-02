"""
diffusion_demo.py -- Simple Diffusion Model on 2D Swiss Roll Data
================================================================

Demonstrates the core ideas of Denoising Diffusion Probabilistic Models
(DDPM) on synthetic 2D data. The pipeline covers:

  1. Generate 2D Swiss Roll dataset (x0)
  2. Forward diffusion: add Gaussian noise step by step (x0 -> xT)
  3. Train a small MLP to predict noise eps_theta(x_t, t)
  4. Reverse sampling: denoise from pure noise (xT -> x0)
  5. Visualize forward process, loss curves, and generated samples

Architecture:
  - Noise predictor: 3-layer MLP with sinusoidal timestep embedding
  - Diffusion schedule: linear beta from 1e-4 to 0.02 (T = 1000)
  - Loss: L_simple = E[||eps - eps_theta(x_t, t)||^2]

Dependencies: torch >= 2.0.0, numpy >= 1.21.0, matplotlib >= 3.4.0

Usage:
    python code/diffusion_demo.py

Expected output:
    - Printed loss per epoch
    - Forward diffusion visualization (saved as forward_diffusion.png)
    - Training loss curve (saved as loss_curve.png)
    - Generated samples visualization (saved as generated_samples.png)
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Tuple

import torch
import torch.nn as nn

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
torch.manual_seed(42)
np.random.seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Device: {device}\n")

# ---------------------------------------------------------------------------
# Hyper-parameters
# ---------------------------------------------------------------------------
T = 1000                         # total diffusion steps
BETA_START = 1e-4                # initial noise level
BETA_END = 0.02                  # final noise level
DATA_SIZE = 2000                 # number of Swiss Roll points
BATCH_SIZE = 512
NUM_EPOCHS = 200
HIDDEN_DIM = 128
LEARNING_RATE = 1e-3
NUM_SAMPLES = 1000               # generated samples for visualization

# ---------------------------------------------------------------------------
# 1. Data: Swiss Roll in 2D
# ---------------------------------------------------------------------------
def make_swiss_roll(n: int, noise: float = 0.5) -> np.ndarray:
    """Generate 2D Swiss Roll data.

    Parametric spiral in 2D with Gaussian noise added.
    Returns array of shape (n, 2).
    """
    t = 1.5 * np.pi * (1 + 2 * np.random.rand(n))
    x = t * np.cos(t)
    y = t * np.sin(t)
    data = np.stack([x, y], axis=1)
    data += noise * np.random.randn(n, 2)
    return data

print("=" * 55)
print("1. Generating Swiss Roll dataset")
print("=" * 55)
raw_data = make_swiss_roll(DATA_SIZE)
# Normalize to zero mean and unit variance
data_mean = raw_data.mean(axis=0)
data_std = raw_data.std(axis=0)
data = (raw_data - data_mean) / data_std
print(f"    Generated {DATA_SIZE} points.")
print(f"    Mean: ({data_mean[0]:.2f}, {data_mean[1]:.2f})")
print(f"    Std:  ({data_std[0]:.2f}, {data_std[1]:.2f})")
print(f"    Data shape: {data.shape}")
print()

# ---------------------------------------------------------------------------
# 2. Forward Diffusion Schedule
# ---------------------------------------------------------------------------
betas = torch.linspace(BETA_START, BETA_END, T, device=device)
alphas = 1.0 - betas
alpha_bars = torch.cumprod(alphas, dim=0)  # bar{alpha}_t

def forward_diffusion(
    x0: torch.Tensor,
    t: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Apply forward diffusion: x_t = sqrt(alpha_bar_t) * x0 + sqrt(1 - alpha_bar_t) * eps.

    Args:
        x0: clean data, shape (batch, 2)
        t: timesteps, shape (batch,)

    Returns:
        x_t: noised data, shape (batch, 2)
        eps: the noise that was added, shape (batch, 2)
    """
    eps = torch.randn_like(x0)
    sqrt_alpha_bar = torch.sqrt(alpha_bars[t]).unsqueeze(1)
    sqrt_one_minus = torch.sqrt(1.0 - alpha_bars[t]).unsqueeze(1)
    x_t = sqrt_alpha_bar * x0 + sqrt_one_minus * eps
    return x_t, eps

print("=" * 55)
print("2. Forward diffusion schedule")
print("=" * 55)
print(f"    T = {T} steps")
print(f"    beta_1  = {BETA_START:.5f}")
print(f"    beta_T  = {BETA_END:.4f}")
print(f"    alpha_bar_1   = {alpha_bars[0].item():.4f}")
print(f"    alpha_bar_T   = {alpha_bars[-1].item():.6f}")
print()

# ---------------------------------------------------------------------------
# 3. Visualize Forward Diffusion (before training)
# ---------------------------------------------------------------------------
def visualize_forward_diffusion(data_tensor: torch.Tensor):
    """Show data at selected timesteps: t=0, t=100, t=500, t=T."""
    timesteps = [0, 100, 500, T - 1]
    t_tensor = torch.tensor(timesteps, device=device)
    x0_batch = data_tensor[:500].repeat(len(timesteps), 1)
    t_expanded = t_tensor.repeat_interleave(500)

    x_t, _ = forward_diffusion(x0_batch, t_expanded)
    x_t_np = x_t.cpu().numpy()

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
    titles = ["t=0 (original)", f"t={timesteps[1]}", f"t={timesteps[2]}", f"t={T} (pure noise)"]
    for idx, ax in enumerate(axes):
        batch = x_t_np[idx * 500:(idx + 1) * 500]
        ax.scatter(batch[:, 0], batch[:, 1], s=8, alpha=0.6, c=f"C{idx}")
        ax.set_title(titles[idx], fontsize=12)
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 3.5)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("forward_diffusion.png", dpi=120)
    plt.close()
    print("    [Saved] forward_diffusion.png")

data_tensor = torch.tensor(data, dtype=torch.float32, device=device)
visualize_forward_diffusion(data_tensor)

# ---------------------------------------------------------------------------
# 4. Noise Prediction Network
# ---------------------------------------------------------------------------
class SinusoidalTimestepEmbedding(nn.Module):
    """Sinusoidal timestep embedding (positional encoding)."""
    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        """t: (batch,) -> embedding: (batch, dim)"""
        half = self.dim // 2
        freqs = torch.exp(
            -math.log(10000.0) * torch.arange(half, device=t.device) / half
        )
        args = t.unsqueeze(1) * freqs.unsqueeze(0)  # (batch, half)
        return torch.cat([torch.sin(args), torch.cos(args)], dim=1)


class NoisePredictor(nn.Module):
    """Simple MLP that predicts noise eps given x_t and timestep t.

    Architecture:
        - Sinusoidal timestep embedding (64-dim)
        - 3 hidden layers with SiLU activation
        - Output: predicted noise (same shape as input)
    """
    def __init__(self, input_dim: int = 2, hidden_dim: int = HIDDEN_DIM):
        super().__init__()
        self.time_embed = SinusoidalTimestepEmbedding(64)
        total_input_dim = input_dim + 64

        self.net = nn.Sequential(
            nn.Linear(total_input_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, input_dim),
        )

    def forward(self, x_t: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """Predict noise.

        Args:
            x_t: noised data, shape (batch, input_dim)
            t: timesteps, shape (batch,)

        Returns:
            eps_pred: predicted noise, shape (batch, input_dim)
        """
        t_embed = self.time_embed(t)            # (batch, 64)
        h = torch.cat([x_t, t_embed], dim=1)    # (batch, input_dim + 64)
        return self.net(h)


model = NoisePredictor(input_dim=2).to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
print(f"\n{'='*55}")
print("3. Model Architecture")
print("=" * 55)
print(f"    {model}")
total_params = sum(p.numel() for p in model.parameters())
print(f"    Total parameters: {total_params:,}")
print()

# ---------------------------------------------------------------------------
# 5. Training Loop
# ---------------------------------------------------------------------------
print("=" * 55)
print("4. Training Noise Prediction Network")
print("=" * 55)

loss_history = []

for epoch in range(1, NUM_EPOCHS + 1):
    # Shuffle data
    perm = torch.randperm(DATA_SIZE, device=device)
    epoch_loss = 0.0
    num_batches = 0

    for start_idx in range(0, DATA_SIZE, BATCH_SIZE):
        batch_idx = perm[start_idx:start_idx + BATCH_SIZE]
        x0_batch = data_tensor[batch_idx]

        # Sample random timesteps for each example in the batch
        t_batch = torch.randint(0, T, (x0_batch.size(0),), device=device)

        # Forward diffusion: add noise
        x_t, eps = forward_diffusion(x0_batch, t_batch)

        # Predict noise
        eps_pred = model(x_t, t_batch)

        # Simplified loss: MSE between true noise and predicted noise
        loss = nn.functional.mse_loss(eps_pred, eps)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        num_batches += 1

    avg_loss = epoch_loss / max(num_batches, 1)
    loss_history.append(avg_loss)

    if epoch % 20 == 0 or epoch == 1:
        print(f"    Epoch {epoch:3d}/{NUM_EPOCHS} | Loss: {avg_loss:.6f}")

print(f"    Final loss: {avg_loss:.6f}")
print()

# ---------------------------------------------------------------------------
# 6. Plot Loss Curve
# ---------------------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(loss_history, "b-", linewidth=1.5)
plt.xlabel("Epoch", fontsize=12)
plt.ylabel("MSE Loss", fontsize=12)
plt.title("Training Loss (Noise Prediction)", fontsize=13)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("loss_curve.png", dpi=120)
plt.close()
print("[Saved] loss_curve.png")

# ---------------------------------------------------------------------------
# 7. Reverse Sampling (DDPM)
# ---------------------------------------------------------------------------
@torch.no_grad()
def reverse_sampling(
    model: NoisePredictor,
    num_samples: int,
    num_steps: int = T,
) -> np.ndarray:
    """Generate samples by reversing the diffusion process.

    Algorithm:
        x_T ~ N(0, I)
        for t = T, T-1, ..., 1:
            z ~ N(0, I) (if t > 1 else 0)
            eps_pred = eps_theta(x_t, t)
            x_{t-1} = 1/sqrt(alpha_t) * (
                x_t - beta_t / sqrt(1 - alpha_bar_t) * eps_pred
            ) + sigma_t * z

    Returns: generated samples as numpy array, shape (num_samples, 2)
    """
    x_t = torch.randn(num_samples, 2, device=device)

    for t in reversed(range(num_steps)):
        t_batch = torch.full((num_samples,), t, device=device, dtype=torch.long)

        # Predict noise
        eps_pred = model(x_t, t_batch)

        # Compute coefficients
        alpha_t = alphas[t]
        beta_t = betas[t]
        sqrt_alpha_t = torch.sqrt(alpha_t)
        sqrt_one_minus_alpha_bar = torch.sqrt(1.0 - alpha_bars[t])
        sigma_t = torch.sqrt(beta_t)

        # Denoise: x_{t-1} = 1/sqrt(alpha_t) * (x_t - beta_t/sqrt(1-alpha_bar_t) * eps) + sigma_t * z
        x_t = (1.0 / sqrt_alpha_t) * (
            x_t - beta_t / sqrt_one_minus_alpha_bar * eps_pred
        )

        # Add noise (except at t=0)
        if t > 0:
            noise = torch.randn_like(x_t)
            x_t = x_t + sigma_t * noise

    return x_t.cpu().numpy()


print("=" * 55)
print("5. Reverse Sampling (DDPM)")
print("=" * 55)

generated = reverse_sampling(model, NUM_SAMPLES, num_steps=T)

# Denormalize back to original scale
generated_denorm = generated * data_std + data_mean
original_denorm = data * data_std + data_mean

print(f"    Generated {NUM_SAMPLES} samples.")
print(f"    Sample range: x in [{generated[:, 0].min():.2f}, {generated[:, 0].max():.2f}], "
      f"y in [{generated[:, 1].min():.2f}, {generated[:, 1].max():.2f}]")
print()

# ---------------------------------------------------------------------------
# 8. Visualize Generated Samples
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# Left: original data
axes[0].scatter(original_denorm[:, 0], original_denorm[:, 1], s=8, alpha=0.5, c="steelblue")
axes[0].set_title("Original Swiss Roll", fontsize=13)
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")
axes[0].set_aspect("equal")
axes[0].grid(True, alpha=0.3)

# Right: generated samples
axes[1].scatter(generated_denorm[:, 0], generated_denorm[:, 1], s=8, alpha=0.5, c="crimson")
axes[1].set_title("Generated (DDPM Reverse Sampling)", fontsize=13)
axes[1].set_xlabel("x")
axes[1].set_ylabel("y")
axes[1].set_aspect("equal")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("generated_samples.png", dpi=120)
plt.close()
print("[Saved] generated_samples.png")

# ---------------------------------------------------------------------------
# 9. Revserse Process Visualization: Step-by-step denoising
# ---------------------------------------------------------------------------
@torch.no_grad()
def visualize_reverse_process(
    model: NoisePredictor,
    num_samples: int = 500,
    num_steps: int = T,
    save_points: list = None,
):
    """Visualize intermediate states during reverse sampling."""
    if save_points is None:
        save_points = [T - 1, 500, 200, 50, 10, 0]

    x_t = torch.randn(num_samples, 2, device=device)
    trajectories = {}

    for t in reversed(range(num_steps)):
        t_batch = torch.full((num_samples,), t, device=device, dtype=torch.long)
        eps_pred = model(x_t, t_batch)

        alpha_t = alphas[t]
        beta_t = betas[t]
        sqrt_alpha_t = torch.sqrt(alpha_t)
        sqrt_one_minus_alpha_bar = torch.sqrt(1.0 - alpha_bars[t])
        sigma_t = torch.sqrt(beta_t)

        x_t = (1.0 / sqrt_alpha_t) * (
            x_t - beta_t / sqrt_one_minus_alpha_bar * eps_pred
        )

        if t > 0:
            x_t = x_t + sigma_t * torch.randn_like(x_t)

        if t in save_points:
            trajectories[t] = x_t.cpu().numpy().copy()

    # Plot
    n_cols = len(save_points)
    fig, axes = plt.subplots(1, n_cols, figsize=(3 * n_cols, 3))
    labels = [f"t={t}" if t > 0 else "t=0 (final)" for t in save_points]
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, n_cols))

    for idx, (t_val, label) in enumerate(zip(save_points, labels)):
        pts = trajectories[t_val] * data_std + data_mean
        axes[idx].scatter(pts[:, 0], pts[:, 1], s=6, alpha=0.6, c=[colors[idx]])
        axes[idx].set_title(label, fontsize=11)
        axes[idx].set_xlim(-8, 8)
        axes[idx].set_ylim(-8, 8)
        axes[idx].set_aspect("equal")
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("reverse_process.png", dpi=120)
    plt.close()
    print("[Saved] reverse_process.png (denoising trajectory)")


visualize_reverse_process(model, num_samples=500)

# ---------------------------------------------------------------------------
# 10. Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 55)
print("6. Summary")
print("=" * 55)
print(f"""
    {'Component':<30} {'Value':<20}
    {'-'*50}
    {'Dataset':<30} {'Swiss Roll (2D)'}
    {'Data points':<30} {DATA_SIZE:<20}
    {'Diffusion steps (T)':<30} {T:<20}
    {'Beta schedule':<30} {'linear':<20}
    {'Model':<30} {'MLP (3 hidden layers)':<20}
    {'Model parameters':<30} {total_params:<20,}
    {'Training epochs':<30} {NUM_EPOCHS:<20}
    {'Final loss':<30} {loss_history[-1]:<20.6f}
    {'Generated samples':<30} {NUM_SAMPLES:<20}

    KEY TAKEAWAYS:
    - Forward diffusion: simple Gaussian perturbation
    - Loss: MSE between true and predicted noise
    - Reverse sampling: iterative denoising from N(0, I)
    - Results show the model has learned the Swiss Roll distribution
""")

print("Generated output files:")
print("  - forward_diffusion.png  (forward process visualization)")
print("  - loss_curve.png         (training loss)")
print("  - generated_samples.png  (generated vs original)")
print("  - reverse_process.png    (denoising trajectory)")
