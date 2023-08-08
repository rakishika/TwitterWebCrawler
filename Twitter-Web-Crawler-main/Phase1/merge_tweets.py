import json
from threading import Thread
import sys
from os import path
from os import listdir
import fnmatch

# This script merges multiple tweet JSON files into bigger ones while filtering
# out duplicate tweets identified by their tweet ID.

# Tweets needed for 10 MB: 32016 tweets
# Tweets needed for 20 MB: 64035 tweets
# Tweets needed for 50 MB: 160085 tweets

if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} <num tweets in a single file> <merge file prefix> <data directory> <merge directory>")
    exit(1)

NUM_TWEETS_IN_FILE = int(sys.argv[1])
MERGE_PREFIX = sys.argv[2]
DATA_DIR = sys.argv[3]
MERGE_DIR = sys.argv[4]

if not path.isdir(DATA_DIR):
    print("Invalid data directory specified!")
    exit(1)

if not path.isdir(MERGE_DIR):
    print("Invalid merge directory specified!")
    exit(1)

merge_counter = 0

if path.isfile(f"{MERGE_DIR}/{MERGE_PREFIX}{merge_counter}.json"):
    print("Initial existing merge file already exists! Please change the merge prefix to prevent overwriting files!")
    exit(1)

def store_tweets(tweets):
    global merge_counter
    global MERGE_DIR
    global MERGE_PREFIX

    old_file_num = merge_counter
    merge_counter = merge_counter + 1

    def store_tweets_threaded(tweets, file_name):
        # Write the filtered tweets to JSON
        with open(file_name, 'w') as f:
            f.write('[')
            tweets_json = [ json.dumps(tweet, indent=4, default=str) for tweet in tweets ]
            f.write(",\n".join(tweets_json))
            f.write("]")

    file_name = f"{MERGE_DIR}/{MERGE_PREFIX}{old_file_num}.json"
    thread = Thread(target = store_tweets_threaded, args = (tweets, file_name,))
    thread.start()

print(f"Merging tweets...")
# Read the tweets file
# Continue reading until we split
tweets_array = []
unique_tweet_ids = set()

# Read unique tweets IDs
if path.isfile(f"{MERGE_DIR}/unique_tweet_ids.txt"):
    with open(f"{MERGE_DIR}/unique_tweet_ids.txt", "r") as ids_file:
        lines = ids_file.readlines()
        for id in lines:
            unique_tweet_ids.add(int(id))

def add_unique_id(tweet):
    unique_tweet_ids.add(int(tweet["id"]))
    return tweet

for file in listdir(DATA_DIR):
    file_path = f"{DATA_DIR}/{file}"
    if not fnmatch.fnmatch(file, '*.json'):
        continue
    
    loaded_array = None
    with open(file_path, 'r') as json_file:
        loaded_array = json.load(json_file)
    
    filtered_tweets = [ add_unique_id(tweet) for tweet in loaded_array if int(tweet["id"]) not in unique_tweet_ids ]

    tweets_array.extend(filtered_tweets)

    if len(tweets_array) >= NUM_TWEETS_IN_FILE:
        save_array = tweets_array[0:NUM_TWEETS_IN_FILE]
        store_tweets(save_array)
        del tweets_array[0:NUM_TWEETS_IN_FILE]

if len(tweets_array) > 0:
    store_tweets(tweets_array)

with open(f"{MERGE_DIR}/unique_tweet_ids.txt", "w") as f:
    f.write("\n".join([ str(tweet_id) for tweet_id in unique_tweet_ids]))