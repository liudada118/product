# JQ Tools 竞品对标 Battlecard: XSENSOR / Tekscan

## 1. 结论摘要

JQ Tools 当前 V2.0 功能列表与 XSENSOR、Tekscan 的主线能力基本对得上，尤其是实时 2D 热力图、坐垫/靠背分区、统计指标、框选区域统计、历史回放、CSV 导出这些核心功能。

但要在汽车座椅研发和科研招标场景中真正“能打”，还需要补强四类能力：

1. 数据可信度：校准、误差、重复性、传感器参数记录。
2. 科研交付：测试项目管理、报告生成、实验信息记录。
3. 对比分析：双组数据对比、分区压力差异、回放对比。
4. 传感器规格证明：点阵数量、采样率、压力范围、厚度、寿命、漂移。

JQ Tools 的优势不应只讲“功能追平”，而要讲“国产纤维压力传感器 + 中文本地化 + 展厅演示 + 科研导出 + 本地交付”的组合价值。

## 2. 竞品概览

### XSENSOR

定位：高端压力成像平台，汽车座椅、人体工学、医疗坐垫、床垫、运动等场景都有布局。

公开资料显示，XSENSOR X3 Pro Seating System 面向汽车座椅设计，支持座面和靠背压力测量，强调 LX 传感器、准确可靠、无需重新校准、重复性、耐久和舒适性测试。XSENSOR 软件强调高质量压力图像、实时测量、AI/ML 分析、桌面/移动/云端工作流，以及可导出的数据。

对 JQ Tools 的主要威胁：

1. 汽车座椅场景品牌强。
2. 传感器准确性和重复性叙事成熟。
3. 软件视觉效果和体验成熟。
4. 报告、分享、客户文件、视频保存等交付能力较强。

### Tekscan

定位：压力映射综合大厂，覆盖汽车、研发、制造、质量、医疗坐垫、床垫、轮胎、电池等场景。

公开资料显示，Tekscan I-Scan、BPMS、CONFORMat 支持 2D/3D 实时和录制数据显示、区域分析、中心压力/中心力轨迹、平均/峰值压力、接触面积、逐帧查看、导出、校准、多传感器和多种传感器规格。I-Scan 系统强调超过 200 种传感器、传感器 MAP、单点/多点校准、高速动态测试和 Windows 软件。

对 JQ Tools 的主要威胁：

1. 传感器规格和应用覆盖极广。
2. 科研和工程客户信任度高。
3. 校准、导出、图表、逐帧回放等能力完整。
4. 区域隔离分析、量尺、对比等细节能力成熟。

## 3. 逐项功能对标

评级说明：

| 标记 | 含义 |
|---|---|
| 能打 | JQ Tools 有机会优于竞品，或更适合中国客户场景 |
| 持平 | 功能方向对齐，但需要实现质量追上 |
| 偏弱 | 竞品已有成熟能力，JQ Tools 当前描述不够完整 |
| 缺口 | 当前需求列表没有覆盖，建议补充 |

