import io
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import requests
import streamlit as st
from matplotlib.colors import hsv_to_rgb
from PIL import Image

# 인터넷에서 모아나 포스터 이미지 직접 가져오기 (파일 업로드 필요 없음)
IMAGE_URL = "https://m.media-amazon.com/images/M/MVBmMjAxNWZhNWItYjA5Yi00ZGEyLTgxNWUtMTI3YTIyNWY3ZmE3XkEyXkFqcGc@._V1_.jpg"


@st.cache_data
def load_poster_image():
  response = requests.get(IMAGE_URL)
  return Image.open(io.BytesIO(response.content))


def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
  angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
  radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
  x = center[0] + radii * np.cos(angles)
  y = center[1] + radii * np.sin(angles)
  return x, y


def make_palette(k=6, mode="pastel", base_h=0.60):
  cols = []
  for _ in range(k):
    if mode == "pastel":
      h = random.random()
      s = random.uniform(0.15, 0.35)
      v = random.uniform(0.9, 1.0)
    elif mode == "vivid":
      h = random.random()
      s = random.uniform(0.8, 1.0)
      v = random.uniform(0.8, 1.0)
    elif mode == "mono":
      h = base_h
      s = random.uniform(0.2, 0.6)
      v = random.uniform(0.5, 1.0)
    else:
      h = random.random()
      s = random.uniform(0.3, 1.0)
      v = random.uniform(0.5, 1.0)
    cols.append(tuple(hsv_to_rgb([h, s, v])))
  return cols


def draw_interactive_moana(
    moana_image, n_layers=8, wobble=0.15, palette_mode="pastel", seed=0
):
  random.seed(seed)
  np.random.seed(seed)
  fig, ax = plt.subplots(figsize=(6, 8))
  ax.axis("off")

  # 모아나 이미지 배경으로 깔기
  ax.imshow(moana_image, extent=[0, 1, 0, 1])

  palette = make_palette(6, mode=palette_mode)
  for _ in range(n_layers):
    cx, cy = random.uniform(0.2, 0.8), random.uniform(0.1, 0.6)
    rr = random.uniform(0.1, 0.3)
    x, y = blob((cx, cy), r=rr, wobble=wobble)
    color = random.choice(palette)
    alpha = random.uniform(0.25, 0.5)
    ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

  return fig


st.set_page_config(page_title="Interactive Moana Poster", layout="centered")
st.title("Interactive Moana Poster")
st.caption("A Moana-themed Generative Art Project")

# 이미지 로드
moana_img = load_poster_image()

st.sidebar.header("Controls")
n_layers = st.sidebar.slider(
    "Ocean Depth", min_value=3, max_value=20, value=8, step=1
)
wobble = st.sidebar.slider(
    "Wave Wobble", min_value=0.01, max_value=0.30, value=0.15, step=0.01
)
palette_mode = st.sidebar.selectbox(
    "Palette mode", ["pastel", "vivid", "mono", "random"]
)
seed = st.sidebar.slider("Seed", min_value=0, max_value=9999, value=0, step=1)

# 포스터 그리기
fig = draw_interactive_moana(moana_img, n_layers, wobble, palette_mode, seed)
st.pyplot(fig)
