# Agent Skills 个人技能集

> 个人维护的 AI Agent 技能集合，遵循 [skills.sh](https://skills.sh) 规范，兼容 `npx skills`、Claude Code、Cursor、Antigravity 等各类 Agent 编程环境。

[English](README.md) | [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills Standard](https://img.shields.io/badge/standard-skills.sh-blue)](https://skills.sh)

---

## 📦 已收录技能

| 技能名称 | 说明 | 触发词 / 场景 |
| :--- | :--- | :--- |
| [`pixel-jpg-to-svg`](skills/pixel-jpg-to-svg) | 通过网格重建算法，将 JPG/PNG 像素画及图标无损转换为真正的 SVG 矢量路径（非简单栅格内嵌）。 | `像素画转矢量`, `jpg to svg`, `pixel logo to svg` |
| [`create-readme`](skills/create-readme) | 按照现代开源最佳实践，快速为项目生成结构严谨、转化率高的规范 `README.md`。 | `写readme`, `生成readme`, `polish readme` |

---

## 🚀 快速上手

你可以在任何支持的 Agent 环境中，使用 [skills CLI](https://skills.sh) 快速安装和使用这些技能：

### 1. 预览仓库中的所有技能（不安装）
```bash
npx skills add Misty-Star/skills --list
```

### 2. 交互式选择安装
```bash
npx skills add Misty-Star/skills
```

### 3. 安装指定技能
```bash
# 仅安装 pixel-jpg-to-svg
npx skills add Misty-Star/skills --skill pixel-jpg-to-svg

# 仅安装 create-readme
npx skills add Misty-Star/skills --skill create-readme
```

### 4. 安装全部技能
```bash
npx skills add Misty-Star/skills --skill '*'
```

---

## 📂 仓库目录结构

```text
skills/
├── README.md                      # 英文说明与安装文档
├── README.zh-CN.md                # 中文说明与安装文档
├── LICENSE                        # MIT 开源协议
├── .gitignore                     # Git 忽略配置
└── skills/                        # 多技能归集目录
    ├── pixel-jpg-to-svg/          # 像素画矢量化技能
    │   ├── SKILL.md               # 技能入口与工作流定义
    │   ├── scripts/               # Python 网格重建脚本
    │   │   └── pixel_jpg_to_svg.py
    │   └── references/            # 算法与调参说明
    │       └── grid-reconstruct.md
    └── create-readme/             # README 规范生成技能
        └── SKILL.md               # 技能入口与模板规范
```

---

## 📄 开源协议

本项目基于 [MIT 协议](LICENSE) 开源。