| 功能模块 | JQ Tools 当前需求 | 对 XSENSOR | 对 Tekscan | 评级 | 建议 |
|---|---|---|---|---|---|
| 一键连接/设备识别 | 一键连接、串口检测、MAC 读取、设备类型 | XSENSOR 更偏整套设备即插即用 | Tekscan 有成熟采集硬件和传感器 MAP | 能打 | 国产硬件可做更简单的中文连接流程 |
| 离线授权/固件校验 | 无联网使用、固件校验、设备授权加密 | XSENSOR 有平台和数据安全能力 | Tekscan 偏工程软件授权 | 能打 | 国内招标和离线实验室场景是优势 |
| 设备类型切换 | 手、床垫、汽车坐垫、汽车靠背、工学椅 | XSENSOR 多解决方案覆盖不同场景 | Tekscan 传感器规格覆盖广 | 偏弱 | 需要传感器 MAP/设备模板机制，否则多设备会混乱 |
| 预压力清零 | 置零、取消置零、按钮状态 | XSENSOR 强调无需重校准和可靠数据 | Tekscan 有单点/多点校准 | 偏弱 | 只做清零不够，需要校准、误差、重复性 |
| 2D 热力图 | 实时热力图、颜色映射 | XSENSOR 图像质量强 | Tekscan 2D 压力图成熟 | 持平 | V2.0 必须做到流畅、可解释、颜色稳定 |
| 坐垫/靠背分区 | 坐垫、靠背分区显示 | XSENSOR 明确支持 seat/back surfaces | Tekscan CONFORMat/BPMS 支持座椅/靠背类应用 | 持平 | 汽车座椅场景必须作为主卖点 |
| 2D 数字矩阵 | 数字矩阵显示 | 竞品更多强调图像和统计 | Tekscan 可查看单个 sensel 数值 | 持平 | 作为专业开关，不应干扰热力图 |
| 画布翻转/缩放/重置 | 左右/上下翻转、滚轮缩放、视图重置 | 竞品通常有视图操作能力 | Tekscan 软件视图能力成熟 | 持平 | 属于基础交互，必须顺滑 |
| 3D 可视化 | Three.js 点图、3D 数字、模型视图 | XSENSOR 有 3D methodology/3D views | Tekscan 支持 2D/3D 实时和录制数据 | 偏弱 | V2.1 做，V2.0 不建议因 3D 拖慢主线 |
| 3D 模型上传 | 后续/整体提到模型上传 | 竞品偏系统内置视图 | Tekscan 偏传感器形状和视图 | 能打但高风险 | 若能上传汽车座椅模型，展示差异明显，但成本高 |
| 可视化调节 | 平滑度、颜色层次、噪点、云图高度、响应速度 | XSENSOR 图像质量和算法强 | Tekscan 有插值、轮廓、平均等显示增强 | 偏弱 | 必须区分“显示滤波”和“原始数据” |
| 框选区域统计 | 矩形框选、坐标输入、区域统计、边界校验 | XSENSOR 有比较/标记类工具 | Tekscan 支持 isolate/analyze specific regions | 持平 | 默认保存全量数据，框选只影响统计和导出 |
| 量尺工具 | 多量尺、选中高亮、删除 | XSENSOR 可能有标记/评估工具 | Tekscan 明确支持两点距离测量 | 偏弱 | 不影响 V2.0 主线，可 V2.2 做 |
| 实时统计指标 | 平均、最大、最小、总和、面积、点数 | XSENSOR 有面积、平均/峰值等 | Tekscan 有 total force/contact area/peak/contact pressure | 持平 | 需要补单位、阈值、口径说明 |
| 压力中心/重心轨迹 | 压力重心点轨迹 | XSENSOR 有 symmetry/3D/分析工具 | Tekscan 明确支持 center of pressure/force trajectory | 偏弱 | 建议 V2.1，但科研场景很重要 |
| 趋势图 | 总和曲线、面积曲线、正态分布 | XSENSOR 有 time series data | Tekscan 有 real-time/stored graphical analysis | 偏弱 | V2.0 至少做总压力和面积曲线 |
| 数据采集 | 开始/停止采集、本地存储 | XSENSOR 可记录和比较多次设计 | Tekscan 可记录实时/存储数据 | 持平 | 需要保证长时间采集和断电恢复 |
| 历史回放 | 播放、暂停、滑块、倍速、退出 | XSENSOR 可保存视频/记录 | Tekscan 可逐帧查看录制数据 | 持平 | V2.0 做基础控件，后续做对比回放 |
| CSV 导出 | CSV、路径选择、进度、成功打开 | XSENSOR 有 export ready data | Tekscan 有 ASCII/export | 持平 | 必须定义 CSV 格式版本 |
| 数据导入 | CSV 上传、外部数据加载 | 竞品公开资料较少强调 | Tekscan 支持导入/导出 subject movie files | 偏弱 | 先定格式，V2.2 再做导入 |
| 数据对比 | 双组选择、对比热力图、分压对比 | XSENSOR 有 compare views | Tekscan 有 side-by-side comparisons | 偏弱 | 这是明显竞品缺口，科研/研发很需要 |
| 历史管理 | 搜索、重命名、备注、删除 | XSENSOR 有客户/文件/报告流程 | Tekscan 面向项目和记录管理 | 偏弱 | 需要引入“测试项目/实验记录”概念 |
| 报告生成 | 当前未明确 | XSENSOR 可生成报告 | Tekscan 可导出并支持分析 | 缺口 | 建议 V2.1 加 PDF/Word 报告 |
| 校准流程 | 当前只有清零 | XSENSOR 强调免重校准和可靠性 | Tekscan 支持单点/多点校准 | 缺口 | 招标场景必须补 |
| 误差/重复性 | 当前未明确 | XSENSOR 明确强调准确性、重复性、耐久 | Tekscan 强调准确、repeatable measurement | 缺口 | 需要硬件测试报告和软件记录 |
| 传感器参数页 | 当前未明确 | XSENSOR 展示压力范围、厚度、准确性等 | Tekscan 展示传感器尺寸、分辨率、压力范围 | 缺口 | 建议 V2.0 就加入设备参数查看 |
| 安装包 | Windows 安装包，macOS 后续 | XSENSOR 有预装/桌面/移动/云端 | Tekscan Windows 软件成熟 | 偏弱 | V2.0 先 Windows 是合理选择 |
| 中文本地化 | 中文界面 | 国外品牌中文本地化弱 | 国外品牌中文本地化弱 | 能打 | 中文报告、中文招标资料是强卖点 |
| 离线本地数据 | 本地缓存、本地存储、无联网 | XSENSOR 有云端能力 | Tekscan 以本地工程软件为主 | 能打 | 国内科研院所离线使用是机会 |
| 60fps 性能目标 | 实时低延迟、60fps | 竞品强调实时和高质量图像 | Tekscan 有高采样/动态测试能力 | 偏弱 | 需要实测数据，不能只写目标 |

