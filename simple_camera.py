from flask import Flask

app = Flask(__name__)

@app.route('/')
def camera():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Browser Camera</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
            background-color: #f0f0f0;
        }
        
        h1 {
            color: #333;
            margin-bottom: 30px;
        }
        
        video {
            width: 100%;
            max-width: 640px;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 10px;
            background-color: #000;
            margin-bottom: 20px;
        }
        
        button {
            padding: 12px 24px;
            margin: 10px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            color: white;
        }
        
        .start-btn {
            background-color: #4CAF50;
        }
        
        .stop-btn {
            background-color: #f44336;
        }
        
        button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        
        .status {
            margin-top: 20px;
            padding: 10px;
            background-color: white;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>📷 Simple Browser Camera</h1>
    
    <video id="video" autoplay muted playsinline></video>
    
    <div>
        <button id="startBtn" class="start-btn" onclick="startCamera()">Start Camera</button>
        <button id="stopBtn" class="stop-btn" onclick="stopCamera()" disabled>Stop Camera</button>
    </div>
    
    <div class="status">
        <p id="status">Click "Start Camera" to begin</p>
    </div>

    <script>
        const video = document.getElementById('video');
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const status = document.getElementById('status');
        
        let stream = null;
        
        function updateStatus(message) {
            status.textContent = message;
            console.log(message);
        }
        
        async function startCamera() {
            try {
                updateStatus('Starting camera...');
                
                // Request camera access
                stream = await navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                });
                
                // Display video
                video.srcObject = stream;
                
                // Update UI
                startBtn.disabled = true;
                stopBtn.disabled = false;
                updateStatus('Camera is active');
                
            } catch (error) {
                console.error('Camera error:', error);
                updateStatus('Error: ' + error.message);
            }
        }
        
        function stopCamera() {
            if (stream) {
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
                stream = null;
                video.srcObject = null;
            }
            
            // Update UI
            startBtn.disabled = false;
            stopBtn.disabled = true;
            updateStatus('Camera stopped');
        }
        
        // Cleanup on page close
        window.addEventListener('beforeunload', stopCamera);
        
        // Check if camera is supported
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            updateStatus('Camera not supported in this browser');
            startBtn.disabled = true;
        }
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    print("Starting Simple Browser Camera...")
    print("Access at: http://localhost:3000")
    app.run(debug=True, host='0.0.0.0', port=3000)
