# skills

面向 Codex / Cursor 工作流的个人 skills 仓库，包含可复用的通用技能，以及少量个人定制技能。

- English version: [README.md](./README.md)

## 概览

这个仓库是本地 AI 编码工具相关 skills 的远程主仓库。

它围绕两种顶层范围组织：

- `general/`：跨项目可复用、适合广泛使用的 skills
- `personal-custom/`：带有个人习惯、机器配置或项目私有特征的 skills

这个仓库主要解决以下问题：

- 为本地 skills 提供一个可持续维护的远程备份
- 按需把 skill 分发到项目里的 `.codex/skills/` 或 `.cursor/skills/`
- 将真正通用的技能和个人定制流程区分开
- 让 skill 目录既适合人工阅读，也适合后续自动化处理

## 仓库结构图

```text
skills/
├── README.md
├── README.zh.md
├── scripts/
│   ├── generate_readme_sections.py
│   ├── install_skill.py
│   ├── sync_skills.py
│   └── validate_index.py
├── skills-index.json
├── general/
│   ├── ai-sync/
│   ├── docs/
│   ├── planning/
│   └── repository-maintenance/
└── personal-custom/
    ├── design/
    ├── logs/
    └── machine-setup/
```

## 分类说明

- `general/`：广泛适用于多个项目和工作流的可复用技能
  - `ai-sync/`：共享 AI 上下文初始化与同步相关 skills
  - `docs/`：文档渲染、预览和审阅相关 skills
  - `planning/`：任务拆分和执行规划相关 skills
  - `repository-maintenance/`：维护本 skills 仓库及目录索引的 skills
- `personal-custom/`：带有个人习惯、机器环境或项目私有特征的技能
  - `machine-setup/`：终端、shell、本机开发环境相关 skills
  - `design/`：设计稿转代码相关 skills
  - `logs/`：个人日志或项目进度记录相关 skills

## 如何判断放在哪一类

适合放进 `general/` 的 skill：

- 能在多个仓库里复用
- 不强依赖某一个私有项目
- 不会明显泄露个人流程假设
- 不需要依赖私有本地上下文才能理解

适合放进 `personal-custom/` 的 skill：

- 和这台机器或 shell 配置强绑定
- 明显围绕个人工作习惯设计
- 绑定某个项目的目录结构、命名或内部流程
- 更像个人工具箱，而不是通用能力包

## Skill 索引

<!-- BEGIN SKILL INDEX -->
| Skill | 范围 | 分类 | 用途 | 路径 |
|---|---|---|---|---|
| `cross-tool-ai-sync` | General | AI Sync | 在 Codex、Cursor、Claude 之间同步共享 AI 上下文。 | `general/ai-sync/cross-tool-ai-sync/` |
| `project-ai-sync-bootstrap` | General | AI Sync | 为新仓库初始化共享 AI 上下文和同步骨架。 | `general/ai-sync/project-ai-sync-bootstrap/` |
| `md-browser-preview` | General | Docs | 将 Markdown 渲染成 HTML 并在浏览器中预览。 | `general/docs/md-browser-preview/` |
| `task-subagent-planner` | General | Planning | 把任务型请求拆成待确认的 subagent 执行方案。 | `general/planning/task-subagent-planner/` |
| `skills-repo-maintainer` | General | Repository Maintenance | 用仓库维护脚本统一做 skill 安装、同步、索引校验和 README 索引生成。 | `general/repository-maintenance/skills-repo-maintainer/` |
| `machine-dev-bootstrap` | Personal Custom | Machine Setup | 恢复这台 Mac 的标准开发环境基线。 | `personal-custom/machine-setup/machine-dev-bootstrap/` |
| `zsh-setup` | Personal Custom | Machine Setup | 配置和排查 zsh 主题、插件和提示符。 | `personal-custom/machine-setup/zsh-setup/` |
| `sketch-to-android` | Personal Custom | Design | 将本地 Sketch 设计稿像素级还原到 Siuper Android UI，并参考 iOS 与真机验证。 | `personal-custom/design/sketch-to-android/` |
| `sketch-to-compose` | Personal Custom | Design | 将 Sketch 设计稿转换为 Jetpack Compose 代码。 | `personal-custom/design/sketch-to-compose/` |
| `parttime-work-log` | Personal Custom | Logs | 记录和汇总个人兼职工作日志。 | `personal-custom/logs/parttime-work-log/` |
| `work-progress-log` | Personal Custom | Logs | 记录和汇总 Siuper 项目进度。 | `personal-custom/logs/work-progress-log/` |
<!-- END SKILL INDEX -->

同一份目录也提供机器可读索引：

- `skills-index.json`

## 如何选择 skill

- 需要初始化或维护跨工具 AI 指令时，用 `general/ai-sync/*`
- 需要文档渲染、预览或阅读辅助时，用 `general/docs/*`
- 需要在执行前先拆分任务时，用 `general/planning/*`
- 需要维护这个 skills 仓库本身时，用 `general/repository-maintenance/*`
- 需要处理终端、shell、本机开发环境时，用 `personal-custom/machine-setup/*`
- 需要做 Sketch 到 Android UI 的转换时，用 `personal-custom/design/*`
- 需要做个人日志或项目进度记录时，用 `personal-custom/logs/*`

