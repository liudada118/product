# CAM 手机作为串口摄像头产品调研

## 1. 调研结论

“把手机当成串口摄像头”需要先明确目标设备是谁：

- 如果目标是电脑软件读取 `COM` 口：可做，推荐做“手机采集画面 + 电脑端桥接成虚拟 COM 口”。
- 如果目标是单片机、控制板、工控设备读取 `UART/TTL/RS232`：可做，但只适合低帧率图片或低分辨率画面，不适合实时高清视频。
- 如果目标是让手机直接插 USB 后被电脑识别成“USB 串口摄像头”：不推荐。普通 Android/iPhone 默认不支持把手机直接伪装成 USB CDC 串口设备，除非做系统级定制、root、内核 gadget 配置或专用硬件。

推荐第一阶段做：

> Android 手机采集摄像头画面，通过 Wi-Fi 或蓝牙发送到电脑，电脑端把图片帧转换成自定义串口协议，并通过虚拟 COM 口提供给上层软件。

如果要接单片机或工控板，推荐做：

> Android 手机通过 USB OTG 连接 USB-TTL/USB-RS232 转换器，手机 App 将压缩后的 JPEG 图片分包发送到串口。

## 2. “串口摄像头”的三种定义

| 定义 | 说明 | 可行性 | 推荐度 |
|---|---|---:|---:|
| 电脑看到一个 COM 口 | 上层 PC 软件通过 COM 口读图片数据 | 高 | 高 |
| 外部设备通过 UART 读手机画面 | MCU/工控板通过 TX/RX 读图片数据 | 中 | 中 |
| 手机直接模拟 USB 串口设备 | 手机插入电脑后枚举成 CDC/ACM 串口设备 | 低 | 低 |

## 3. 典型使用场景

### 3.1 电脑端旧软件只支持 COM 口

部分老系统、工控软件或测试工具只会从串口读数据。如果要让这些软件读手机摄像头画面，可以在电脑端创建虚拟串口：

```text
手机摄像头
  -> 手机 App 压缩图片
  -> Wi-Fi / 蓝牙 / USB 网络
  -> 电脑端接收服务
  -> 虚拟 COM 口
  -> 旧软件读取图片帧
```

这种路线最适合作为第一版，因为不用改手机系统，也不需要外部硬件。

### 3.2 单片机或控制板要读取手机摄像头

如果目标是 Arduino、STM32、ESP32、工控板等设备，可以让 Android 手机通过 OTG 连接 USB 转串口模块：

```text
Android 手机
  -> CameraX 采集
  -> JPEG 压缩
  -> USB OTG
  -> USB-TTL / USB-RS232 转换器
  -> MCU / 工控设备 UART
```

这种路线硬件链路清晰，但串口带宽限制很明显。它适合抓拍、低分辨率预览、二维码/状态图传输，不适合 720p/1080p 实时视频。

### 3.3 手机直接变成 USB 串口外设

这条路线听起来最理想：

```text
手机 USB-C
  -> 电脑
  -> 系统出现 COM 口
```

但普通手机 App 无法直接改变手机 USB 枚举类型。Android 官方 USB 模式主要包括 host 和 accessory。手机作为 USB host 时可以控制外设；手机作为 accessory 时外部硬件是 host。要让手机模拟 CDC 串口设备通常需要系统权限、内核 USB gadget 支持或定制 ROM，不适合作为常规产品方案。

## 4. 技术依据

### 4.1 Android USB Host / Accessory

Android 官方文档说明 Android 支持 USB host 和 USB accessory 两种模式。Host 模式下 Android 设备作为主机枚举外设；accessory 模式下外部硬件作为 host，Android 设备作为 accessory。

这意味着 Android App 可以比较自然地做“手机连接 USB 串口模块并发送数据”，但不能简单地让普通 App 把手机变成电脑可识别的 USB 串口设备。

资料：

- Android USB host/accessory overview: https://developer.android.com/develop/connectivity/usb
- Android USB host overview: https://developer.android.com/develop/connectivity/usb/host
- Android Open Accessory Protocol: https://source.android.com/docs/core/interaction/accessories/protocol

### 4.2 Android USB 串口库

`usb-serial-for-android` 是常用 Android USB Host 串口库，可与 Arduino、CDC、FTDI 等 USB 串口硬件通信。它提供类似 `read()` / `write()` 的原始串口读写能力，不需要 root。

资料：

- usb-serial-for-android: https://github.com/mik3y/usb-serial-for-android

