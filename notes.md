# 笔记

## WebRTC协议栈

WebRTC调用了多个其他协议：ICE, STUN, TURN, DTLS, SRTP, RTP/RTCP, SCTP, UDP, TCP

### 寻找连接路径

- ICE用于寻找最优P2P路径。通讯双方会实时交换自身的所有网卡地址，并不断寻找更优的地址对。
- STUN用于寻找内网设备的公网地址
- TURN用于在直接连接建立失败时提供中继

### 可靠传输

- DTLS用于加密全部WebRTC连接数据
- SCTP用于实现数据流的可靠传输，基于DTLS

### 媒体传输

- SRTP用于加密媒体数据
- RTP/RTCP用于传输数据和获取控制信息，默认基于UDP，UDP被墙等场景会使用TCP

## WebRTC连接建立逻辑

WebRTC首先需要外部协议来协商SDP(Session Description Protocol)，可使用HTTP。
请求方会先生成自身的SDP内容，具体为一段长文本，包括收/发需求，视频/音频信息，编码方式，传输协议栈，网络信息等。
接收方会生成自身的SDP并返回给发送方，双方分别存储本地及目标的SDP至WebRTC接口。
此时WebRTC连接建立完成，协议的实现会在内部管理后续数据交互（例如服务器将请求的track发送给客户端）

## ICE实时更新

ICE(Iteractive Connection Establishment)需要实时更新网络信息，包括ip，连通性，带宽等信息。
ICE信息交换也不在WebRTC内部实现，通常使用WebSocket实现。在C/S架构中，主要由C端发送ICE信息，S端将其更新至WebRTC接口。

## Track的recv方法调用

在连接建立后，WebRTC会不断调用Track的recv方法。对于实际的视频源，recv会在拉取下一帧时产生阻塞。但对于模拟产生的数据，则需要手动延时来控制帧率。