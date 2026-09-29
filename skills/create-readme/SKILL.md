---
name: create-readme
description: Create an appealing, structured, and comprehensive README.md for a project following open-source best practices. Activate when the user asks to write, generate, update, or polish a README.md.
metadata:
  type: workflow
  version: "1.0"
---

## Role

You're a senior expert software engineer with extensive experience in open source projects. You always make sure the README files you write are appealing, informative, and easy to read.

## Core Principles

Before writing, answer three questions: what is this, why is it worth using, and how do I get it running right now? The README guides the reader from "unfamiliar" to "first success" — deep detail belongs in `docs/`, `CONTRIBUTING.md`, or the project site, not here.

Read order: title and one-liner → visual proof → value → install → minimal working example → contribution and license. Follow this order.

## Recommended Structure

Sections marked **Required** belong in almost every project. Others are optional but valuable where noted.

| Order | Section | Required? | Notes |
|-------|---------|-----------|-------|
| 1 | Title + Logo | Required | Match the repo / package name |
| 2 | Badges | Strongly recommended | CI, license, version — 4–6 max |
| 3 | One-liner description | Required | What, who, differentiator |
| 4 | Language switcher | When international | Link at the very top |
| 5 | Demo (screenshot / GIF / link) | Required for UI/CLI | Highest-conversion section |
| 6 | Table of contents | When > ~100 lines | |
| 7 | Background / motivation | Optional but valuable | Why this exists |
| 8 | Features | Recommended | 3–7 concrete, differentiating points |
| 9 | Stack / architecture / directory | Medium-large projects | Mental model for contributors |
| 10 | Requirements | Recommended | Avoid "can't install" frustration |
| 11 | Installation / quick start | Required | Shortest copy-paste path to running |
| 12 | Usage examples | Required | Minimal runnable + 1–2 advanced |
| 13 | Configuration | When configurable | Table: name / default / description |
| 14 | API / docs link | Library projects | Link out; don't paste the full API here |
| 15 | Testing / dev setup | When welcoming contributors | How to run tests and lint |
| 16 | Roadmap / known limits | Optional | Manages expectations |
| 17 | Contributing | Required (can link out) | Where to ask, whether PRs welcome |
| 18 | Community / support | Optional | Issues, Discussions, chat |
| 19 | Credits / who uses it | Optional | Trust and attribution |
| 20 | License | Required — always last | SPDX identifier + link to LICENSE file |

## How to Write Each Section

**Title and one-liner.** The heading should match the repo or package name exactly. The line below it answers in plain language: what it does, who it's for, and how it differs from the closest alternative. Avoid internal jargon. Compare: "An XXX-based framework" vs. "A zero-config API mock tool for small teams."

