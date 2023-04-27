from flask import *
from pyaudio import PyAudio, paInt32
from flask_restful import Api, Resource
import wave
import os
import whisper 

app = Flask(__name__)
api = Api(app)

def record_audio(CHUNK=1024, FORMAT=paInt32, CHANNELS=1,
                 RATE=44100, RECORD_SECONDS=15):

    p = PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = [stream.read(CHUNK) for _ in range(RATE // CHUNK * RECORD_SECONDS)]

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    save_path = os.path.join(os.getcwd(), 'recorded', 'test.wav')

    with wave.open(save_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    return save_path

def transcribe(audio, model='tiny', save_file=False):
    model = whisper.load_model(model)
    text = model.transcribe(audio)['text']

    if not save_file:
        os.remove(audio) 
        
    return text

class MicrophoneAPI(Resource):
    def post(self):
        text = main()
        return make_response(jsonify(text=text), 200)

def main():
    return transcribe(record_audio())

api.add_resource(MicrophoneAPI, "/mic-api")
if __name__ == '__main__': 
    app.run(debug=True)
