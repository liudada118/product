# 机器人触觉产品常用 PM Skills 笔记

## 1. 当前产品方向

当前方向可以拆成 3 条产品线：

1. 机器人皮肤：柔性触觉传感器、电子皮肤、机器人表面压力/温度/接近/剪切力感知。
2. 触觉手套：手部动作捕捉、力反馈、振动反馈、遥操作、机器人示教。
3. 全身传感衣：全身动作捕捉、触觉反馈、生理数据、训练/仿真/康复/机器人控制。

这三个方向都属于“机器人触觉与人机交互传感系统”，但客户、竞品、卖点和 PRD 不能混在一起写。建议先分别调研，再决定先做哪一个 beachhead segment。

## 2. 最常用 Skills

| 使用阶段 | 推荐 Skill | 用途 |
|---|---|---|
| 竞品调研 | `competitor-analysis` | 找机器人皮肤、触觉手套、全身传感衣的直接竞品和差异化机会 |
| 竞品销售对标 | `competitive-battlecard` | 单独对标 HaptX、SenseGlove、Teslasuit、GelSight 等竞品 |
| 市场细分 | `market-segments` | 拆分机器人厂商、科研院所、XR 训练、康复医疗、工业遥操作等客户群 |
| 首发市场选择 | `beachhead-segment` | 判断先做机器人皮肤、手套还是全身传感衣 |
| 产品方向 | `product-strategy` | 定义愿景、客户、价值主张、取舍和护城河 |
| 价值主张 | `value-proposition` | 提炼“为什么客户要买你” |
| 定位文案 | `positioning-ideas` | 生成差异化定位，例如“国产柔性机器人触觉皮肤” |
| 风险假设 | `identify-assumptions-new` | 找出技术、市场、客户、成本、交付风险 |
| 假设优先级 | `prioritize-assumptions` | 判断哪些假设必须先验证 |
| 用户访谈 | `interview-script` | 访谈机器人公司、实验室、XR 训练客户 |
| 需求整理 | `analyze-feature-requests` | 整理客户提出的功能需求 |
| 功能优先级 | `prioritize-features` | 把需求排成 V1/V2/后续版本 |
| PRD | `create-prd` | 写产品需求文档 |
| 研发故事 | `user-stories` | 拆成研发可执行用户故事 |
| 测试验收 | `test-scenarios` | 写 QA 测试用例和验收清单 |
| 指标体系 | `metrics-dashboard` | 设计传感数据看板、算法指标、设备健康指标 |
| 商业模式 | `business-model` | 梳理硬件、软件、SDK、定制项目收入 |
| 定价 | `pricing-strategy` | 做硬件套装、软件授权、SDK、项目制报价 |
| 上市策略 | `gtm-strategy` | 做发布、渠道、试点客户、销售资料 |
| 发布前风险 | `pre-mortem` | 评估发布失败原因 |

## 3. 推荐工作流

### 阶段 A：先判断方向

1. `market-segments`
2. `competitor-analysis`
3. `beachhead-segment`
4. `product-strategy`

目标：判断先做机器人皮肤、触觉手套，还是全身传感衣。

### 阶段 B：形成产品方案

1. `value-proposition`
2. `positioning-ideas`
3. `identify-assumptions-new`
4. `prioritize-assumptions`

目标：明确核心客户、核心场景、核心卖点和最大风险。

### 阶段 C：进入研发需求

1. `analyze-feature-requests`
2. `prioritize-features`
3. `create-prd`
4. `user-stories`
5. `test-scenarios`

目标：形成可给研发和 QA 的 PRD、用户故事、测试用例。

### 阶段 D：商业化准备

1. `competitive-battlecard`
2. `pricing-strategy`
3. `gtm-strategy`
4. `metrics-dashboard`
5. `pre-mortem`

目标：形成销售话术、定价、试点计划、上线风险清单。

## 4. 三条产品线分别用什么 Skill

### 4.1 机器人皮肤

优先用：

1. `competitor-analysis`
2. `market-segments`
3. `product-strategy`
4. `create-prd`
5. `user-stories`
6. `test-scenarios`

重点调研对象：

1. CySkin：模块化柔性人工皮肤，适配不同表面。
2. APEX SENSING：机器人触觉与电子皮肤，压力、温度、接近、剪切力等多模态方向。
3. LOOMIA：可定制电子纺织层，可做机器人表面压力映射。
4. FlexiTac：开源、可扩展柔性触觉方案。
5. GelSight / DIGIT：机器人指尖高分辨率触觉传感器。

