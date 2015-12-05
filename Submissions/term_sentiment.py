####################################################################
# Sentiment score of a single word based on nearest neighbours.
# The program needs two inputs (text files):
# Input1: Sentiment dictionary ("AFINN-111")
# Input2: Tweets ("20-lines-output-file")
# We run the program as:
# python tweet_sentiment.py AFINN-111.txt problem_1_submission.txt
#####################################################################
import sys
import json
import re

# Read the sentiment_file, build dictionary of terms and their scores.
def dictFromSentimentFile(sf):
    scores = {}
    for line in sf:
        term, score = line.split('\t')
        term = re.sub(r"\s+", '-', term)  # Replace whitespace by single dash
        scores[term] = int(score)
    return scores

# Read the tweet_file.
# Extract each tweet per line.
# Append to the tweet_data list.
def readTweetFile(tf):
    tweet_data = []
    for line in tf:
        response = json.loads(line)
        if "text" in response.keys():
            tweet_data.append(response["text"])
    return tweet_data

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

def computeTermSentiment(td, sc, ts):
    idx = 0
    occur = {} # stores occurences of a word
    new_score = {}

    for t in td:
        words = filterTweet(t.encode('utf-8'))
        for w in words:
            occur[w] = 0

    for t in td:

#        print '***** tweet:', idx

        words = filterTweet(t.encode('utf-8'))
        for w in words:
            occur[w] = occur[w] + 1

            if w not in sc:
                sc[w] = ts[idx]
            else:
                sc[w] = (sc[w] + ts[idx]) / occur[w]  # take the average

#            print w + " occur: ", occur[w]
#            print w + " score: ", sc[w]

        idx = idx + 1

#    print sc.items()

    return sc

def main():

    senti_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
	
    scores = dictFromSentimentFile(senti_file)
#    for (key,value) in scores.items():
#        print str(key), ' ', float(value)

    tweet_data = readTweetFile(tweet_file)
#    print tweet_data

    tweet_sentiments = computeTweetSentiment(tweet_data, scores)
#*****    for s in tweet_sentiments:
#*****        print s
	
    computeTermSentiment(tweet_data, scores, tweet_sentiments)

    for (key,value) in scores.items():
        print str(key), ' ', float(value)

if __name__ == '__main__':
	main()