## 使用方式

你可以把需要的 skill 目录复制到项目的 `.cursor/skills/` 或 `.codex/skills/` 下，并保持 skill 目录自包含，包括 `SKILL.md` 以及配套的 `scripts/`、`assets/`、`references/`、`agents/` 等子目录。

如果需要重复安装，优先使用仓库自带脚本，而不是手写复制命令。

### 安装脚本

列出所有已索引 skills：

```bash
python3 scripts/install_skill.py --list
```

只列出 `general` 下的 skills：

```bash
python3 scripts/install_skill.py --list --scope general
```

安装一个 skill 到当前项目的 Codex skills 目录：

```bash
python3 scripts/install_skill.py md-browser-preview --tool codex --project-root .
```

安装多个 skill 到当前项目的 Cursor skills 目录：

```bash
python3 scripts/install_skill.py cross-tool-ai-sync task-subagent-planner --tool cursor --project-root .
```

覆盖已有安装：

```bash
python3 scripts/install_skill.py md-browser-preview --tool codex --project-root . --force
```

直接安装到自定义目录：

```bash
python3 scripts/install_skill.py sketch-to-compose --target-dir /absolute/path/to/.codex/skills
```

### 校验脚本

校验 `skills-index.json` 是否和仓库内容一致：

```bash
python3 scripts/validate_index.py
```

根据 `skills-index.json` 重新生成 README 索引区块：

```bash
python3 scripts/generate_readme_sections.py
```

### 同步脚本

将指定 skills 从本机源目录同步进当前仓库：

```bash
python3 scripts/sync_skills.py md-browser-preview task-subagent-planner \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills
```

从一组本机 source roots 同步全部已索引 skill：

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills
```

仅预览即将同步的内容，不落盘：

```bash
python3 scripts/sync_skills.py --all \
  --source-root ~/.codex/skills \
  --source-root ~/project/Siuper/siuper-sdk-android/.codex/skills \
  --source-root ~/project/Siuper/.codex/skills \
  --dry-run
```

### 安装示例

先克隆仓库：

```bash
git clone --branch develop git@github.com:arno-peng/skills.git
```

安装一个 skill 到项目的 Codex skills 目录：

```bash
mkdir -p .codex/skills
cp -R /path/to/skills/general/docs/md-browser-preview .codex/skills/
```

安装一个 skill 到项目的 Cursor skills 目录：

```bash
mkdir -p .cursor/skills
cp -R /path/to/skills/general/planning/task-subagent-planner .cursor/skills/
```

安装一个个人定制 skill：

```bash
mkdir -p .codex/skills
cp -R /path/to/skills/personal-custom/design/sketch-to-compose .codex/skills/
```

复制时不要改 skill 目录名，并保留其内部配套子目录。

## 更新已安装 skill

刷新单个 skill：

```bash
rm -rf .codex/skills/md-browser-preview
cp -R /path/to/skills/general/docs/md-browser-preview .codex/skills/
```

刷新多个 skills：

```bash
cp -R /path/to/skills/general/ai-sync/cross-tool-ai-sync .codex/skills/
cp -R /path/to/skills/general/planning/task-subagent-planner .codex/skills/
```

如果某个 skill 会影响目标项目里的共享 AI 上下文或工具适配文件，安装后记得在目标项目里执行相应的同步命令。

## 仓库维护流程

日常维护这个仓库时，建议按下面流程：

1. 在真实 source location 里更新或创建 skill
2. 确认 `skills-index.json` 正确
3. 如果希望助手统一驱动维护流程，使用 `general/repository-maintenance/skills-repo-maintainer/`
4. 执行 `scripts/sync_skills.py`，把本机最新 skill 内容同步进仓库
5. 执行 `scripts/validate_index.py`
6. 如果目录索引有变化，执行 `scripts/generate_readme_sections.py`
7. 检查 git diff
8. 提交并推送到 `develop`

## 贡献流程

新增或修改 skill 时：

1. 在其真实 source location 中编辑
2. 保持 skill 自包含，只保留实际需要的资源
3. 放到正确的分类目录下
4. 更新 `skills-index.json`
5. 确认 `scripts/install_skill.py --list` 输出正确
6. 运行 `scripts/validate_index.py`
7. 如果公开目录或索引有变化，运行 `scripts/generate_readme_sections.py`
8. 提交到 `develop`

## 质量标准

每个 skill 应该满足：

- `SKILL.md` 中有清晰的 `name` 和 `description`
- 聚焦于一个工作或一组紧密相关的流程
- 主体说明保持简洁，不在正文里重复堆大量参考资料
- 必要的配套目录要完整保留，例如 `scripts/`、`assets/`、`references/`、`agents/`
- 除非本来就属于 `personal-custom/`，否则不要夹带明显的私有项目假设

## 命名约定

- skill 目录名使用小写连字符风格
- 分类目录表达工作域，而不是实现细节
- 尽量使用简短、动作导向的名字，例如 `md-browser-preview`、`task-subagent-planner`
- 机器相关或个人日志相关 skills 放在 `personal-custom/`，不要放进 `general/`

## 分支

- 主工作分支：`develop`
