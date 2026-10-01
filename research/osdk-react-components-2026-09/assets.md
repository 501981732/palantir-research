# 图片资产与逐图说明

获取日：2026-10-01 UTC。所有本地图像为真实来源，不含 AI 合成图。官方公告原图、Storybook 实拍、本地 mock 分别标记；不含生产 Ontology 数据。Storybook 是当日动态部署，不能把部署分支的 ref 当成 npm 0.61.0 build source。UI 行为另由发布源码核验。

图片用于解释组件研究，未声明图片/商标随源码 Apache-2.0 一并许可。公告/产品界面归 Palantir，mock fixture 归其来源作者；PDF截图含论文 *Trace-based Just-in-Time Type Specialization for Dynamic Languages*（Andreas Gal 等，PLDI 2009）首面局部，归原作者/出版方，不镜像论文。官方 [fixture](https://palantir.github.io/osdk-ts/storybook/compressed.tracemonkey-pldi-09.pdf) 和 [使用位置](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/DocumentViewer/DocumentViewer.stories.tsx#L26-L95) 可复核。代码许可不替代这些素材归属。

Storybook 数据与媒体来自 faux/MSW/公开 fixture：[preview](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/.storybook/preview.tsx)、[Action story](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/ActionForm/ActionForm.stories.tsx#L21-L57)。本地验证页代码见 [harness](probes/react19/README.md)，页面明确 Local Mock，仅本地 React state，无外部提交。

## assets/00-announcement.png

![官方公告原图](assets/00-announcement.png)

官方公布的组合界面形态；能力以源码核验为准。

- 类型：官方公告原图
- 原始 URL / 采集入口：[来源](https://www.palantir.com/docs/resources/foundry/announcements/release-notes/2026-09-29-161936-developer-console-screenshot-2026-09-22-at-13-50-04-pn.png)
- 来源页面：[页面](https://www.palantir.com/docs/foundry/announcements/2026-09)
- 获取日期：2026-10-01 UTC
- 尺寸：2550 × 1314；大小：548,896 bytes
- SHA-256：`df928442f771e0e3bb0aab41548927978d34db345d8876105a00a6909bd2fd03`

## assets/01-object-table.jpg

![官方 Storybook 实拍（mock/fixture）](assets/01-object-table.jpg)

默认对象表格、mock 属性与行；实际 React UI，非生产 Ontology。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-objecttable--default)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-objecttable--default)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：146,849 bytes
- SHA-256：`785e45f7c9eaa1dd5701c126f46139c73da5ff4a0ae23dd00865798ee7b91b6b`

## assets/02-column-menu.jpg

![官方 Storybook 实拍（mock/fixture）](assets/02-column-menu.jpg)

点击姓名列菜单，显示排序、pin、多列排序、配置入口。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-objecttable--default)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-objecttable--default)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：119,682 bytes
- SHA-256：`9bfb48a895c736dfc25f6f714d03832a79c3f74bb907d8abc386a39684f3b5f1`

## assets/03-column-config.jpg

![官方 Storybook 实拍（mock/fixture）](assets/03-column-config.jpg)

打开列配置对话框，显示可见列和可添加属性。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-objecttable--default)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-objecttable--default)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：86,134 bytes
- SHA-256：`c8609f37cee4610bf2da73d794b726024ff9c082101f826ce04e39710c6a0f9e`

## assets/04-filter-table.jpg

![官方 Storybook 实拍（mock/fixture）](assets/04-filter-table.jpg)

选择之前，筛选容器与对象表格联动示例。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--combined-with-object-table)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--combined-with-object-table)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：105,561 bytes
- SHA-256：`9a2add7196bac0e42fe487e4244e74f9f8a69eac23b6bfc8c8b6621b14257556`

## assets/05-filter-engineering.jpg

![官方 Storybook 实拍（mock/fixture）](assets/05-filter-engineering.jpg)

实际点击 Engineering 后选中与表格变化；mock 后端。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--combined-with-object-table)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--combined-with-object-table)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：80,501 bytes
- SHA-256：`550ef4041741da65f30b0bd6105b2453e808d5e4bc2bf50c154fd687a130cfc9`

## assets/06-filter-types.jpg

![官方 Storybook 实拍（mock/fixture）](assets/06-filter-types.jpg)

不同筛选输入的可见部分；不是每个内部 input 都公开。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--with-all-filter-types)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--with-all-filter-types)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：60,109 bytes
- SHA-256：`5760e206bf116f034c2ad5404c92ad56abdaea2141b524a9442d47b7ec2867ce`

