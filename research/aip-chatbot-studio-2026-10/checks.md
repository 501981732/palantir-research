# 检查记录与验证边界

核验窗口：2026-10-01–02 UTC。本文是公开资料研究与交付物核验，不是 Foundry 租户、EOS运行、生产写入或性能测试。

## 内容与证据

- 主文覆盖构建/模型/prompt、知识与检索、应用上下文/会话、Ontology/Actions/Functions/Logic、Workshop/Commands、API/OSDK自建React、身份/确认/日志/Evals、版本/Marketplace、其它AIP产品边界与EOS建议。
- 技术主张由官方文档或固定源码支撑；公开博客、原始PR、伙伴视频、社区社媒保留作者关系、日期、解决状态与当前版本限制。没有复制全文或把旧社区限制写成当前承诺。
- EOS仅引用已公开[历史静态对照](../workshop-runtime-2026-10/eos-comparison/README.md)，没有读取新的内部源码或公司资料；新增设计与验收都标建议，未报告当前差距已复现或产品已实现。

## 源码、API与示例

接入附录固定Platform SDK与OSDK提交及package版本；逐项核对路由、方法、类型与源码行号。普通SDK chat组件/LMS、Function streaming与Chatbot Sessions分开，不机械更名现存API字段。具体行号和相对链接核查记录见[集成来源](notes/integration-sources.json)。示意代码未编译、未连接租户，不称端到端验证通过。

## 媒体与图件

32个媒体文件：30张官方原图、2张伙伴视频局部截图，共9,376,784 bytes。逐图视检与重新解码/尺寸/bytes/SHA-256核验见[媒体台账](notes/media-manifest.json)与[观察](media-evidence.md)。制作日期未知明确unknown，截图示例版本/模型名单不当当前规格。概览两图案例不同、工具alt与画面不同、Action待点击/未写入的限制均保留。

四幅关系/时序图均实际渲染PNG/SVG并附DOT源，逐图视检；概念图不是伪造产品UI、内部服务拓扑或租户trace。[图件manifest](diagrams/manifest.json)记录渲染时间、尺寸、bytes/hash。D3明确Command仅在其实现调用业务API时进入该路径。

视频只核验原页和指定局部画面：伙伴教程10:48连接错误、11:13 OAuth申请；11:31播放器报错，字幕不可用，未核验后续成功或性能。官方DevCon2等仅元数据/发布者关系，不声称看过完整演示。session-logging、Marketplace页面没有可取产品图，不以合成UI补足。

## 可重跑的交付物检查

```sh
python3 research/aip-chatbot-studio-2026-10/checks/build_registry.py
python3 research/aip-chatbot-studio-2026-10/checks/check_links.py
python3 research/aip-chatbot-studio-2026-10/checks/validate.py
```

本轮最终结构核验237/237通过；公开HTTP136条为128可访问、0失效重定向、8不可达/受限。结果：[结构核验](checks/results.json)、[公开HTTP](checks/links.json)。脚本验证文件/本地链接/heading/围栏、全部引文登记、媒体清单与hash/解码、可编辑渲染图件、已有索引内容保留、旧专题没有修改，以及敏感路径/凭据模式。模式扫描不是全部隐私保证；HTTP200也不代表事实正确、片段支持命题、视频已观看或租户能力可用。链接脚本默认复用本轮刚核验记录，仅请求新增来源；`--refresh`重做全部公开HTTP。

普通公开HTTP对部分Medium/官方博客返回403，部分YouTube/Substack网络不可达；相应来源的网页正文/正常浏览器观察与限制分开保留，没有改凭据、绕付费/登录/DRM或权限。所有实际限制以links.json逐条结果为准，不能说全部外链200。媒体原URL曾有临时503，各在同一URL重试一次后200；错误记录在manifest。

## 仓库完整性与运行边界

仓库公开 main 基线为 `e64916da0d781652d5a337ce77f05a579ff49ef8`。新增本主题，两份索引追加条目，保留所有旧内容；既有专题未修改。结构核验检查索引旧行保留和主题变更范围。

基线未发现 `.github/workflows`；本稿没有 CI 执行结果。交付物脚本通过不等于 CI、真实租户、业务写入或 EOS 运行验收通过。
