import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from track import SyntheticVideoStreamTrack as Track
import json

pcs = set()


async def index(request):
    return web.FileResponse("index.html")


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("ICE connection state is %s" % pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # Use the synthetic video track as the video source
    video_track = Track()
    pc.addTrack(video_track)

    # Set remote description and create an answer
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response(
        {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )


async def websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    pc = RTCPeerConnection()
    pcs.add(pc)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            data = json.loads(msg.data)
            if "sdp" in data:
                offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
                await pc.setRemoteDescription(offer)
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                await ws.send_json(
                    {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
                )

            elif "candidate" in data:
                candidate = data["candidate"]
                if candidate:
                    await pc.addIceCandidate(candidate)

        elif msg.type == web.WSMsgType.ERROR:
            print(f"WebSocket connection closed with exception {ws.exception()}")

    return ws


async def cleanup():
    # Close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


app = web.Application()
app.add_routes(
    [web.post("/offer", offer), web.get("/ws", websocket), web.get("/", index)]
)

if __name__ == "__main__":
    web.run_app(app, port=8080)
