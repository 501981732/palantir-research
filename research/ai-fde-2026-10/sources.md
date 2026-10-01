# AI FDE 来源台账

> 核验截止/访问日期：2026-10-01（UTC）。主文是研究者的中文归纳，不镜像第三方全文、字幕或内部资料。

本轮核验官方机制、原始实践/社区、视频页面、关键源码评论与图像，并记录各类证据的可见范围。A/B1/B2/C说明证据用途，官方文档也不构成独立收益评测。具体作者、日期、版本未知和解决状态见正文§11–12。

公开HTTP复核覆盖85个去掉fragment后的URL：65个返回200，20个受访问/网络限制；YouTube同一视频的时间点/评论链接是不同URL，不是独立视频。HTTP200只证明页面响应，不能证明登录内容可见或产品运行；官方HTML还含user-content前缀锚点，release notes正文按动态渲染核验。Medium返回403、LinkedIn个人页999，YouTube/Reddit网络访问受限；没有绕过限制，保留已核验的原始页面/索引与相应证据边界。

视频证据包括页面元数据、部分公开说明、章节导航、评论，以及Ontologize Getting Started 13:10的局部实际画面（图20）。未完整观看，也未取得可靠转写；其他章节和二级摘要不替代实际观看证据。图像原URL、来源页、时间、尺寸与哈希另见[assets.md](assets.md)。

## 逐条引用（含精确章节、时间点与评论链接）

