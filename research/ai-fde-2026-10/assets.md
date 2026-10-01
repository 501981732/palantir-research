# 图片资产台账

获取及视检日期：2026-10-01。以下图 1–22 按[研究正文](README.md)中首次出现的顺序编号，编号与原图文件名前缀独立。共 22 张真实界面图：21张官方公开产品界面截图（12 张 AI FDE、6 张 Global Branching、1 张 Action 外部调用设置、2 张 AIP Evolve），另有1张伙伴教程实际视频帧。概念插画与存在默认值版本差异的保留策略截图未纳入本台账。

21张官方原图从所列公开页面的实际 `img src` 提取下载地址，保留下载所得 PNG 字节；1张JPEG是在公开原视频正常播放时保存的页面截图，保留标题、频道及时间。全部未裁剪、重绘或生成界面，逐张视检并核对MIME、尺寸、字节和SHA-256；HTTP状态仅适用下载原图。观察不代表本轮登录租户测试，视频局部观察和未完整观看的边界另列。

图片权利归 Palantir Technologies Inc. 等原权利方。此台账记录研究用途和来源归因，不猜测图片许可，也不主张公开可访问图片具备通用再分发许可；本仓库不作通用再分发授权承诺。

| 正文图序 | 本地原图 | 研究用途 |
| --- | --- | --- |
| 1 | [09-ai-fde-beta-context.png](assets/09-ai-fde-beta-context.png) | 发布沿革；仅展示初期界面 |
| 2 | [10-ai-fde-beta-tools.png](assets/10-ai-fde-beta-tools.png) | 发布沿革与工具配置演进；仅初期界面 |
| 3 | [11-ai-fde-ga-skills.png](assets/11-ai-fde-ga-skills.png) | GA历史证据；不据此推断9月AIP Skills所有行为 |
| 4 | [02-ai-fde-input.png](assets/02-ai-fde-input.png) | 发起任务、模式与模型配置 |
| 5 | [03-ai-fde-sessions.png](assets/03-ai-fde-sessions.png) | 新会话与历史会话管理 |
| 6 | [05-ai-fde-context.png](assets/05-ai-fde-context.png) | 显式上下文管理 |
| 7 | [06-ai-fde-outline.png](assets/06-ai-fde-outline.png) | 操作可见性与长会话上下文管理 |
| 8 | [07-ai-fde-tools.png](assets/07-ai-fde-tools.png) | 最小工具集及执行审批配置 |
| 9 | [04-ai-fde-modes.png](assets/04-ai-fde-modes.png) | 按任务裁剪工具和文档上下文 |
| 10 | [21-ai-fde-evals-mode.png](assets/21-ai-fde-evals-mode.png) | 函数案例的验证能力配置 |
| 11 | [22-ai-fde-evals-failure.png](assets/22-ai-fde-evals-failure.png) | 真实界面中的评测失败与修复反馈 |
| 12 | [08-ai-fde-approval.png](assets/08-ai-fde-approval.png) | 动作执行前的人类审批 |
| 13 | [12-global-branching-changes.png](assets/12-global-branching-changes.png) | 跨产品治理支撑：变更审查 |
| 14 | [16-global-branching-security.png](assets/16-global-branching-security.png) | 跨产品治理支撑：分支访问控制 |
| 15 | [17-global-branching-protection.png](assets/17-global-branching-protection.png) | 跨产品治理支撑：资源保护和独立审批 |
| 16 | [14-global-branching-reviewers.png](assets/14-global-branching-reviewers.png) | 跨产品治理支撑：审批与职责划分 |
| 17 | [13-global-branching-checks.png](assets/13-global-branching-checks.png) | 跨产品治理支撑：检查与失败定位 |
| 18 | [15-global-branching-merge-build.png](assets/15-global-branching-merge-build.png) | 跨产品治理支撑：合并后的构建副作用 |
| 19 | [23-action-external-calls-branch-setting.png](assets/23-action-external-calls-branch-setting.png) | 分支不能隔离外部调用副作用的治理边界 |
| 20 | [24-ontologize-mode-recovery-1310.jpg](assets/24-ontologize-mode-recovery-1310.jpg) | 伙伴视频局部实证：工具错误与后续成功结果 |
| 21 | [19-aip-evolve-review.png](assets/19-aip-evolve-review.png) | 跨产品边界比较；不是AI FDE界面 |
| 22 | [20-aip-evolve-proposal.png](assets/20-aip-evolve-proposal.png) | 跨产品边界比较；示例结果不是普遍性能承诺 |

