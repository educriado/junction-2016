from threading import Thread
import requests
import json



calais_url = 'https://api.thomsonreuters.com/permid/calais'
access_token = 'oNqeEfDTsuBOi4OIv9nm0sHWF9pcNrLw'
headers = {
    'X-AG-Access-Token' : access_token,
    'Content-Type' : 'text/raw',
    'outputformat' : 'application/json'
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

def API_call(text, bot):
    bot_conversation = bot.get_conversation()
    temp_file_object = open('/tmp/conv.txt', 'w+')
    list_to_file(bot_conversation, temp_file)
    files = {'tmp_file': temp_file_object}
    response = requests.post(calais_url, files=files, headers=headers,
                             timeout=80)
    temp_file_object.close()
    topics = fetch_topics(response)
    existing_topics = bot.get_topics_count()
    for topic in topics:
        if topic in existing_topics:
            bot.update_topic(topic)
        else:
            bot.add_topic(topic)



def main():
    # While true loop receiven messages from the main program and telling
    # the bot to return response.
    topics_count = {'cats': 1, 'sports': 1, 'music': 1}
    topic_files  = [i + '.aiml' for i in topics_count]
    bot = Bot(topics, files)
    # We won't call the API all the time
    count = 0
    while True:

        # Read string
        print 'We have received a message.'
        #text = read_message() # NOT IMPLEMENTED
        count += 1
        if count % 5 == 0:
            # API call and topics - start new thread, it's too sloooow!
            thread = Thread(target=API_call, args=(text, bot))
            thread.start()
            count = 0
        # call brain for response 

        # return message to main program
        


class Bot:

    def __init__(self, topics, files, conversation):
        '''
        topics: initial list of topics (have to match previous AIML files)
        files:  list of AIML files used for responses.
        '''
        self.topics_count = topics
        self.files = files
        self.conversation = conversation

    def get_topics_count(self):
        return self.topics_count

    def get_conversation(self):
        return self.conversation

    def add_topic(self, topic_name):
        self.topics_count[topic_name] = 1
        # Create new words for topic, use them for new AIML file from template

    def update_topic(self, topic_name):
        self.topics_count[topic_name] += 1

    def update_conversation(self, new_phrase):
        self.conversation.append(new_phrase)


if __name__ == '__main__':
    main()