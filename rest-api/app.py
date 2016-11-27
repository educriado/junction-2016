#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from bot import Bot


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

topics_count = {'cats': 1, 'sports': 1, 'music': 1}
topic_files = [i + '.aiml' for i in topics_count]
conversation = []
bot = Bot(topics_count, topic_files, conversation)

# http://121.0.0.0:5000/message?question=what
@app.route('/message')
def return_message_response():
    message = request.args.get('question')
    # Add content to conversation
    bot.update_conversation(message)
    bot.threaded_call()
    print message
    response = bot.dummy_answer(message)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run()