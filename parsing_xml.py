import xml.etree.ElementTree as ET
import json
import requests
import os
import time

url = "https://api.github.com/repos/maxtortime/Hello-World/import/issues"

headers = {
    'Accept': "application/vnd.github.golden-comet-preview+json",
    'authorization': "token a8fef66d49021ee61f9f03762a3427504ccefbe8",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "f164bccc-ddcd-3865-da1b-8036db19a635",
    'User-Agent': 'postman-test'
}

for file_name in os.listdir('./boards/'):
    tree = ET.parse(str('./boards/' + file_name))
    root = tree.getroot()

    try:
        comments = [
            {
                'date' : comment.find('pubDate').text if comment.find('pubDate') != None else '0',
                'desc' : comment.find('description').text if comment.find('description') != None else 'None'
            }
        for comment in root[13].findall('item')]
    except IndexError:
        continue

    issue_json = json.dumps({"issue" : { "title" : root[4].text,
                                         "body" : root[5].text,
                                         "closed" : False if root[3].text is '0'
                                         else True
                                        },
                             "comments" : [
                                {
                                    "created_at" :
                                    time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                    time.localtime(int(comment['date']))),
                                    "body" : comment['desc']
                                }
                             for comment in comments]})

    response = requests.request("POST", url, data=issue_json, headers=headers)
    print(response.text)
