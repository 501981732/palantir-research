# 来源清单与证据层级

核验日期：2026-10-01。此目录列专题实际引用的直接 URL；正文与附录保留更细的固定行号。目录不是全文镜像，也不是仅凭 HTTP 200 判定功能有效。

- **产品事实**以当日官方文档为准；历史公告保留日期，不能替代当前功能。
- **实现事实**以 widget npm 3.74.0 的发布 provenance 提交 `fb8ec172d540ef7819382ff036aa2a692614af75` 为主，并逐文件比对实际 source map；CLI/config/UI 各按附录的独立版本与提交锁定，main `e53b94…` 仅作比较。
- **版本事实**来自官方 npm registry / tarball / provenance；本轮匹配摘要与提交，未执行独立签名信任链验证。
- **作者 PR**核对 state、draft、merged_at；未合并项不作为已发布能力。
- **社区/视频**只支持该作者在该版本/时间点的操作观察，不泛化为全部产品保证。
- **本地实测**见 checks.md；mock bridge、JSDOM、官方 no-OSDK 模板均与真实租户验收分开。
- EOS 部分为建议；没有检查 EOS 源码。

媒体原始资源 URL、发布时间/时间点、逐图字节与 hash 见 [assets.md](assets.md)；来源 URL 的公开 HEAD 检查见 [http-checks.json](evidence/http-checks.json)，拒绝与超时保留，不绕过。

## C 具名作者实践

