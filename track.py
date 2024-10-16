import cv2
import threading
import time
from aiortc import MediaStreamTrack
from av import VideoFrame
from fractions import Fraction

# Shared video source class to capture frames in the background
class SharedVideoSource:
    def __init__(self, camera_index=0, frame_rate=30):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception(f"Unable to open video source {camera_index}")

        self.frame_rate = frame_rate
        self.frame = None
        self.lock = threading.Lock()
        self.stopped = False

        # Start background thread to capture frames
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        """Continuously capture frames in a background thread."""
        while not self.stopped:
            with self.lock:
                ret, frame = self.cap.read()
                if ret:
                    self.frame = frame
            time.sleep(1 / self.frame_rate)

    def get_frame(self):
        """Return the most recent frame."""
        with self.lock:
            return self.frame

    def stop(self):
        """Stop the video capture."""
        self.stopped = True
        self.thread.join()
        self.cap.release()


# Track class for each WebRTC connection, using the shared video source
class Track(MediaStreamTrack):
    kind = "video"  # This is a video track

    def __init__(self, video_source: SharedVideoSource, frame_rate=30):
        super().__init__()  # Initializes as a MediaStreamTrack
        self.video_source = video_source
        self.frame_rate = frame_rate
        self.frame_count = 0

    async def recv(self):
        # Retrieve the latest frame from the shared video source
        frame = self.video_source.get_frame()
        if frame is None:
            raise Exception("No frame available")

        # Convert to AV VideoFrame
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")

        # Increment frame count and set presentation timestamp
        self.frame_count += 1
        video_frame.pts = self.frame_count
        video_frame.time_base = Fraction(1, self.frame_rate)

        return video_frame
