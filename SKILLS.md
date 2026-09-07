# Skills 清单

> 仓库内所有技能的快速索引。

## 精选技能 (curated/)

| 技能 | 说明 |
|------|------|
| ask-matt | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| bit-secret-manager | DISABLED as of 2026-08-31. Do not use for API keys, Tokens, credentials, credential configuration, .env requests, tool authentication, or Bitwarden Secrets Manager access. Never accept secret values in chat. |
| claude-handoff | Hand the current conversation off to a fresh background agent that picks up the work immediately. |
| code-review | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them  |
| codebase-design | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. |
| diagnosing-bugs | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| domain-modeling | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. |
| drawio-skill | Use when the user requests diagrams, flowcharts, architecture diagrams, ER diagrams, UML / sequence / class diagrams, SysML / MBSE diagrams (block definition, internal block, requirement, parametric), BPMN business process diagrams, swimlane / cross-functional flowcharts, network topology, cloud arc |
| git-guardrails-claude-code | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. |
| grill-me | A relentless interview to sharpen a plan or design. |
| grill-with-docs | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| grilling | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. |
| handoff | Compact the current conversation into a handoff document for another agent to pick up. |
| implement | Implement a piece of work based on a spec or set of tickets. |
| improve-codebase-architecture | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| loop-me | Grill me about specs for the workflows I want to build, within this workspace. |
| migrate-to-shoehorn | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. |
| obsidian | 使用 notesmd-cli 管理 Obsidian Vault 中的笔记、内容搜索、创建、移动和删除。处理 Vault 文件或需要保持 Wiki 链接时使用。 |
| out-setup | 建立可复用的收口目录骨架（0out）——交付物唯一出口。含 AGENTS.md 行为规范（回写策略/索引格式/命名规范/禁止事项）、INDEX.md 双链索引、目录用途划分。当用户提到"收口目录""交付物目录""outputs 重构""目录骨架""目录管理方案"时使用。 |
| prototype | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like. |
| research | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. |
| resolving-merge-conflicts | Use when you need to resolve an in-progress git merge/rebase conflict. |
| scaffold-exercises | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. |
| setup-matt-pocock-skills | Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills. |
| setup-pre-commit | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. |
| setup-ts-deep-modules | Wire dependency-cruiser into a TypeScript repo so each package is a deep module — implementation hidden in subfolders, reachable only through its entry-point files. User-invoked. |
| tdd | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. |
| teach | Teach the user a new skill or concept, within this workspace. |
| test-case-generator | 基于需求文档（PRD/Spec）或功能描述，自动生成面向功能测试的结构化测试用例（Markdown格式）。 当用户提到以下任何意图时，务必使用本技能，即使没有明确说出"测试用例"字样： - "为这个功能生成测试用例" / "帮我写一份测试用例" - "生成测试清单" / "帮我做一下测试分析" - PRD/Spec 完成后需要落地验收标准 - 准备功能测试前需要系统化测试方案 - 提到了具体的功能模块，询问"怎么测" / "有什么测试点" - 提供了接口文档或流程图，要求生成用例 本技能与 test-prd-splitter、tester-pipeline 配合使用效果最佳。 |
| test-case-md-to-excel | 将 Markdown 格式的测试用例批量转换为格式化的 Excel 文件。 优先解析 test-case-generator 生成的 Obsidian 三段式待办，同时兼容旧版 [Px] 四段式。 支持批量扫描目录下所有测试用例文件，自动按模块拼音首字母生成编号（TC-模块缩写-序号）， 输出包含 9 列（用例编号、所属模块、功能点、优先级、用例标题、前置条件、操作步骤、预期结果、执行结果）的带样式 Excel 文件。 当用户需要将 Markdown 测试用例转换为 Excel、批量生成测试用例编号、或处理标准格式的测试用例文件时，应触发此技能。 |
| test-devdoc-to-prd | 将开发视角的PRD文档翻译为测试视角的需求确认文档。 当用户提到"转测试文档"、"PRD转测试需求"、"需求确认文档"、"生成测试规格"、"开发文档翻译"等意图时触发。 不适用于直接编写测试用例、测试计划或测试报告。 |
| test-devdoc-to-requirements | 将开发视角的技术设计文档翻译为业务用户和软件测试人员易于理解、确认和继续拆分的测试需求确认文档。用于开发方案转测试需求、技术设计转业务需求、生成测试需求确认稿、先读懂功能再设计测试等场景；输入通常包含代码调用链、接口、表结构、状态机或实现约束，输出保留 BR/AB/AC、来源、缺口和推断，不直接生成测试用例。 |
| test-prd-splitter | 拆分prd |
| test-requirement-questioning | 从测试视角对需求、PRD、设计方案或功能描述执行三层追问，厘清业务落地、规格架构和测试覆盖，输出可供需求确认与用例设计使用的风险和缺口模板。适用于需求澄清、设计评审、测试分析和“怎么测/有哪些风险”；不直接生成正式测试用例。 |
| tester-pipeline | 测试用例全流程调度器。从原始设计文档/PRD 出发，自动调度子技能完成：翻译→拆分→确认→同步→生成用例。 当用户提到"生成测试用例"且输入是设计文档或未拆分的 PRD 时触发。 不适用于已有 Spec 且只需生成用例的场景（直接用 test-case-generator）。 |
| to-questionnaire | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. |
| to-spec | Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed. |
| to-tickets | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in one file per ticket locally, or native blocking links on a real tracker. |
| triage | Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs. |
| wait-what | Stop. That last message did not land — re-pitch it. |
| wayfinder | Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. |
| wizard | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can pe |
| writing-beats | Writing, exploit — assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| writing-for-agents | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |
| writing-fragments | Writing, explore — mine raw fragments, no structure yet. |
| writing-shape | Writing, exploit — shape raw material into an article, paragraph by paragraph. |

