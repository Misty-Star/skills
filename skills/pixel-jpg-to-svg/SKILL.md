---
name: pixel-jpg-to-svg
description: Convert JPG/PNG logos and pixel art into true SVG vector paths with optional transparent background. Use when the user asks to turn a jpg into svg, vectorize pixel art, trace a flat logo, keep crisp pixel blocks, or export a scalable icon. Prefer grid reconstruction for pixel art. Do not treat this as embedding a raster inside an svg wrapper unless the user only needs a container.
metadata:
  type: workflow
  version: "1.0"
---

# Pixel JPG to SVG

把位图 logo / 像素画转成可缩放 SVG。默认做**真路径**，不是把 JPG 嵌进 SVG。

## 先判断模式

读图后先分类，再动手：

- 像素风、图标、色块少、边缘呈台阶 → **网格重建**（本 skill 主路径）
- 扁平 logo、文字、清晰描边但非像素格 → 分色层轮廓描摹
- 照片、复杂渐变、人像 → 先说明效果差；用户仍坚持再做高色数海报化

用户没给图时，先要图，并确认四件事：真矢量还是仅包装、背景是否透明、是否保留彩色、能否减色。

## 环境约束

沙盒里通常有 `Pillow`、`numpy`、ImageMagick `convert`。不要假设有 `sklearn`、`cv2`、`potrace`、`vtracer`、`inkscape`。网格重建用捆绑脚本即可。

脚本路径：`scripts/pixel_jpg_to_svg.py`

## 网格重建流程（像素 logo）

1. 用 `read_file` 看原图，确认是像素风而不是照片。
2. 跑脚本。先探测格点，再导出 SVG + 透明预览 PNG：

```bash
python3 scripts/pixel_jpg_to_svg.py INPUT.jpg \
  --out-svg /home/workdir/artifacts/logo.svg \
  --out-preview /home/workdir/artifacts/logo_preview.png \
  --transparent --pad 2
```

3. 用 `read_file` 打开预览 PNG，对照原图检查高光、描边、台阶是否错位。
4. 若格点偏了或颜色糊了，加参数重跑，不要手写一整份新脚本：
   - `--period N` / `--ox N` / `--oy N` 锁定格点
   - `--thresh N` 颜色合并阈值（默认 14；越大越减色）
   - `--bg-dist N` 背景判定（默认 22）
   - `--bg-rgb R G B` 背景色；也可用 `--auto-bg`
5. 把 SVG 和预览交给用户。说明这是像素矩形路径、可无限缩放、背景透明。

脚本算法与调参细节见 `references/grid-reconstruct.md`。

## SVG 约定

- `viewBox` 用像素格坐标，一格 = 1 用户单位。
- 背景不画矩形，保持透明。
- 根节点加 `shape-rendering="crispEdges"`，保留像素感。
- 同色相邻格合并成更大的 `<rect>`，按亮度从深到浅绘制，高光在上。
- 不要把整张 JPG base64 嵌进 SVG，除非用户只要包装模式。

## 包装模式（仅当用户只要容器）

```bash
convert INPUT.jpg SVG:output.svg
```

先告诉用户放大仍会糊。

## 非像素扁平 logo

没有可靠描边工具时：量化前景色 → 每色做成二值掩膜 → 按连通域输出矩形或路径。颜色很少时也可用本脚本近似。不要对照片承诺描成干净矢量。

## 交付

- 主文件：`.svg`
- 对照预览：透明底 PNG
- 用 `render_file` 给出下载
- 简要说明模式、画布格数、颜色数、已知差异（JPG 抗锯齿残留等）