### 4.3 蓝牙 SPP / RFCOMM

Android 支持基于 RFCOMM 的蓝牙 socket。RFCOMM 常被称为 Serial Port Profile，也就是蓝牙串口。它可以让手机和电脑或蓝牙串口模块建立类似串口的数据通道。

但蓝牙串口带宽较低，适合传小图、状态、控制命令，不适合高帧率视频。

资料：

- Android BluetoothServerSocket: https://developer.android.com/reference/android/bluetooth/BluetoothServerSocket
- Bluetooth Serial Port Profile: https://www.bluetooth.com/specifications/specs/serial-port-profile-1-2/

### 4.4 iPhone 限制

iOS 对传统串口类外设限制更强。Apple 的 External Accessory 框架主要用于 MFi 外设；普通 iOS App 不能像 Android 那样自由接 USB 串口模块，也不能简单提供传统蓝牙 SPP 串口能力。

因此第一版不建议支持 iPhone 串口摄像头。iPhone 更适合走普通网络摄像头、WebRTC、HTTP stream 或 macOS 连续互通相机路线。

资料：

- Apple External Accessory: https://developer.apple.com/documentation/externalaccessory/
- Apple QA1657 External Accessory with Bluetooth: https://developer.apple.com/library/archive/qa/qa1657/_index.html

## 5. 串口带宽评估

串口传输图片的瓶颈是带宽。

常见串口有效吞吐可以按 `波特率 / 10` 粗略估算，因为 8N1 串口每 1 字节通常需要 10 bit。

| 波特率 | 理论有效速度 | 适合内容 |
|---:|---:|---|
| 115200 bps | 约 11 KB/s | 小图、状态、低频抓拍 |
| 460800 bps | 约 46 KB/s | 低分辨率 JPEG 抓拍 |
| 921600 bps | 约 92 KB/s | 较小 JPEG，低帧率 |
| 2 Mbps | 约 200 KB/s | 仍然不适合高清视频 |

参考传统串口摄像头模块：

- Adafruit VC0706 TTL Serial JPEG Camera 支持 VGA/QVGA/QQVGA，默认 38400，最高 115200 baud。
- DFRobot 0.3MP Serial JPEG Camera UART 最高 115200 bps。
- OpenMV Cam 支持 UART 通信，但通常用于控制、结果输出或小数据传输，不是把高清视频完整走 UART。

资料：

- Adafruit TTL Serial JPEG Camera: https://www.adafruit.com/product/397
- DFRobot Serial JPEG Camera: https://wiki.dfrobot.com/sen0099/
- OpenMV UART Control: https://docs.openmv.io/openmvcam/tutorial/uart_control.html

## 6. 竞品与替代方案

## 6.1 传统串口 JPEG 摄像头

代表：

- Adafruit VC0706 TTL Serial JPEG Camera
- DFRobot SEN0099 Serial JPEG Camera
- 4D Systems uCAM 系列

特点：

- 直接提供 UART。
- 协议简单。
- 可被 MCU 直接读取。
- 分辨率和帧率较低。
- 更像“拍照模块”，不是实时高清摄像头。

对本项目的启发：

- 串口摄像头协议应采用“命令 + 图片分包 + 校验 + ACK/重传”的方式。
- 不应该尝试通过串口裸传实时视频。

## 6.2 OpenMV

OpenMV 是可编程机器视觉模块，支持 MicroPython 和 UART 通信。它更适合在摄像头端完成识别，再通过串口输出识别结果。

对本项目的启发：

- 如果最终目标是算法结果，不一定要把完整图像通过串口传走。
- 可以在手机端先做识别，再通过串口输出坐标、类别、分数等结构化结果。

## 6.3 ESP32-CAM

ESP32-CAM 常用于低成本图像采集。它通常通过 Wi-Fi 做图传，通过串口做烧录、控制或调试。它证明了低成本摄像头采集可行，但也说明串口不适合承担主要视频链路。

对本项目的启发：

- 如果目标是嵌入式图传，Wi-Fi 图传 + 串口控制比纯串口图传更合理。

## 6.4 手机 webcam 工具

代表：

- DroidCam
- iVCam
- Camo
- Iriun Webcam

这些工具把手机变成电脑摄像头，但输出的是虚拟摄像头，不是串口。它们适合会议、直播、OBS，不适合只支持 COM 口的旧系统。

对本项目的启发：

- 手机摄像头采集和电脑端接收不是难点。
- 真正差异点在“串口协议输出”和“低带宽图片策略”。

