import tweepy
from authentication import authenticate
import tweet_stream as tws  # stream tweets
import tweet_track as twt  # lookup tweets
import tweet_mine_helpers as twminion
import schedule  # pip install schedule
from time import sleep
from http.client import IncompleteRead
import threading


__curr_follow_stream = None


def stream_follow_user_job(auth, stream_listener, user_ids):

    global __curr_follow_stream
    stream_on = True
    while stream_on:
        try:
            __curr_follow_stream = tweepy.Stream(auth, stream_listener)
            __curr_follow_stream.filter(follow=user_ids)
            stream_on = False
        except IncompleteRead:
            continue


# 1. Stream public tweets, and also write tweet ids and user ids to a separate file
#    Output file(s): tweetData, tweetIDs
# 2. Using user_ids, stream tweets from these users using `follow` operator
#    Output file(s): tweetUserFollow
# 3. Using tweet_ids, lookup tweets to track for changes
#    Output file(s): One tweetTrack files at each specified interval (default: 15 minutes for 12 hours)

def __main():

    # Settings
    file_batch_no = '001_'
    file_tweet_data = file_batch_no + 'tweetData.txt'
    file_tweet_ids = file_batch_no + 'tweetIDs.txt'
    file_tweet_track = file_batch_no + 'tweetTrack.txt'
    file_tweet_user_follow = file_batch_no + 'tweetUserFollow.txt'
    limit_tweet_status = 900  # How many Twitter data to stream. Includes tweet/status, event, etc
    limit_tweet_per_lookup = 100  # How many tweets (ids) to track. API limit: 100 (safety to be handled by function)
    limit_tweet_per_window = 900  # How many tweets (ids) to track in a 15-min window. API limit: 900 (safety to be handled by function)
    limit_user_follow = 5000  # How many user ids to stream from. API limit: 5000
    tweet_track_duration = 720  # 12 hours
    tweet_track_interval = 15  # minutes
    auth, api = authenticate()

    # 1. Stream public tweets, and also write tweet ids and user ids to a separate file
    #    Output file(s): tweetData, tweetIDs
    #
    # Stream tweets from USA only
    print('Streaming tweets from USA...\n')
    filter_loc = [-117.333984, 32.567648, -69.521484, 44.357242]
    stream_listener = tws.StreamListener(statuslimit=limit_tweet_status, targetpath=file_tweet_data)
    stream = tweepy.Stream(auth, stream_listener)
    stream.filter(locations=filter_loc)

    tweet_ids = list(stream_listener.tweet_id_list)
    user_ids = list(stream_listener.user_id_list)
    if len(user_ids) > limit_user_follow:
        user_ids = user_ids[:limit_user_follow]

    twminion.write_tweetID_userID(tweet_ids, user_ids, targetpath=file_tweet_ids)

    # 2. Using user_ids, stream tweets from these users using `follow` operator
    #    Output file(s): tweetUserFollow
    #
    # Set up asynchronous stream
    # To end together with a scheduled job below.
    print('\n====== FOLLOWING USERS ========================================\n'
          'Start streaming tweets from selected users...\n\n'
          '===============================================================\n')

    stream_listener = tws.StreamListener(targetpath=file_tweet_user_follow)
    t = threading.Thread(target=stream_follow_user_job, args=(auth, stream_listener, user_ids))
    t.start()

    # 3. Using tweet_ids, lookup tweets to track for changes
    #    Output file(s): One tweetTrack files at each specified interval (default: 15 minutes for 12 hours)
    #
    # Schedule tracking job to start after 15 minutes.
    print('\n****** TRACKING TWEETS ****************************************\n'
          'Scheduling tweet tracking for every 15 minutes for 12 hours.\n'
          '48 rounds in total.\n'
          'To start in 15 minutes...\n\n'
          '**************************************************************\n')
    twt.set_track_rounds(int(tweet_track_duration/tweet_track_interval))
    job1 = schedule.every(tweet_track_interval).minutes.do(twt.job_track_tweet, api, tweet_ids, file_tweet_track,
                                                           warning=False, tweet_per_lookup=limit_tweet_per_lookup,
                                                           tweet_per_window=limit_tweet_per_window)

    while job1 in schedule.jobs:
        schedule.run_pending()
        sleep(1)

    __curr_follow_stream.disconnect()  # stop thread

    print('\n======== ALL JOBS DONE! =========\n'
          '  =============================\n'
          '     =======================\n'
          '        =================\n'
          '           ===========\n'
          '              =====\n'
          '                =\n\n'
          '  Disconnecting Twitter stream.\n'
          '               YAY!\n'
          '            Good Bye!\n'
          '=================================\n')


if __name__ == '__main__':
    __main()