| ID | 来源 / 直接入口 | 支撑位置 | 访问日期 |
| --- | --- | --- | --- |
| C01 | [community.palantir.com/t/how-to-create-a-custom-widget-for-workshop/2182](https://community.palantir.com/t/how-to-create-a-custom-widget-for-workshop/2182) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |

## D 官方产品文档

| ID | 来源 / 直接入口 | 支撑位置 | 访问日期 |
| --- | --- | --- | --- |
| D01 | [ai-fde/modes-and-capabilities](https://www.palantir.com/docs/foundry/ai-fde/modes-and-capabilities) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D02 | [ai-fde/prefill-sessions](https://www.palantir.com/docs/foundry/ai-fde/prefill-sessions) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D03 | [announcements/2025-08](https://www.palantir.com/docs/foundry/announcements/2025-08/) | [README.md](README.md)、[lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D04 | [custom-widgets/auto-sizing](https://www.palantir.com/docs/foundry/custom-widgets/auto-sizing) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| D05 | [custom-widgets/core-concepts](https://www.palantir.com/docs/foundry/custom-widgets/core-concepts) | [build-release.md](build-release.md)、[lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D06 | [custom-widgets/core-concepts](https://www.palantir.com/docs/foundry/custom-widgets/core-concepts/) | [README.md](README.md) | 2026-10-01 |
| D07 | [custom-widgets/create](https://www.palantir.com/docs/foundry/custom-widgets/create) | [build-release.md](build-release.md)、[media-evidence.md](media-evidence.md) | 2026-10-01 |
| D08 | [custom-widgets/create](https://www.palantir.com/docs/foundry/custom-widgets/create/) | [README.md](README.md) | 2026-10-01 |
| D09 | [custom-widgets/dark-theme](https://www.palantir.com/docs/foundry/custom-widgets/dark-theme) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| D10 | [custom-widgets/development](https://www.palantir.com/docs/foundry/custom-widgets/development) | [build-release.md](build-release.md)、[media-evidence.md](media-evidence.md) | 2026-10-01 |
| D11 | [custom-widgets/development](https://www.palantir.com/docs/foundry/custom-widgets/development/) | [README.md](README.md)、[eos-implementation.md](eos-implementation.md) | 2026-10-01 |
| D12 | [custom-widgets/embedding-in-workshop](https://www.palantir.com/docs/foundry/custom-widgets/embedding-in-workshop/) | [README.md](README.md) | 2026-10-01 |
| D13 | [custom-widgets/iframe-attributes](https://www.palantir.com/docs/foundry/custom-widgets/iframe-attributes) | [media-evidence.md](media-evidence.md)、[protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| D14 | [custom-widgets/iframe-attributes](https://www.palantir.com/docs/foundry/custom-widgets/iframe-attributes/) | [README.md](README.md)、[eos-implementation.md](eos-implementation.md) | 2026-10-01 |
| D15 | [custom-widgets/manage-node-version-in-foundry-code-repository](https://www.palantir.com/docs/foundry/custom-widgets/manage-node-version-in-foundry-code-repository) | [build-release.md](build-release.md) | 2026-10-01 |
| D16 | [custom-widgets/marketplace](https://www.palantir.com/docs/foundry/custom-widgets/marketplace) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D17 | [custom-widgets/open-url-in-workshop](https://www.palantir.com/docs/foundry/custom-widgets/open-url-in-workshop) | [protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| D18 | [custom-widgets/overview](https://www.palantir.com/docs/foundry/custom-widgets/overview) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D19 | [custom-widgets/overview](https://www.palantir.com/docs/foundry/custom-widgets/overview/) | [README.md](README.md) | 2026-10-01 |
| D20 | [custom-widgets/parameters-and-events](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events) | [protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| D21 | [custom-widgets/parameters-and-events](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events/) | [README.md](README.md)、[eos-implementation.md](eos-implementation.md) | 2026-10-01 |
| D22 | [custom-widgets/publish](https://www.palantir.com/docs/foundry/custom-widgets/publish) | [build-release.md](build-release.md) | 2026-10-01 |
| D23 | [custom-widgets/publish](https://www.palantir.com/docs/foundry/custom-widgets/publish/) | [README.md](README.md) | 2026-10-01 |
| D24 | [custom-widgets/troubleshooting](https://www.palantir.com/docs/foundry/custom-widgets/troubleshooting) | [protocol-api.md](protocol-api.md) | 2026-10-01 |
| D25 | [custom-widgets/use-osdk](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk) | [protocol-api.md](protocol-api.md) | 2026-10-01 |
| D26 | [custom-widgets/use-osdk](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk/) | [README.md](README.md)、[eos-implementation.md](eos-implementation.md) | 2026-10-01 |
| D27 | [palantir-mcp/available-tools](https://www.palantir.com/docs/foundry/palantir-mcp/available-tools) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D28 | [pilot/build-a-widget](https://www.palantir.com/docs/foundry/pilot/build-a-widget) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D29 | [pilot/build-a-widget](https://www.palantir.com/docs/foundry/pilot/build-a-widget/) | [README.md](README.md) | 2026-10-01 |
| D30 | [pilot/deploy-a-widget](https://www.palantir.com/docs/foundry/pilot/deploy-a-widget) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D31 | [pilot/deploy-a-widget](https://www.palantir.com/docs/foundry/pilot/deploy-a-widget/) | [README.md](README.md) | 2026-10-01 |
| D32 | [superrepo/core-concepts](https://www.palantir.com/docs/foundry/superrepo/core-concepts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| D33 | [workshop/widget-display-optimization](https://www.palantir.com/docs/foundry/workshop/widget-display-optimization/) | [README.md](README.md) | 2026-10-01 |
| D34 | [workshop/widgets-iframe](https://www.palantir.com/docs/foundry/workshop/widgets-iframe) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |

## G 公开源码与工作流

| ID | 来源 / 直接入口 | 支撑位置 | 访问日期 |
| --- | --- | --- | --- |
| G01 | [github.com/palantir/aip-community-registry](https://github.com/palantir/aip-community-registry) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G02 | [OSDK Widget in Foundry/README.md](https://github.com/palantir/aip-community-registry/blob/2545a91fe6026441af71d4accfd36e8dc41ff22f/OSDK%20Widget%20in%20Foundry/README.md) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G03 | [github.com/palantir/aip-community-registry/tree/2545a91fe6026441af71d4accfd36e8dc41ff22f/OSDK Widget in Foundry](https://github.com/palantir/aip-community-registry/tree/2545a91fe6026441af71d4accfd36e8dc41ff22f/OSDK%20Widget%20in%20Foundry) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G04 | [github.com/palantir/osdk-ts/actions/runs/36603145053/attempts/1](https://github.com/palantir/osdk-ts/actions/runs/36603145053/attempts/1) | [build-release.md](build-release.md) | 2026-10-01 |
| G05 | [packages/react-components/README.md](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/README.md) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G06 | [packages/react-components/src/object-table/ObjectTableApi.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G07 | [packages/widget.preview/README.md](https://github.com/palantir/osdk-ts/blob/e1f16d9273eb60122571341fbd2efb6f0cde361d/packages/widget.preview/README.md) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G08 | [packages/widget.preview/src/__tests__/preview.test.tsx](https://github.com/palantir/osdk-ts/blob/e1f16d9273eb60122571341fbd2efb6f0cde361d/packages/widget.preview/src/__tests__/preview.test.tsx) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G09 | [packages/widget.preview/src/useWidgetPreviewState.ts](https://github.com/palantir/osdk-ts/blob/e1f16d9273eb60122571341fbd2efb6f0cde361d/packages/widget.preview/src/useWidgetPreviewState.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G10 | [packages/faux/CHANGELOG.md](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/CHANGELOG.md) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G11 | [packages/faux/src/FauxFoundry/FauxDataStore.test.ts](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/FauxDataStore.test.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G12 | [packages/faux/src/FauxFoundry/FauxDataStore.ts](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/FauxDataStore.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G13 | [packages/faux/src/FauxFoundry/getObjectsFromSet.test.ts](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/getObjectsFromSet.test.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G14 | [packages/faux/src/FauxFoundry/getObjectsFromSet.ts](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/getObjectsFromSet.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G15 | [packages/widget.client-react/src/utils/extendParametersWithObjectSets.ts](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/widget.client-react/src/utils/extendParametersWithObjectSets.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G16 | [packages/widget.client-react/src/utils/transformEmitEventPayload.ts](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/widget.client-react/src/utils/transformEmitEventPayload.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G17 | [packages/cli/src/commands/widgetset/deploy/index.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/commands/widgetset/deploy/index.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G18 | [packages/cli/src/commands/widgetset/deploy/widgetSetDeployCommand.mts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/commands/widgetset/deploy/widgetSetDeployCommand.mts) | [build-release.md](build-release.md) | 2026-10-01 |
| G19 | [packages/cli/src/commands/widgetset/version/index.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/commands/widgetset/version/index.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G20 | [packages/cli/src/net/widget-registry/Release.mts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/net/widget-registry/Release.mts) | [build-release.md](build-release.md) | 2026-10-01 |
| G21 | [packages/cli/src/net/widget-registry/ReleaseLocator.mts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/net/widget-registry/ReleaseLocator.mts) | [build-release.md](build-release.md) | 2026-10-01 |
| G22 | [packages/cli/src/net/widget-registry/deleteRelease.mts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/net/widget-registry/deleteRelease.mts) | [build-release.md](build-release.md) | 2026-10-01 |
| G23 | [packages/cli/src/net/widget-registry/listReleases.mts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/net/widget-registry/listReleases.mts) | [build-release.md](build-release.md) | 2026-10-01 |
| G24 | [packages/cli/src/net/widget-registry/publishRelease.mts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/cli/src/net/widget-registry/publishRelease.mts) | [build-release.md](build-release.md) | 2026-10-01 |
| G25 | [packages/client/src/scenarios/withScenario.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/client/src/scenarios/withScenario.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G26 | [packages/create-widget.template.react.v2/templates/package.json.no-osdk.hbs](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget.template.react.v2/templates/package.json.no-osdk.hbs) | [build-release.md](build-release.md) | 2026-10-01 |
| G27 | [packages/create-widget.template.react.v2/templates/package.json.osdk.hbs](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget.template.react.v2/templates/package.json.osdk.hbs) | [build-release.md](build-release.md) | 2026-10-01 |
| G28 | [packages/create-widget.template.react.v2/templates/src/client.ts.osdk.hbs](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget.template.react.v2/templates/src/client.ts.osdk.hbs) | [build-release.md](build-release.md) | 2026-10-01 |
| G29 | [packages/create-widget.template.react.v2/templates/src/main.tsx.hbs](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget.template.react.v2/templates/src/main.tsx.hbs) | [build-release.md](build-release.md) | 2026-10-01 |
| G30 | [packages/create-widget.template.react.v2/templates/src/useDarkTheme.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget.template.react.v2/templates/src/useDarkTheme.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G31 | [packages/create-widget/src/cli.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget/src/cli.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G32 | [packages/create-widget/src/generate/generateFoundryConfigJson.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget/src/generate/generateFoundryConfigJson.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G33 | [packages/create-widget/src/run.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget/src/run.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G34 | [packages/foundry-config-json/src/autoVersion.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/foundry-config-json/src/autoVersion.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G35 | [packages/foundry-config-json/src/config.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/foundry-config-json/src/config.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G36 | [packages/react/src/index.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/react/src/index.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G37 | [packages/widget.api/src/config.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts) | [protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| G38 | [packages/widget.api/src/messages/hostMessages.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/hostMessages.ts) | [protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| G39 | [packages/widget.api/src/messages/widgetMessages.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/widgetMessages.ts) | [README.md](README.md)、[protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| G40 | [packages/widget.api/src/parameters.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/parameters.ts) | [README.md](README.md)、[protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| G41 | [packages/widget.api/src/permissions.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/permissions.ts) | [protocol-api.md](protocol-api.md) | 2026-10-01 |
| G42 | [packages/widget.api/src/utils/asyncValue.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/utils/asyncValue.ts) | [README.md](README.md)、[protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| G43 | [packages/widget.client-react/src/ErrorBoundary.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/ErrorBoundary.tsx) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G44 | [packages/widget.client-react/src/client.test.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.test.tsx) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G45 | [packages/widget.client-react/src/client.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.tsx) | [README.md](README.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| G46 | [packages/widget.client-react/src/context.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/context.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G47 | [packages/widget.client-react/src/index.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/index.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G48 | [packages/widget.client-react/src/utils/extendParametersWithObjectSets.test.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/extendParametersWithObjectSets.test.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G49 | [packages/widget.client-react/src/utils/extendParametersWithObjectSets.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/extendParametersWithObjectSets.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G50 | [packages/widget.client-react/src/utils/initializeParameters.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/initializeParameters.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G51 | [packages/widget.client-react/src/utils/transformEmitEventPayload.test.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/transformEmitEventPayload.test.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G52 | [packages/widget.client-react/src/utils/transformEmitEventPayload.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/transformEmitEventPayload.ts) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| G53 | [packages/widget.client/src/client.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/client.ts) | [README.md](README.md)、[protocol-api.md](protocol-api.md)、[react-adapter.md](react-adapter.md) | 2026-10-01 |
| G54 | [packages/widget.client/src/host.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/host.ts) | [protocol-api.md](protocol-api.md) | 2026-10-01 |
| G55 | [packages/widget.client/src/tokenProvider.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/tokenProvider.ts) | [protocol-api.md](protocol-api.md) | 2026-10-01 |
| G56 | [packages/widget.vite-plugin/package.json](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/package.json) | [build-release.md](build-release.md) | 2026-10-01 |
| G57 | [packages/widget.vite-plugin/src/build-plugin/FoundryWidgetBuildPlugin.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/build-plugin/FoundryWidgetBuildPlugin.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G58 | [packages/widget.vite-plugin/src/build-plugin/buildWidgetSetManifest.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/build-plugin/buildWidgetSetManifest.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G59 | [packages/widget.vite-plugin/src/build-plugin/extractBuildOutputs.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/build-plugin/extractBuildOutputs.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G60 | [packages/widget.vite-plugin/src/build-plugin/getWidgetBuildOutputs.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/build-plugin/getWidgetBuildOutputs.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G61 | [packages/widget.vite-plugin/src/build-plugin/getWidgetSetInputSpec.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/build-plugin/getWidgetSetInputSpec.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G62 | [packages/widget.vite-plugin/src/build-plugin/validateWidgetSet.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/build-plugin/validateWidgetSet.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G63 | [packages/widget.vite-plugin/src/client/entrypointIframe.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/client/entrypointIframe.tsx) | [build-release.md](build-release.md) | 2026-10-01 |
| G64 | [packages/widget.vite-plugin/src/common/constants.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/common/constants.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G65 | [packages/widget.vite-plugin/src/common/extractWidgetConfig.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/common/extractWidgetConfig.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G66 | [packages/widget.vite-plugin/src/common/validateWidgetConfig.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/common/validateWidgetConfig.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G67 | [packages/widget.vite-plugin/src/common/visitNpmPackages.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/common/visitNpmPackages.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G68 | [packages/widget.vite-plugin/src/dev-plugin/FoundryWidgetDevPlugin.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/dev-plugin/FoundryWidgetDevPlugin.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G69 | [packages/widget.vite-plugin/src/dev-plugin/buildDevModeManifest.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/dev-plugin/buildDevModeManifest.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G70 | [packages/widget.vite-plugin/src/dev-plugin/codeWorkspacesMode.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/dev-plugin/codeWorkspacesMode.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G71 | [packages/widget.vite-plugin/src/dev-plugin/extractInjectedScripts.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/dev-plugin/extractInjectedScripts.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G72 | [packages/widget.vite-plugin/src/dev-plugin/getFoundryToken.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/dev-plugin/getFoundryToken.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G73 | [packages/widget.vite-plugin/src/dev-plugin/network.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/dev-plugin/network.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G74 | [packages/widget.vite-plugin/src/dev-plugin/publishDevModeSettings.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/dev-plugin/publishDevModeSettings.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G75 | [packages/widget.vite-plugin/src/index.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.vite-plugin/src/index.ts) | [build-release.md](build-release.md) | 2026-10-01 |
| G76 | [github.com/palantir/osdk-ts/commit/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c](https://github.com/palantir/osdk-ts/commit/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c) | [build-release.md](build-release.md) | 2026-10-01 |
| G77 | [github.com/palantir/osdk-ts/commit/fb8ec172d540ef7819382ff036aa2a692614af75](https://github.com/palantir/osdk-ts/commit/fb8ec172d540ef7819382ff036aa2a692614af75) | [build-release.md](build-release.md) | 2026-10-01 |
| G78 | [LICENSE.md](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/LICENSE.md) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G79 | [README.md](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/README.md) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G80 | [src/internal/messages.ts](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/internal/messages.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G81 | [src/internal/variableTypeWithDefaultValue.ts](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/internal/variableTypeWithDefaultValue.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G82 | [src/transform-config/transformConfigCallbacks.ts](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/transform-config/transformConfigCallbacks.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G83 | [src/types/configDefinition.ts](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/types/configDefinition.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G84 | [src/useWorkshopContext.ts](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/useWorkshopContext.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| G85 | [src/utils.ts](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/utils.ts) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |

## N npm 发布物与 provenance

| ID | 来源 / 直接入口 | 支撑位置 | 访问日期 |
| --- | --- | --- | --- |
| N01 | [registry.npmjs.org/-/npm/v1/attestations/@osdk/widget.client-react@3.74.0](https://registry.npmjs.org/-/npm/v1/attestations/@osdk%2fwidget.client-react@3.74.0) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| N02 | [registry.npmjs.org/-/npm/v1/attestations/@osdk/widget.vite-plugin@3.74.0](https://registry.npmjs.org/-/npm/v1/attestations/@osdk%2fwidget.vite-plugin@3.74.0) | [build-release.md](build-release.md) | 2026-10-01 |
| N03 | [registry.npmjs.org/@osdk/faux](https://registry.npmjs.org/@osdk%2Ffaux) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| N04 | [registry.npmjs.org/@osdk/widget.client-react](https://registry.npmjs.org/@osdk%2Fwidget.client-react) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| N05 | [registry.npmjs.org/@osdk/workshop-iframe-custom-widget](https://registry.npmjs.org/@osdk%2Fworkshop-iframe-custom-widget) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| N06 | [registry.npmjs.org/@osdk/cli/0.101.0](https://registry.npmjs.org/@osdk%2fcli/0.101.0) | [build-release.md](build-release.md) | 2026-10-01 |
| N07 | [registry.npmjs.org/@osdk/create-widget/3.74.0](https://registry.npmjs.org/@osdk%2fcreate-widget/3.74.0) | [build-release.md](build-release.md) | 2026-10-01 |
| N08 | [registry.npmjs.org/@osdk/foundry-config-json/1.13.0](https://registry.npmjs.org/@osdk%2ffoundry-config-json/1.13.0) | [build-release.md](build-release.md) | 2026-10-01 |
| N09 | [registry.npmjs.org/@osdk/widget.vite-plugin/3.74.0](https://registry.npmjs.org/@osdk%2fwidget.vite-plugin/3.74.0) | [build-release.md](build-release.md) | 2026-10-01 |
| N10 | [registry.npmjs.org/@osdk/widget.client-react/-/widget.client-react-3.74.0.tgz](https://registry.npmjs.org/@osdk/widget.client-react/-/widget.client-react-3.74.0.tgz) | [react-adapter.md](react-adapter.md) | 2026-10-01 |

## P 作者 PR 与评审

| ID | 来源 / 直接入口 | 支撑位置 | 访问日期 |
| --- | --- | --- | --- |
| P01 | [palantir/osdk-ts PR #2033](https://github.com/palantir/osdk-ts/pull/2033) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P02 | [palantir/osdk-ts PR #2214](https://github.com/palantir/osdk-ts/pull/2214) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P03 | [palantir/osdk-ts PR #2216](https://github.com/palantir/osdk-ts/pull/2216) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P04 | [palantir/osdk-ts PR #2218](https://github.com/palantir/osdk-ts/pull/2218) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P05 | [palantir/osdk-ts PR #2294](https://github.com/palantir/osdk-ts/pull/2294) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P06 | [palantir/osdk-ts PR #2474](https://github.com/palantir/osdk-ts/pull/2474) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P07 | [palantir/osdk-ts PR #2538](https://github.com/palantir/osdk-ts/pull/2538) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P08 | [palantir/osdk-ts PR #2545](https://github.com/palantir/osdk-ts/pull/2545) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P09 | [palantir/osdk-ts PR #3023](https://github.com/palantir/osdk-ts/pull/3023) | [react-adapter.md](react-adapter.md) | 2026-10-01 |
| P10 | [palantir/osdk-ts PR #3418](https://github.com/palantir/osdk-ts/pull/3418) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| P11 | [palantir/osdk-ts PR #4070](https://github.com/palantir/osdk-ts/pull/4070) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| P12 | [palantir/osdk-ts PR #4102](https://github.com/palantir/osdk-ts/pull/4102) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| P13 | [palantir/osdk-ts PR #4103](https://github.com/palantir/osdk-ts/pull/4103) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| P14 | [palantir/osdk-ts PR #4104](https://github.com/palantir/osdk-ts/pull/4104) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| P15 | [palantir/osdk-ts PR #4105](https://github.com/palantir/osdk-ts/pull/4105) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |
| P16 | [palantir/osdk-ts PR #4120](https://github.com/palantir/osdk-ts/pull/4120) | [lineage-cases.md](lineage-cases.md) | 2026-10-01 |

## V 公开视频

| ID | 来源 / 直接入口 | 支撑位置 | 访问日期 |
| --- | --- | --- | --- |
| V01 | [www.youtube.com/watch?v=U_EB06sWv-s](https://www.youtube.com/watch?v=U_EB06sWv-s) | [media-evidence.md](media-evidence.md) | 2026-10-01 |
| V02 | [www.youtube.com/watch?v=kD6R1lGTQEo](https://www.youtube.com/watch?v=kD6R1lGTQEo) | [media-evidence.md](media-evidence.md) | 2026-10-01 |

## 可复现来源记录

| 记录 | 内容与边界 |
| --- | --- |
| [protocol-sources.json](evidence/protocol-sources.json) | 发布源固定行号、源文件 hash 和实际 npm 对应关系 |
| [protocol-npm-audit.json](evidence/protocol-npm-audit.json) | API/client 发布时间、tarball hash/SRI、文件清单 |
| [react-release.json](evidence/react-release.json)、[React 来源台账](evidence/react-sources.md) | React adapter 发布与七个 runtime source map 对应 |
| [react-components-release.json](evidence/react-components-release.json) | UI 库 0.61.0 的独立发布与 ObjectTable API 源匹配 |
| [build-package-versions.json](evidence/build-package-versions.json)、[source-map audit](evidence/build-source-map-audit.json) | plugin/create/CLI/config 版本与来源；中间 JS 与原 TS 不作字节等同 |
| [lineage-pr-state.json](evidence/lineage-pr-state.json) | 已合并与 open/draft 的精确状态/时间 |
| [lineage-documentary-sources.json](evidence/lineage-documentary-sources.json) | 当前文档与作者案例的提炼结论 |
| [media-evidence.md](media-evidence.md) | 正常浏览器播放/字幕尝试、真实帧和未取得证据 |
