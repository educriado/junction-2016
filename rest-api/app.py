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
conversation = ['Nature, in the broadest sense, is the natural, physical, or material world or universe. Nature can refer to the phenomena of the physical world, and also to life in general. The study of nature is a large part of science. Although humans are part of nature, human activity is often understood as a separate category from other natural phenomena.']
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
    app.run('0.0.0.0')
