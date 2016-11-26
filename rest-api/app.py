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
conversation = ['On September 28, 2015, karate was featured on a shortlist along with baseball, softball, skateboarding, surfing, and sport climbing to be considered for inclusion in the 2020 Summer Olympics. On June 1, 2016, the International Olympic Committees executive board announced they were supporting the inclusion of all five sports (counting baseball and softball as only one sport) for inclusion in the 2020 Games.']
bot = Bot(topics_count, topic_files, conversation)


@app.route('/message', methods=['POST'])
def return_message_response():
    message = request.json['content']
    # Add content to conversation
    bot.update_conversation(message)
    bot.threaded_call()
    response = bot.answer_back()
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
