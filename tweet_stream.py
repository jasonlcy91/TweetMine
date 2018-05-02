import tweepy
import json
from time import strftime
import tweet_mine_helpers as twminion
import sys


# This StreamListener can be used to stream live public tweets.
class StreamListener(tweepy.StreamListener):

    def __init__(self, statuslimit=50000, targetpath='tweetData.txt', timestamp=True, print_stream=True):
        timestamp_str = ''
        if timestamp:
            timestamp_str = '_' + strftime('%Y%m%d_%H%M%S')

        self.last_target_path = targetpath.split('.txt')[0] + timestamp_str + '.txt'
        self.__outfile = open(self.last_target_path, 'w')
        self.__statuslimit = statuslimit
        self.__statuscounter = 1
        self.__print_stream = print_stream
        self.tweet_id_list = set()
        self.user_id_list = set()

    # If data is a status (has 'in_reply_to_status_id' field), cast to on_status()
    # Close the file once desired datalimit is reached.
    def on_data(self, raw_data):

        if 'in_reply_to_status_id' in raw_data:
            self.on_status(raw_data)
            # self.__outfile.write(raw_data[:-1])

            self.__statuscounter += 1
            if self.__statuslimit is not None and self.__statuscounter > self.__statuslimit:
                self.__outfile.close()
                return False

            return True

    # Write status (json string) to TweetData file.
    # Collect TweetID for future tracking (to be used with track_tweet.py)
    # If specified, print Tweet while streaming
    def on_status(self, status):
        self.__outfile.write(status[:-1])
        status_json = json.loads(status)   # print(json.dumps(status_json, indent=4))
        self.tweet_id_list.add(str(status_json['id']))
        self.user_id_list.add(str(status_json['user']['id']))

        if self.__print_stream:
            print(self.__statuscounter, '.', status_json['user']['screen_name'], ':', status_json['text'])

    def on_error(self, status):
        print("Error " + str(status))
        if status == 420:
            print("Rate Limited")
            return False


def __main(tweet_data_targetpath='tweetData.txt', datalimit_tweet_data=50000, tweet_ids_targetpath='tweetIDs.txt'):
    from authentication import authenticate
    auth, api = authenticate()

    # Stream tweets from USA only
    print('Streaming tweets from USA...\n')
    filter_loc = [-117.333984, 32.567648, -69.521484, 44.357242]

    stream_listener = StreamListener(datalimit=datalimit_tweet_data, targetpath=tweet_data_targetpath)
    stream = tweepy.Stream(auth, stream_listener)
    stream.filter(locations=filter_loc)

    # Get tweet_ids and user_ids
    tweet_ids = stream_listener.tweet_id_list
    user_ids = stream_listener.user_id_list

    # Save tweet IDs and user IDs to file as reference
    twminion.write_tweetID_userID(tweet_ids, user_ids, targetpath=tweet_ids_targetpath)


if __name__ == '__main__':
    __main(sys.argv[1], int(sys.argv[2]), sys.argv[3])

