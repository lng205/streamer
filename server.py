from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from track import Track, SharedVideoSource

# Create a shared video source
video_source = SharedVideoSource()


async def index(request):
    return web.FileResponse("index.html")


async def offer(request: web.Request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    video_track = Track(video_source)
    pc.addTrack(video_track)

    # Set remote description and create an answer
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response(
        {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )


app = web.Application()
app.add_routes([web.post("/offer", offer), web.get("/", index)])

if __name__ == "__main__":
    web.run_app(app, port=8080)
