# 检查记录与可重跑边界

研究/验证日：2026-10-01 UTC。所有“通过”均限定下表范围；没有全仓测试、真实 Foundry 权限/Action、性能或无障碍认证。

| 检查 | 已执行结果 | 证据 / 限制 |
|---|---|---|
| npm 发布版本/日期/tag | 官方 registry latest0.61.0；beta旧版；核心2.75.0另批 | [release JSON](npm-release-evidence.json)；tag 为研究日状态 |
| tarball | bytes/SHA256/SHA512 SRI 对应 | [provenance JSON](npm-provenance-evidence.json)；未独立认证完整签名链 |
| Source ↔ npm declarations ↔ ESM exports | 30 JS入口，98runtime/170type对齐；531参数 | [API审计](evidence/api-reference-checks.json)、[inventory](public-export-inventory.json)；AST/type不能替代运行 |
| 固定提交文件/行号 | 组装后链接逐一对本地固定 checkout 检查 | [assembly-checks.json](evidence/assembly-checks.json)；不是每个URL都另发一次HTTP |
| Markdown本地与引用链接、JSON | 组装后检查 | 同上 |
| 官方叙述页HTTP | 两篇引用的16个官方页面均200，未见soft404 | [HTTP记录](evidence/http-checks.json)；不是所有动态Storybook/PR的逐URL复测 |
| 图片 | 16张来源/尺寸/bytes/SHA256逐张核对，视觉检查 | [assets.md](assets.md) / [manifest](assets-manifest.json) |
| table pure helpers | selection objectSet、snapshot10000、function concurrency/error通过 | [记录](evidence/table-artifact-probes.json)、[脚本](probes/table-artifact-probes.mjs) |
| filter pure helpers | Date round-trip为string、scope分支、NO_VALUE零count | [记录](evidence/filter-artifact-probes.json)、[脚本](probes/filter-artifact-probes.mjs)；复现边界非宣称无缺陷 |
| form pure helpers | 6条实际npm断言通过 | [脚本](probes/react19/pure-utils.mjs) / [结果](probes/react19/checks-pure-utils.json) |
| React19 BaseForm | 4/4行为断言，fetch throwing spy未调用 | [harness](probes/react19/README.md)、[summary](probes/react19/checks-summary.json) |
| client-only Vite build | exit0，BaseUI directive/chunk-size warnings | 同上；无SSR/RSC结论，不把harness总chunk当tree-shaken包体积 |
| Storybook真实UI |列菜单、配置、Engineering联动；空表单required；PDF侧栏；dark主题 | 官方动态部署 + mock/fixtures；不是npm0.61全量独立部署/真实Foundry |
| 真实浏览器本地UI | requiredFalse拒绝，optionalFalse提交本地JSON | 本地mock；图15仅必填错误局部，无Action |
| 上游tests | 源码阅读 | 未执行；具体路径见专题和sources |

API审计的 hashes 记录的是原始审阅输入；组装时拆分 viewer 表和纠正说明文字，最终内容以当前文件及 assembly 校验为准。参数名称/类型未因编辑而新增 API。报告主稿经独立只读审阅，对精确 prop 名、Base/Wrapper 差异和默认行为做纠偏。

## 有限 React 19 结果

Node22.17.0 / pnpm11.24.0；React/React DOM19.3.0，OSDK api/client/react2.75.0，components0.61.0，RHF7.71.2、BaseUI1.3.0，Vitest5.0.3 + HappyDOM20.14.5。普通文本正/负、required booleanFalse负向/True正向、optionalFalse正向。4项测试包含边界复现，不意味着全部校验正确。

requiredFalse与RHF规则链有关，不能归因React19；未在上游修复。全组件React19、对象字段/provider、backend validation/权限、PDF worker/SSR、portal/CSS宿主组合和生产Action均未验证。

## 重跑

先按 [React19 harness](probes/react19/README.md) 安装固定锁版本，然后在其目录运行 test / probe:pure / build。table/filter脚本接受实际npm包目录作为第一个参数（默认本topic的已安装harness node_modules包）；它们访问内部实现仅为研究验证，不是建议消费者deep import。无需任何Foundry凭据，不应对生产Action重跑。

## 发布复核

版本与产品阶段固定到本研究日，后续升级需要新一轮兼容验证。
