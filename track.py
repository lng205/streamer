import time
import numpy as np
import cv2
from aiortc import MediaStreamTrack
from av import VideoFrame

from fractions import Fraction


class SyntheticVideoStreamTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        self.width = 640
        self.height = 480
        self.frame_rate = 30
        self.frame_count = 0  # Use a frame counter

    async def recv(self):
        # Time elapsed since the start (for dynamic content)
        elapsed_time = time.time()

        # Create a blank image (black background)
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Generate dynamic color
        color = (
            int(127 + 127 * np.sin(elapsed_time)),
            int(127 + 127 * np.sin(elapsed_time + 2)),
            int(127 + 127 * np.sin(elapsed_time + 4)),
        )

        frame[:] = color

        # Add dynamic text to the frame
        cv2.putText(
            frame,
            f"Frame: {self.frame_count}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        # Convert to a WebRTC-compatible VideoFrame
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")

        # Update the PTS and time_base using the frame counter
        self.frame_count += 1
        video_frame.pts = self.frame_count
        video_frame.time_base = Fraction(
            1, self.frame_rate
        )  # Proper fraction for time_base

        return video_frame
