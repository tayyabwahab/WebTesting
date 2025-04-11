let socket;

self.onmessage = function(event) {
    const { type, data } = event.data;
    if (type === 'frame') {
        processFrame(data);
    } else if (type === 'start') {
        socket = new WebSocket(data.wsUrl);

        socket.onopen = function() {
            console.log('WebSocket connection established');
        };

        socket.onmessage = function(event) {
            console.log('Message from server ', event.data);
        };

        socket.onerror = function(error) {
            console.log('WebSocket error: ', error);
        };
    }
};

function processFrame(blob) {
    const reader = new FileReader();
    reader.onloadend = function() {
        const base64data = reader.result.split(',')[1];
        socket.send(JSON.stringify({ frame: base64data }));
    }
    reader.readAsDataURL(blob);
}
