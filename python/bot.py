from threading import Thread
import requests
import json
import time

calais_url = 'https://api.thomsonreuters.com/permid/calais'
access_token = 'oNqeEfDTsuBOi4OIv9nm0sHWF9pcNrLw'
headers = {
    'X-AG-Access-Token': access_token,
    'Content-Type': 'text/raw',
    'outputformat': 'application/json'
}


def fetch_topics(response):
    # Look for topics values in the _typeGroup responses and add them to topics
    # or update the count
    found_topics = []
    parsed_content = json.loads(response.text)
    for key, value in parsed_content.iteritems():
        if '_typeGroup' in value:
            # Filter topics
            if value['_typeGroup'] == 'topics':
                print 'Found topic: {}'.format(value['name'])
                found_topics.append(value['name'])
    return found_topics


def list_to_file(list, file_object):
    for item in list:
        file_object.write('{}\n'.format(item))


def api_call(bot):
    # type: (object) -> object
    temp_file_object = open('/tmp/conv.txt', 'w+')
    list_to_file(bot.conversation, temp_file_object)
    files = {'tmp_file': temp_file_object}
    response = requests.post(calais_url, files=files, headers=headers,
                             timeout=80)
    temp_file_object.close()
    topics = fetch_topics(response)
    for topic in topics:
        if topic in bot.topics_count:
            bot.update_topic(topic)
            print 'We update the topic: {}'.format(topic)
        else:
            bot.add_topic(topic)
            print 'We add the topic: {}'.format(topic)


def main():
    # While true loop receiven messages from the main program and telling
    # the bot to return response.
    topics_count = {'cats': 1, 'sports': 1, 'music': 1}
    topic_files = [i + '.aiml' for i in topics_count]
    conversation = 'On September 28, 2015, karate was featured on a shortlist along with baseball, softball, skateboa' \
                   'rding, surfing, and sport climbing to be considered for inclusion in the 2020 Summer Olympics. On' \
                   ' June 1, 2016, the International Olympic Committees executive board announced they were supportin' \
                   'g the inclusion of all five sports (counting baseball and softball as only one sport) for inclusi' \
                   'on in the 2020 Games.'
    bot = Bot(topics_count, topic_files, conversation)
    # We won't call the API all the time
    count = 0
    test_count = 0
    while test_count < 10:

        # Read string
        print 'We have received a message.'
        # text = read_message() # NOT IMPLEMENTED
        count += 1
        if count % 5 == 0:
            # API call and topics - start new thread, it's too sloooow!
            thread = Thread(target=api_call, args=(bot,))
            thread.start()
            count = 0
        # call brain for response 
        print 'Call for AIML response'
        # return message to main program
        print 'We send message back'
        # Right now simulate that it takes time to receive a response
        time.sleep(5)


class Bot:
    def __init__(self, topics, files, conversation):
        '''
        topics: initial list of topics (have to match previous AIML files)
        files:  list of AIML files used for responses.
        '''
        self.topics_count = topics
        self.files = files
        self.conversation = conversation

    def add_topic(self, topic_name):
        self.topics_count[topic_name] = 1
        # Create new words for topic, use them for new AIML file from template

    def update_topic(self, topic_name):
        self.topics_count[topic_name] += 1

    def update_conversation(self, new_phrase):
        self.conversation.append(new_phrase)

    def finish_conversation(self):
        # Save conversation in file, save topics in file
        f_conv = open('conversation.txt', 'w')
        for item in bot.conversation.split():
            f_conv.write(item)
        f_conv.close()
        f_topic = open('topics.txt', 'w')
        for topic, count in bot.topics_count:
            f_topic.write('{}, {}'.format(topic, count))
        f_topic.close()


if __name__ == '__main__':
    main()
