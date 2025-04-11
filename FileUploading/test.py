# test.py
import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def process_frame(frame):
    # Your frame processing logic here
    print(f"Processing frame: {frame}")

def receive_frames():
    channel_layer = get_channel_layer()
    
    def frame_received(event):
        frame = event["frame"]
        process_frame(frame)

    async_to_sync(channel_layer.group_add)("camera_frames", "test_consumer")
    
    try:
        while True:
            async_to_sync(channel_layer.receive)("test_consumer")
    except KeyboardInterrupt:
        async_to_sync(channel_layer.group_discard)("camera_frames", "test_consumer")

if __name__ == "__main__":
    receive_frames()