| ID | 原始链接 / 标题 | 层级与日期/边界 | 用于主文 | 链接复核 |
| --- | --- | --- | --- | --- |
| S001 | [AI FDE • Overview • Palantir](https://www.palantir.com/docs/foundry/ai-fde/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §1、§2、§3、§13、§15 | HTTP 200 |
| S002 | [2025 • November 2025 • Palantir](https://www.palantir.com/docs/foundry/announcements/2025-11) | A：官方历史公告；节点见正文时间线；不能作为当前支持矩阵 | §1、§2 | HTTP 200 |
| S003 | [March 2026 • Announcements • Palantir](https://www.palantir.com/docs/foundry/announcements/2026-03) | A：官方历史公告；节点见正文时间线；不能作为当前支持矩阵 | §1、§2 | HTTP 200 |
| S004 | [AI FDE • Modes and capabilities • Palantir](https://www.palantir.com/docs/foundry/ai-fde/modes-and-capabilities) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §1、§2、§3、§5、§7、§15 | HTTP 200 |
| S005 | [AI FDE • Security and governance • Palantir](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §1、§4、§8、§15 | HTTP 200 |
| S006 | [Global Branching • Core concepts • Palantir](https://www.palantir.com/docs/foundry/global-branching/core-concepts) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §1、§6、§9 | HTTP 200 |
| S007 | [Global Branching • Integrations • Palantir](https://www.palantir.com/docs/foundry/global-branching/integrations) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §1、§7、§9 | HTTP 200 |
| S008 | [2025 Q2 官方材料](https://investors.palantir.com/files/Palantir%20Q2%202025%20Business%20Update.pdf) | A：官方投资者材料；2025 Q2材料；证明DevCon 3已宣布，不把PDF发布时间当首次亮相日 | §2 | HTTP 200 |
| S009 | [DevCon 3 视频](https://www.youtube.com/watch?v=SDqkGVuL1b8) | A：官方视频页面说明；Palantir Developers，2025-07-03；页面元数据/说明；无产品内容截帧/字幕，未完整观看 | §2、§12 | HTTP读取受限/未单独检查 |
| S010 | [April 2026 • Announcements • Palantir](https://www.palantir.com/docs/foundry/announcements/2026-04) | A：官方历史公告；节点见正文时间线；不能作为当前支持矩阵 | §2、§6、§7 | HTTP 200 |
| S011 | [May 2026 • Announcements • Palantir](https://www.palantir.com/docs/foundry/announcements/2026-05) | A：官方历史公告；节点见正文时间线；不能作为当前支持矩阵 | §2 | HTTP 200 |
| S012 | [July 2026 • Announcements • Palantir](https://www.palantir.com/docs/foundry/announcements/2026-07) | A：官方历史公告；节点见正文时间线；不能作为当前支持矩阵 | §2、§13 | HTTP 200 |
| S013 | [September 2026 • Announcements • Palantir](https://www.palantir.com/docs/foundry/announcements/2026-09) | A：官方历史公告；节点见正文时间线；不能作为当前支持矩阵 | §2、§9、§13 | HTTP 200 |
| S014 | [2026 • Release notes • Palantir](https://www.palantir.com/docs/foundry/release-notes) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §2 | HTTP 200 |
| S015 | [AI FDE • Pre-fill sessions with URL parameters • Palantir](https://www.palantir.com/docs/foundry/ai-fde/prefill-sessions) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §2、§4、§14 | HTTP 200 |
| S016 | [AI FDE • Best practices • Palantir](https://www.palantir.com/docs/foundry/ai-fde/best-practices) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §3、§6、§15 | HTTP 200 |
| S017 | [AI FDE • Navigation • Palantir](https://www.palantir.com/docs/foundry/ai-fde/navigation) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §4、§8、§13 | HTTP 200 |
| S018 | [AI FDE • Overview • Palantir / 概览的上下文管理](https://www.palantir.com/docs/foundry/ai-fde/overview#context-management) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §4 | HTTP 200；锚点存在 |
| S019 | [AI FDE • Navigation • Palantir / 导航的上下文管理](https://www.palantir.com/docs/foundry/ai-fde/navigation#manage-context) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §4 | HTTP 200；锚点存在 |
| S020 | [AI FDE • Navigation • Palantir / Chat outline](https://www.palantir.com/docs/foundry/ai-fde/navigation#chat-outline) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §4 | HTTP 200；锚点存在 |
| S021 | [AI FDE • Best practices • Palantir / 工具与上下文最佳实践](https://www.palantir.com/docs/foundry/ai-fde/best-practices#limit-tools-and-context) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §4 | HTTP 200；锚点存在 |
| S022 | [AI FDE • Navigation • Palantir / 工具配置](https://www.palantir.com/docs/foundry/ai-fde/navigation#tool-configuration) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §4、§8 | HTTP 200；锚点存在 |
| S023 | [AI FDE • Modes and capabilities • Palantir / capabilities](https://www.palantir.com/docs/foundry/ai-fde/modes-and-capabilities#capabilities) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §4、§5 | HTTP 200；锚点存在 |
| S024 | [Core concepts • Selecting the right modeling tool • Palantir](https://www.palantir.com/docs/foundry/model-integration/what-to-use) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §5 | HTTP 200 |
| S025 | [Data Connection • Troubleshooting • Palantir](https://www.palantir.com/docs/foundry/data-connection/troubleshooting) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §5 | HTTP 200 |
| S026 | [9/23 agent worker 发布记录](https://www.palantir.com/docs/foundry/release-notes/2026/#95340bd2-48a5-48b4-b04d-ca1d073b6d3a) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §5 | HTTP 200；条目经渲染页核验 |
| S027 | [SQL worksheet（9/23）](https://www.palantir.com/docs/foundry/release-notes/2026/#68b31d23f14fca1471c886f5e6a07c8de4ef796c969a425d1ea8a5b07ea2d22c) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §5 | HTTP 200；条目经渲染页核验 |
| S028 | [cover page（9/21）](https://www.palantir.com/docs/foundry/release-notes/2026/#6c94d48c1ddb581ec8b3deec757e2a5f5fd6a54b1d72f62bd97ccdf2ec27aa01) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §5 | HTTP 200；条目经渲染页核验 |
| S029 | [100条会话（9/21）](https://www.palantir.com/docs/foundry/release-notes/2026/#2aff432af41b5161901781c72f558408087909e76e60603a825c8d35769119da) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §5 | HTTP 200；条目经渲染页核验 |
| S030 | [OSDK React 分支（9/21）](https://www.palantir.com/docs/foundry/release-notes/2026/#b9004d1893e824bc87e42408b2c485487352bc056d1e01df9b12c7749a24a90e) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §5 | HTTP 200；条目经渲染页核验 |
| S031 | [已有 agent repo（9/21）](https://www.palantir.com/docs/foundry/release-notes/2026/#b8ef2daac88f3f804dc48b3a4a6f52b829a85a8dad296b6699f52b7b3a8b19c9) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §5 | HTTP 200；条目经渲染页核验 |
| S032 | [AI FDE • Overview • Palantir / 闭环操作](https://www.palantir.com/docs/foundry/ai-fde/overview#closed-loop-operation) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §6、§7 | HTTP 200；锚点存在 |
| S033 | [AIP Evals • Overview • Palantir](https://www.palantir.com/docs/foundry/aip-evals/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §6、§7 | HTTP 200 |
| S034 | [Action types • Branching action types • Palantir](https://www.palantir.com/docs/foundry/action-types/branching-action-types) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §7、§10 | HTTP 200 |
| S035 | [Developer Console • Core concepts • Hosting an application on Foundry • Palantir](https://www.palantir.com/docs/foundry/developer-console/deploy-custom-application-on-foundry) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §7 | HTTP 200 |
| S036 | [Custom widgets • Embedding a widget in Workshop • Palantir](https://www.palantir.com/docs/foundry/custom-widgets/embedding-in-workshop) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §7 | HTTP 200 |
| S037 | [AI FDE • Security and governance • Palantir / 安全专页](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance#user-approval-for-sensitive-actions) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §8 | HTTP 200；锚点存在 |
| S038 | [AI FDE • Security and governance • Palantir / Session access and security](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance#session-access-and-security) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §8 | HTTP 200；锚点存在 |
| S039 | [Administration • Control LLM data access with Markings • Palantir](https://www.palantir.com/docs/foundry/aip/control-llm-data-access-with-markings) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §8 | HTTP 200 |
| S040 | [AIP security and privacy • Palantir](https://www.palantir.com/docs/foundry/aip/aip-security) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §8 | HTTP 200 |
| S041 | [Global Branching • Overview • Palantir](https://www.palantir.com/docs/foundry/global-branching/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200 |
| S042 | [Global Branching • Core concepts • Palantir / core concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts#editing-resources) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200；锚点存在 |
| S043 | [Data Lineage • Branching data lineage • Palantir](https://www.palantir.com/docs/foundry/data-lineage/branching-data-lineage) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200 |
| S044 | [Object edits and materializations • Materializations • Palantir](https://www.palantir.com/docs/foundry/object-edits/materializations) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200 |
| S045 | [Concepts • Branching restricted views • Palantir](https://www.palantir.com/docs/foundry/security/branching-restricted-views) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200 |
| S046 | [Global Branching • Branch security • Palantir](https://www.palantir.com/docs/foundry/global-branching/branch-security) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200 |
| S047 | [Global Branching • Branch security • Palantir / Organizations](https://www.palantir.com/docs/foundry/global-branching/branch-security#organizations) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200；锚点存在 |
| S048 | [Global Branching • Resource protection and approval policies • Palantir](https://www.palantir.com/docs/foundry/global-branching/resource-protection-and-approval-policies) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200 |
| S049 | [Global Branching • Core concepts • Palantir / 生命周期](https://www.palantir.com/docs/foundry/global-branching/core-concepts#branch-and-proposal-lifecycle) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §9 | HTTP 200；锚点存在 |
| S050 | [AIP Evals • Evaluate Ontology edits • Palantir](https://www.palantir.com/docs/foundry/aip-evals/ontology-edits) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §10 | HTTP 200 |
| S051 | [Action types • Branching action types • Palantir / branch Action 副作用](https://www.palantir.com/docs/foundry/action-types/branching-action-types#managing-side-effects-on-branches) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §10 | HTTP 200；锚点存在 |
| S052 | [Action types • Test run • Palantir / Test run](https://www.palantir.com/docs/foundry/action-types/test-run#external-calls) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §10 | HTTP 200；锚点存在 |
| S053 | [作者原文](https://medium.com/@MaheshRamamurthy/i-built-an-enterprise-grade-app-backend-in-14-hours-with-ai-heres-what-that-actually-means-780bc90749ba) | B1：具名一手项目自述；Mahesh Ramamurthy，2026-02-20；职业/认证自述；14小时是个案，AWS对照为估算，未独立复现 | §11 | HTTP 403 |
| S054 | [本人 LinkedIn](https://www.linkedin.com/in/tenacious-mahesh-ramamurthy) | B1：作者身份索引；Mahesh本人页面/索引交叉信息；不能独立认证当前任职、认证或商业关系 | §11 | HTTP 999 |
| S055 | [原视频](https://www.youtube.com/watch?v=Ta19YD794RY) | B1：伙伴教程页面说明；Ontologize，2026-06-03；页面说明与局部实际观察见§12/图20；章节本身不代表全段已看，未完整观看，无可靠字幕 | §11、§12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S056 | [AI FDE Simplifies Work in Foundry with Conversational Interface / Gena Coblentz posted on the topic / LinkedIn](https://www.linkedin.com/posts/gena-coblentz_aip-foundry-palantir-activity-7468337522910179329-bySL) | B1：演示者本人说明；Gena Coblentz / Ontologize；日期相对表达不伪造精确日；伙伴商业关系见官网 | §11 | HTTP 200 |
| S057 | [Palantir Training, Fellowships & Exams](https://www.ontologize.com/) | B1：伙伴自有身份页；自述前Palantir工程师及Official Training & Assessment Partner；有商业关系 | §11 | HTTP 200 |
| S058 | [The Ouroboros AI Forge – using AI to build a system that uses AI to teach you foundry (and AI) – Michael Ellerbeck](https://michaelellerbeck.com/2026/02/20/the-ouroboros-ai-forge-using-ai-to-build-a-system-that-uses-ai-to-teach-you-foundry-and-ai/) | B1：作者实验博客；Michael Ellerbeck，2026-02-20；自有原型过程，不将后续手工工程全部归功AI FDE | §11 | HTTP 200 |
| S059 | [GitHub - s-andthat/palantir-ai-fde-library: A community prompt and agent architecture library for Palantir's AI FDE. · GitHub](https://github.com/s-andthat/palantir-ai-fde-library) | B1：社区公开工件；s-andthat，作者发布帖2026-03-16；模板方法可借鉴，性能汇编非复现实验 | §11 | HTTP 200 |
| S060 | [AI-FDE Core Architecture Library - Ask the Community - Palantir Developer Community](https://community.palantir.com/t/ai-fde-core-architecture-library/6199) | B1：社区工件作者发布帖；s-andthat，2026-03-16；真实身份未知；非原生Skill兼容或benchmark证明 | §11 | HTTP 200 |
| S061 | [AI FDE Context Management - Product Feedback - Palantir Developer Community](https://community.palantir.com/t/ai-fde-context-management/6272) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S062 | [Feature Request: Add Data Expectations to Pipeline Builder DSL - Product Feedback - Palantir Developer Community](https://community.palantir.com/t/feature-request-add-data-expectations-to-pipeline-builder-dsl/6426) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S063 | [AI FDE Error: Failed to load Workshop module due to missing Action Parameter RID - Ask the Community - Palantir Developer Community](https://community.palantir.com/t/ai-fde-error-failed-to-load-workshop-module-due-to-missing-action-parameter-rid/6506) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S064 | [Feature Request: AI FDE able to integrate Linter - Product Feedback - Palantir Developer Community](https://community.palantir.com/t/feature-request-ai-fde-able-to-integrate-linter/6513) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S065 | [AI FDE performance - Product Feedback - Palantir Developer Community](https://community.palantir.com/t/ai-fde-performance/6573) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S066 | [Welcome skills in AI FDE! (but how can I added?) - Ask the Community - Palantir Developer Community](https://community.palantir.com/t/welcome-skills-in-ai-fde-but-how-can-i-added/6880) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S067 | [Any tips to reduce AI-FDE rate limiting? - Ask the Community - Palantir Developer Community](https://community.palantir.com/t/any-tips-to-reduce-ai-fde-rate-limiting/7121) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S068 | [AI-FDE bug: approval always required for container_transform_preview - Product Feedback - Palantir Developer Community](https://community.palantir.com/t/ai-fde-bug-approval-always-required-for-container-transform-preview/7157) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S069 | [Need configurability for Sub Agents In AIFDE - Product Feedback - Palantir Developer Community](https://community.palantir.com/t/need-configurability-for-sub-agents-in-aifde/7204) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S070 | [AI FDE Model Auto Select - Product Feedback - Palantir Developer Community](https://community.palantir.com/t/ai-fde-model-auto-select/7276) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S071 | [AI FDE returns HTTP 500 even for a simple prompt in a new session - Ask the Community - Palantir Developer Community](https://community.palantir.com/t/ai-fde-returns-http-500-even-for-a-simple-prompt-in-a-new-session/7205) | B2：社区原帖/后续；作者、首次日期、回应与解决状态见§11.5；公开账号身份/build未独立核验，未租户复现 | §11 | HTTP 200 |
| S072 | [原帖及讨论](https://www.reddit.com/r/dataengineering/comments/1v3u40k/my_experience_working_with_palantir_as_a_client/) | C：未核身份的客户自述；CuriousMemo，2026年7月（搜索日期7/22）；正文与后续自我修正均保留，项目与AI FDE归因未验证 | §11 | HTTP读取受限/未单独检查 |
| S073 | [迁移视频](https://www.youtube.com/watch?v=e90qUUh8_us) | A：官方视频页面说明；Palantir，2026-03-11；页面元数据/说明；无产品内容截帧/字幕，未完整观看 | §11 | HTTP读取受限/未单独检查 |
| S074 | [AIP Evolve • Overview • Palantir](https://www.palantir.com/docs/foundry/aip-evolve/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §11、§13 | HTTP 200 |
| S075 | [DevCon 6 视频](https://www.youtube.com/watch?v=GZHSCMz6Aio) | A：官方视频页面说明；Palantir / Developers，2026-07-14；页面元数据/说明；无产品内容截帧/字幕，未完整观看 | §11、§12 | HTTP读取受限/未单独检查 |
| S076 | [DevCon 5 AI FDE](https://www.youtube.com/watch?v=pyudERNI1Qo) | A：官方视频页面说明；Palantir Developers，2026年3月；早期页面3/9与本轮3/10显示有差异，原因未确认；页面元数据/说明；无产品内容截帧/字幕，未完整观看 | §12 | HTTP读取受限/未单独检查 |
| S077 | [Ontology Functions](https://www.youtube.com/watch?v=GaSe4U2khI0) | B1：伙伴教程页面说明；Ontologize，2026-07-29；页面元数据/说明；无产品内容截帧/字幕，未完整观看 | §12 | HTTP读取受限/未单独检查 |
| S078 | [Voice-Enabled OSDK Application](https://www.youtube.com/watch?v=_Zr2wjbenyU) | B1：伙伴教程页面说明；Ontologize，2026-08-12；页面元数据/说明；无产品内容截帧/字幕，未完整观看 | §12 | HTTP读取受限/未单独检查 |
| S079 | [4:20 modes](https://www.youtube.com/watch?v=Ta19YD794RY&t=260s) | B1：伙伴教程页面说明；Ontologize，2026-06-03；页面说明与局部实际观察见§12/图20；章节本身不代表全段已看，未完整观看，无可靠字幕 | §12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S080 | [8:49 analysis](https://www.youtube.com/watch?v=Ta19YD794RY&t=529s) | B1：伙伴教程页面说明；Ontologize，2026-06-03；页面说明与局部实际观察见§12/图20；章节本身不代表全段已看，未完整观看，无可靠字幕 | §12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S081 | [12:35 transformation](https://www.youtube.com/watch?v=Ta19YD794RY&t=755s) | B1：伙伴教程页面说明；Ontologize，2026-06-03；页面说明与局部实际观察见§12/图20；章节本身不代表全段已看，未完整观看，无可靠字幕 | §12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S082 | [8:41 PR/preview](https://www.youtube.com/watch?v=_Zr2wjbenyU&t=521s) | B1：伙伴教程页面说明；Ontologize，2026-08-12；页面元数据/说明与章节导航；无产品内容截帧/字幕，未完整观看 | §12 | HTTP读取受限/未单独检查 |
| S083 | [10:36 hosting](https://www.youtube.com/watch?v=_Zr2wjbenyU&t=636s) | B1：伙伴教程页面说明；Ontologize，2026-08-12；页面元数据/说明与章节导航；无产品内容截帧/字幕，未完整观看 | §12 | HTTP读取受限/未单独检查 |
| S084 | [7:41 Evolve](https://www.youtube.com/watch?v=GZHSCMz6Aio&t=461s) | A：官方视频页面说明；Palantir / Developers，2026-07-14；页面元数据/说明与章节导航；无产品内容截帧/字幕，未完整观看 | §12 | HTTP读取受限/未单独检查 |
| S085 | [12:46 workflow](https://www.youtube.com/watch?v=GZHSCMz6Aio&t=766s) | A：官方视频页面说明；Palantir / Developers，2026-07-14；页面元数据/说明与章节导航；无产品内容截帧/字幕，未完整观看 | §12 | HTTP读取受限/未单独检查 |
| S086 | [实际帧对应原视频时间点](https://www.youtube.com/watch?v=Ta19YD794RY&t=790s) | B1：伙伴视频局部实际画面；Ontologize，2026-06-03；13:10已亲自观察并保存图20；仅模式错误/成功结果，不是全流程复现，无可靠转写 | §12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S087 | [@VentsSansRive](https://www.youtube.com/watch?v=Ta19YD794RY&lc=UgwVrxeKDn2CmlzVmt54AaABAg) | C：YouTube用户评论；账号/相对日期见§12，读取于截止日；使用背景未核验，不能当普遍缺陷或效果 | §12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S088 | [@ajathreya](https://www.youtube.com/watch?v=Ta19YD794RY&lc=Ugz5Big2dnvesmSzAR94AaABAg) | C：YouTube用户评论；账号/相对日期见§12，读取于截止日；使用背景未核验，不能当普遍缺陷或效果 | §12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S089 | [@GeorgeGorzhiyev](https://www.youtube.com/watch?v=Ta19YD794RY&lc=UgySM_rI7i60EMLCpVR4AaABAg) | C：YouTube用户评论；账号/相对日期见§12，读取于截止日；使用背景未核验，不能当普遍缺陷或效果 | §12 | HTTP读取受限/未单独检查；原页可见/图20局部画面已核验 |
| S090 | [Pilot • Overview • Palantir](https://www.palantir.com/docs/foundry/pilot/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S091 | [SuperRepo • Overview • Palantir](https://www.palantir.com/docs/foundry/superrepo/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S092 | [AIP Analyst • Overview • Palantir](https://www.palantir.com/docs/foundry/aip-analyst/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S093 | [AIP Assist • Overview • Palantir](https://www.palantir.com/docs/foundry/assist/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S094 | [Codex CLI / ChatGPT Learn](https://learn.chatgpt.com/docs/codex/cli) | A：OpenAI官方文档；只用于外部代码工作区Agent边界，不用于Foundry权限或效果承诺 | §13 | HTTP 200 |
| S095 | [Palantir MCP • Overview • Palantir](https://www.palantir.com/docs/foundry/palantir-mcp/overview) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S096 | [SuperRepo • Coming in the future • Palantir](https://www.palantir.com/docs/foundry/superrepo/in-development) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S097 | [[OSDK] Add Agent.md by Leolide · Pull Request #2628 · palantir/osdk-ts · GitHub / 作者原始评论](https://github.com/palantir/osdk-ts/pull/2628#issuecomment-3985012402) | A：官方源码库原始讨论；Leolide，PR #2628，2026-03-09已合并；原始评论已读取核验；作者意图不是所有产物依赖保证 | §13 | HTTP 200；原始评论核验 |
| S098 | [Palantir MCP • Available tools • Palantir](https://www.palantir.com/docs/foundry/palantir-mcp/available-tools) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S099 | [Palantir MCP • Tool search • Palantir](https://www.palantir.com/docs/foundry/palantir-mcp/tool-search) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S100 | [Palantir MCP • Security • Palantir](https://www.palantir.com/docs/foundry/palantir-mcp/security) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §13 | HTTP 200 |
| S101 | [AIP Analyst • Using AIP Analyst • Palantir / Analyst Skills](https://www.palantir.com/docs/foundry/aip-analyst/using-aip-analyst#skills) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §14 | HTTP 200；锚点存在 |
| S102 | [Skill menu（9/14）](https://www.palantir.com/docs/foundry/release-notes/2026/#fa68fe10953b155c28317e2a64b8c68bf6b0be87c56ebcd6b02c6adaa9c92196) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §14 | HTTP 200；条目经渲染页核验 |
| S103 | [prefill/Evolve 标题（9/14）](https://www.palantir.com/docs/foundry/release-notes/2026/#655f177018e6851c30b3e73c8a8a9aaf2a05490073d4b89e982c6de6824421d8) | A：官方带日期更新；稳定条目链接；可见发布条目已核验，初始HTML不含全部条目 | §14 | HTTP 200；条目经渲染页核验 |
| S104 | [AI FDE • Overview • Palantir / 模型支持](https://www.palantir.com/docs/foundry/ai-fde/overview#model-support) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §14 | HTTP 200；锚点存在 |
| S105 | [Bring your own model • Bring your own model to AIP • Palantir](https://www.palantir.com/docs/foundry/aip/bring-your-own-model) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §14 | HTTP 200 |
| S106 | [Administration • LLM capacity management • Palantir](https://www.palantir.com/docs/foundry/aip/llm-capacity-management) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §14 | HTTP 200 |
| S107 | [Compute usage with AIP • Palantir](https://www.palantir.com/docs/foundry/aip/aip-compute-usage) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §14 | HTTP 200 |
| S108 | [AI FDE • Best practices • Palantir / 基础设施约束](https://www.palantir.com/docs/foundry/ai-fde/best-practices#consider-infrastructure-constraints) | A：官方当前文档；行为契约；滚动更新，配置/租户可能不同；不是独立成效测试 | §14 | HTTP 200；锚点存在 |

## 取舍与未使用材料

竞争方LLM文档评分、外部coding benchmark、投资解说和AI摘要仅用于发现线索，不支撑AI FDE成功率、内部实现或竞品排名。未取得完整原视频的二级时间码未纳入已观察流程。没有因某个社区问题无答复就断言产品不支持，也没有将首帖已澄清/解决的问题列为现版缺陷。

普通网页图片仍归原权利人；公开访问不自动提供通用再分发许可。本仓库保存具明确研究目的与逐图归因的官方原图和1张伙伴原视频实际帧。合成业务案例、机制关系图和EOS方案均为研究者分析，不是原始厂商实测。
