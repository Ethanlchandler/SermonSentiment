import speech_recognition as sr
import urllib.request
import urllib
import sys


# lists

botb = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', 'First Samuel', 'Second Samuel',
'First Kings', 'Second Kings', 'First Chronicles', 'Second Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms',
'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark',
'Luke', 'John', 'The Acts', 'Romans', 'First Corinthians', 'Second Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians',
'First Thessalonians', 'Second Thessalonians', 'First Timothy', 'Second Timothy', 'Titus', 'Philemon', 'Hebrews', 'James',
'First Peter', 'Second Peter', 'First John', 'Second John', 'Third John', 'Jude', 'Revelation']

# Speech Recognition

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error" : None,
        "transcription": None
    }


    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False,
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

# Bible API Class

class ESVSession:
    def __init__(self, key):
        options = ['include-short-copyright=0',
                   'output-format=plain-text',
                   'include-passage-horizontal-lines=0',
                   'include-heading-horizontal-lines=0']
        self.options = '&'.join(options)
        self.baseUrl = 'http://www.esvapi.org/v2/rest/passageQuery?key=%s' % (key)

    def doPassageQuery(self, passage):
        passage = passage.split()
        passage = '+'.join(passage)
        url = self.baseUrl + '&passage=%s&%s' % (passage, self.options)
        page = urllib.request.urlopen(url)
        return page.read()


try:
    key = sys.argv[1]
except IndexError:
    key = 'TEST'

#Bible Verse voice Parser

def find_verse(input):
    input = input.lower()
    for item in botb:
        if item in input:
            book = input.find(item)
        else:
            book = 0

    eob = input.find(" ", book)
    eoc = input.find(" ", eob+1)
    eov = input.find(" ", eoc+1)

    return input[book:eob] + " " + input[eob:eoc] + ":" + input[eoc+1:eov]

# Program


if __name__ == '__main__':
    print("Begin Speaking")
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=0)
    response = recognize_speech_from_mic(recognizer, mic)

    bible = ESVSession(key)
    voice = response['transcription']

    print('\nSuccess : {}\n Error   : {}\n\nText from Speech\n{}\n\n{}\n Bible Verse is \n {}' \
          .format(response['success'],
                  response['error'],
                  '-'*17,
                  response['transcription'],
                  'Placeholder for verse',
                  bible.doPassageQuery(find_verse(voice))
                  ))
