import speech_recognition as sr
import urllib.request
import urllib
import sys


botb = ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 'ruth', 'first samuel', 'second samuel',
'first kings', 'second kings', 'first chronicles', 'second chronicles', 'ezra', 'nehemiah', 'esther', 'job', 'psalms',
'proverbs', 'ecclesiastes', 'song of solomon', 'isaiah', 'jeremiah', 'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel',
'amos', 'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai', 'zechariah', 'malachi', 'matthew', 'mark',
'luke', 'john', 'acts', 'romans', 'first corinthians', 'second corinthians', 'galatians', 'ephesians', 'philippians', 'colossians',
'first thessalonians', 'second thessalonians', 'first timothy', 'second timothy', 'titus', 'philemon', 'hebrews', 'james',
'first peter', 'second peter', 'first john', 'second john', 'third john', 'jude', 'revelation']


def find_verse(input):
    input = input.lower()
    for item in botb:
        if item in input:
            book = input.find(item)

    eob = input.find(" ", book)
    eoc = input.find(" ", eob+1)
    eov = input.find(" ", eoc+1)

    return input[book:eob] + " " + input[eob:eoc] + ":" + input[eoc+1:eov]