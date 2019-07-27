# TweetMine - Twitter Tweet Mining Machine

My advanced Twitter Tweet Mining Machine that can mine tweets by batches with interval.

```
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
```