## 6.5 虚拟串口工具

代表：

- Windows: com0com / hub4com
- Python: pySerial RFC2217
- Linux/macOS: socat PTY

这些工具可以把网络流、程序输出或两个应用连接成虚拟串口。

资料：

- com0com: https://sourceforge.net/projects/com0com/
- pySerial RFC2217 examples: https://pyserial.readthedocs.io/en/latest/examples.html

对本项目的启发：

- 第一版可以不写内核驱动，先用现成虚拟串口工具验证协议。
- 等协议和场景验证后，再决定是否开发自己的 Windows 虚拟串口驱动或安装器。

## 7. 推荐产品方案

## 7.1 方案 A：手机到电脑虚拟 COM 口

这是最推荐的第一版。

```text
Android 手机
  -> 摄像头采集
  -> JPEG 压缩
  -> Wi-Fi / USB 网络 / 蓝牙
  -> Windows 接收程序
  -> 虚拟 COM 口
  -> 旧软件 / 业务系统
```

优点：

- 不需要 root。
- 不需要改 Android 系统。
- 电脑端可控。
- 方便调试协议。
- 可先用现成虚拟串口工具验证。

缺点：

- 电脑端需要安装接收程序。
- 如果用虚拟串口驱动，安装和签名会增加复杂度。
- 不是真正硬件串口，主要服务 PC 软件。

适合：

- 旧 Windows 软件只支持 COM 口。
- 业务系统希望用串口协议读取图片。
- 内部采集、测试、演示。

## 7.2 方案 B：Android 手机到 USB-TTL/RS232

适合连接单片机或工控设备。

```text
Android 手机
  -> USB OTG
  -> USB 转 TTL / RS232 模块
  -> 外部设备串口
```

优点：

- 输出是真实 UART/RS232。
- 外部设备可以像读普通串口摄像头一样读数据。
- 不需要电脑中转。

缺点：

- 需要 OTG 线和串口转换器。
- Android 机型兼容性需要测试。
- 带宽低。
- 手机供电、外设供电、线缆稳定性需要处理。

适合：

- MCU 抓拍。
- 工控设备低频读取图片。
- 设备没有网络能力，只能串口通信。

## 7.3 方案 C：蓝牙 SPP 串口摄像头

```text
Android 手机
  -> 蓝牙 SPP/RFCOMM
  -> Windows 蓝牙 COM 口 / 蓝牙串口模块
  -> 上层系统
```

优点：

- 无线。
- 对电脑可表现为 COM 口。
- 不需要 Wi-Fi 网络。

缺点：

- 带宽更低。
- 配对和稳定性受设备影响。
- 不适合连续图像。
- iPhone 不适合这条路。

适合：

- 只传抓拍图片。
- 只传识别结果。
- 临时调试和低速链路。

## 7.4 方案 D：手机直接 USB CDC 串口设备

不推荐作为第一版。

原因：

- 普通 Android App 不能直接改变 USB 枚举为 CDC/ACM 设备。
- 需要系统级权限、root、内核 gadget 配置或定制硬件。
- iPhone 路线更受限制。
- 研发成本和兼容性风险高。

适合：

- 自研 Android 设备。
- 可控硬件平台。
- 有系统镜像和内核修改能力。

## 8. 串口图片协议建议

不要直接裸传图片。建议定义简单可靠的分包协议。

### 8.1 帧结构

```text
帧头:
  magic: 2 bytes，例如 0xCA 0x4D
  version: 1 byte
  type: 1 byte
  frame_id: 4 bytes
  packet_index: 2 bytes
  packet_count: 2 bytes
  payload_len: 2 bytes
  crc16: 2 bytes

负载:
  JPEG 分片数据
```

### 8.2 命令类型

| type | 含义 |
|---:|---|
| 0x01 | 开始采集 |
| 0x02 | 停止采集 |
| 0x03 | 图片数据包 |
| 0x04 | ACK |
| 0x05 | NACK |
| 0x06 | 心跳 |
| 0x07 | 设置分辨率 |
| 0x08 | 设置 JPEG 质量 |
| 0x09 | 请求单张图片 |

### 8.3 推荐传输策略

- 默认传 JPEG，不传原始 RGB/YUV。
- 默认抓拍模式，不做视频流模式。
- 初始分辨率建议 `320x240` 或 `640x480`。
- 每包 payload 控制在 128 到 512 bytes，方便 MCU 缓冲。
- 支持 ACK/NACK，避免丢包后整张图片损坏。
- 支持只传识别结果，减少带宽压力。

