# Ethernet 采集方案调研

> 项目：人体全身压力采集  
> 日期：2026-05-17  
> 结论：第一版建议用“压力衣控制器 + Ethernet + 采集电脑”的 TCP 长连接方案。100Hz x 1024 点位的数据量很小，100Mbps Ethernet 已够用，1GbE 更稳。第一版重点不是高带宽，而是时间戳、掉线恢复、数据完整性和回放对齐。

## 1. 先说结论

你们的压力衣数据非常适合走 Ethernet。

按 1024 点位、100Hz 估算：

| 数据格式 | 单帧大小 | 每秒数据量 | 约等于 |
| --- | ---: | ---: | ---: |
| uint16，每点 2 字节 | 2048 B | 204.8 KB/s | 1.64 Mbps |
| float32，每点 4 字节 | 4096 B | 409.6 KB/s | 3.28 Mbps |
| 加时间戳、帧头、校验 | 约 2.1-4.3 KB | < 0.5 MB/s | < 5 Mbps |

所以：

- `100Mbps Ethernet` 足够传压力数据。
- `1GbE` 更推荐，主要是为了稳定、通用、和相机/其他设备共网。
- 不需要一开始上复杂工业总线。
- 不建议用 BLE 传完整 1024 点 x 100Hz 数据。
- Wi-Fi 可以做调试，不建议作为正式采集链路。

## 2. 推荐链路

第一版推荐链路：

```text
压力传感阵列
  -> 采集前端 ADC/扫描电路
  -> 主控 MCU/SoC
  -> Ethernet MAC/PHY 或 W5500 Ethernet 控制器
  -> RJ45 网口
  -> 网线
  -> 交换机或直连采集电脑
  -> 采集软件
  -> 本地数据文件
  -> 回放工具
```

如果加相机：

```text
压力衣 --Ethernet--> 采集电脑
USB/网络相机 --> 采集电脑
同步灯/蜂鸣器 --> 采集电脑控制
```

第一版不要把所有设备都做成复杂的统一硬同步。先用软件时间戳 + LED/蜂鸣同步事件完成对齐。

## 3. 硬件架构选型

### 3.1 方案 A：MCU 自带 Ethernet MAC + 外接 PHY

链路：

```text
MCU Ethernet MAC -> RMII/RGMII -> Ethernet PHY -> RJ45
```

常见 PHY：

- Microchip LAN8720A：10/100 Ethernet PHY，RMII 接口。
- 其他 10/100 PHY 或千兆 PHY。

优点：

- 性能稳定。
- 软件可控性强。
- 适合正式产品化。
- 可配合 lwIP、FreeRTOS 等做 TCP/UDP。

缺点：

- 硬件设计和驱动调试门槛比 W5500 高。
- PCB、时钟、阻抗、EMC 要认真做。

适合：

- 你们准备重做控制板或量产控制器。

参考：

- Microchip LAN8720A：https://www.microchip.com/en-us/product/lan8720a
- Microchip Ethernet MCU/MPU：https://www.microchip.com/en-us/products/high-speed-networking-and-video/ethernet/ethernet-mcus-and-mpus

### 3.2 方案 B：W5500 硬件 TCP/IP Ethernet 模块

链路：

```text
MCU -> SPI -> W5500 -> RJ45
```

W5500 是带硬件 TCP/IP 协议栈的 Ethernet 控制器，支持 TCP、UDP、IPv4 等。官方文档说明其通过 SPI 连接外部 MCU，SPI 可到 80MHz，并集成 10/100 MAC 与 PHY。

优点：

- 上手最快。
- MCU 不需要自己跑完整 TCP/IP 协议栈。
- 很适合样机和 MVP。
- 市面模块便宜，调试资料多。

缺点：

- 性能和灵活性不如 MCU 原生 Ethernet。
- SPI 带宽和 W5500 buffer 需要注意。
- 复杂网络能力有限。

适合：

- 你们之前没做过 Ethernet。
- 想快速做出压力衣 Ethernet 样机。
- 目标只是 100Hz x 1024 点压力数据。

参考：

- WIZnet W5500 官方文档：https://docs.wiznet.io/Product/Chip/Ethernet/W5500

### 3.3 方案 C：小型 Linux 主控

链路：

```text
传感采集板 -> USB/SPI/UART -> Raspberry Pi/工控 Linux 板 -> Ethernet -> 采集电脑
```

