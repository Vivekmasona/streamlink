from flask import Flask, request, jsonify
from streamlink import Streamlink

app = Flask(__name__)

@app.route('/get_audio_stream', methods=['GET'])
def get_audio_stream():
    """
    API endpoint jo YouTube URL se best stream ka direct URL return karta hai.
    Example usage:
        GET /get_audio_stream?url=https://www.youtube.com/watch?v=XXXXXXXXXXX
    """
    youtube_url = request.args.get('url')
    if not youtube_url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        # Streamlink session create karte hain
        session = Streamlink()
        streams = session.streams(youtube_url)

        if not streams:
            return jsonify({'error': 'No streams found for the provided URL'}), 404

        # Yahan hum "best" stream choose kar rahe hain. 
        # Aap specific quality ya audio-only stream ke liye filtering kar sakte hain.
        stream = streams.get('best')
        if not stream:
            # Fallback: sabse pehla available stream choose karen
            stream = next(iter(streams.values()))

        stream_url = stream.to_url()
        return jsonify({'stream_url': stream_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Host aur port ko customize kar sakte hain
    app.run(host='0.0.0.0', port=5000, debug=True)
