// Alternative approach using WebRTC Insertable Streams
// This allows direct frame manipulation without canvas

async function startOAKVideoDirectStream() {
    try {
        log('🔶 Starting OAK direct video stream...');

        // Create a dummy video track first
        const dummyCanvas = document.createElement('canvas');
        dummyCanvas.width = 1280;
        dummyCanvas.height = 720;
        const dummyStream = dummyCanvas.captureStream(30);
        const videoTrack = dummyStream.getVideoTracks()[0];

        // Get audio track
        const audioStream = await navigator.mediaDevices.getUserMedia({
            audio: true,
            video: false
        });

        // Create combined stream
        localStream = new MediaStream([
            videoTrack,
            ...audioStream.getAudioTracks()
        ]);

        // Use Insertable Streams to inject OAK frames directly
        if (videoTrack.insertableStreamTrack) {
            const writer = new MediaStreamTrackGenerator({ kind: 'video' });
            const writerStream = writer.writable.getWriter();

            // Replace the video track with our custom one
            localStream.removeTrack(videoTrack);
            localStream.addTrack(writer);

            // Handle OAK frames directly
            oakWs.onmessage = function (event) {
                if (event.data instanceof Blob && isOAKActive) {
                    // Convert blob to VideoFrame directly
                    createImageBitmap(event.data).then(bitmap => {
                        const frame = new VideoFrame(bitmap, {
                            timestamp: performance.now() * 1000
                        });
                        writerStream.write(frame);
                        bitmap.close();
                    });
                }
            };

            log('✅ OAK direct stream ready with Insertable Streams');
        } else {
            log('⚠️ Insertable Streams not supported, falling back to canvas');
            // Fallback to canvas method
            return startOAKVideoCanvasMethod();
        }

    } catch (error) {
        log(`❌ Error with direct stream: ${error}`);
        // Fallback to canvas method
        return startOAKVideoCanvasMethod();
    }
}