优点：

- 开发最快。
- 可以直接用 Python/C++。
- 网络、文件、日志、升级都方便。
- 适合实验室原型。

缺点：

- 体积、功耗、启动时间和稳定性不如 MCU。
- 对可穿戴产品不一定合适。

适合：

- 早期验证。
- 不想马上改底层硬件。
- 压力衣已有数据输出，但没有 Ethernet。

## 4. 第一版推荐方案

如果你们“之前没做过 Ethernet”，建议这样走：

### 4.1 最快 MVP

```text
现有压力衣控制器
  -> 现有数据接口，例如 UART/USB
  -> 小 Linux 网关或上位机
  -> Ethernet/本机采集软件
```

这个适合先验证软件、数据格式和回放工具。

### 4.2 稳妥硬件 MVP

```text
压力衣主控 MCU
  -> SPI
  -> W5500
  -> RJ45
  -> 采集电脑
```

这个适合快速做出“真正 Ethernet 输出”的样机。

### 4.3 产品化版本

```text
主控 MCU/SoC 自带 Ethernet MAC
  -> PHY
  -> RJ45 或防水航空接口
  -> 采集电脑/交换机
```

这个适合之后量产和工业化。

## 5. TCP 还是 UDP

### 5.1 第一版建议：TCP 长连接

第一版建议用 TCP，因为你们的核心诉求是完整保存数据，不是极限低延迟。

链路：

```text
采集电脑启动 TCP Server
压力衣作为 TCP Client 连接电脑
开始采集后连续发送 length-prefixed frame
```

或者：

```text
压力衣启动 TCP Server
采集电脑作为 TCP Client 连接压力衣
```

我更推荐第一种：压力衣作为 Client。

原因：

- 压力衣插上网络后主动找采集电脑。
- 多件衣服时更容易由采集电脑统一管理。
- 采集电脑可以固定 IP，设备配置简单。

TCP 数据格式建议：

```text
[4 bytes length]
[frame_header]
[pressure_payload]
[crc32]
```

优点：

- 不会丢包。
- 不需要自己处理 UDP 分片重组。
- 采集软件更容易写。
- 适合 MVP 和数据集采集。

注意：

- 开启 `TCP_NODELAY`，减少 Nagle 算法带来的延迟。
- 每帧要有 `frame_id` 和 `device_timestamp_us`。
- 即使 TCP 不丢包，也要写 CRC，防止解析或存储错误。
- 断线要能重连，重连后 frame_id 不能混乱。

### 5.2 后续可选：UDP

UDP 适合实时显示，但要自己处理丢包。

注意一个关键点：

1024 点 x uint16 = 2048 字节，已经超过普通 Ethernet MTU 下安全 UDP payload 大小。普通 MTU 1500 时，UDP payload 通常应控制在约 1472 字节以内，否则会 IP 分片。分片包任何一片丢失，整帧就不可用。

如果用 UDP，有两种做法：

1. 开 Jumbo Frame，把 MTU 调到 9000。
2. 不开 Jumbo Frame，把一帧拆成多个小包。

推荐 UDP 分包格式：

```text
frame_id
chunk_id
chunk_count
sensor_start_index
sensor_count
timestamp_us
payload
crc32
```

第一版不建议 UDP，除非你们有很强嵌入式网络经验。

## 6. 数据帧设计

每一帧压力数据都要有独立头信息。

建议 frame_header：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| magic | uint32 | 固定标识，例如 0x50525353 |
| protocol_version | uint16 | 协议版本 |
| header_length | uint16 | 头长度 |
| device_id | uint32 | 设备编号 |
| session_id | uint32 | 本次采集编号 |
| frame_id | uint64 | 压力帧序号 |
| device_timestamp_us | uint64 | 设备侧时间戳 |
| sample_rate_hz | uint16 | 采样率，例如 100 |
| sensor_count | uint16 | 点位数，例如 1024 |
| value_type | uint8 | 0=uint16, 1=float32 |
| flags | uint16 | 标记位，例如 sync_event |
| payload_length | uint32 | 数据长度 |
| header_crc16 | uint16 | 头校验，可选 |

payload：

```text
sensor_0001, sensor_0002, ... sensor_1024
```

帧尾：

```text
crc32(payload)
```

## 7. 时间戳和同步

