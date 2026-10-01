# 架构研究检查与限制

研究日：2026-10-01 UTC。本文为源码/类型/测试审读和发布溯源，不执行生产Ontology/Actions。

| 检查 | 结果与范围 | 记录 |
|---|---|---|
| 核心npm2.75.0与UI0.61.0 | 实际registry日期/tag/provenance，分别commit | [release](npm-release-evidence.json)、[provenance](npm-provenance-evidence.json) |
| OAuth/shared发布源 | 单独registry/provenance，3真实tarball SRI；浏览器maps sourcesContent对应 | [codegen-auth evidence](evidence/codegen-auth-core-npm-evidence.json)、[source verification](evidence/auth-source-verification.json) |
| 源码引用 | 原始独立稿129 fixedlinks，0错误；最终另全稿检查 | [原稿检查](evidence/architecture-checks.json)、[组装检查](evidence/assembly-checks.json) |
| API/codegen/auth审读 | 74路径/行核验及发布JS/maps行为比对 | [checks](evidence/codegen-auth-checks.json)；不称全repo行为已审 |
| 包地图 | 95 packages/* manifests，44private/51未private | [inventory](package-inventory.json)；非发布包数或全workspace数 |
| 许可证 | 关键包/若干依赖manifest | [license metadata](evidence/codegen-auth-license-metadata.json)；非完整传递依赖NOTICE审计 |
| 官方叙述页HTTP | 两篇引用的16个官方页面均200，未见soft404 | [HTTP记录](evidence/http-checks.json)；不代表所有动态Storybook/PR逐一HTTP复测 |
| 上游unit/integration/e2e | 关键assertion/source阅读 | 没有重跑，不声称当前tests全部pass |
| React19运行验证 | 配套组件篇的普通BaseForm隔离路径 | [组件checks](../osdk-react-components-2026-09/checks.md)；不代替完整cache/backend验证 |

未独立验证完整provenance密码学信任链；原始源码/tarball在临时工作区核验，不在研究库镜像；记录保留URL、摘要与对照结果。文中的cache/Action/stream分支是固定源码观察，生产权限、latency、断线恢复、真实数量/分页、跨组件全部刷新、全部浏览器与SSR仍需实际受控环境。

事实、类型、上游测试意图与EOS建议分开。邻近maker/faux/widget/agents等只做系统地图及关键关联，不把全仓范围理解为每包完整运行审计。AI/Pilot具体产品关联深入放在[组件AI章](../osdk-react-components-2026-09/ai-generation.md)，避免重复props/API图鉴。