## 9. MVP 建议

## 9.1 第一版范围

第一版建议只做 Android + Windows。

功能：

- Android 手机端调用摄像头。
- 支持拍单张 JPEG。
- 支持设置分辨率和 JPEG 质量。
- 支持 Wi-Fi 发送到 Windows 接收端。
- Windows 接收端转发到虚拟 COM 口。
- 提供一个串口测试工具读取图片并保存为 `.jpg`。
- 定义 CAM 串口图片协议。

不做：

- iPhone。
- 直接 USB CDC 设备模式。
- 1080p 实时视频。
- 多手机接入。
- 公网远程。
- 商业化账号系统。

## 9.2 第二版范围

- Android USB OTG 到 USB-TTL/RS232。
- 蓝牙 SPP 模式。
- 串口 ACK/NACK 重传。
- 连续低帧率抓拍。
- 电脑端虚拟 COM 安装器。
- 输出结构化识别结果。

## 9.3 第三版范围

- 支持更多 Android 机型。
- 支持多分辨率动态调整。
- 支持加密和配对。
- 支持 SDK/API。
- 如有必要，再评估 iOS。

## 10. 验证实验

### 实验 1：串口图片大小和耗时测试

目标：

- 测试 `320x240`、`640x480` JPEG 在不同质量下的大小。
- 计算在 115200、460800、921600 bps 下的传输耗时。

验收：

- 找到可接受的默认分辨率和质量。
- 明确是否能满足业务使用。

### 实验 2：Android + USB-TTL 实测

目标：

- Android App 使用 `usb-serial-for-android` 打开 USB 串口。
- 发送一张 JPEG 到电脑串口助手或 MCU。

验收：

- 能稳定发送完整图片。
- 接收端能校验并保存图片。

### 实验 3：Windows 虚拟 COM 桥接

目标：

- 手机通过 Wi-Fi 发送 JPEG 到 Windows。
- Windows 接收程序写入虚拟 COM。
- 串口测试程序从 COM 口读出图片。

验收：

- 不依赖真实硬件即可完成端到端流程。

### 实验 4：蓝牙 SPP 可用性

目标：

- Android 通过 RFCOMM 连接 Windows 蓝牙 COM 或蓝牙串口模块。
- 发送小图和心跳包。

验收：

- 判断蓝牙是否适合目标场景。

## 11. 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 串口带宽不足 | 无法实时传视频 | 默认抓拍和低分辨率，必要时只传识别结果 |
| Android 机型 USB OTG 兼容性差 | 部分手机无法连接串口模块 | 先限定测试机型 |
| 手机无法直接模拟 CDC 串口 | 无法做到插上即 COM 口 | 不把该路线作为 MVP |
| Windows 虚拟串口驱动安装复杂 | 用户部署麻烦 | 原型阶段用 com0com，后续再做安装器 |
| 蓝牙 SPP 不稳定 | 传输中断、速度慢 | 只作为低速备选 |
| iOS 限制大 | 开发成本高 | 第一阶段不支持 iPhone |
| MCU 内存小 | 收不下一整张图 | 分包、流式写入 SD 卡或降低分辨率 |

## 12. 产品定位建议

不要把它定义成“手机 webcam”。普通 webcam 方案已经很多。

更准确的定位是：

> CAM 串口图像采集桥：把 Android 手机摄像头采集到的 JPEG 图片，通过虚拟 COM、蓝牙 SPP 或 USB-TTL 输出给只支持串口的电脑软件、单片机和工控设备。

核心差异点：

- 面向串口系统，而不是会议软件。
- 支持低带宽图片协议。
- 支持虚拟 COM 和真实 UART 两种输出。
- 可以作为内部采集、测试、算法输入和设备调试工具。

## 13. 最终推荐

建议分两条线验证：

### 主线：Android + Windows 虚拟 COM

这是最容易做出 MVP 的路线。

第一版目标：

- 手机拍照。
- Windows 接收。
- 虚拟 COM 输出。
- 串口工具保存 JPEG。

### 支线：Android + USB-TTL

这是最接近真实“串口摄像头”的路线。

第一版目标：

- 手机通过 OTG 打开 USB 串口。
- 发送一张 JPEG。
- MCU 或电脑串口助手接收。

不建议第一阶段做：

- iPhone。
- 手机直接 USB CDC 串口。
- 串口高清视频。