## 4. Where We Win

### 4.1 中文、本地化、招标响应

JQ Tools 可以在中文界面、中文报告、本地交付、离线授权、定制开发、国产替代方面胜出。XSENSOR 和 Tekscan 产品强，但国内客户在采购、售后、二次开发和招标材料适配上会有摩擦。

Sales Talk:

“国外系统功能成熟，但通常是标准化交付。JQ Tools 可以按您的座椅型号、传感器规格、报告模板和招标参数做本地化适配。”

### 4.2 展厅/门店演示

JQ Tools 可以把实时热力图、大屏展示、坐垫/靠背分区、实时指标做得更轻、更直观。Tekscan 更偏工程测试，XSENSOR 强但价格和采购门槛高。

Sales Talk:

“如果您的场景不只是实验室，还包括展厅和门店演示，JQ Tools 可以把复杂压力数据变成客户一眼能看懂的展示画面。”

### 4.3 国产纤维压力传感器

纤维压力传感器如果能证明柔性、贴合、耐用、成本和可定制优势，会形成硬件差异化。这个点不能只写口号，必须配测试数据。

Sales Talk:

“我们不是只做软件平替，而是用国产纤维压力传感器和 JQ Tools 软件形成软硬件一体方案。”

## 5. Where They Win

### 5.1 XSENSOR 赢在汽车座椅定位和图像质量

XSENSOR 对汽车座椅设计、座面/靠背、LX 传感器、重复性和无需重校准的表达非常成熟。JQ Tools 当前还缺少可公开对外表达的准确性、重复性和耐久数据。

Counter:

JQ Tools 不要直接硬碰“全球高端品牌”，应强调国产替代、本地交付、中文报告、成本和定制。

### 5.2 Tekscan 赢在科研工程完整度

Tekscan 的强项是传感器规格、校准、区域分析、中心轨迹、图表、导出、逐帧回放、对比和多行业案例。JQ Tools 当前 V2.0 还只是覆盖主流程。

Counter:

V2.0 先完成闭环，V2.1/V2.2 快速补齐校准、报告、对比、压力中心轨迹和数据格式。

### 5.3 两家都赢在“可信数据”

竞品都强调准确、可靠、重复性、校准或免重校准。JQ Tools 当前需求列表偏功能操作，还缺数据可信度材料。

Counter:

必须建立传感器验证包，包括误差、重复性、漂移、寿命、采样率、压力范围、厚度和校准说明。

## 6. Common Objections & Responses

