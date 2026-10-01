# OSDK React19 本地 mock 验证

这是研究用 throwaway harness，界面运行实际 npm `@osdk/react-components@0.61.0` 的公开 `BaseForm`，只使用普通 TEXT_INPUT/RADIO_BUTTONS。没有 OsdkProvider、生产 Ontology、后端 Action、对象选择或外部资源创建。两个 Submit 仅记录本地 React state。页面明确标为 LOCAL MOCK。

固定直接依赖：`@osdk/api/client/react@2.75.0`、React/React DOM `19.3.0`、React Hook Form `7.71.2`（同发布源码 lock 版本）、classnames `2.5.1`。相关实际传递依赖 Base UI 为 `1.3.0`。完整重复安装版本见 pnpm-lock.yaml；Node `22.17.0`、pnpm `11.24.0`、Vite `8.3.1`、Vitest `5.0.3`、Happy DOM `20.14.5`、Testing Library React `16.3.3`。

从本目录运行：

```sh
pnpm install --ignore-scripts --frozen-lockfile --registry https://registry.npmjs.org
pnpm dev
pnpm test
pnpm probe:pure
pnpm build
```

演示地址 `http://127.0.0.1:5197/`。只有本机监听；不访问 Foundry。验证安装使用隔离 pnpm store。该目录自己的 pnpm-workspace.yaml 关闭“运行 script 前自动 reinstall”，避免执行验证时改变 lock/依赖或误用用户默认镜像；认证/全局配置未修改。

2026-10-01 实测结果：

- 普通必填文本可提交原值；空必填文本显示错误且不提交。
- `isRequired:true` 的布尔 RADIO，已选 `False` 仍显示 `This field is required`、不提交。改为 `True` 后错误清除且可提交。
- `isRequired:false` 的布尔 `False` 可以保持原值提交。
- 上述 4 项测试全部通过；测试将全局 fetch 设为抛错的 spy，并每项断言未被调用。这些是确认行为的断言，其中包括确认缺陷边界，不能将“测试通过”写成组件所有校验无缺陷。
- 6 条实际 npm 内部纯函数断言通过；脚本是 `pure-utils.mjs`。该脚本为研究检查实现文件，并不把内部路径当公共消费 API。
- Vite production build 退出码 0；有 Base UI `use client` directive 和 chunk size 警告。普通 client mock build 不能证明 SSR/RSC 兼容。

`checks-summary.json` 是可发布的简洁结果；`checks-pure-utils.json` 为纯函数运行结果。原始 `checks-vitest.json`、`checks-package-versions.json`、build/dev日志留在本地用于追溯。研究者真实浏览器独立复现 required False 被拒绝、optional False 产生 `{enabled:false}` 本地JSON，已采集必填错误局部截图。截图应标“本地 mock 演示，真实 npm 组件”，不能标 Foundry 集成实测。

此现象也可在 RHF 7.71.2 的 createFormControl 单独复现，不能归因于 React19；应用可评估为布尔字段使用存在性自定义校验，但本研究未修复上游。覆盖仅限 plain-field BaseForm，不代表全组件 React19 回归、真实 Action/权限测试或所有浏览器兼容。

此目录仅保留可重跑最小代码、lock 与简洁结果，未包含 node_modules、dist 或原始本机日志。
