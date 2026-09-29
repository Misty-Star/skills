# Agent Skills Collection

> A curated collection of personal AI agent skills compatible with `npx skills`, Claude Code, Cursor, and other agentic coding environments.

[English](README.md) | [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills Standard](https://img.shields.io/badge/standard-skills.sh-blue)](https://skills.sh)

---

## 📦 Included Skills

| Skill | Description | Triggers / Keywords |
| :--- | :--- | :--- |
| [`pixel-jpg-to-svg`](skills/pixel-jpg-to-svg) | Converts raster logos and pixel art (JPG/PNG) into crisp, scalable SVG vector paths using grid reconstruction. | `vectorize pixel art`, `jpg to svg`, `pixel logo to svg` |
| [`create-readme`](skills/create-readme) | Generates structured, high-conversion open-source `README.md` files adhering to 2026 developer standards. | `create readme`, `generate readme`, `polish readme` |

---

## 🚀 Quick Start

You can install and use these skills in any supported agent via the [skills CLI](https://skills.sh):

### 1. Preview skills without installing
```bash
npx skills add Misty-Star/skills --list
```

### 2. Interactive installation (choose skills)
```bash
npx skills add Misty-Star/skills
```

### 3. Install a specific skill
```bash
# Install pixel-jpg-to-svg only
npx skills add Misty-Star/skills --skill pixel-jpg-to-svg

# Install create-readme only
npx skills add Misty-Star/skills --skill create-readme
```

### 4. Install all skills
```bash
npx skills add Misty-Star/skills --skill '*'
```

---

## 📂 Repository Structure

```text
skills/
├── README.md                      # English documentation & guide
├── README.zh-CN.md                # Chinese documentation & guide
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
└── skills/                        # Multi-skill collection directory
    ├── pixel-jpg-to-svg/          # Pixel art & logo vectorization skill
    │   ├── SKILL.md               # Entry point & procedural workflow
    │   ├── scripts/               # Python grid reconstruction script
    │   │   └── pixel_jpg_to_svg.py
    │   └── references/            # Algorithm tuning reference
    │       └── grid-reconstruct.md
    └── create-readme/             # README generation & styling skill
        └── SKILL.md               # Entry point & template guidelines
```

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).