| Prospect Says | Respond With |
|---|---|
| “XSENSOR 是行业标杆，为什么不用它？” | “XSENSOR 很强，尤其是高端座椅研发。但如果您需要中文软件、中文报告、离线部署、本地定制和更可控的采购成本，JQ Tools 更适合国内落地。” |
| “Tekscan 功能更全。” | “Tekscan 的工程能力很完整。JQ Tools V2.0 会先覆盖您最常用的实时采集、2D 热力图、统计、回放和 CSV 导出；后续可以按您的测试流程定制，而不是购买一套复杂系统后再适配。” |
| “你们有没有校准和误差证明？” | “这是我们当前最重视的交付材料。V2.0 会把清零、设备参数、采样记录和数据导出做进系统，同时补充误差、重复性和传感器寿命测试报告。” |
| “3D 为什么不先做完整？” | “3D 对展示有价值，但研发和科研首先看数据稳定、采集、统计、回放和导出。我们建议先把基础数据闭环做扎实，再把 3D 作为 V2.1 展示增强。” |
| “框选后能不能只采集框选区域？” | “可以导出框选区域，但默认应保存全量原始数据。这样后续回放、复查和科研分析不会丢数据。” |

## 7. Landmines to Plant

在客户评估 XSENSOR 或 Tekscan 时，可以问：

1. 是否必须中文界面、中文报告和本地招标材料？
2. 是否需要离线使用，不能依赖云端或外部网络？
3. 是否需要按汽车座椅、靠背、工学椅、床垫等设备类型定制模板？
4. 是否需要本地团队快速改软件界面、报告字段和导出格式？
5. 是否关注采购成本、交付周期和售后响应？
6. 是否需要把压力系统用于展厅/门店大屏演示，而不只是实验室测试？

## 8. Win / Loss Patterns

### We Tend To Win When

1. 客户预算有限，但要接近 XSENSOR/Tekscan 的核心能力。
2. 客户重视国产替代、本地交付和快速定制。
3. 客户需要展厅、门店、销售演示，不只是实验室研发。
4. 客户需要中文界面、中文报告和离线使用。
5. 客户愿意参与试点，一起打磨座椅场景。

### We Tend To Lose When

1. 招标参数直接按 Tekscan 或 XSENSOR 高端配置写死。
2. 客户强制要求成熟校准体系、误差证明和长期案例。
3. 客户需要马上使用完整 3D、对比分析、报告、中心轨迹、量尺等高级功能。
4. 客户更看重国际品牌背书，而不是本地化和成本。

### Key Differentiator

JQ Tools 的关键不是“每个功能都比竞品多”，而是：

**用国产纤维压力传感器和中文 JQ Tools 软件，把汽车座椅压力数据采集、实时展示、区域分析、回放导出和本地交付做成一套更适合中国客户的系统。**

## 9. 功能补强建议

### V2.0 必补

1. 设备参数页：传感器类型、点阵数量、采样率、压力范围、设备 MAC、设备类型。
2. 清零记录：清零时间、清零状态、清零值是否写入采集文件。
3. CSV 格式版本：否则后续导入、对比和报告会返工。
4. 测试项目字段：项目名、座椅型号、测试人员、设备类型、备注。

### V2.1 建议补

1. 校准流程。
2. PDF/Word 报告生成。
3. 压力中心轨迹。
4. 图像平滑和噪点处理。
5. 3D 点图模型。

### V2.2 建议补

1. 双组数据对比。
2. 对比热力图。
3. 分区压力差异分析。
4. CSV 数据导入。
5. 多量尺管理。

## 10. Sources

1. XSENSOR Seating & Ergonomics: https://www.xsensor.com/solutions-and-platform/design-and-safety/seating-ergonomics
2. XSENSOR Software: https://www.xsensor.com/solutions-and-platform/software
3. XSENSOR Pressure Sensor Technology: https://learn.xsensor.com/pressure-sensor
4. XSENSOR Wheelchair Seating: https://www.xsensor.com/solutions-and-platform/csm/wheelchair-seating
5. Tekscan I-Scan: https://www.tekscan.com/products-solutions/systems/i-scan-system
6. Tekscan BPMS: https://www.tekscan.com/products-solutions/systems/body-pressure-measurement-system-bpms
7. Tekscan CONFORMat: https://www.tekscan.com/products-solutions/systems/conformat-system
8. Tekscan Pressure Mapping Technology: https://www.tekscan.com/products-solutions/pressure-mapping-technology

