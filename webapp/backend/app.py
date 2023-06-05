from flask import Flask, render_template, request, jsonify
import time
import sys
import os
# sys.path.append(os.path.abspath('../..'))
# from predict import load_model, run_predict
# from src.utils import get_args
# from src.pangu_alpha_config import set_parse

from flask_cors import CORS

app = Flask(__name__, static_folder='../dist')
CORS(app, resources={r"/*": {"origins": "http://147.91.175.237:52628"}})
model_predict= None
config= None


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
        data = request.get_json()

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
        input_lang = request.json['input_lang']
        output_lang = request.json['output_lang']

        # opt = get_args(True)
        # set_parse(opt)
        # output_text = run_predict(model_predict, config, opt, input_lang, output_lang, input_text)
        output_text=input_text+' | '+input_lang+' | '+input_lang
        response_data = {'message': output_text}
        return jsonify(response_data)
    except Exception as s:
        error_message = {'error': s}
        return jsonify(error_message), 412

def main():
    global model_predict
    global config
    # opt = get_args(True)
    # set_parse(opt)
    # model_predict, config = load_model(opt)
    print("Model loaded")
    # prediction = run_predict(model_predict, config, opt, 'en', 'sr', "test")
    print("Initialized")

    print("Server stararted. Port 52628")
    from waitress import serve
    serve(app, host="0.0.0.0", port=52628)
    #app.run(debug=True)


if __name__ == '__main__':
    main()
    