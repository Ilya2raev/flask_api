from flask import *
from pyaudio import PyAudio, paInt32
import wave
import os
import whisper 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaaa'

def main():
    return transcribe(record_audio())

def record_audio(CHUNK=1024, FORMAT=paInt32, CHANNELS=1,
                 RATE=44100, RECORD_SECONDS=5):

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

    with wave.open(os.path.join(os.getcwd(), 'recorded', 'test.wav'), 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    return os.path.join(os.getcwd(), 'recorded', 'test.wav')

def transcribe(audio, model='tiny', save_file=True):
    model = whisper.load_model(model)
    text = model.transcribe(audio)['text']

    if not save_file:
        os.remove(audio) 
        
    return text
 
@app.route('/mic', methods=('GET', 'POST')) 
def record():
    text = None
    errors = None 
    
    if request.method == 'POST':
        try: 
            text = main()
        except Exception:
            flash('Ошибка')
    
    return render_template("file_transcribe_form.html", text=text)
 
if __name__ == '__main__': 
    app.run(debug=True)