## assets/07-action-form.jpg

![官方 Storybook 实拍（mock/fixture）](assets/07-action-form.jpg)

mock metadata 自动表单，未执行有效 Action。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-actionform--default)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-actionform--default)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：56,145 bytes
- SHA-256：`6fa797ab9376f875752ec8973b066c4ca577508799d67d2edcdcc469ba6b1fdd`

## assets/08-form-validation.jpg

![官方 Storybook 实拍（mock/fixture）](assets/08-form-validation.jpg)

空姓名提交产生 required / 1 issue；只有本地校验。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-actionform--default)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-actionform--default)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：58,452 bytes
- SHA-256：`61a9e3bc0fa3e8f0168e3287a95d1e853933a1d326d0595d6d204ab5d5f58b04`

## assets/09-pdf-viewer.jpg

![官方 Storybook 实拍（mock/fixture）](assets/09-pdf-viewer.jpg)

PDF 工具栏与缩略图 sidebar；第三方论文公开 fixture 的局部。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-documentviewer--pdf)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-documentviewer--pdf)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：129,658 bytes
- SHA-256：`d6c32261169c88c88f3788bc60d865d684af4d0fca85d73640f88faa0f7fa35e`

## assets/10-spreadsheet.jpg

![官方 Storybook 实拍（mock/fixture）](assets/10-spreadsheet.jpg)

mock XLSX 的只读 sheet/table，非电子表格编辑器。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-documentviewer--spreadsheet)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-documentviewer--spreadsheet)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：48,042 bytes
- SHA-256：`6cb7361724d3f193dbebb5faf15cd48566c784470796eb166242d0fb6a1aea0e`

## assets/11-email.jpg

![官方 Storybook 实拍（mock/fixture）](assets/11-email.jpg)

公开 mock RFC822 邮件的 header/body，非真实邮箱。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-documentviewer--email)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-documentviewer--email)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：48,389 bytes
- SHA-256：`069f912f54367c8caeac087665659745acb5154516894568a22b592b8a7f397b`

## assets/12-workshop-dark.jpg

![官方 Storybook 实拍（mock/fixture）](assets/12-workshop-dark.jpg)

切换 Workshop Dark；视觉对齐不能证明代码同源。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--combined-with-object-table)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-filterlist--combined-with-object-table)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：102,176 bytes
- SHA-256：`f8694f5596a5b9c58fcbcf4074742e8681b97ad68725807782767524848dbabe`

## assets/13-aip-chat.jpg

![官方 Storybook 实拍（mock/fixture）](assets/13-aip-chat.jpg)

BaseAipAgentChat 模拟会话，未发模型请求/运行 Agent。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-aipagentchat--with-conversation)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-aipagentchat--with-conversation)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：70,567 bytes
- SHA-256：`9c734a46bf53f0ae7b80069dc060a394b54ebbb8ac400d80caf42ca18aa35959`

## assets/14-cbac-picker.jpg

![官方 Storybook 实拍（mock/fixture）](assets/14-cbac-picker.jpg)

BaseCbacPicker 公开测试分类/标记，非真实受限数据或授权结果。

- 类型：官方 Storybook 实拍（mock/fixture）
- 原始 URL / 采集入口：[来源](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-cbacpicker--with-banner)
- 来源页面：[页面](https://palantir.github.io/osdk-ts/storybook/?path=/story/components-cbacpicker--with-banner)
- 获取日期：2026-10-01 UTC
- 尺寸：1280 × 720；大小：51,050 bytes
- SHA-256：`c0567a02ad9e15b3864042067114312a7082d1ca1eb07e03ebbeaceb88f98800`

## assets/15-react19-validation.jpg

![本地 mock 演示（实际 npm 组件）](assets/15-react19-validation.jpg)

BaseForm 必填 False 拒绝状态的局部；同页 optional False 正例由断言/DOM复核，无 Foundry/Action。

- 类型：本地 mock 演示（实际 npm 组件）
- 原始 URL / 采集入口：[来源](http://127.0.0.1:5197/)
- 来源页面：[页面](http://127.0.0.1:5197/)
- 获取日期：2026-10-01 UTC
- 尺寸：418 × 235；大小：8,153 bytes
- SHA-256：`2967d29c781442be3dd09ba855476902cecfd7486e626488e27123921653d407`

