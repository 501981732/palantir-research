# Workshop 运行研究：公开来源与追溯索引

核验日期：2026-10-01。本文连接 [主报告](README.md)、[变量与事件](variables-events.md)和[数据、Actions与版本](data-actions-versioning.md)的第一方公开证据，共 52 个官方页面或固定公开源码文件；另引用既有研究专题及经授权公开的EOS现状对照。每项技术声明的具体支持段落已在正文附近链接；两篇附录还提供声明编号与页面节标题，避免用总索引替代逐声明证据。

## 证据如何使用

- Palantir 产品文档用于确认可观察行为、配置条件、限制和公开保证。访问日期不是文档发布时间，也不证明某个租户已部署相同能力。
- 公开 OSDK 源码使用固定 commit；只把能观察到的客户端行为写为源码事实，不借它推断整个闭源 Workshop 的调度、缓存或传输实现。
- 图是综合公开关系的概念模型。图中文字和边界必须由相邻证据支持，不能将合并流程当作完整后端拓扑。
- 通用研究建议和后续实验方案在正文单独标记。本次未在 Foundry 租户、Registry 或业务环境执行这些实验，详见 [checks](checks.md)。

动态网页可能改版；附录抓取正文行号仅供本次审阅定位。应优先用稳定 URL 与节标题重新核对，不把抓取行号当作永久锚点。官方不同页面存在的结构体初始化说明差异已在变量附录 S02 保留，未自行将差异消解为一个产品保证。

## 创作、OSDK 与组件交付

