#Import the necessary libraries
import tweepy           
import json         #To parse the data
import time         #To use time functionality
import re           #To use Regex

#User credentials to access Twitter API 
access_token = ""			#Add the keys here
access_token_secret = ""			
consumer_key = "" 	
consumer_secret = ""  

#Word that is tracked
keyWord=raw_input("Enter the desired Keyword: ")

class StdOutListener(tweepy.StreamListener):
    dict={}             #To store the words,with their count and time stamp
    list30=[]           #To store all the words for a 30-second period
    printTime=0         #To check whether its time to print or not
    timeStamp=0         #Representation of 30-second periods
    delList=[]          #The words that need to be deleted
    
    def __init__(self):
        StdOutListener.last=time.time()     #To store the actually clock count

    def on_data(self, data):
        msg=json.loads(data)                #Parsing tweet data
        try:
            if 'text' in msg:
                words=msg['text'].split()                   #Spliting the tweet into words
                StdOutListener.list30.extend(words)         #Adding words to our buffer
        except:
           del msg;                                         #In case the msg is truncated
        
        if (time.time()-StdOutListener.last)>30:
            for word in StdOutListener.list30: 
                if re.match(r'^\w{4,}$',word.lower()):              #Regex to check for words greater than 4 characters in length
                    #Incrementing word count if already present else adding it to dict, also updating time stamp
                    if StdOutListener.dict.has_key(word.lower()):
                        StdOutListener.dict[word.lower()][0]+=1   
                        StdOutListener.dict[word.lower()][1]=StdOutListener.timeStamp
                    else:
                        StdOutListener.dict[word.lower()]=[1,StdOutListener.timeStamp]
            
            #Checking for words that were not found 
            for word in StdOutListener.dict:
                if StdOutListener.dict[word][1]!=StdOutListener.timeStamp:
                    StdOutListener.dict[word][0]-=1
                    if StdOutListener.dict[word][0]<=0:
                        StdOutListener.delList.append(word)
            
            #Deleting words in delList
            for elem in StdOutListener.delList:
               del StdOutListener.dict[elem]
            
            #Reseting Buffer lists
            StdOutListener.delList=[]
            StdOutListener.list30=[]
            
            #Printing the required output
            if StdOutListener.printTime == 1:
                print"\nTime Passed: %d mins"%((StdOutListener.timeStamp+1)/2)
                print "Count\tWord"
                for key in StdOutListener.dict :
                    if StdOutListener.dict[key][0]>1:
                        print "%d\t%s"%(StdOutListener.dict[key][0],key)

            StdOutListener.printTime=1-StdOutListener.printTime         #Alternating between print and dont print
            StdOutListener.last=time.time()                             #Updating time
            StdOutListener.timeStamp+=1                                 #Updating time stamp
        return True

    #def on_error(self, status):
     #   print status                                                    #To output Error status


if __name__ == '__main__':
    l = StdOutListener()                                                #Creates object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)           #Authenticating access
    auth.set_access_token(access_token, access_token_secret)            
    
    
    stream = tweepy.Stream(auth, l)                                     #Setting up stream with required keyword
    stream.filter(track=[keyWord])                          
