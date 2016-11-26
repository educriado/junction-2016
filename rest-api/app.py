#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/message', methods=['POST'])
def return_message_response():
    message = request.json['content']
    # Add content to conversation
    response = 'hey buddy!'
    return jsonify({'response': response})
if __name__ == '__main__':
    app.run(debug=True)