## 图 1：Beta 的 Ontology 上下文菜单

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [09-ai-fde-beta-context.png](assets/09-ai-fde-beta-context.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/announcements/release-notes/2025-11-18-045416-ai-fde-screenshot-2025-11-13-at-2-53-56-pm-pn.png) |
| 来源页面 | [2025年11月官方公告](https://www.palantir.com/docs/foundry/announcements/2025-11/) |
| 获取时间（UTC） | `2026-10-01T00:58:59.622991+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1922 × 546 px / 80,382 bytes |
| SHA-256 | `5850235fb856cfa1dbf7c20d4b5c409accbee99e219106963dcfedbad2810b9a` |
| 来源时期 / 版本边界 | 2025-11-18公告，截图文件标注2025-11-13 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Beta截图的Ontology菜单列Action type、Interfaces、Object type；工具计数为4/3/12/5/6等，模型栏显示Claude 3.7 Sonnet。

使用边界：

- 仅用于2025-11发布沿革，不作为当前UI与能力全量清单。

## 图 2：Beta 的工具配置菜单

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [10-ai-fde-beta-tools.png](assets/10-ai-fde-beta-tools.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/announcements/release-notes/2025-11-18-045420-ai-fde-screenshot-2025-11-13-at-2-54-22-pm-pn.png) |
| 来源页面 | [2025年11月官方公告](https://www.palantir.com/docs/foundry/announcements/2025-11/) |
| 获取时间（UTC） | `2026-10-01T00:58:59.970167+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 2190 × 1000 px / 147,984 bytes |
| SHA-256 | `fe8cd943c2cd9b4a46fd57dda1b5a8591cc0475a7dfe1dcce6d8e185d46a24a2` |
| 来源时期 / 版本边界 | 2025-11-18公告，截图文件标注2025-11-13 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Beta工具菜单顶端使用Default/None/Functions/Pipelines/Ontology/Read-only/Search等Presets；Code Workspaces 6/6，container_sync权限配置按master分支Ask、Else Allow。

使用边界：

- 历史工具数/权限演示不代表2026-10当前默认值。

## 图 3：GA 的 Agent 和 Domain skills

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [11-ai-fde-ga-skills.png](assets/11-ai-fde-ga-skills.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/announcements/release-notes/2026-03-11-191923-ai-fde-ai-fde-skills-selector-pn.png) |
| 来源页面 | [2026年3月官方公告](https://www.palantir.com/docs/foundry/announcements/2026-03/) |
| 获取时间（UTC） | `2026-10-01T00:59:00.134392+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1940 × 1064 px / 112,005 bytes |
| SHA-256 | `428bc0543da728db8abf8e61c758caa41a0960b69106158e8a2b4f8e7b52175d` |
| 来源时期 / 版本边界 | 2026-03-12 GA公告，图片文件2026-03-11 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：GA公告Skills菜单分Agent skills和Domain skills；包含Change mode、Request clarification、Load documentation、Manage context、Manage skills等开关，Generate plan/Execute actions/Filesystem operations等画面中未启用。

使用边界：

- 这是Agent/Domain操作能力菜单；不得将画面当作后来的可复用AIP Skill资产库。

## 图 4：当前文档输入框

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [02-ai-fde-input.png](assets/02-ai-fde-input.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/ai-fde/ai-fde-input-field.png) |
| 来源页面 | [AI FDE：Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation/) |
| 获取时间（UTC） | `2026-10-01T00:58:57.207386+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1976 × 368 px / 93,764 bytes |
| SHA-256 | `cc3b5a26a91f92b604ef802b4be1700ef797183681124abea7fe96f6e2bec69d` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：输入栏上方显示Modes、Skills、Documentation、Files、Ontology、Functions；下方显示工具计数、模型GPT-5.3 Codex及发送按钮。

使用边界：

- 画面中的模型只是截图选择，不能证明所有租户都已启用。

## 图 5：会话管理

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [03-ai-fde-sessions.png](assets/03-ai-fde-sessions.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/ai-fde/ai-fde-session-manager.png) |
| 来源页面 | [AI FDE：Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation/) |
| 获取时间（UTC） | `2026-10-01T00:58:57.032248+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 2552 × 392 px / 40,524 bytes |
| SHA-256 | `d4972f5ed304e8b6ef120dd091270d131cd326c7c7a8a2bf1ae3943a02d7dc6a` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：顶部New session下拉包括创建新会话及一个已有Create New Ontology Request会话；右侧可见Outline入口。

使用边界：来源未给出精确产品构建版本；本图用于说明所展示的控制入口，不据此承诺所有租户当前界面一致。

## 图 6：文档上下文选择

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [05-ai-fde-context.png](assets/05-ai-fde-context.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/ai-fde/ai-fde-ribbon-tool-options.png) |
| 来源页面 | [AI FDE：Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation/) |
| 获取时间（UTC） | `2026-10-01T00:58:57.480190+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1958 × 768 px / 142,408 bytes |
| SHA-256 | `4a461768dff71dc847adc32ae1a6c3eecbd4f513538eb0044623eef2ee7ad583` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Documentation展开为自定义文档、Documentation bundles和Documentation pages；画面同时显示资源上下文入口。

使用边界：

- 自定义文档示例名称AI FDE 3.7 Tool Guidance不能用来推断当前产品版本。

## 图 7：对话与工具纲要

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [06-ai-fde-outline.png](assets/06-ai-fde-outline.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/ai-fde/ai-fde-chat-outline.png?width=500) |
| 来源页面 | [AI FDE：Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation/) |
| 获取时间（UTC） | `2026-10-01T00:58:57.361277+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1002 × 1542 px / 141,950 bytes |
| SHA-256 | `7dc7c52838a38c42ea5240564116cd097d21b8c065f32e255f4dbef1614763a1` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Outline展示分支和action上下文、Create a new branch请求、create_foundry_branch/load_action_types调用，逐消息token及底部约33.1K/200K token状态。

使用边界：

- 200K是截图所示会话窗口，不是所有模型和会话的统一上限。

## 图 8：工具与条件策略

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [07-ai-fde-tools.png](assets/07-ai-fde-tools.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/ai-fde/ai-fde-tools-menu.png) |
| 来源页面 | [AI FDE：Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation/) |
| 获取时间（UTC） | `2026-10-01T00:58:59.526464+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1968 × 850 px / 190,196 bytes |
| SHA-256 | `51b9ce684d85a63ae53bef9fd7e4f9ef2ae2a18e2b6b6d0878b3c48e8653d699` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：工具菜单分列类别、具体工具、container_sync说明和条件审批；Code Workspaces 8/8中包含文件读写、终端、git、transform preview，右侧对master分支显示Ask。

使用边界：

- 画面中的master规则只是演示配置，不是所有默认branch策略。
- 工具名称/数量作为截图证据，不推断内部实现。

## 图 9：模式及配置选择

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [04-ai-fde-modes.png](assets/04-ai-fde-modes.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/ai-fde/ai-fde-mode-selector.png) |
| 来源页面 | [AI FDE：Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation/) |
| 获取时间（UTC） | `2026-10-01T00:58:57.762631+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1936 × 1022 px / 214,885 bytes |
| SHA-256 | `092481f1aca94979b3f4e66cbbe65fb02a03a345345c9fa968cee11882ae3368` |
| 来源时期 / 版本边界 | 当前文档；GA公告也使用同内容截图 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Modes菜单含Transform data、Modify ontology、Write functions、Exploration、Governance、OSDK React、Platform Q&A；选中数据转换时可配置Python/Pipeline Builder、分支模式、代码编辑方式，并显示Adds 26 tools。

使用边界：

- 截图列举的模式/工具数是所示版本，不代表2026-10全部模式；当前文本还包含新增Data connection与机器学习。

## 图 10：函数模式的 Evals 配置

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [21-ai-fde-evals-mode.png](assets/21-ai-fde-evals-mode.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/announcements/release-notes/2026-04-13-154154-ai-fde-image-31-pn.png) |
| 来源页面 | [2026年4月官方公告](https://www.palantir.com/docs/foundry/announcements/2026-04/) |
| 获取时间（UTC） | `2026-10-01T01:05:35.520957+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1946 × 1070 px / 126,100 bytes |
| SHA-256 | `219ab03083165122438ac9abb6d601e31205333155b6f99f16c34f2e24dadbdb` |
| 来源时期 / 版本边界 | 2026-04-14公告，图片文件标注2026-04-13 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Write functions模式列Logic、TypeScript v1/v2、Python；Advanced settings的Include Evals tools已启用，显示Adds 30 tools，左列出现Data connection，模型栏为GPT-5.4。

使用边界：

- 工具数和模型仅是公告示例配置，不是所有版本或租户的全量清单。

## 图 11：AI FDE 读取失败的评测结果

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [22-ai-fde-evals-failure.png](assets/22-ai-fde-evals-failure.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/announcements/release-notes/2026-04-13-154158-ai-fde-image-32-pn.png) |
| 来源页面 | [2026年4月官方公告](https://www.palantir.com/docs/foundry/announcements/2026-04/) |
| 获取时间（UTC） | `2026-10-01T01:05:35.572481+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1770 × 1316 px / 116,772 bytes |
| SHA-256 | `99b8862029e186366bc1d3872c68970f2f729cb97117182385e157aac88ec57f` |
| 来源时期 / 版本边界 | 2026-04-14公告，图片文件标注2026-04-13；截图中评测运行日期2026-03-31 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：AI FDE的load_evaluation_runs工具返回评测卡；运行时间2026-03-31，Tests 10 / Passed 9 / Failed 1；10 tests × 3 runs中Required Actions Match为29 pass / 1 fail / 96.7%，并列函数耗时、compute-seconds、LLM input/output tokens。

使用边界：

- 这是一轮函数评测的失败结果，不应写成AI FDE产品故障或整体成功率。
- 数值来自官方示例截图，本研究没有运行该评测。

## 图 12：执行前工具审批

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [08-ai-fde-approval.png](assets/08-ai-fde-approval.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/ai-fde/ai-fde-tool-approval.png) |
| 来源页面 | [AI FDE：Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation/) |
| 获取时间（UTC） | `2026-10-01T00:58:59.521412+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1692 × 912 px / 82,320 bytes |
| SHA-256 | `6266855c419e74cb8817f1440872e6e111e26dd49f2a887b307f8a5b7ea66403` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：create_object_type_permissions_datasets工具调用显示folderRid和datasetNames参数；审批区含Always allow for this session、Reject、Allow，底部Waiting for tool approval。

使用边界：

- 公开文档示例RID不是本研究租户数据。

## 图 13：跨资源变更差异

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [12-global-branching-changes.png](assets/12-global-branching-changes.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/announcements/release-notes/2026-09-16-194100-global-branching-proposal-changes-pn.png) |
| 来源页面 | [2026年9月官方公告](https://www.palantir.com/docs/foundry/announcements/2026-09/) |
| 获取时间（UTC） | `2026-10-01T00:58:59.440924+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 2550 × 1433 px / 372,855 bytes |
| SHA-256 | `135982992be37663fe30598f6d211cad3aeafbc39cf7c81dc986cdc29f4ed384` |
| 来源时期 / 版本边界 | 2026-09公告，图片文件2026-09-16 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：新Changes页签左列跨资源清单，右侧显示Order Risk Functions代码逐行diff；分支名带ai-fde/cindyz/order-exception-bootstrap，画面同时出现Awaiting approval和Checks failed，并提供按文件Approve/Reject。

使用边界：

- 这是Global Branching界面，不能宣称本研究执行过该AI FDE案例。

## 图 14：分支角色与资源权限

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [16-global-branching-security.png](assets/16-global-branching-security.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/global-branching/branch-security.png) |
| 来源页面 | [Global Branching：Branch security](https://www.palantir.com/docs/foundry/global-branching/branch-security/) |
| 获取时间（UTC） | `2026-10-01T00:59:03.173871+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 3024 × 1618 px / 394,763 bytes |
| SHA-256 | `98b31de2e67aeae3836a6c6cbb591936d176966f2f4909639ec7f681c3808fbf` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Branch Security页显示Owner及Organizations；蓝色提示明确分支角色不控制资源编辑权限，修改还需project/resource级权限。

使用边界：

- 该图只显示Owner，不据此否定当前文字列举的其他分支角色。

## 图 15：资源保护政策

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [17-global-branching-protection.png](assets/17-global-branching-protection.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/global-branching/project-with-custom-approval-policy.png) |
| 来源页面 | [Global Branching：Resource protection and approval policies](https://www.palantir.com/docs/foundry/global-branching/resource-protection-and-approval-policies/) |
| 获取时间（UTC） | `2026-10-01T00:59:02.634064+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 2394 × 1290 px / 131,031 bytes |
| SHA-256 | `a2a587f14c2a6688229b1868ff641f9eb47d34ba1bcd5f5662a5244ae4db385c` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：项目Branch protection侧栏配置至少2名组内用户审批、贡献者不可自审、自动保护新文件；截图底部支持类型提示仅Workshop。

使用边界：

- 这是具体Workshop项目演示；当前资源支持范围以文档文字和integration表为准，不能据图断言Global Branching只支持Workshop。

## 图 16：Reviewer 与政策管理

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [14-global-branching-reviewers.png](assets/14-global-branching-reviewers.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/global-branching/proposal-page-manage-reviewers.png) |
| 来源页面 | [Global Branching：Core concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts/) |
| 获取时间（UTC） | `2026-10-01T00:59:02.303476+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1512 × 808 px / 170,094 bytes |
| SHA-256 | `c0b4a7a42aa5b1cc7eb919b816db7b444f28c17c2c6cde6af534eb1128e48425` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Manage reviewers弹层列所选2名reviewer及Approval policies 3页签；Employee等待审批，而其他部分资源可Auto-approved。

使用边界：

- 人员已由官方原图模糊处理，本研究未改图。

## 图 17：资源检查与冲突

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [13-global-branching-checks.png](assets/13-global-branching-checks.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/global-branching/proposal-page-checks.png) |
| 来源页面 | [Global Branching：Core concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts/) |
| 获取时间（UTC） | `2026-10-01T00:59:02.336596+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1512 × 808 px / 166,334 bytes |
| SHA-256 | `13a6e5a2657711541d7f42446e0dff09589d64e152cb1a50e4dd295df92663bc` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Proposal的Employee资源Checks弹层显示Ontology和validation通过、与main有冲突，提供Rebase；表格分别列Reviewers与Checks。

使用边界：

- Checks失败与审批完成可以同时存在，审批不等于可合并。

## 图 18：合并时构建策略

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [15-global-branching-merge-build.png](assets/15-global-branching-merge-build.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/global-branching/build-dialog.png) |
| 来源页面 | [Global Branching：Core concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts/) |
| 获取时间（UTC） | `2026-10-01T00:59:03.626713+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 3024 × 1619 px / 568,122 bytes |
| SHA-256 | `85c87b55eb9b1a4e377896947b7d34f420a76e06cfcbbaf8d1183681b0bb0b7c` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Merge proposal对话框列三种构建策略：Build modified resources and everything in between、Build only modified resources、Do not build resources，最后一项标May cause breaking changes。

使用边界：

- 截图首项名称与当前core concepts正文Build all affected resources不同；说明功能思路时以正文为准，保留UI标签版本差异。

## 图 19：分支外部调用开关

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [23-action-external-calls-branch-setting.png](assets/23-action-external-calls-branch-setting.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/action-types/action-function-setting.png) |
| 来源页面 | [Action types：Branching action types](https://www.palantir.com/docs/foundry/action-types/branching-action-types/) |
| 获取时间（UTC） | `2026-10-01T01:05:34.966897+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1754 × 448 px / 68,873 bytes |
| SHA-256 | `25e90968b2301cfd8742ffcb79466f554c007587397639775fad3be129ff009c` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：Action的Testing on branches设置同时显示webhook执行开关关闭、external function calls开关开启；tooltip明确开启后分支会像main一样执行外部函数调用，关闭时包含外部调用的Action将失败。

使用边界：

- 真实界面展示分支外部副作用控制；不是AI FDE界面，也非本研究修改的设置。
- 分支上的外部调用不等于外部系统被沙箱隔离。

## 图 20：伙伴视频中的模式错误与后续成功结果

| 项目 | 记录 |
| --- | --- |
| 本地原始截图 | [24-ontologize-mode-recovery-1310.jpg](assets/24-ontologize-mode-recovery-1310.jpg) |
| 来源视频 / 时间点 | [Ontologize：Getting Started with AI FDE，13:10](https://www.youtube.com/watch?v=Ta19YD794RY&t=790s) |
| 原始来源页 | [YouTube 原视频](https://www.youtube.com/watch?v=Ta19YD794RY) |
| 视频发布日期 | 2026-06-03（原页面元数据）；当前播放器总长16:48，早期元数据16:49 |
| 截图保存时间（UTC） | `2026-10-01T02:03:44.429164+00:00` |
| 获取方式 / MIME | 原视频正常播放时的页面截图 / `image/jpeg`；不是官方文档下载图 |
| 尺寸 / 字节数 | 1470 × 775 px / 135,309 bytes |
| SHA-256 | `008349413206fe208a40493d888edf638d03539c44716c6bb93402a928a257ac` |
| 作者 / 商业关系 | Gena / Ontologize；官方培训合作伙伴，不是无商业关系的独立测评 |
| 来源时期 / 版本边界 | 2026年6月教程；正式产品build未知，画面模型和工具是该演示配置 |
| 视觉检查 | 2026-10-01，亲自观看该局部真实画面并视检保存截图 |

视检观察：保留视频标题、Ontologize频道与13:10/16:48播放时间。AI FDE会话中可见change_mode无效modeConfig错误，随后另一change_mode显示Transform data / Python transforms成功，下方出现文件夹读取；右侧Outline列出数据元信息与SQL查询调用。

使用边界：

- 完整页面截图未重绘、合成、翻译或替换UI；页面推荐区与广告不是产品内容，分析只引用视频播放器内可读区域。
- 仅核验局部画面；没有完整观看、取得可靠字幕、复现任务、验证完整清洗/CI/合并或测试数据。
- 截图后的播放器错误与字幕缺口另记，不能用早期元数据或章节补齐未见流程。
- 图片归原视频权利人；公开访问不自动提供通用再分发许可，仅作可归因研究讨论。

## 图 21：Evolve 优化合同

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [19-aip-evolve-review.png](assets/19-aip-evolve-review.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-1.png) |
| 来源页面 | [AIP Evolve：Overview](https://www.palantir.com/docs/foundry/aip-evolve/overview/) |
| 获取时间（UTC） | `2026-10-01T00:59:03.849892+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1440 × 900 px / 138,497 bytes |
| SHA-256 | `1e52423b4c7e5c21bb1bf81ed551748bf207d6f0b31eb04ccb978c58be5ad42f` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：AIP Evolve Review页指定AIP Logic目标、Optimize cost、10个test cases、side-by-side comparison、model swapping/prompt tweaks、5次迭代限制，底部显示Prompt sent to AI FDE。

使用边界：

- 这是Evolve界面，显示其向AI FDE委托的边界；截图的测试数和迭代数是案例配置。

## 图 22：Evolve 提案与证据

| 项目 | 记录 |
| --- | --- |
| 本地原图 | [20-aip-evolve-proposal.png](assets/20-aip-evolve-proposal.png) |
| 原始图片链接 | [官方原始 PNG](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-3.png) |
| 来源页面 | [AIP Evolve：Overview](https://www.palantir.com/docs/foundry/aip-evolve/overview/) |
| 获取时间（UTC） | `2026-10-01T00:59:03.818501+00:00` |
| HTTP / MIME | `200` / `image/png` |
| 尺寸 / 字节数 | 1440 × 900 px / 126,396 bytes |
| SHA-256 | `04c7ccf7826e6b67539b0b255b5ed26574e7e035aa7edac5c9999db2cce26e63` |
| 来源时期 / 版本边界 | 当前文档，未公开界面版本 |
| 视觉检查 | 2026-10-01，逐张查看本地原图 |

视检观察：AIP Evolve提案展示GPT-4o迁移GPT-5.4 Mini、compute cost降低65%、10个测试不回退、prompt guardrails；提供Resume with Feedback与Review in Branching入口。

使用边界：

- 65%是官方示例结果，不是普遍保证，也非本研究跑出的性能数据。
