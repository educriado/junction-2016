import requests
import os
import json

def saveFile(file_name, output_dir, content):
    output_file_name = os.path.basename(file_name)
    output_file = open(os.path.join(output_dir, output_file_name), 'wb')
    output_file.write(content.encode('utf-8'))
    output_file.close()

file_name = 'text.txt'
f_object = open(file_name, 'rb')
files = {
    'test_text': f_object
}
calais_url = 'https://api.thomsonreuters.com/permid/calais'
access_token = 'oNqeEfDTsuBOi4OIv9nm0sHWF9pcNrLw'
headers = {
    'X-AG-Access-Token' : access_token,
    'Content-Type' : 'text/raw',
    'outputformat' : 'application/json'
    }

response = requests.post(calais_url, files=files, headers=headers, timeout=80)
print 'status code: %s' % response.status_code
content = response.text
# Response in SocialTag: importance: 1, 2, 3 (from more important to less)
# Topic tag
# print 'Results received: %s' % content
saveFile('response.json', '.', content)

# Get interesting json response terms
# Use topics and entities
# JSON content is a dictionary
parsed_content = json.loads(content)
# print parsed_content['doc']
for key, value in parsed_content.iteritems():
    if '_typeGroup' in value:
        # Filter topics
        if value['_typeGroup'] == 'topics':
            print 'Found topic: {}'.format(value['name'])