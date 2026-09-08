# agent-skills

> Agent 技能统一管理仓库 — 精选、社区、模板一体化。

将多年沉积在各个 workspace 中的技能**集中管理、版本控制、方便复用**。

## 目录结构

```
agent-skills/
├── curated/        🏆 自研/精选技能（你亲手写的）
├── community/      📦 社区技能本地快照（按来源分组；`matt/` 来自 mattpocock/skills）
├── templates/      📋 技能开发模板
├── scripts/        🔧 管理工具
└── docs/           📖 文档
```

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/arykai031/agent-skills.git

# 2. 查看技能清单
cat SKILLS.md

# 3. 安装某个自研技能
./scripts/deploy-curated-skill.sh install <skill-name> <workspace>/skills
```

## 本地质量检查

管理脚本使用 Python 3 和 `scripts/requirements.txt` 中固定的 PyYAML。
在自己的虚拟环境中安装依赖后执行：

```bash
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s tests -v
bash scripts/validate-skill.sh
bash scripts/build-registry.sh
```

校验与索引使用同一技能包边界：分组目录递归查找，遇到技能入口后不再把
包内同名配套文档注册成独立技能。当前为 59 个技能包，而非 61 个同名文件。
校验会解析 Frontmatter，拒绝语法错误、重复键、缺失闭合标记和非字符串的
`name` / `description`；允许合法社区扩展字段，支持 CRLF 和 UTF-8 BOM。
错误输出只显示路径与位置，不复制源内容。该校验不等于运行环境或技能业务验收。

## 技能来源说明

| 来源 | 路径 | 说明 |
|------|------|------|
| 🏆 自研 | `curated/` | 你自己开发的技能，可版本控制、可发布到 SkillHub |
| 📦 社区 | `community/` | 从 SkillHub 安装的技能副本，锁定版本防止上游变更 |

`curated/` 是自研 Skill 的唯一可编辑来源。Workspace、Vault 和 Agent
全局目录中的同名目录都是部署副本，不接受手工修改。检查副本是否漂移：

```bash
./scripts/deploy-curated-skill.sh check <skill-name> <workspace>/skills
```
