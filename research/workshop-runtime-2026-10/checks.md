# Workshop 运行研究：验证记录与证据边界

核验日期：2026-10-01。本文件记录确实完成的资料、文件和图像检查；不把静态研究写成产品验收。

## 已完成

| 检查 | 本次结果 | 可证明的范围 |
|---|---|---|
| 第一方公开资料与固定源码追溯 | 三篇公开资料正文追溯52个官方页面或固定公开源码文件；声明就近引用，两篇附录提供声明与节标题矩阵 | 产品公开契约与所引客户端行为；不证明闭源实现或租户部署状态 |
| 端到端主线 | 已连接手写/Pilot React、OSDK hooks/components、Widget Set、Registry、变量事件、Ontology读写、页面配置与版本 | 研究职责完整；Palantir图是综合概念模型 |
| 独立公开资料审阅 | 独立审阅者读取正文及官方来源，检查过度推论、遗漏、图中前提与发布依赖 | 公开事实和图示的语义复核 |
| 公开资料修订 | Action重试覆盖执行/提交期间的瞬时失败；Logic写入须已发布并经Action调用，但并非全部Action使用Logic；auto-refresh在嵌入模块上下文不生效；补宿主刷新桥接及ObjectSet参数范围 | 与对应官方文档一致，不扩大完整缓存/事务保证 |
| EOS静态源码核对 | 分支main，HEAD `ea071209ca3bce25e45bbca87a9f90f959ef59ed`；当前工作区已有27个tracked文档修改/删除及5个untracked顶层条目 | 明确固定提交、未提交文档与当前源码的区别；已实现只表示消费者/装配点存在 |
| EOS公开拷贝与独立复核 | 原5份只读报告按用户明确授权转换；移除绝对工作站路径、内部地址和无关内容；保留源码相对路径、实现差异、架构图及静态风险 | 用户已批准的公开架构/对照范围；未包含原始源码包 |
| EOS引用定位 | 重新只读核验399个唯一文件引用及5个目录/通配引用；文件、目录及全部引用行号有效 | 当前工作区证据可定位；不是行为或后端验收 |
| 图12父侧复核修订 | 只读复核Action成功finalize、committed回调、手动registry监听及queued结果：onSubmit仅挂成功Action路径并等待回调返回；手动刷新不派发它；离线成功边注明SUCCESS条件 | 前端源码的顺序/调用边界；等待committed回调不等于所有新查询与下游组件就绪 |
| Markdown与本地链接 | 11个专题Markdown文件围栏闭合，正文图像和本地链接目标存在；源码引用保持相对路径代码文本 | 文档结构与所选研究仓库base内的文件目标 |
| Mermaid实际解析与导出 | 全部15个源图使用已有Mermaid 10.9.1离线解析，导出30个PNG/SVG；ELK虚线按解析出的edge.stroke恢复并逐边核对 | 图可实际渲染，源文字/拓扑与导出连线一致；不证明产品机制执行通过 |
| 图像视觉检查 | 所有PNG以原尺寸实际查看；EOS图另由两位审阅者分组复核；中文、箭头、分组标题、标签和证据边界页脚完整可读，无阻塞裁切/遮挡 | 本次导出尺寸的视觉可读性；没有登录GitHub做平台界面预览 |
| 图像独立性与素材校验 | SVG无脚本、foreignObject或外链资源；离线重开结果与对应PNG校验一致；30个图像大小、尺寸和SHA-256记录在assets.md | 导出图可独立保存和打开，字节可复核 |
| 发布文件辅助扫描 | 对本专题白名单逐文件扫描，未检出绝对工作站路径、个人邮箱、凭据形状或内部服务地址；EOS符号及相对证据属于用户授权范围 | 辅助扫描及人工复核；不将删除名称视为公开授权依据 |
| 既有专题与发布依赖 | Custom Widget PR4已由用户合并，merge/main基线为 `fb55381b270b766d061036e9fdce8157482cfeed`；四个专题文件及其他跨专题相对链接在此main存在 | 引用可追溯；本次不修改Custom Widget文件，索引保留既有条目 |

修订依据：[Action重试](https://www.palantir.com/docs/foundry/action-types/consistency-guarantees/)、[Logic写入前提](https://www.palantir.com/docs/foundry/logic/core-concepts/)、[Auto-refresh嵌入限制](https://www.palantir.com/docs/foundry/workshop/auto-refresh/)、[Widget宿主刷新选项](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk/#refresh-host-data-on-action)。所有素材的正文归属、日期和校验值见 [assets](assets.md)，来源索引见 [sources](sources.md)。

## 未执行与未证实

没有登录Foundry租户、发起Ontology业务查询/Action、创建Registry release、运行Widget Set构建或执行Workshop页面。没有性能测量或租户侧网络、缓存、错误恢复实验。引用既有专题的构建和协议结论时保留其原日期与版本，不重复声称已实测。

EOS项目始终只读，没有改代码/配置、安装依赖、运行产品脚本、构建或测试，也没有对该项目提交或推送。没有读取eos-core后端，因此服务器CAS、事务、幂等、授权、部署状态及实际故障恢复仍未验证。D2/D4/D5/D9为静态风险，未称为已复现故障。AI评审方案仍待评审，ADR0004仍proposed，候选生成及禁写预览为拟新增能力。

公开资料没有给出完整Workshop canonical schema、宿主cache键/TTL、全链派生完成屏障、autosave/并发写协议的直接证据。未知项已列明；不能从公开文档未见某机制推出产品没有该机制。

图像检查使用现有本机Mermaid、Node、Playwright和Chrome，浏览器网络已阻断，未安装新依赖。浏览器用于离线图像解析与视觉检查，没有执行EOS或Palantir业务页面。图像通过与产品运行验收严格分开。

## 发布范围与审阅状态

用户已明确批准在公开`501981732/palantir-research`保存EOS架构、具体差异、图和相对源码引用。公开专题限定为11份Markdown及30个图像，根索引只增加Workshop一行。原始源码、未处理的私有报告、读取输出、上传映射、辅助脚本及本机路径不进入仓库。

Workshop研究作为独立draft PR对main审阅，main已包含用户合并的Custom Widget PR4。根索引保留已有专题，不合并其他任务内容。本文交付是研究审阅稿；具体提交和draft PR状态以仓库及PR记录为准，不表示已合并或通过产品验收。
