from youtube_transcript_api import YouTubeTranscriptApi
import re
import numpy as np
from textblob import TextBlob
import pandas as pd

# These are for the wordcloud
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
#%matplotlib inline
import plotly.offline as py
#py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

#Thesea re for the streamlit and working word cloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import streamlit as st
from PIL import Image


# Get Transcript from Youtube

def getTranscript(url):
    ytID = (url[url.index('=')+1:])
    sermonDict = YouTubeTranscriptApi.get_transcript(ytID)
    sermonList = [d['text'] for d in sermonDict]
    transcript = " ".join(sermonList)
    return transcript

# Split sermon from Music

def get_sermon(text):
    # create segment list
    service_segments = []
    # find all music instances
    for m in re.finditer('\[Music\]', text):
        service_segments.append(m.end())
    # generate list of difference between segments between [Music]
    diff_segments = [j-i for i, j in zip(service_segments[:-1], service_segments[1:])]
    # create var that contains the longest segment between music and it will be understood as the sermon
    sermon = text[(service_segments[diff_segments.index(max(diff_segments))]):
                 (service_segments[diff_segments.index(max(diff_segments))+1])]
    # print sermon for troubleshooting
    # print(sermon)
    return sermon


# Full Sentiment

def get_full_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Split Lines by 100 words and get sentiment per

def split_lines_func(sermon_input):
    # Create list from text of individual entities
    newlist = [i for j in sermon_input.split() for i in (j, ' ')][:-1]

    # create list of 100 list items per string
    z = 0
    sentences = []
    while z <= len(newlist):
        sentences.append(''.join(newlist[z:z + 100]))
        z = z + 100

    # create sentence_df
    sentence_df = pd.DataFrame(sentences)
    sentence_df = sentence_df.rename(columns={0: 'sentence'})

    def detect_polarity(text):
        return TextBlob(text).sentiment.polarity

    sentence_df['polarity'] = sentence_df.sentence.apply(detect_polarity)
    sentence_df.head()

    return sentence_df

# Word Cloud


def cloud(text):
    stopwords = set(STOPWORDS)
    # Create and generate a word cloud image:
    wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot(plt)


def gauge(row):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=row.mean(),
        mode="gauge+number",
        title={'text': "Polarity"},
        # delta = {'reference': 380},
        gauge={'axis': {'range': [-1, 1]},
               'steps': [
                   {'range': [-1, 1], 'color': "red"},
                   {'range': [-0.5, 0.5], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0}}))

    return st.write(fig)


def line_chart(df,col):
    plt.xticks(df[col], df.index.values) # location, labels
    plt.plot(df[col])
    st.pyplot(plt)



def main():
    st.write("# Analyze Sermon Sentiment and WordCloud")
    st.write("[Ethan Chandler](https://ethanc.dev)")
    yt_link = st.text_area("Add full Youtube Link", value='https://www.youtube.com/watch?v=fHbmtZMkXQs&t=4585s')
    trans = get_sermon(getTranscript(yt_link))
    if yt_link is not None:
        if st.button("Analyze"):
            st.write(cloud(trans))
            sermon_table = split_lines_func(trans)
            gauge(sermon_table.polarity)
            st.write("## Sermon Transcript")
            st.write(trans)
            st.sidebar.write("Sermon Video")
            st.sidebar.video(yt_link)
            #st.sidebar.write(line_chart(sermon_table, 'polarity'))







if __name__=="__main__":
  main()



# x = getTranscript('https://www.youtube.com/watch?v=fHbmtZMkXQs&t=4583s')
#
# y = get_sermon(x)
#
# fullSentimentNum = get_full_sentiment(y)
#
# table = split_lines_func(y)
#
# print(table)

#plt.xticks( sentence_df['polarity'], sentence_df.index.values ) # location, labels
#plt.plot( sentence_df['polarity'] )
#plt.show()

