# File: webrtc.py

import asyncio
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaStreamTrack
from aiortc.contrib.signaling import object_from_string, object_to_string

class RTCConnection:
    def __init__(self):
        self.pc = None
        self.remote_description = None
        self.data_channel = None
        self.pending_candidates = []

    async def create_offer(self):
        if not self.pc:
            self.pc = RTCPeerConnection()
            self.pc.oniceconnectionstatechange = self.on_ice_connection_state_change
            self.pc.ondatachannel = self.on_data_channel

        self.data_channel = self.pc.createDataChannel('frames')

        @self.data_channel.on('message')
        def on_message(message):
            # Process received frame data
            print('Received frame:', message)

        return await self.pc.createOffer()

    async def set_remote_description(self, sdp_data):
        if not self.pc:
            self.pc = RTCPeerConnection()
            self.pc.oniceconnectionstatechange = self.on_ice_connection_state_change
            self.pc.ondatachannel = self.on_data_channel

        try:
            sdp = sdp_data['sdp']
            sdp_type = sdp_data['type']

            if sdp_type not in ['offer', 'answer', 'pranswer', 'rollback']:
                raise ValueError(f"Invalid SDP type: {sdp_type}")

            self.remote_description = RTCSessionDescription(
                sdp_type, sdp
            )

            await self.pc.setRemoteDescription(self.remote_description)

            for candidate in self.pending_candidates:
                await self.pc.addIceCandidate(candidate)
            self.pending_candidates = []

            if sdp_type == 'offer':
                answer = await self.pc.createAnswer()
                await self.pc.setLocalDescription(answer)
                return {'sdp': self.pc.localDescription.sdp, 'type': self.pc.localDescription.type}

        except Exception as e:
            # Handle exceptions gracefully (e.g., log, handle_disconnect())
            print(f"Error setting remote description: {e}")

    async def add_ice_candidate(self, candidate):
        if self.pc and self.remote_description:
            ice_candidate = RTCIceCandidate(
                candidate['candidate'], candidate['sdpMid'], candidate['sdpMLineIndex']
            )
            if self.remote_description:
                await self.pc.addIceCandidate(ice_candidate)
            else:
                self.pending_candidates.append(ice_candidate)

    def on_ice_connection_state_change(self):
        if self.pc and self.pc.iceConnectionState == 'failed':
            self.pc.close()
            self.pc = None

    def on_data_channel(self, channel):
        self.data_channel = channel
        @channel.on('message')
        def on_message(message):
            # Process received frame data
            print('Received frame:', message)
