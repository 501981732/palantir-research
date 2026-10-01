# Carbon 检查与证据边界

核验日2026-10-01。结构检查脚本只验证研究交付物完整性；公开契约由逐项来源与内容审阅支撑，不以文件检查替代租户功能试验。

## 内容与范围

- 覆盖workspace/module/home、固定与按需tabs、输入输出和来源状态、区内/区外发现、组织推广/组默认、权限分离、版本/分发和Insight变化。
- 当前事实、带日期原帖/公告、EOS架构分析与未知分别标记；没有把dynamic module、custom section、外链或Workshop widget等同于任意OSDK原生模块。
- Application access与Carbon导航限制仅控制前端体验；资源、对象与Action权限仍独立。
- 新tab保留来源状态不推导全会话持久化；Carbon ObjectSet filter通道与普通Workshop URL routing分开。
- 本篇未读取EOS内部代码；既有ObjectViews/Workshop机制仅交叉引用。

## 媒体与图表

14幅官方PNG逐图打开视检，原字节保留，来源/日期/尺寸/bytes/hash见[assets](assets.md)与[media manifest](notes/media-manifest.json)，解码及检查见[media checks](notes/media-checks.json)。三幅自绘概念图已实际渲染PNG/SVG并逐图检查，附可编辑DOT源与[图表清单](diagrams/manifest.json)。M05图未出现替换模块控件、M03入口图Promoted apps为0，这些画面限制在图注中保留。

有限官方媒体列表与公开视频检索未取得已观看的Carbon工作台视频/GIF；未生成虚构视频关键帧或将静图当播放证据。媒体制作时间未知时不以检索日期替代；2026-09公告日期也不等于截图制作日期。

## 可重跑检查

```sh
python3 research/carbon-2026-10/checks/validate.py
python3 research/carbon-2026-10/checks/check_links.py
```

[本地结果](checks/results.json)记录链接/heading、围栏、source登记、所有PNG解码与尺寸、SHA/bytes、图表三件套、敏感文本模式与既有八专题索引保留。脚本失败会给非零退出码。模式扫描不能保证发现一切隐私数据。

[公开HTTP记录](checks/links.json)记录64成功、0无效重定向、1普通HTTP不可达。CodeStrap Medium原文已通过公开网页读取，普通HTTP检查返回403；保留限制，不使用其他凭据或登录绕过。HTTP成功不代表视频已观看、租户功能可用、账号身份已认证或官方承诺适用于所有版本。

## 尚未执行的产品验收

未登录Foundry租户、未创建或发布Carbon真实配置、未提交业务Action、未测性能。原生OSDK注册、跨设备恢复、tab淘汰、全来源刷新、原子发布与Insight旧链接兼容仍是公开证据缺口；主文第12节给出逐项验证用例。本篇没有承诺这些未知能力不存在。
