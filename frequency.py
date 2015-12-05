####################################################################
# Compute the frequency of terms stream
# The program needs an input: tweets ("20-lines-output-file")
# We run the program as:
# python frequency.py problem_1_submission.txt
#####################################################################
import sys
import json
import re
import string

# Read the tweet_file. Extract each tweet per line. Append to the tweet_data list.
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

def computeTermFrequency(td):
   
    terms = {} # occurences of terms

    for t in td:
        words = filterTweet(t.encode('utf-8'))

#        print ' ******* tweet '
#        print words

        for w in words:
            # Check if we know this term already
            data = terms.get(w)
            if data == None: # if so increment
                terms[w] = 1
            else:            # update existing term
                terms[w] = terms[w] + 1
                
    # Calculate term frequencies:
    for term in terms:
        print term,' ', terms[term]/float(len(terms))

def main():

    tweet_file = open(sys.argv[1])
	
    tweet_data = readTweetFile(tweet_file)
#    print tweet_data

    computeTermFrequency(tweet_data)
	
if __name__ == '__main__':
	main()
