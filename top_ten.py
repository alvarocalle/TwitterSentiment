############################################
# Top ten hash tags
# We run the script as:
# python top_ten.py <tweet_file>
############################################
import sys
import json
import string
import operator

def main():

    tweet_file = open(sys.argv[1])
    hashtags_popularity = {}
    
    for line in tweet_file:

        # JSON format
        tweet = json.loads(line)
#        print tweet

        # Ignore tweets without hashtags
        if not "entities" in tweet.keys():
            continue
        if not "hashtags" in tweet['entities'].keys():
            continue
        hashtags = tweet['entities']['hashtags']
        if hashtags == None or hashtags == []:
            continue

        # Ensure unicode encoded
        tweet_text = tweet['text'].encode('utf-8')

        for tag in hashtags:
#            print tag
            if tag['text'] in hashtags_popularity:
                hashtags_popularity[tag['text']] += 1.0
            else:
                hashtags_popularity[tag['text']] = 1.0

    hashtags_popularity_sorted = sorted(hashtags_popularity.items(),
                                        key=operator.itemgetter(1), reverse=True)

    count = 0
    for tag in hashtags_popularity_sorted:        
        print tag[0], " ", tag[1]
        count +=1 
        if count == 10:
            break
                
if __name__ == '__main__':
    main()

