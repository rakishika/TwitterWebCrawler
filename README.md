# CS172 Project Phase 1 
![Screenshot 2023-08-09 at 12 03 46 AM](https://github.com/rakishika/TwitterWebCrawler/assets/33856993/4b24c7b1-d051-450d-b387-56b908ddbefd)

Link to demo video:
https://www.youtube.com/watch?v=roeCK38RP8o


## Setup
This is a python project. Please make sure to have Python 3 installed as well as PIP. The recommended method to install the python dependencies for this project are creating a Python Virtual Environment. Once python has been setup and installed, you can install the neccesary python dependencies for this project via `pip install -r requirements.txt`.

Next, copy and rename the `.env-example` to `.env`, and fill the `BEARER_TOKEN` value with your bearer token from the Twitter Developer API.

## Twitter Streaming
`stream.py` allows you to stream real time tweets that match specific search criteria. This search critera is
defined in the `stream_rules.json` file. Each rule can be built from [twitter's filtered stream rule operators](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule). 

The python file will add / remove stream rules based on the `stream_rules.json` file to the streaming end point.

The stream will store tweets into a single JSON file based on the constants defined in the `.env` file. To stop the stream,
either enter "quit" or `CTRL+C`.
