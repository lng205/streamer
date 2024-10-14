# 直播应用实现

- 通过aiortc库调用WebRTC协议实现直播应用，`server.py`为服务器端代码。
- `track.py`用于生成视频流。目前使用opencv库模拟变化的RGB帧作为视频源。
- `index.html`为客户端代码，通过浏览器访问，实现视频流的接收。

## 运行

1. 安装依赖`pip install -r requirements.txt`
2. 运行服务器`python server.py`
3. 浏览器访问`http://localhost:8080`（或使用网络中的其他设备访问服务器IP的8080端口）