**Badges.** Stick to 4–6 that carry real signal: CI status, test coverage, latest published version, and license. Source from [shields.io](https://shields.io). A wall of decorative badges undermines credibility, especially if CI is actually failing.

**Demo.** For anything with UI or CLI output, this is the highest-conversion section — many readers decide here whether to read the install instructions. A 5–15 second GIF or a real terminal screenshot is enough; a link to an online playground works for libraries.

**Features.** Write differences, not truisms.

Weak: "High performance", "Easy to use", "Open source"

Better: "Single binary, no runtime dependencies", "OpenAPI 3.1 compatible out of the box", "Cold start < 50 ms (see benchmarks)"

Three to seven items is the right range.

**Quick start.** This is the core of the README. The goal: a stranger copies 3–8 lines and sees a result. Structure it as: (1) requirements, (2) install, (3) minimal working example, (4) link to full docs. Make sure every command works from a clean clone right now — stale commands damage trust more than having no README at all. Put complex config in `.env.example`; the README just says "copy and fill in."

**Usage and configuration.** Lead with the most common case, then show one or two advanced ones. List configuration options in a table: name / default / description. Always mark code blocks with a language tag (`bash`, `python`, `ts`, etc.).

**Architecture and directory tree.** For medium to large projects, a short annotated tree is enough — contributors need to know where to look, not read a design document.

```text
src/        # core logic
tests/      # mirrors src/
docs/       # full documentation
scripts/    # build and release helpers
```

A Mermaid diagram is a bonus; a wall of prose is not.

**Contributing, community, license.** Keep the README section short and link to dedicated files for the detail. At minimum state: where to ask questions (Issues / Discussions), whether PRs are welcome, and the license as an SPDX identifier linked to the `LICENSE` file. License belongs at the end of the file — this follows the [Standard Readme](https://github.com/RichardLitt/standard-readme) convention and signals "terms are here when you need them, not in the way."

## Project Type Adjustments

**Library / SDK (npm, PyPI, crates).** Emphasize the install command, a minimal API example, and compatible language / runtime versions. Link to full API docs rather than pasting them in. Trim the architecture section.

**Application / CLI.** Emphasize screenshots or terminal recordings, configuration, and deployment options (Docker, binary, Compose). Show what it looks like when running.

**Framework / platform.** Focus on the conceptual model, the directory structure, extension points, and the link to the documentation site. The README is an entry point, not a tutorial.

**Data science / research.** Emphasize where the data comes from, how to reproduce experiments, and which lockfile pins the environment (`environment.yml`, `requirements.txt`). Note clearly that raw data should not be modified.

**Documentation site or Awesome list.** The install / usage sections can be minimal; focus on scope, contribution criteria, and license.

**Language strategy.** For projects targeting global GitHub audiences: `README.md` in English, `README.zh-CN.md` (or equivalent BCP-47) for the second language, with a switcher link at the very top of each. Technical keywords (FastAPI, RAG, WebSocket) stay in the original to aid search. If the project only serves a single-language community, one language is fine.

## Boilerplate Template

Use this as a starting skeleton and delete what doesn't apply.

```markdown
# Project Name

> One sentence: what it does, who it's for, and what makes it different.

[![CI](https://img.shields.io/github/actions/workflow-status/user/repo/ci.yml)]()
[![License](https://img.shields.io/github/license/user/repo)]()
[![Release](https://img.shields.io/github/v/release/user/repo)]()

[English](README.md) | [简体中文](README.zh-CN.md)

![Demo](docs/demo.gif)

## Features

- Feature 1: concrete and verifiable
- Feature 2: …
- Feature 3: …

## Quick Start

### Requirements

- Node 20+ (or whatever applies)

### Install

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
npm install
\`\`\`

### Minimal example

\`\`\`ts
import { Client } from 'package'
const client = new Client()
console.log(await client.ping())
\`\`\`

## Usage

Common usage here. Link complex scenarios to `docs/`.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `info` | Log verbosity |

See `.env.example` for a full template.

## Development

\`\`\`bash
npm test
npm run lint
\`\`\`

## Contributing

Issues and PRs welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

[MIT](LICENSE) © Author / Org
```

## Files That Belong Alongside the README

The README handles "get in and run it." These handle everything else:

- `LICENSE` — always required
- `CONTRIBUTING.md` — branch naming, commit style, how to run tests, PR checklist
- `CODE_OF_CONDUCT.md`
- `SECURITY.md` — responsible disclosure process
- `CHANGELOG.md` or GitHub Releases
- `docs/` — architecture, API reference, tutorials
- `.env.example`, `Makefile` or task scripts

Stuffing all of this into the README makes it unmaintainable fast.

## Modern Habits (2025–2026)

- **AI-tool friendliness.** Correct directory structure, real runnable commands, and a clear test entry point improve the accuracy of coding assistants significantly. Some projects add `AGENTS.md` or `llms.txt` for agent-specific context, but this does not replace a human-readable README.
- **GitHub-specific syntax.** `[!NOTE]` / `[!WARNING]` admonition blocks, `<details>` for collapsible advanced content, and centered logos all improve scannability. Don't overuse them at the cost of plain-text readability.
- **Stay honest.** Only document what the current version actually does. An outdated install command destroys trust faster than no README at all.
- **Fill in the repo About panel.** Description, website URL, and topics affect discoverability and should echo the README's first paragraph.

## Common Anti-Patterns to Avoid

- Project name only, no "what is this"
- Install steps that work locally but break on a clean clone (hardcoded paths, missing deps)
- Pasting the entire API reference into the README — it gets stale and no one updates it
- Badges that are purely decorative while CI is actually red
- Mixed languages in the same paragraph with no language switcher
- "License: use as you wish" with no actual `LICENSE` file — legally ambiguous
- Contributing section that says only "PRs welcome" but gives no hint how to run tests

## Task

1. Review the entire project and workspace thoroughly before writing.
2. Take inspiration from these README files for structure, tone, and content depth:
   - https://raw.githubusercontent.com/Azure-Samples/serverless-chat-langchainjs/refs/heads/main/README.md
   - https://raw.githubusercontent.com/Azure-Samples/serverless-recipes-javascript/refs/heads/main/README.md
   - https://raw.githubusercontent.com/sinedied/run-on-output/refs/heads/main/README.md
   - https://raw.githubusercontent.com/sinedied/smoke/refs/heads/main/README.md
3. Follow the structure table above. Include required sections; include optional sections only where they add real value for this specific project.
4. Do not overuse emojis. Keep the README concise and to the point.
5. Do not include LICENSE, CONTRIBUTING, or CHANGELOG sections — those have dedicated files.
6. Use GFM formatting throughout. Use GitHub admonition syntax (`[!NOTE]`, `[!WARNING]`, etc.) where appropriate.
7. If the project has a logo or icon, use it in the header.
8. Every code block must have a language tag and must be runnable from a clean clone of the repo at the current HEAD.