| 一手资料 | 本次使用位置 |
|---|---|
| [client.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/client.ts) | [README.md](README.md) |
| [官方参数指南](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events) | [README.md](README.md) |
| [官方发布文档](https://www.palantir.com/docs/foundry/custom-widgets/publish) | [README.md](README.md) |
| [Refresh host data on action](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk) | [README.md](README.md) |
| [OSDK React](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/osdk-react) | [README.md](README.md) |
| [OSDK React components](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/osdk-react-components) | [README.md](README.md) |
| [Build a custom widget](https://www.palantir.com/docs/foundry/pilot/build-a-widget) | [README.md](README.md) |
| [Build an application](https://www.palantir.com/docs/foundry/pilot/build-an-application) | [README.md](README.md) |
| [Pilot widget deployment](https://www.palantir.com/docs/foundry/pilot/deploy-a-widget) | [README.md](README.md) |
| [Pilot application deployment](https://www.palantir.com/docs/foundry/pilot/deploy-an-application) | [README.md](README.md) |

## 宿主变量、事件、布局与版本

| 一手资料 | 本次使用位置 |
|---|---|
| [Use Actions in Workshop](https://www.palantir.com/docs/foundry/workshop/actions-use) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Auto-refresh](https://www.palantir.com/docs/foundry/workshop/auto-refresh) | [data-actions-versioning.md](data-actions-versioning.md)、[variables-events.md](variables-events.md) |
| [Changelog panel](https://www.palantir.com/docs/foundry/workshop/changelog) | [README.md](README.md)、[data-actions-versioning.md](data-actions-versioning.md) |
| [Events](https://www.palantir.com/docs/foundry/workshop/concepts-events) | [variables-events.md](variables-events.md) |
| [Layouts](https://www.palantir.com/docs/foundry/workshop/concepts-layouts) | [README.md](README.md) |
| [Workshop permissions](https://www.palantir.com/docs/foundry/workshop/concepts-permissions) | [README.md](README.md)、[data-actions-versioning.md](data-actions-versioning.md) |
| [Variables](https://www.palantir.com/docs/foundry/workshop/concepts-variables) | [variables-events.md](variables-events.md) |
| [Derived properties](https://www.palantir.com/docs/foundry/workshop/derived-properties) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Use Functions in Workshop](https://www.palantir.com/docs/foundry/workshop/functions-use) | [data-actions-versioning.md](data-actions-versioning.md)、[variables-events.md](variables-events.md) |
| [Module interface](https://www.palantir.com/docs/foundry/workshop/module-interface) | [variables-events.md](variables-events.md) |
| [Object set filter variables](https://www.palantir.com/docs/foundry/workshop/object-set-filter-variables) | [variables-events.md](variables-events.md) |
| [Workshop overview](https://www.palantir.com/docs/foundry/workshop/overview) | [README.md](README.md) |
| [Performance Profiler](https://www.palantir.com/docs/foundry/workshop/performance-profiler) | [README.md](README.md)、[data-actions-versioning.md](data-actions-versioning.md)、[variables-events.md](variables-events.md) |
| [Routing](https://www.palantir.com/docs/foundry/workshop/routing) | [README.md](README.md) |
| [SQL query variables](https://www.palantir.com/docs/foundry/workshop/sql-query-variables) | [variables-events.md](variables-events.md) |
| [State saving](https://www.palantir.com/docs/foundry/workshop/state-saving) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Struct variables](https://www.palantir.com/docs/foundry/workshop/struct-variables) | [variables-events.md](variables-events.md) |
| [Variable-backed layouts](https://www.palantir.com/docs/foundry/workshop/variable-backed-layouts) | [variables-events.md](variables-events.md) |
| [Variable transformations](https://www.palantir.com/docs/foundry/workshop/variable-transformations) | [variables-events.md](variables-events.md) |
| [Publishing and versioning](https://www.palantir.com/docs/foundry/workshop/versions) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Widget display optimization](https://www.palantir.com/docs/foundry/workshop/widget-display-optimization) | [data-actions-versioning.md](data-actions-versioning.md)、[variables-events.md](variables-events.md) |
| [AIP Chatbot](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot) | [data-actions-versioning.md](data-actions-versioning.md) |
| [AIP Generated Content](https://www.palantir.com/docs/foundry/workshop/widgets-aip-generated-content) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Button Group](https://www.palantir.com/docs/foundry/workshop/widgets-button-group) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Data Freshness](https://www.palantir.com/docs/foundry/workshop/widgets-data-freshness) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Filter List](https://www.palantir.com/docs/foundry/workshop/widgets-filter-list) | [variables-events.md](variables-events.md) |
| [Inline Action](https://www.palantir.com/docs/foundry/workshop/widgets-inline-action-form) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Object Dropdown](https://www.palantir.com/docs/foundry/workshop/widgets-object-dropdown) | [variables-events.md](variables-events.md) |
| [Object Table](https://www.palantir.com/docs/foundry/workshop/widgets-object-table) | [data-actions-versioning.md](data-actions-versioning.md)、[variables-events.md](variables-events.md) |

## Ontology Actions 与运行态 AIP

| 一手资料 | 本次使用位置 |
|---|---|
| [Undo or revert Actions](https://www.palantir.com/docs/foundry/action-types/action-reverts) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Consistency and isolation](https://www.palantir.com/docs/foundry/action-types/consistency-guarantees) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Action monitoring](https://www.palantir.com/docs/foundry/action-types/monitoring) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Action type permissions](https://www.palantir.com/docs/foundry/action-types/permissions) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Submission criteria](https://www.palantir.com/docs/foundry/action-types/submission-criteria) | [data-actions-versioning.md](data-actions-versioning.md) |
| [AIP Analyst Workshop widget](https://www.palantir.com/docs/foundry/aip-analyst/workshop-widget) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state) | [data-actions-versioning.md](data-actions-versioning.md) |
| [User-facing errors](https://www.palantir.com/docs/foundry/functions/user-facing-error) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Logic core concepts](https://www.palantir.com/docs/foundry/logic/core-concepts) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Execution mode settings](https://www.palantir.com/docs/foundry/logic/execution-mode-settings) | [data-actions-versioning.md](data-actions-versioning.md) |
| [AIP Logic overview](https://www.palantir.com/docs/foundry/logic/overview) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Staged writes in AIP Logic](https://www.palantir.com/docs/foundry/logic/staged-writes) | [data-actions-versioning.md](data-actions-versioning.md) |
| [Object Set Service limitations](https://www.palantir.com/docs/foundry/ontologies/oss-limitations) | [data-actions-versioning.md](data-actions-versioning.md) |

## 与既有研究的关系和版本边界

本专题承接下列已有公开研究的职责，不重新实施其构建、探针或组件测试：

| 既有专题 | 本专题使用范围 |
|---|---|
| [Pilot](../pilot-2026-09/README.md) | 生成源应用/Widget的创作入口，当前部署行为另核对官方文档 |
| [OSDK TypeScript](../osdk-typescript-2026-09/README.md) | typed Ontology client与业务读写契约 |
| [OSDK React Components](../osdk-react-components-2026-09/README.md) | hooks/provider与可复用UI能力 |
| [AI FDE](../ai-fde-2026-10/README.md) | 研发Agent与运行态AIP的职责区分 |
| [Custom Widgets](../custom-widgets-2026-10/README.md) | 参数/事件协议、adapter、Widget Set构建与Registry交付 |

Custom Widget固定源码引用为 `palantir/osdk-ts@fb8ec172d540ef7819382ff036aa2a692614af75`。旧专题对应发布包和固定源码的结论保持其原有版本边界；本次官方网页中的新增默认选项不能无证据回溯为旧包已有保证。尤其 `refreshHostDataOnAction` 的当前文档默认与单Widget覆盖应按实际版本核验。

其他专题相对链接位于同一仓库 `research/` 下。Custom Widget [PR #4](https://github.com/501981732/palantir-research/pull/4)已由用户于2026-10-01合并，合并提交为 `fb55381b270b766d061036e9fdce8157482cfeed`，也是本专题所用main基线。该专题的相对文件链接在此基线有效；本次不再修改其文件，根索引保留已有条目，只追加Workshop。

## EOS本地源码与方案证据

[EOS对照总览](eos-comparison/README.md)及四份细证据记录相对源路径和本次读取行号。其代码基线为 `main @ ea071209ca3bce25e45bbca87a9f90f959ef59ed`，现行方案还包含读取时未提交的文档。EOS源文件不存于本研究仓库，也没有可供外部读者访问的公开源码URL；这些引用只定位在项目负责人拥有的checkout中。本次确认仅限静态源码和装配，不验证后端、部署或业务运行。

项目负责人已明确授权公开EOS架构说明、具体差异、图及相对源码引用。工作站绝对路径、个人信息、内部服务地址、原始源码整包及原私有工作记录不随对照稿发布。
