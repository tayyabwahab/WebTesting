import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64
import random

class CameraConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.last_frame_time = None
        self.bold_step_one = False 
        super().__init__()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    def generate_joint_data(self):
        # Generate random values for joints
        joints_data = {
            'hip_left': random.randint(60, 180),
            'hip_right': random.randint(60, 180),
            'knee_left': random.randint(70, 190),
            'knee_right': random.randint(70, 190)
        }
        
        # Define acceptable ranges for each joint
        ranges = {
            'hip_left': {'step1': (65, 85), 'step2': (155, 175)},
            'hip_right': {'step1': (65, 85), 'step2': (155, 175)},
            'knee_left': {'step1': (70, 90), 'step2': (165, 185)},
            'knee_right': {'step1': (70, 90), 'step2': (165, 185)}
        }

        remarks = {}
        for joint, value in joints_data.items():
            if ranges[joint]['step1'][0] <= value <= ranges[joint]['step1'][1] or \
               ranges[joint]['step2'][0] <= value <= ranges[joint]['step2'][1]:
                remarks[joint] = 'Great'
            elif value < min(ranges[joint]['step1'][0], ranges[joint]['step2'][0]) or \
                 value > max(ranges[joint]['step1'][1], ranges[joint]['step2'][1]):
                remarks[joint] = 'Dangerous'
            else:
                remarks[joint] = 'Warning'
        
        return joints_data, remarks

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        frame_data = text_data_json['frame']
        show_colored_overlay = text_data_json.get('show_colored_overlay', False)
        show_angles_on_overlay = text_data_json.get('show_angles_on_overlay', False)
        show_info_table = text_data_json.get('show_info_table', False)
        if 'selected_exercise' in text_data_json:
            self.selected_exercise = text_data_json['selected_exercise']
            print("Exercise selected:", self.selected_exercise)
        # Decode the base64 image
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        np_arr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Generate random joint data and remarks
        joints_data, remarks = self.generate_joint_data()

        # Apply the image_set filter with toggle states and joint data
        processed_frame = self.image_set(frame, joints_data, remarks, 
                                         show_colored_overlay, show_angles_on_overlay, show_info_table)
        _, buffer = cv2.imencode('.jpg', processed_frame)
        processed_frame_data = base64.b64encode(buffer).decode('utf-8')
        print(self.bold_step_one)
        # Send both the processed frame, joint data, and step bolding information
        await self.send(text_data=json.dumps({
            'processed_frame': f'data:image/jpeg;base64,{processed_frame_data}',
            'joints_data': joints_data,
            'remarks': remarks,
            'bold_step_one': self.bold_step_one  # Send the bolding preference
        }))

    def image_set(self, img, joints_data, remarks, show_colored_overlay, show_angles_on_overlay, show_info_table):
        # Convert to grayscale and process
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        equ = cv2.equalizeHist(gray) 
        blurred = cv2.GaussianBlur(src=equ, ksize=(3, 5), sigmaX=0.5) 
        edges = cv2.Canny(blurred, 70, 135)

        # Overlay optional features
        if show_colored_overlay:
            overlay = img.copy()
            cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)

        if show_angles_on_overlay:
            for joint, angle in joints_data.items():
                cv2.putText(img, f'{joint}: {angle}', (10, 30 + 20 * list(joints_data.keys()).index(joint)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        if show_info_table:
            y_offset = 20
            for joint, remark in remarks.items():
                cv2.putText(img, f'{joint}: {remark}', (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                y_offset += 20

        return edges
