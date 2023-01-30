
import pandas as pd
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
import json
import streamlit as st
import base64
import datetime


# In[2]:


def twitter_scraper(hastag, limit, start_date, end_date):
    tweet_list = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{hastag} since:{start_date} until:{end_date}').get_items()):
        data = [
            tweet.date,
            tweet.user.username,
            tweet.rawContent,
            tweet.lang,
            tweet.viewCount,
            tweet.replyCount,
            tweet.likeCount,
            tweet.retweetCount,
        ]
        tweet_list.append(data)
        if i > limit:
            break
            
    return tweet_list

def create_dataframe(tweet_list):
    tweet_data = pd.DataFrame(tweet_list, columns = [
        'Date Time',
        'Username',
        'Tweet Content',
        'Tweet Language',
        'Tweet Views',
        'Reply Count',
        'like Count',
        'Retweet Count',
    ]
                             )
    return tweet_data                             


# In[3]:


#title

st.title("Twitter Scraper")

# Get user input for keyword or hashtag
keyword = st.text_input("Enter keyword or hashtag:")

# Get user input for start date
start_date = st.date_input("Select start date:", key='start_date')

# Get user input for end date
end_date = st.date_input("Select end date:", key='end_date')

# Get user input for tweet limit
tweet_limit = st.slider("Enter tweet limit:", 0,50,100)

# Scrape tweets

if st.button("Scrape tweets"):
        tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
        tweet_data = create_dataframe(tweets)
        st.dataframe(tweet_data)
        

# Upload to MongoDB
if st.button("Upload to MongoDB"):
    
        tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
        tweet_data = create_dataframe(tweets)

        client = MongoClient('mongodb://localhost:27017/')
        db = client['twitter_db_streamlit']
        collection = db['tweets']
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
                "hashtag_or_keyword": keyword,
                "timestamp": current_timestamp,
                "tweets": json.loads(tweet_data.to_json(orient='records'))
            }
        
        collection.insert_one(data)
        st.success("Uploaded to MongoDB!")

# Download as CSV
if st.button("Download as CSV"):
        tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
        tweet_data = create_dataframe(tweets)

        st.write("Saving dataframe as CSV")
        csv = tweet_data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="tweet_data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

# Download as JSON
if st.button("Download as JSON"):
        tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
        tweet_data = create_dataframe(tweets)
        
        st.write("Saving dataframe as JSON")
        json_string = tweet_data.to_json(indent=2)
        b64 =     base64.b64encode(json_string.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="tweet_data.json">Download JSON File</a>'
        st.markdown(href, unsafe_allow_html=True)
