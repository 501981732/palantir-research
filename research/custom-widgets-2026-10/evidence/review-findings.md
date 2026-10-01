# 独立质量审查

审查日期：2026-10-01 UTC。审查目录为 `research/custom-widgets-2026-10/`；装配基线为 `9a3bf0898d1505cc34fb5823d22042025b7b7a1f`。范围包括正文、协议、React、构建发布、沿革、EOS 建议、媒体、来源索引及 [只读装配检查](../probes/check-assembly.py)。

**技术复核结论：所核对的公开源码与文字主张未发现未修复的重大技术误述。** 插件局部验证、React 生命周期、异步输出和 UI 库 Beta 均按各自证据范围表述。此结论不代表真实 Workshop、发布或 EOS 验收通过。

## Standards：仓库规范与交付组织

规范依据为仓库 [AGENTS.md](../../../AGENTS.md)：来源优先一手；事实与分析分离；来源和媒体逐项登记；标明 Beta/限制；提交前检查链接及图片摘要。

| 检查 | 观察与结论 |
| --- | --- |
| 事实与建议分离 | 正文开头及 EOS 附录明确未检查 EOS 源码；建议字段、状态机、M0/M1/M2 与 Palantir 事实分开，没有把建议写成现有实现 |
| 固定版本 | 发布包按 3.74.0 / `fb8ec172…` 锚定，CLI 另锁 0.101.0；main `e53b94…` 用于比较/沿革，draft head 另列；未将未合并 PR 或非空测试 merge SHA 当成正式发布 |
| Beta 标注 | React 附录开头已补 `@osdk/react-components@0.61.0` 的 Beta 状态，并直接链接发布源码 README |
| 媒体归属 | 14 PNG + 1 作者录像 JPG 有出处、日期、尺寸、bytes/hash 和逐图观察；静态图与本轮租户操作分开；录像是加载界面的有限帧，未补写为完整交互 |
| 获取失败 | 媒体附录明确短录屏和可用字幕没有取得，并保留普通访问/编码工具失败记录；未用 stale frame、广告、mock 或静态图转视频替代 |
| 原专题保留 | 对固定基线，既有文件的改动仅限根 README 和 research README，另新增本专题；原五专题 122 个 tracked 文件没有改动；两个索引仍列原五专题 |
| 依赖目录 | `probes/react-adapter/.gitignore` 忽略 node_modules，未发现待提交依赖目录 |

组装初检执行命令：

```sh
python3 research/custom-widgets-2026-10/probes/check-assembly.py 9a3bf0898d1505cc34fb5823d22042025b7b7a1f
```

最终装配的 JSON 解析、媒体 bytes/SHA-256 与相对链接结果见 [review-assembly.json](review-assembly.json)。该脚本只检查装配与 Git 保留，不检查产品行为；heading 检查使用常见 GitHub slug 规则与显式 HTML anchor，不能代替渲染器。

## Spec：技术准确性与任务要求

| 要求面 | 独立审查结论与证据边界 |
| --- | --- |
| 宿主协议 | 正确描述公开 client 消费 `window.__PALANTIR_WIDGET_API__`，而非自行实现全部 parent postMessage；bridge 的 CustomEvent `detail` 与 hostEventTarget 的 payload 有区分。没有据客户端缺少代码就断言闭源宿主缺少 origin 校验 |
| 参数与事件 | 完整区分 schema、AsyncValue/wire 与 OSDK/React 值；experimental mapTileLayer、额外 allow-modals 分列；浅 type guard、JS 逃逸与 TS 负例没有扩大为宿主漏洞 |
| ObjectSet / scenario | ObjectSet RID 水合的惰性和身份缓存与记录查询分开；输出临时 RID 序列化与受控 selection 恢复分开；scenario 透传不等于自动改全部查询上下文 |
| 双向状态 | emit 不改本地 context，需要宿主回传；刻意 partial payload 实验明确不符合完整 typed map、且无真实宿主增量消息证据，未标为 Workshop 产品缺陷 |
| React 竞态与生命周期 | latest-call 仅限同 ID 的重叠异步转换；同步交错/卸载不统一作废。effect 的 bridge/observer/HMR 清理与遗留内部匿名 listener 分开；StrictMode 结论只指本地开发态；动态 config/client 闭包风险不是已证实宿主升级行为 |
| 故障恢复 | child ErrorBoundary、wrapper render、CustomEvent handler 与 Promise rejection 不混为一类；没有把 reload 请求、HMR 修复或 iframe 隔离说成自动恢复/性能隔离保证 |
| 身份和权限 | 配置 SDK、开启 Ontology APIs、查看者权限、API allowlist、placeholder token、CSP/浏览器能力分层；存储、workers、隐藏卸载、subscriptions 与当前官方文档一致 |
| 构建发布 | manifest 版本、业务版本、library/protocol 版本分开；源码求值不是 AST 提取；official no-OSDK build、placeholder RID、ZIP 检查均非 Foundry CI/Registry 发布成功 |
| 沿革与 AI | 旧 iframe 的 postMessage、认证和 temporaryObjectSetRid 与 Registry 路线分开；已合并 #3418、未合并 preview/SuperRepo 草案及工具目录可见范围明确；没有虚构私有生成器调用图 |
| EOS 可实施建议 | 覆盖 Registry、Adapter、runtime、Compiler/IR/DSL、造物/生成交付、契约升级与回退，明确前置源码审计问题；没有以 Palantir 客户端代答 EOS 已具备什么 |

### 已修复的准确性问题

**R1 / P2：不要将 Vite 插件说成完整权限与事件验证器。** 不应概括为“校验入口、参数、事件、权限和对象类型约束”。发布 `validateWidgetConfig` 仅检查 widget ID/name/description、parameter ID/ObjectSet metadata、只读地图参数更新等局部约束；`buildWidgetManifestConfig` 将 `permissions` 原样写入。该概括与构建附录自己的“局部校验”边界不一致。正文准确表述为“plugin 检查入口、标识符、对象类型 RID 和只读参数等局部约束；permissions 原样写入 manifest，类型与宿主授权另行约束”。直接依据：[验证器](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/common/validateWidgetConfig.ts#L28)、[manifest 构造](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/build-plugin/buildWidgetSetManifest.ts#L75)。该表述与固定发布 JS 一致。

React 附录另明确：入站 unknown key/helper 抛错与出站 primitive/objectSet 分支验证范围；异步调用 ID 不代表全局 last-wins 或卸载取消；Beta 依赖状态。这些限定不构成额外的运行验证。

## 审查方法与尚未取得的证据

复核方法包括阅读官方 use-osdk/development/iframe-attributes 正文，发布 React 源文件、ObjectSet 输入输出 helper、ErrorBoundary，以及实际发布插件的验证/manifest JS；逐图打开复核 Registry、Workshop dev mode、iframe 能力和作者录像帧的主张。媒体采集未在本项复核中重复执行。来源、provenance、source-map、PR 和 probe 的既有记录被核对其范围与结论；**本项复核未重新运行上游测试集或 13/11/14 客户端、React、插件探针**；核对已保存结果不等于独立复算通过。

本报告仍无真实租户的 transport/origin、查看者授权、事件时序/原子性、完整 schema 控件、故障恢复或升级/回退证据；无 EOS 当前源码；无可交付短录屏/字幕。它们在专题中被正确标为未知或缺口，属于来源边界，不应因本次文字审查关闭。