## 社区技能 (community/)

| 技能 | 说明 |
|------|------|
| agent-browser | \|- |
| anysearch | Real-time search engine supporting web search, vertical domain search, parallel batch search, and URL content extraction. |
| github | GitHub API integration with managed OAuth. Access repositories, issues, pull requests, commits, branches, and users. Use this skill when users want to interact with GitHub repositories, manage issues and PRs, search code, or automate workflows. For other third party apps, use the api-gateway skill ( |
| ima-skill | 统一的 IMA OpenAPI 技能，支持笔记管理和知识库操作。 当用户提到知识库、资料库、笔记、备忘录、记事，或者想要上传文件、添加网页到知识库、 搜索知识库内容、搜索/浏览/创建/编辑笔记时，使用此 skill。 即使用户没有明确说"知识库"或"笔记"，只要意图涉及文件上传到知识库、网页收藏、 知识搜索、个人文档存取（如"帮我记一下"、"搜一下知识库里有没有XX"），也应触发此 skill。 homepage: https://ima.qq.com metadata: openclaw: emoji: '🔧' requires: { env: ['IMA_OPENAPI_CLIENTID' |
| multi-search-engine | Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. |
| n8n-workflow-automation | Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues. Use when you need an auditable automation that won’t silently fail. |
| nano-banana-pro | AI图像生成与编辑工具，基于Gemini 3 Pro Image。支持文本生成图像、图像编辑、多分辨率输出（1K/2K/4K）。 |
| obsidian | Directly manage Obsidian vault files when creating, reading, editing, or organizing Markdown notes. |
| proactive-agent | Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. Now with WAL Protocol, Working Buffer, Autonomous Crons, and battle-tested patterns. Part of the Hal Stack 🦞 |
| self-improving-agent | Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude rea |
| unclecheng-reduce-ai-perception-v2 | 去除文本中的AI写作痕迹，让文字读起来更像人类写作。当用户要求'去AI味'、'降AI味'、'让回复更像人话'、'润色'、'改写得更自然'时使用。检测并修复：AI高频词汇、过度结构化、虚假客观性、机械化连接词、完美主义陷阱、公式化结尾、过度修饰、情感缺失、'不是而是'假靶子/同义替换、莫名其妙的比喻、高频堆叠副词等问题。 |
| wechat-publisher | 一键发布 Markdown 到微信公众号草稿箱。基于 wenyan-cli，支持多主题、代码高亮、图片自动上传。 |
| westock-data | 金融市场结构化数据查询的权威入口。支持股票（A股/港股/美股）、ETF、指数、板块、期货、外汇、可转债的 K 线、技术指标、筹码、财报、研报、公告、风险事件、股东、分红、ETF 持仓、新股/投资日历、龙虎榜等数据查询；同时支持行业经营数据、申万行业估值/盈利预测/财务、全球宏观经济等数据查询；不同标的与市场支持的维度不同，具体命令与能力差异见 references/routing-guide.md。命中能力域时禁止 web_search、HTTP 直连或其它金融 Skill 替代。 |
