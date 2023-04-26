from flask import *
import os
import whisper
from flask_restful import Api, Resource
import wget

app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aac', 'mpeg', 'mpga'}
app.config['SECRET_KEY'] = 'aaaa'

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Api(Resource):
    def post(self):
        """ Код в комментарии - API для файла в виде переменной, если понадобится"""

        url = request.json['text']
        if url == "":
            return make_response(jsonify(text='Выберите файл для загрузки'), 400)

        if url and allowed_file(url):
            try:
                wget.download(url, out=os.path.join(os.getcwd(), 'uploaded', 'test.wav'))
                model = whisper.load_model('tiny')
                text = model.transcribe(os.path.join(os.getcwd(), 'uploaded', 'test.wav'))['text']
                os.remove(os.path.join(os.getcwd(), 'uploaded', 'test.wav'))
                return make_response(jsonify(text=text), 200)
            except Exception:
                return make_response(jsonify(text='Не удалось загрузить файл'), 400)
        
        else:
            return make_response(jsonify(text='Недопустимый формат файла'), 400)

        # if 'file' not in request.files:
        #     return make_response(jsonify(text='No file part in the request'), 400)
            
        # file = request.files['file']
        # if file.filename == '':
        #     return make_response(jsonify(text='Выберите файл для загрузки'), 400)
        
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(os.getcwd(), 'uploaded', file.filename))
        #     model = whisper.load_model('tiny')
        #     text = model.transcribe(os.path.join(os.getcwd(), 'uploaded', filename))['text']
        #     os.remove(os.path.join(os.getcwd(), 'uploaded', filename))
        #     return make_response(jsonify(text=text), 200)
        
        # else:
        #     return make_response(jsonify(text='Недопустимый формат файла'), 400)

api.add_resource(Api, "/api")
if __name__ == '__main__':
    app.run(debug=True)
