# Sources

核验日：2026-09-30。以下为本报告直接依赖的 28 条 Palantir 官方一手资料。每条链接均读取正文核验；HTTP 200 之外还检查了标题/正文，避免把网站返回的软 404 当作可访问来源。

3月公告只用于首发历史；当前产品机制以本轮访问文档为准。未核实 widget 路径首发日期；没有引用内部飞书或客户资料，也没有把官方图作为本次租户亲测证据。

| ID | 官方来源 | 用途 / 可支撑的主张 | 访问日 | 结果 |
| --- | --- | --- | --- | --- |
| S01 | [2026-03-05 Pilot announcement](https://www.palantir.com/docs/foundry/announcements/2026-03#introducing-pilot-foundrys-ai-powered-tool-for-building-react-osdk-applications) | 首发日期、3月9日所在周的Beta开放计划、当时独立应用生成/部署链路；图1历史来源 | 2026-09-30 | HTTP 200；正文核验 |
| S02 | [Pilot overview](https://www.palantir.com/docs/foundry/pilot/overview) | 当前Beta、前提、两种React/OSDK交付物、总体生命周期 | 2026-09-30 | HTTP 200；正文核验 |
| S03 | [Getting started](https://www.palantir.com/docs/foundry/pilot/getting-started) | 创建入口、Save location、上下文、容器与源码；图2 | 2026-09-30 | HTTP 200；正文核验 |
| S04 | [Provide context and attachments](https://www.palantir.com/docs/foundry/pilot/provide-context) | 可附实体/functions、文档/图片格式与需求建议；图3 | 2026-09-30 | HTTP 200；正文核验 |
| S05 | [Build an application](https://www.palantir.com/docs/foundry/pilot/build-an-application) | Ontology、设计规范、前端/seed生成，Editor和Deploy数据差异 | 2026-09-30 | HTTP 200；正文核验 |
| S06 | [Ontology tab](https://www.palantir.com/docs/foundry/pilot/ontology-tab) | Existing/Proposed、seed预览、默认与逐实体修改控制、breaking changes；图4–6 | 2026-09-30 | HTTP 200；正文核验 |
| S07 | [Models and agent modes](https://www.palantir.com/docs/foundry/pilot/models-and-modes) | Act/Plan、模型族、专业agents、工具和线程；图7 | 2026-09-30 | HTTP 200；正文核验 |
| S08 | [Workspace overview](https://www.palantir.com/docs/foundry/pilot/workspace-overview) | Preview/Code/logs、状态监控、Editor/Deploy及widget生产数据toggle；图8–9 | 2026-09-30 | HTTP 200；正文核验 |
| S09 | [Deploy an application](https://www.palantir.com/docs/foundry/pilot/deploy-an-application) | 生产操作、分支/proposal、应用/域名/CI/tag、配置文件、更新流程；图10–11 | 2026-09-30 | HTTP 200；正文核验 |
| S10 | [Pilot troubleshooting](https://www.palantir.com/docs/foundry/pilot/troubleshooting) | 生产即时编辑、角色/marking、Action RID迁移、CSP/依赖/重载故障 | 2026-09-30 | HTTP 200；正文核验 |
| S11 | [Build a custom widget](https://www.palantir.com/docs/foundry/pilot/build-a-widget) | Workshop sandbox、Parameters/Events、seed/production及模型数据边界；图12 | 2026-09-30 | HTTP 200；正文核验 |
| S12 | [Deploy a custom widget](https://www.palantir.com/docs/foundry/pilot/deploy-a-widget) | 不使用Developer Console/专用子域，Main、CI、Registry与宿主固定版本；图13 | 2026-09-30 | HTTP 200；正文核验 |
| S13 | [Embedding a widget in Workshop](https://www.palantir.com/docs/foundry/custom-widgets/embedding-in-workshop) | 准确嵌入路径、首次发布、dev mode、变量/事件绑定；图14–15 | 2026-09-30 | HTTP 200；正文核验 |
| S14 | [Custom widgets core concepts](https://www.palantir.com/docs/foundry/custom-widgets/core-concepts) | widget set Compass resource、入口/版本/权限与宿主契约 | 2026-09-30 | HTTP 200；正文核验 |
| S15 | [Custom widgets overview](https://www.palantir.com/docs/foundry/custom-widgets/overview) | 支持Workshop宿主与组件定位 | 2026-09-30 | HTTP 200；正文核验 |
| S16 | [Parameters and events](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events) | 参数类型、50/50限制、camelCase、非一等类型、events | 2026-09-30 | HTTP 200；正文核验 |
| S17 | [Use OSDK in a widget set](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk) | API开启权限、用户token、受支持端点/订阅限制、宿主刷新 | 2026-09-30 | HTTP 200；正文核验 |
| S18 | [Enable additional iframe attributes](https://www.palantir.com/docs/foundry/custom-widgets/iframe-attributes) | browser sandbox附加能力和宿主/最终用户授权 | 2026-09-30 | HTTP 200；正文核验 |
| S19 | [Publish a widget set](https://www.palantir.com/docs/foundry/custom-widgets/publish) | 通用CI/CLI/ZIP机制、manifest、autoVersion；区分Pilot实际入口 | 2026-09-30 | HTTP 200；正文核验 |
| S20 | [Developer Console permissions](https://www.palantir.com/docs/foundry/developer-console/permissions) | 创建/域名角色、用户OAuth、前端不可存client credentials、restrictions/依赖、Compass/Legacy差异 | 2026-09-30 | HTTP 200；正文核验 |
| S21 | [Global Branching overview](https://www.palantir.com/docs/foundry/global-branching/overview) | 分支资源与Action隔离、proposal、与release management的区别 | 2026-09-30 | HTTP 200；正文核验 |
| S22 | [OSDK React applications overview](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/overview) | Foundry后端、React UI及专业开发路径 | 2026-09-30 | HTTP 200；正文核验 |
| S23 | [OSDK React library](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/osdk-react) | typed hooks、actions/functions、cache；不推断Pilot生成项目固定版本 | 2026-09-30 | HTTP 200；正文核验 |
| S24 | [Development lifecycle](https://www.palantir.com/docs/foundry/platform-overview/development-life-cycle) | Beta/GA的官方状态含义 | 2026-09-30 | HTTP 200；正文核验 |
| S25 | [Workshop overview](https://www.palantir.com/docs/foundry/workshop/overview) | 对象数据、Actions/Functions、布局、组件与事件的应用编排职责 | 2026-09-30 | HTTP 200；正文核验 |
| S26 | [Workshop publishing and versioning](https://www.palantir.com/docs/foundry/workshop/versions) | Workshop模块的发布与版本职责 | 2026-09-30 | HTTP 200；正文核验 |
| S27 | [SuperRepo overview](https://www.palantir.com/docs/foundry/superrepo/overview) | 边界比较：Ontology-first pro-code monorepo；不重写旧专题 | 2026-09-30 | HTTP 200；正文核验 |
| S28 | [SuperRepo core concepts](https://www.palantir.com/docs/foundry/superrepo/core-concepts) | 边界比较：组件、CLI预览、bundle/deploy、Marketplace；不推断Pilot内置SuperRepo | 2026-09-30 | HTTP 200；正文核验 |

## 引用方法与范围

正文的技术事实直接链接到对应官方页；分析、建议与验证计划有明确标签。短术语和UI名称保留原文，其余为中文概括，不镜像整篇文章。

本轮未取得可复核的Pilot公开源码实现或独立演示视频地址，因此没有把代码仓库或视频当作产品内部实现的证据。OSDK与通用widget文档仅用于解释其底层能力，不据此保证每个Pilot生成项目采用相同版本或配置。

公开资料无法证明特定enrollment实际可用、生成质量、部署成功率或生产稳定性；未解决问题见[正文第12节](README.md#limits)。所有相对文件链接、来源URL与所引用段落锚点的检查结果见[checks.md](checks.md)。
