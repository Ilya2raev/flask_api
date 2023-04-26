from flask import *
import os
import whisper 
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aac', 'mpeg', 'mpga'}
app.config['SECRET_KEY'] = 'aaaa'

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/file', methods=('GET', 'POST')) 
def upload():
    text = None
    errors = None 
    
    if request.method == 'POST': 
        f = request.files['file'] 
        f.save(os.path.join(os.getcwd(), 'downloaded', f.filename))
        if f and allowed_file(f.filename):
            model = whisper.load_model('tiny')
            text = model.transcribe(os.path.join(os.getcwd(), 'downloaded', f.filename))['text']
            os.remove(os.path.join(os.getcwd(), 'downloaded', f.filename))
        else:
            flash('Недопустимый формат файла')
    
    return render_template("file_upload_form.html", text=text)
 
if __name__ == '__main__': 
    app.run(debug=True)

