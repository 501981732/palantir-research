# 渲染与视觉 QA

日期：2026-10-01。三图均为原创概念图，无上游原图 URL；支撑来源与归纳边界见 [README.md](README.md)。

## 执行与结果

- `python3 render.py` 实际调用 Graphviz，生成三份 PNG 和三份 SVG；所有调用退出状态为 0，未产生渲染警告。
- Pillow 对每份 PNG 执行 `Image.verify()`，随后读取实际尺寸与色彩模式；全部通过。
- XML 解析三份 SVG，检查非空文本、中文标题与“公开资料概念归纳，非官方内部实现”声明；全部通过。
- 用 `view_image` 逐图查看实际 PNG；完成初版和修订版检查。原始 PNG 未经图片编辑或后期裁切。
- SHA-256 与字节数对本目录实际文件计算；完整源文件、SVG、PNG 清单见 [manifest.json](manifest.json)。

## 逐图视觉检查

| 文件 | 尺寸 | 结果与调整 |
| --- | --- | --- |
| `01-evolve-conceptual-architecture.png` | 2737 × 1585 | 中文正常、节点文字完整，箭头方向清楚。将第一版的阶梯式宽布局压缩为三层；候选修改与验证的跨分组箭头终止于 Foundry 分组边界，避免穿过分组标题。人工审阅到发布使用虚线。未见文字裁切、重叠或缺字。 |
| `02-evolution-validation-flow.png` | 1900 × 2464 | 主流程从上至下；迭代与 Resume 回边使用虚线，旁侧限制框清楚标为官方示例。底部说明搜索/停止规则未知。未见文字裁切、重叠或缺字。 |
| `03-graphs-and-state-boundaries.png` | 2165 × 2027 | 上半部分两种图分组清晰；下半部分独立表示定义变更、运行副作用与交付状态。未绘制固定 agent DAG。中文与英文术语可读，未见文字裁切、重叠或缺字。 |

## PNG 资产台账

| 文件 | 绘制日期 | 来源 | bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `01-evolve-conceptual-architecture.png` | 2026-10-01 | 原创；Evolve overview；治理边界补充见 README | 439394 | `69ccaa1b3e6aed68047920eb5a5cf777fbdcc355b72d01138c326da28a6aab29` |
| `02-evolution-validation-flow.png` | 2026-10-01 | 原创；Evolve overview 的示例流程 | 417033 | `bc645a40ff72f32fa0381bbcd049225ba4d7fba2ec9aeab27123e400f3959b92` |
| `03-graphs-and-state-boundaries.png` | 2026-10-01 | 原创；Evolve overview；AI FDE security；Global Branching core concepts | 420783 | `f1c62da4db88f3f382f93a1c8a6dca4921e38deca537436ab48e558a2d3f6d21` |

## 内容边界

三图不证明 Evolve 自有服务架构、统一变更范围、固定 agent DAG、beam/evolution 算法、严格代码预算、实际断点恢复、完整数据隔离或自动发布能力。图中示例数字不能提升为默认值或成功保证。运行副作用和交付部分是平台边界的概念归纳，不能提升为 Evolve 新增机制。
