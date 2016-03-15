# twitter-streaming
Simple Text Mining

#Purpose
The repository is basically for streaming tweets from twitter. It tracks a word given as input to filter the results and then keeps a count of all the words greater than 3 characters in length (to avoid unnecessary punctuation being included). Every 30-seconds the count is updated and if a word has not been found for the last 30-seconds its count decreases by one. Once the count reaches zero its removed from the dictionary. Every minute the count of each of the words in the dictionary is printed.

#Usage
Firstly, you need the tweepy , which you can get from https://github.com/tweepy/tweepy.
Now take this repository and edit the file streamTwitter.py to include your API keys. A tutorial for the same can be found at: http://adilmoujahid.com/posts/2014/07/twitter-analytics/ .
You are good to go.