建议产品定位：

国产柔性机器人触觉皮肤，面向机器人表面、末端执行器、仿生手、科研平台和工业测试。

### 4.2 触觉手套

优先用：

1. `competitor-analysis`
2. `competitive-battlecard`
3. `market-segments`
4. `value-proposition`
5. `create-prd`
6. `test-scenarios`

重点调研对象：

1. HaptX Gloves G1：微流体触觉反馈、力反馈、手部动作捕捉，面向培训和机器人。
2. SenseGlove：力反馈、振动反馈、XR 训练、遥操作和机器人示教。
3. bHaptics TactGlove：消费级/开发者触觉手套方向。

建议先区分两类产品：

1. 输入型手套：动作捕捉、手势识别、机器人遥操作。
2. 反馈型手套：振动、压力、力反馈、触觉反馈。

### 4.3 全身传感衣

优先用：

1. `market-segments`
2. `competitor-analysis`
3. `product-strategy`
4. `business-model`
5. `pricing-strategy`
6. `gtm-strategy`

重点调研对象：

1. TESLASUIT：全身智能服，包含触觉反馈、动作捕捉、生物数据。
2. bHaptics TactSuit：VR/游戏/仿真触觉背心和周边。
3. HaptX Nexus NX1：整合手套、步行平台、鞋和全身追踪的人机交互系统。

建议先明确产品到底是：

1. 全身动作捕捉衣。
2. 全身触觉反馈衣。
3. 全身压力/接触/姿态传感衣。
4. 面向机器人训练的数据采集服。

这四个方向不是同一个产品。

## 5. 这个方向最应该先问的问题

1. 客户是谁：机器人公司、科研院所、XR 训练公司、医疗康复、工业遥操作，还是消费电子？
2. 你卖的是传感器、整套硬件、软件平台、SDK，还是定制项目？
3. 首发产品是机器人皮肤、手套，还是全身传感衣？
4. 传感能力包括哪些：压力、温度、接近、剪切力、弯曲、拉伸、IMU、生物电？
5. 软件是否需要实时可视化、数据采集、回放、导出、SDK？
6. 是否需要给机器人控制系统输出实时数据？
7. 是否对接 ROS、Unity、Unreal、Python、C++ SDK？
8. 关键指标是什么：采样率、分辨率、延迟、柔性、耐久、可清洗、标定、成本？

## 6. 建议你下一步直接用的 Prompt

### 机器人皮肤调研

`$competitor-analysis 帮我调研机器人皮肤/电子皮肤/柔性触觉传感器竞品，重点看 CySkin、APEX SENSING、LOOMIA、FlexiTac、GelSight/DIGIT，并分析我们的差异化机会。`

### 触觉手套调研

`$competitor-analysis 帮我调研触觉手套/力反馈手套/机器人遥操作手套竞品，重点看 HaptX、SenseGlove、bHaptics，并区分输入型手套和反馈型手套。`

### 全身传感衣调研

`$competitor-analysis 帮我调研全身传感衣/全身触觉反馈服/动作捕捉服竞品，重点看 TESLASUIT、bHaptics、HaptX Nexus NX1，并分析科研、XR 训练、机器人训练场景。`

### 判断先做哪个方向

`$beachhead-segment 帮我在机器人皮肤、触觉手套、全身传感衣三个方向里选择首发细分市场，按痛点强度、付费意愿、可交付性、竞争强度、复购和扩展性评分。`

### 写产品策略

`$product-strategy 帮我为机器人触觉传感产品写产品策略，候选方向包括机器人皮肤、触觉手套和全身传感衣。`

## 7. 参考资料

1. CySkin: https://www.cyskin.com/
2. APEX SENSING: https://www.apexsensing.com/
3. LOOMIA Electronic Layer: https://humanoidroboticstechnology.com/company/loomia/loomia-electronic-layer-lel/
4. FlexiTac: https://flexitac.github.io/
5. GelSight Robotics: https://www.gelsight.com/solutions/tactile-robotics-applications/
6. GelSight DIGIT 360: https://www.gelsight.com/gelsight-and-meta-ai-introduce-digit-360-tactile-sensor/
7. HaptX Gloves G1: https://haptx.com/gloves-g1/
8. SenseGlove: https://www.senseglove.com/
9. TESLASUIT: https://teslasuit.io/products/teslasuit-4/
10. bHaptics: https://www.bhaptics.com/
