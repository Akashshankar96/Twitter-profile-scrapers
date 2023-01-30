
# Twitter Scraping
To build a solution that should be able to scrape the twitter data and store that in the database and allow the user to download the data with multiple data formats.



## Requirement(or rather, what I used)

 - [Python-3.8](https://www.python.org/)
 - [Pandas](https://pandas.pydata.org/)
 - [streamlit](https://streamlit.io/)
 - [snscrape]()
 - [MongoDB](https://www.mongodb.com/)



## Installation process

To install the packages, run the following command

```bash
   !pip install pandas 
   !pip instal  snscrape
   !pip install streamlit 
   !pip install pymongo

```


## Importing packages

After install the packages, run the following command to execute the packages

```bash
   import  pandas  as pd
   import  snscrape.modules.twitter as sntwitter
   import  streamlit as st
   import  pymongo as py

```
## Statement:

Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, you want to scrape the data from Twitter. You Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.
## Scrap Twitter-Approaching Methods

●	By using the “snscrape” Library, Scrape the twitter data from Twitter [Reference](https://medium.com/dataseries/how-to-scrape-millions-of-tweets-using-snscrape-195ee3594721)

●	Create a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
```bash
  
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
```
●	Store each collection of data into a document into Mongodb along with the hashtag or key word we use to  Scrape from twitter. 

```bash
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
```

## Create a GUI using streamlit
It should contain the feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count need to be scraped. After scraping, the data needs to be displayed in the page and need a button to upload the data into Database and download the data into csv and json format.


## Output view 

![project](https://user-images.githubusercontent.com/117355351/215387021-e81329fb-bf30-470b-ae03-2df6e892223a.png)
