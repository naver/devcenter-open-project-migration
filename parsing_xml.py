import xml.etree.ElementTree as ET
import json
import requests

url = "https://api.github.com/repos/maxtortime/Hello-World/import/issues"

headers = {
    'Accept': "application/vnd.github.golden-comet-preview+json",
    'authorization': "token a8fef66d49021ee61f9f03762a3427504ccefbe8",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "f164bccc-ddcd-3865-da1b-8036db19a635",
    'User-Agent': 'postman-test'
}

tree = ET.parse('issue.xml')
root = tree.getroot()

for child in root:
    issue_json = json.dumps({"issue" : { "title" : child[4].text,
                                         "body" : child[5].text,
                                         "closed" : False if child[3].text is '0'
                                         else True
                                        }})

    response = requests.request("POST", url, data=issue_json, headers=headers)
    print(response.text)
