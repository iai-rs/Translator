from flask import Flask, request, jsonify
import datetime
import requests
import json
import sys
import os
from waitress import serve
from flask_cors import CORS
sys.path.append(os.path.abspath('../..'))
from predict import load_model, run_predict
from src.utils import get_args
from src.pangu_alpha_config import set_parse

langs = ['vi', 'ko', 'en', 'nl', 
                'de', 'ms', 'id', 'tl', 
                'mn', 'my', 'th', 'lo', 
                'km', 'lt', 'et', 'lv', 
                'hu', 'pl', 'cs', 'sk', 
                'sl', 'hr', 'bs', 'sr',
                'bg', 'mk', 'ru', 'uk', 
                'be', 'el', 'ka', 'hy', 
                'ro', 'fr', 'es', 'pt',
                'fa', 'he', 'ar', 'ps', 
                'tr', 'kk', 'uz', 
                'az', 'hi', 'ta', 
                'ur', 'bn', 'ne', 'zh']


app = Flask(__name__, static_folder='../dist')
CORS(app, resources={r"/*": {"origins": "http://147.91.175.237:52628"}})
model_predict= None
config= None

def getInfo(ipaddress):
    request_url = 'https://geolocation-db.com/jsonp/' + ipaddress
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)
    return result


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and app.static_folder:
        return app.send_static_file(path)
    return app.send_static_file('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    global model_predict
    global config

    try:
        try:
            data = request.get_json()
        except:
            error_message = {'error': 'Content-type error'}
            return jsonify(error_message), 412
        if 'input_text' not in data:
            error_message = {'error': 'Missing required filed "input_text"'}
            return jsonify(error_message), 412
        elif 'input_lang' not in data:
            error_message = {'error': 'Missing required filed "input_lang"'}
            return jsonify(error_message), 412
        elif 'output_lang' not in data:
            error_message = {'error': 'Missing required filed "output_lang"'}
            return jsonify(error_message), 412
        input_text = request.json['input_text']
        if len(input_text)>5000:
            error_message = {'error': 'Input text is limited to 1000 characters'}
            return jsonify(error_message), 412
        input_lang = request.json['input_lang']
        if input_lang not in langs:
            error_message = {'error': 'Invalid input language'}
            return jsonify(error_message), 412
        output_lang = request.json['output_lang']
        if output_lang not in langs:
            error_message = {'error': 'Invalid output language'}
            return jsonify(error_message), 412

        opt = get_args(True)
        set_parse(opt)
        output_text = run_predict(model_predict, config, opt, input_lang, output_lang, input_text)
        response_data = {'message': output_text}


        try:
            info=getInfo(request.remote_addr)
            with open("/home/kamenko/log/log.txt", 'a') as file:
                file.write(str(datetime.datetime.now().replace(microsecond=0))+'|' + request.remote_addr +'|'+ info["country_name"] +'|'+ info["city"] +'|' + input_text.replace("\n", "") +'|' + input_lang +'|' + output_text.replace("\n", "")+'|' + output_lang+'\n')
        except Exception as e:
            pass
        return jsonify(response_data)
    except Exception as s:
        error_message = {'error': s}
        return jsonify(error_message), 412

def main():
    global model_predict
    global config
    opt = get_args(True)
    set_parse(opt)
    model_predict, config = load_model(opt)
    print("Model loaded")
    prediction = run_predict(model_predict, config, opt, 'en', 'sr', "test")
    print("Initialized")

    print("Server stararted. Port 52628")
    serve(app, host="0.0.0.0", port=52628)
    #app.run(debug=True)

if __name__ == '__main__':
    main()
    