### 7.1 第一版同步

第一版建议用三层时间：

1. `device_timestamp_us`：压力衣设备内部时间。
2. `host_receive_time_ns`：采集电脑收到该帧的时间。
3. `sync_event_time`：LED/蜂鸣同步事件时间。

采集软件保存时补充：

```json
{
  "frame_id": 12345,
  "device_timestamp_us": 987654321,
  "host_receive_time_ns": 1779000000000000000
}
```

同步事件：

```json
{
  "event": "sync_flash_1",
  "host_time_ns": 1779000001234567890,
  "pressure_frame_id": 2468
}
```

这样后处理可以把视频时间轴和压力时间轴对齐。

### 7.2 PTP 什么时候需要

PTP 是 IEEE 1588 定义的网络时钟同步协议。IEEE 标准说明它用于同步网络化分布式系统中的实时钟，适用于包括 Ethernet 在内的网络。工业相机领域也常用 PTP；例如 Basler 文档说明 PTP 可同步同一网络中的多个 GigE 相机。

你们第一版暂时不需要 PTP。

需要 PTP 的情况：

- 多件压力衣同时采集。
- 多个 Ethernet 相机同时采集。
- 客户要求帧级同步。
- 同步误差要小于 50ms，甚至小于 10ms。
- 后续要和 GigE Vision 工业相机统一时间。

第一版目标 <500ms，用软件时间戳 + 同步灯足够。

参考：

- IEEE 1588-2019：https://standards.ieee.org/standard/1588-2019.html
- Basler PTP 文档：https://docs.baslerweb.com/precision-time-protocol
- A3 GigE Vision 标准说明：https://www.automate.org/vision/vision-standards/vision-standards-gige-vision

## 8. IP 地址和网络拓扑

### 8.1 直连采集电脑

最简单：

```text
压力衣 RJ45 <----网线----> 采集电脑 RJ45
```

配置：

- 采集电脑 IP：`192.168.10.1`
- 压力衣 IP：`192.168.10.101`
- 子网掩码：`255.255.255.0`

优点：

- 简单。
- 网络干扰少。
- 适合实验室采集。

缺点：

- 一台电脑网口可能不够。
- 同时接相机/多设备时不方便。

### 8.2 交换机拓扑

推荐正式采集：

```text
压力衣 ----\
相机 ------> 千兆交换机 -> 采集电脑
同步器 ----/
```

配置：

- 使用千兆交换机。
- 采集网络独立，不接办公室大网。
- 所有设备固定 IP。
- 采集电脑单独一个有线网口接采集网络。

建议网段：

```text
采集电脑：192.168.10.1
压力衣 1：192.168.10.101
相机 1：192.168.10.201
同步器：192.168.10.250
```

## 9. PoE 是否需要

PoE 是 Power over Ethernet，可以一根网线同时传数据和供电。IEEE 802.3af/at/bt 是常见 PoE 标准。

第一版不建议上 PoE。

原因：

- 压力衣是穿戴设备，供电和人体安全要谨慎。
- PoE 需要 48V 输入和降压模块，硬件复杂度上升。
- 你们先验证数据采集和回放，不需要一根线解决所有问题。

第一版建议：

```text
压力衣电池供电或独立低压供电
Ethernet 只传数据
```

后续如果做固定场景设备或充电底座，再评估 PoE。

参考：

- Microchip PoE 标准概览：https://developerhelp.microchip.com/xwiki/bin/view/applications/ethernet/poe/standards/
- Cisco PoE 介绍：https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-power-over-ethernet.html

## 10. 采集软件设计

采集软件建议包含 5 个线程/模块：

1. 设备连接管理
2. 网络接收
3. 帧解析与校验
4. 数据写盘
5. 实时预览/回放缓存

流程：

```text
启动软件
  -> 选择采集任务
  -> 等待压力衣连接
  -> 握手
  -> 校验设备信息
  -> 开始采集
  -> 接收压力帧
  -> 写 pressure_raw.bin/csv
  -> 同时写 capture_log.jsonl
  -> 停止采集
  -> 生成 metadata.json
```

### 10.1 握手协议

压力衣连接后先发：

```json
{
  "type": "hello",
  "device_id": "suit_001",
  "firmware": "0.1.0",
  "sample_rate_hz": 100,
  "sensor_count": 1024,
  "value_type": "uint16",
  "supports_sync_event": true
}
```

