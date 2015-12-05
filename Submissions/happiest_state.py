####################################################################
# Find the happiest state
# The program needs two inputs (text files):
# Input1: Sentiment dictionary ("AFINN-111")
# Input2: Tweets ("three_minutes_tweets.json")
# We run the program as:
# python happiest_state.py AFINN-111.txt three_minutes_tweets.json
#####################################################################
import sys
import json
import re

# Read sentiment_file and build dictionary
def dictFromSentimentFile(sf):
    scores = {}
    for line in sf:
        term, score = line.split('\t')
        term = re.sub(r"\s+", '-', term)  # Replace whitespace by single dash
        scores[term] = int(score)
    return scores

# Read tweet_file. Extract each tweet per line. Append to tweet_data list.
def readTweetFile(tf):
    tweet_data  = []
    tweet_state = []

    for line in tf:
        response = json.loads(line)
        
        # Ignore badly formatted tweets
        if not "text" in response.keys():
            continue
        
        # Ignore non-US tweets and those without state
        if not "place" in response.keys() or response["place"] == None:
            continue
        if not response["place"]["country_code"] == "US":
            continue
        if not response["place"]["full_name"]:
            continue

        tweet_data.append(response["text"])
        tweet_state.append(response["place"]["full_name"][-2:])

    return tweet_data, tweet_state

def filterTweet(et):
    # Remove punctuations and non-alphanumeric chars from tweets
    pattern = re.compile('[^A-Za-z0-9]+')
    et = pattern.sub(' ', et)
    
    words = et.split()

    # Filter unnecessary words
    for w in words:
        if w.startswith("RT") or w.startswith("www") or w.startswith("http"):
            words.remove(w)

    return words

def computeTweetSentiment(td, sc):
    sentiments = []
	
    for t in td:
        sentiment = 0.0
        words = filterTweet( t.encode('utf-8') )

        # Tweet's sentiment (sum up sentiments of individual words)
        for w in words:
            if w in sc:
                sentiment = sentiment + sc[w]

        sentiments.append(sentiment)
	
    return sentiments

def computeHappiestState(t_state, t_sent, states):

    idx = 0

    for t in t_state:
        if t in states:
            states[t] += t_sent[idx]
        idx += 1

    state_max_score = 0;
    happiest = "";
    for state in states:
        if int(states[state]) > int(state_max_score):
            state_max_score = int(states[state])
            happiest = state
            
    return happiest

def main():

    senti_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
	
    # US state abbreviations
    states = {
        'AK': 0,
        'AL': 0,
        'AR': 0,
        'AS': 0,
        'AZ': 0,
        'CA': 0,
        'CO': 0,
        'CT': 0,
        'DC': 0,
        'DE': 0,
        'FL': 0,
        'GA': 0,
        'GU': 0,
        'HI': 0,
        'IA': 0,
        'ID': 0,
        'IL': 0,
        'IN': 0,
        'KS': 0,
        'KY': 0,
        'LA': 0,
        'MA': 0,
        'MD': 0,
        'ME': 0,
        'MI': 0,
        'MN': 0,
        'MO': 0,
        'MP': 0,
        'MS': 0,
        'MT': 0,
        'NA': 0,
        'NC': 0,
        'ND': 0,
        'NE': 0,
        'NH': 0,
        'NJ': 0,
        'NM': 0,
        'NV': 0,
        'NY': 0,
        'OH': 0,
        'OK': 0,
        'OR': 0,
        'PA': 0,
        'PR': 0,
        'RI': 0,
        'SC': 0,
        'SD': 0,
        'TN': 0,
        'TX': 0,
        'UT': 0,
        'VA': 0,
        'VI': 0,
        'VT': 0,
        'WA': 0,
        'WI': 0,
        'WV': 0,
        'WY': 0
        }

    scores = dictFromSentimentFile(senti_file)
#    for (key,value) in scores.items():
#        print str(key), ' ', float(value)

    tweet_data, tweet_state = readTweetFile(tweet_file)
#    print tweet_data
#    print tweet_state

    tweet_sentiments = computeTweetSentiment(tweet_data, scores)

#    print len(tweet_sentiments), len(tweet_data)
#    for s in tweet_sentiments:
#        print s

    print computeHappiestState(tweet_state, tweet_sentiments, states)

if __name__ == '__main__':
	main()
