from flask import *
import os
import whisper
from flask_restful import Api, Resource
import wget
import urllib.request

app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aac', 'mpeg', 'mpga'}
app.config['SECRET_KEY'] = 'aaaa'

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class API(Resource):
    def post(self):
        """ Код в комментарии - API для файла в виде переменной, если понадобится"""

        url = request.json['text']
        if url == "":
            return make_response(jsonify(text='Выберите файл для загрузки'), 400)

        if url and allowed_file(url):
            try:
                upload_route = os.path.join(os.getcwd(), 'uploaded', 'test.wav')
                file = urllib.request.urlopen(url)
                if file.length > 50 * 1000 * 1000:
                    return make_response(jsonify(text='Файл превышает допустимые размеры'), 413)
                wget.download(url, out=upload_route)
                model = whisper.load_model('tiny')
                text = model.transcribe(upload_route)['text']
                os.remove(upload_route)
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

api.add_resource(API, "/api")
if __name__ == '__main__':
    app.run(debug=True)