电脑返回：

```json
{
  "type": "start_session",
  "session_id": "carry_box_20260517_001",
  "host_time_ns": 1779000000000000000
}
```

### 10.2 写盘格式

建议不要第一版只写 CSV。

原因：

- CSV 体积大。
- 写盘慢。
- 1024 列不方便实时写。

推荐：

- 原始数据：`pressure_raw.bin`
- 索引：`pressure_index.csv`
- 清洗数据：后处理生成 `pressure_clean.csv` 或 `pressure_clean.parquet`
- 日志：`capture_log.jsonl`

如果团队只会 CSV，也可以先用 CSV，但要注意写盘缓存。

## 11. 设备端最小功能

压力衣 Ethernet 固件至少要支持：

- 配置 IP
- 连接采集电脑
- hello 握手
- start/stop 采集
- 连续发送压力帧
- 心跳包
- 断线重连
- frame_id 单调递增
- device_timestamp_us 单调递增
- CRC 校验
- 设备状态上报

设备状态建议：

```json
{
  "type": "status",
  "battery": 82,
  "temperature": 36.5,
  "sample_rate_hz": 100,
  "frames_sent": 12345,
  "dropped_internal_frames": 0
}
```

## 12. 错误处理

必须处理这些问题：

| 问题 | 现象 | 处理 |
| --- | --- | --- |
| 网线拔掉 | TCP 断开 | 采集软件报警，设备重连 |
| 电脑写盘慢 | 缓存堆积 | 内存队列报警，暂停采集或降级 |
| 帧序号跳变 | 数据丢失或设备重启 | 标记异常，写入质量报告 |
| CRC 错误 | 数据损坏 | 丢弃该帧，记录错误 |
| 采样率漂移 | 100Hz 不稳定 | 报告中记录实际采样率 |
| 时间戳回退 | 设备时钟异常 | 标记该段不可用 |
| 多设备 IP 冲突 | 连接失败 | 软件扫描并提示 |

## 13. 验收标准

Ethernet MVP 验收标准：

- 连续采集 30 分钟不断线。
- 实际帧率稳定在 100Hz ± 5%。
- frame_id 连续，无异常跳变。
- CRC 错误率 < 0.01%。
- 采集电脑端无明显数据积压。
- 单条 20 秒动作样本完整保存。
- 采集结束后能自动生成样本目录。
- 回放工具能读取压力数据并与视频对齐。
- 拔插网线后软件能明确提示断线。
- 设备重连后不会覆盖旧数据。

## 14. 推荐开发路线

### 阶段 1：PC 模拟器

先写一个“压力衣模拟器”在电脑上发 TCP 数据。

目标：

- 验证协议。
- 验证采集软件。
- 验证写盘。
- 验证回放工具。

### 阶段 2：W5500/网关样机

用 W5500 或 Linux 网关把真实压力数据发到采集电脑。

目标：

- 连续采集真实数据。
- 处理断线。
- 处理时间戳。
- 输出样本目录。

### 阶段 3：正式控制板

如果路线验证成立，再做 MCU 原生 Ethernet 或 SoC 方案。

目标：

- 减小体积。
- 提升稳定性。
- 支持更多设备管理。
- 支持后续 PTP 或硬同步。

## 15. 采购建议

第一版需要：

- 千兆交换机 1 台
- Cat6 网线若干
- USB 千兆网卡 1 个，可选
- W5500 模块若干，若走 W5500 方案
- ESP32/STM32 开发板，可选
- RJ45 防呆接口或转接板

暂时不需要：

- PoE 交换机
- PTP grandmaster
- 工业级网管交换机
- 万兆网卡
- 光纤链路

## 16. 最终建议

你们现在最务实的方案：

```text
第一版：TCP over Ethernet
硬件：W5500 或 Linux 网关
拓扑：压力衣 -> 网线 -> 千兆交换机 -> 采集电脑
协议：length-prefixed TCP frame
同步：device timestamp + host receive timestamp + LED/蜂鸣事件
目标：稳定采集和回放对齐，不追求 PTP
```

等客户愿意做试点后，再升级：

```text
正式版：MCU/SoC 原生 Ethernet + 固定 IP + 更完整状态管理
同步增强：PTP 或硬件 trigger
供电增强：评估 PoE，但穿戴端谨慎使用
```

