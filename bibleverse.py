import urllib
import urllib.request
import sys

class ESVSession:
    def __init__(self, key):
        options = ['include-short-copyright=0',
                   'output-format=plain-text',
                   'include-passage-horizontal-lines=0',
                   'include-heading-horizontal-lines=0']
        self.options = '&'.join(options)
        self.baseUrl = 'http://www.esvapi.org/v2/rest/passageQuery?key=%s' % (key)

    def doPassageQuery(self, passage):
        print("input" + str(passage))
        passage = passage.split()
        print("after split" + str(passage))
        passage = '+'.join(passage)
        print("after join" + str(passage))
        url = self.baseUrl + '&passage=%s&%s' % (passage, self.options)
        page = urllib.request.urlopen(url)
        return page.read()


try:
    key = sys.argv[1]
except IndexError:
    key = 'TEST'

bible = ESVSession(key)

passage = input('Enter Passage: ')
while passage != 'quit':
    print(bible.doPassageQuery(passage))
    passage = input('Enter Passage: ')