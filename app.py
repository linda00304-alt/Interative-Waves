import math
import random
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# 변형된 유기적 물결(Blob) 생성 함수
def generate_ripple(center=(0.5, 0.5), r=0.3, points=300, wobble=0.15):
  angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
  # 파도의 일렁임을 표현하기 위한 복합 파형
  radii = r * (
      1
      + wobble
      * (
          np.sin(3 * angles) * 0.5
          + np.cos(5 * angles) * 0.3
          + (np.random.rand(points) - 0.5) * 0.2
      )
  )
  x = center[0] + radii * np.cos(angles)
  y = center[1] + radii * np.sin(angles)
  return x, y


# 모아나 바다 윤슬 & 물보라 렌더링
def draw_ocean_ripples(
    n_layers=12, foam_density=150, sunline_power=0.5, wobble=0.15, seed=42
):
  random.seed(seed)
  np.random.seed(seed)

  # 배경: 깔끔하고 깊은 모아나 딥블루 레이아웃
  fig, ax = plt.subplots(figsize=(7, 9), facecolor="#0B192C")
  ax.axis("off")
  ax.set_facecolor("#0B192C")

  # 1. 겹겹이 쌓이는 수중 윤슬 물결 (Ocean Ripples)
  for i in range(n_layers):
    cx, cy = random.uniform(0.2, 0.8), random.uniform(0.2, 0.8)
    rr = random.uniform(0.15, 0.45)
    x, y = generate_ripple((cx, cy), r=rr, wobble=wobble)

    # 딥블루 -> 에메랄드 -> 민트 청록색으로 이어지는 레이어
    base_r = 0.0
    base_g = random.uniform(0.5, 0.9)
    base_b = random.uniform(0.7, 1.0)
    alpha = random.uniform(0.15, 0.35)

    # 윤슬 면 채우기
    ax.fill(x, y, color=(base_r, base_g, base_b, alpha), edgecolor="none")
    # 물결 테두리 선 강조 (햇빛 반사 느낌)
    ax.plot(
        x,
        y,
        color=(0.8, 1.0, 1.0, alpha * 1.5),
        linewidth=random.uniform(0.5, 1.8),
    )

  # 2. 표면에 반짝이는 햇살 윤슬 (Sunlight Sparkles)
  n_sparkles = int(100 * sunline_power)
  sx = np.random.uniform(0.05, 0.95, n_sparkles)
  sy = np.random.uniform(0.05, 0.95, n_sparkles)
  s_sizes = np.random.uniform(10, 80, n_sparkles) * sunline_power
  ax.scatter(
      sx,
      sy,
      s=s_sizes,
      color="#E0F7FA",
      alpha=random.uniform(0.4, 0.8),
      edgecolors="none",
      marker="*",
  )

  # 3. 해안가/물결 고유의 하얀 물보라 입자 (Ocean Foams)
  fx = np.random.uniform(0.0, 1.0, foam_density)
  fy = np.random.uniform(0.0, 1.0, foam_density)
  f_sizes = np.random.uniform(3, 25, foam_density)
  ax.scatter(
      fx,
      fy,
      s=f_sizes,
      color="#FFFFFF",
      alpha=np.random.uniform(0.2, 0.6, foam_density),
      edgecolors="none",
  )

  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)
  return fig


# Streamlit UI 구성
st.set_page_config(page_title="Moana Ocean Ripples", layout="centered")
st.title("🌊 Moana Ocean Ripples & Foams")
st.caption("A Moana-themed Generative Art Project — Pure Code Implementation")

st.sidebar.header("Ocean Controls")
n_layers = st.sidebar.slider("Ripple Layers (물결 겹수)", 5, 30, 15, step=1)
wobble = st.sidebar.slider(
    "Wave Wobble (물결 일렁임)", 0.05, 0.35, 0.15, step=0.01
)
sunline_power = st.sidebar.slider(
    "Sunlight Intensity (햇살 윤슬 강도)", 0.1, 2.0, 1.0, step=0.1
)
foam_density = st.sidebar.slider(
    "Foam Density (물보라 입자 수)", 50, 400, 200, step=10
)
seed = st.sidebar.slider("Random Seed", 0, 9999, 42)

fig = draw_ocean_ripples(n_layers, foam_density, sunline_power, wobble, seed)
st.pyplot(fig)
