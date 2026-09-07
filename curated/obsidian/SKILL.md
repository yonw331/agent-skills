---
name: obsidian
description: 使用 notesmd-cli 管理 Obsidian Vault 中的笔记、内容搜索、创建、移动和删除。处理 Vault 文件或需要保持 Wiki 链接时使用。
---

# Obsidian

`notesmd-cli` 管理已注册的 Obsidian Vault。先确认命令可用，再处理笔记。

```bash
command -v notesmd-cli
notesmd-cli --version
```

命令不存在时停止，不自建兼容包装器，也不猜测安装方式。

## 选择 Vault

先查看默认 Vault：

```bash
notesmd-cli list-vaults --default --path-only
```

没有默认 Vault 时，先执行 `notesmd-cli list-vaults --json`，请用户确认目标 Vault。后续命令带上 `--vault <名称>`；除非用户明确要求，不要调用 `add-vault`、`set-default-vault` 或改动 Obsidian 配置。

不要把机器上的 Vault 绝对路径写进脚本或笔记。

## 查找与读取

按文件名查找时，使用 `rg --files`。内容搜索使用非交互模式，避免命令停在选择界面：

```bash
notesmd-cli search-content "关键词" --vault <名称> --no-interactive --format text
notesmd-cli print "笔记路径" --vault <名称>
```

需要读取 YAML Frontmatter 时：

```bash
notesmd-cli frontmatter "笔记路径" --vault <名称> --print
```

## 写入与改名

写入前先读取目标 Vault 的 `AGENTS.md` 和写作规则。写入给人阅读的 Markdown 时，用自然、直接的语言复核一遍，删掉空泛套话；事实、命令、路径和验收条件不得因此改变。

创建笔记时，路径和内容必须来自用户请求或已确认的任务：

```bash
notesmd-cli create "目录/笔记名" --vault <名称> --content "正文"
```

同名笔记默认不覆盖。只有用户明确同意覆盖时，才添加 `--overwrite`。

需要保留 Wiki 链接语义时，用 CLI 改名或移动，再检查引用：

```bash
notesmd-cli move "旧路径" "新路径" --vault <名称>
notesmd-cli search-content "新笔记名" --vault <名称> --no-interactive --format text
```

隔离 Vault 已验证：`move` 会将 `[[旧笔记名]]` 更新为 `[[新笔记名]]`。仍须针对实际 Vault 的受影响笔记复核结果。

## 删除与打开

删除前，先用 `print` 确认目标内容和路径，并取得用户对该目标的明确确认：

```bash
notesmd-cli delete "笔记路径" --vault <名称>
```

`notesmd-cli open` 和 `--editor` 会打开图形应用或终端编辑器。仅在用户明确要求打开笔记且交互环境可用时调用；不要把它用在自动化流程中。

## 完成检查

- 确认操作针对了用户指定的 Vault。
- 创建、移动或删除后检查目标文件和受影响的 Wiki 链接。
- 对本次改动运行范围限定的格式检查，例如 `git diff --check -- <文件>`。
