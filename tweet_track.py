import json
from time import time
from time import strftime
from time import localtime
import schedule  # pip install schedule

__track_rounds = 0


def set_track_rounds(rounds=10):
    global track_rounds
    track_rounds = rounds


# Scheduled job to track specified tweets.
# Write to TweetTrack file, including ids of deleted tweets.
# Twitter statuses lookup limit per call: 100 tweet ids
# Twitter statuses lookup limit per window: 900 tweet ids
# By default, this function makes 9 calls, one after another.
# Suggested improvement: Save to file to track last runs in the last 15 minutes and
#                        total tweet ids looked up so far
def job_track_tweet(api, tweet_ids, targetpath='tweetTrack.txt', tweet_per_lookup=100, tweet_per_window=900,
                    timestamp=True, warning=True):
    global track_rounds
    t0 = time()
    t0_str = strftime('%Y/%m/%d %H:%M:%S', localtime(t0))
    print('****** TRACKING TWEETS ****************************************\n'
          '{} rounds left...\n'
          'Time now: {}\n\n'
          '**************************************************************\n'.format(track_rounds, t0_str))

    if (len(tweet_ids) > 100) & warning:
        print('++ ALERT: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
              'Twitter statuses_lookup can only support up to 100 status ids,\n'
              'and up to 900 statuses in a 15-minutes window.\n'
              'Set warning=False to ignore.\n'
              'Press Ctrl+C or Ctrl+Z to exit if required.\n\n'
              '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

    timestamp_str = ''
    if timestamp:
        timestamp_str = '_' + strftime('%Y%m%d_%H%M%S')

    targetpath = targetpath.split('.txt')[0] + timestamp_str + '.txt'
    f = open(targetpath, 'a')

    returned_ids = []

    max_track = len(tweet_ids) if len(tweet_ids) < tweet_per_window else tweet_per_window
    for i in range(0, max_track, tweet_per_lookup):
        lookup = tweet_ids[i:i+tweet_per_lookup] if (i+tweet_per_lookup) < max_track else tweet_ids[i:max_track]

        tweets = api.statuses_lookup(lookup)

        for tweet in tweets:
            returned_ids.append(str(tweet.id))
            json.dump(tweet._json, f)
            f.write('\n')

    for x in tweet_ids[:900]:
        if x not in returned_ids:
            f.write('{{"last_checked": {}, "deleted_id" : {}}}\n'.format(t0_str, x))

    f.close()
    lookup_n = 900
    deleted_n = lookup_n - len(returned_ids)
    print('****** TRACKING TWEETS ****************************************\n'
          'Time used: {}. Lookup: {}, Deleted: {}.\n'.format(time()-t0, lookup_n, deleted_n))

    track_rounds -= 1
    if track_rounds <= 0:
        print('FINISHED!\n')
        if max_track == tweet_per_window:
            print('LOOKUP LIMIT EXHAUSTED. Please wait for another 15 minutes\n')
        print('**************************************************************\n')
        return schedule.CancelJob
    else:
        print('Waiting for next round...\n\n'
              '**************************************************************\n')


def __main():
    print()


if __name__ == '__main__':
    __main()
