import xml.etree.ElementTree as ET
import http.client
import codecs

conn = http.client.HTTPConnection("staging.dev.naver.com")

headers = {
    'cache-control': "no-cache",
    'postman-token': "8b767685-07a0-2c87-edda-adb97d9d359c"
    }

conn.request("GET", "/projects/d2coding/issue.xml", headers=headers)

res = conn.getresponse()
data = res.read()

with codecs.open('issue.xml','w','utf-8') as f:
    f.write(data.decode('utf-8'))

tree = ET.parse('issue.xml')
root = tree.getroot()

for child in root:
    each_board =  child[0].text + '.xml'
    conn.request("GET", "/projects/d2coding/issue/" + each_board
    , headers=headers)

    res = conn.getresponse()
    data = res.read()

    with codecs.open('boards/' + each_board, 'w', 'utf-8') as f:
        f.write(data.decode('utf-8'))
