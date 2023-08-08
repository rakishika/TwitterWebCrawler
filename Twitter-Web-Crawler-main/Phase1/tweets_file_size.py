import json
import sys
import string
import random
from os.path import getsize as file_size, exists as file_exists
from os import remove as delete_file

### Get the number of tweets needed to satisfy a specific file size.

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <file size in MB> <sample tweet file> <temp file>")
    exit(1)

TARGET_FILE_SIZE = int(sys.argv[1])
SAMPLE_FILE_PATH = sys.argv[2]
TEMP_FILE_PATH = sys.argv[3]

if not file_exists(SAMPLE_FILE_PATH):
    print(f"Sample file could not be found!")
    exit(1)

# Find statistics for the sample file
sample_data = None
with open(SAMPLE_FILE_PATH, "r") as sample_file:
    sample_data = json.load(sample_file)

num_sample_tweets = len(sample_data)
total_text_len = sum([ len(tweet["text"]) for tweet in sample_data ])
total_device_len = sum([ len(tweet["device"]) for tweet in sample_data ])

avg_text_len = int(total_text_len / float(num_sample_tweets))

print(f"Average Text Length: {avg_text_len}")

mb_of_file = lambda file_path: file_size(file_path) / 1000000.0
sample_data_size = mb_of_file(SAMPLE_FILE_PATH)

print(f"Sample Data File Size: {sample_data_size} mb")

# Create a random tweet
def create_temp_tweet():
    global avg_text_len

    devices = [ "Twitter for Android", "Twitter for iPhone", "Twitter Web App"]
    device = random.choice(devices)
    text = "".join([ random.choice(string.ascii_letters) for _ in range(avg_text_len) ])

    return {
        "id": 1523389397625831424,
        "user_id": 890922581808828417,
        "created_at": "2022-05-08 19:48:35+00:00",
        "device": device,
        "text": text,
        "likes": 0,
        "retweets": 0
    }

def get_temp_tweets_size(num_tweets):
    global TEMP_FILE_PATH
    tweets = [ create_temp_tweet() for _ in range(num_tweets)]

    # Create a temp file with the number of random tweets
    with open(TEMP_FILE_PATH, 'w') as f:
        f.write('[')
        tweets_json = [ json.dumps(tweet, indent=4, default=str) for tweet in tweets ]
        f.write(",\n".join(tweets_json))
        f.write("]")
    
    temp_file_size = mb_of_file(TEMP_FILE_PATH)
    delete_file(TEMP_FILE_PATH)

    return temp_file_size


# Generation Loop
iteration = 0
old_optimal_num_tweets = 0
# Number of Sample Tweets / Sample Tweets File Size = x / Target File Size
optimal_num_tweets = int((num_sample_tweets / sample_data_size) * TARGET_FILE_SIZE)
print(f"Starting Number of Tweets: {optimal_num_tweets}")

while abs(optimal_num_tweets - old_optimal_num_tweets) > 1:
    iteration += 1
    tweets_file_size = get_temp_tweets_size(optimal_num_tweets)
    error_bound = TARGET_FILE_SIZE - tweets_file_size
    step_size = int((num_sample_tweets / sample_data_size) * error_bound)
    old_optimal_num_tweets = optimal_num_tweets
    optimal_num_tweets += step_size

    print("")
    print("Iteration: " + str(iteration))
    print(f"File Size: {tweets_file_size} MB")
    print(f"Error: {error_bound} MB")
    print(f"Step Size: {step_size} tweets")
    print(f"New Optimal number of tweets: {optimal_num_tweets} tweets")

print("")
print(f"Number of Tweets needed for {TARGET_FILE_SIZE} MB: {optimal_num_tweets} tweets!")