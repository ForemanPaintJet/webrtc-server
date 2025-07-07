// Using WebCodecs API for efficient video processing
// This provides the most direct path from raw frames to WebRTC

class OAKWebCodecsStream {
    constructor() {
        this.encoder = null;
        this.decoder = null;
        this.trackGenerator = null;
        this.writer = null;
    }

    async initialize() {
        try {
            // Check WebCodecs support
            if (!window.VideoEncoder || !window.VideoDecoder || !window.MediaStreamTrackGenerator) {
                throw new Error('WebCodecs not supported');
            }

            // Create video track generator
            this.trackGenerator = new MediaStreamTrackGenerator({ kind: 'video' });
            this.writer = this.trackGenerator.writable.getWriter();

            // Configure video encoder for optimal performance
            this.encoder = new VideoEncoder({
                output: (chunk) => {
                    // Encoded chunks can be sent directly over WebRTC
                    console.log('Encoded chunk:', chunk);
                },
                error: (error) => {
                    console.error('Encoder error:', error);
                }
            });

            this.encoder.configure({
                codec: 'vp8',  // or 'h264' for better compatibility
                width: 1280,
                height: 720,
                bitrate: 2000000,  // 2 Mbps
                framerate: 30
            });

            console.log('✅ WebCodecs stream initialized');
            return true;

        } catch (error) {
            console.error('❌ WebCodecs initialization failed:', error);
            return false;
        }
    }

    processRawFrame(frameData, width, height) {
        try {
            // Create VideoFrame from raw data
            const frame = new VideoFrame(frameData, {
                format: 'RGBA',
                codedWidth: width,
                codedHeight: height,
                timestamp: performance.now() * 1000
            });

            // Send directly to MediaStream
            this.writer.write(frame);
            frame.close();

        } catch (error) {
            console.error('Error processing frame:', error);
        }
    }

    getMediaStreamTrack() {
        return this.trackGenerator;
    }

    close() {
        if (this.writer) {
            this.writer.close();
        }
        if (this.encoder) {
            this.encoder.close();
        }
        if (this.trackGenerator) {
            this.trackGenerator.stop();
        }
    }
}

// Usage in the OAK client
async function startOAKWebCodecsStream() {
    const webCodecsStream = new OAKWebCodecsStream();

    if (await webCodecsStream.initialize()) {
        // Handle raw frames from WebSocket
        oakWs.onmessage = function (event) {
            if (event.data instanceof ArrayBuffer && isOAKActive) {
                // Parse raw frame data
                const dataView = new DataView(event.data);
                const width = dataView.getUint32(0, true);  // little endian
                const height = dataView.getUint32(4, true);
                const frameData = event.data.slice(8);  // Skip header

                // Process frame directly
                webCodecsStream.processRawFrame(frameData, width, height);
            }
        };

        // Create MediaStream with the WebCodecs track
        const audioStream = await navigator.mediaDevices.getUserMedia({
            audio: true,
            video: false
        });

        localStream = new MediaStream([
            webCodecsStream.getMediaStreamTrack(),
            ...audioStream.getAudioTracks()
        ]);

        log('✅ OAK WebCodecs stream ready');
        return true;
    } else {
        log('❌ WebCodecs not available, falling back to canvas');
        return false;
    }
}
