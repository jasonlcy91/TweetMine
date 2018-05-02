import json
from time import strftime


# MINE HELPER MINIONS

# 1. Write tweetID to TweetID file.
def write_tweetID_userID(tweet_ids, user_ids, targetpath='tweetIDs.txt', timestamp=True):
    timestamp_str = ''
    if timestamp:
        timestamp_str = '_' + strftime('%Y%m%d_%H%M%S')

    targetpath = targetpath.split('.txt')[0] + timestamp_str + '.txt'

    with open(targetpath, 'w') as f:
        # f.write('{{"tweet_ids": {}, "user_ids" : {}}}\n'.format(list(tweet_ids), list(user_ids)))
        tweet_ids_user_ids = dict(tweet_ids=list(tweet_ids), user_ids=list(user_ids))
        json.dump(tweet_ids_user_ids, f)


# 2. Read TweetID_userID file and return list of tweet IDs.
def get_IDs_from_file(TweetID_userID_filepath):

    with open(TweetID_userID_filepath, 'r') as f:
        ids = json.load(f)
        return ids


# 3. Read TweetData file and return list of tweet IDs.
# If specified, write to file.
def extract_IDs(sourcepath, targetpath=None, count=100):
    ids = []

    with open(sourcepath, 'r') as file:
        for line in file:
            status = json.loads(line)
            ids.append(str(status['id']))

            if len(ids) >= count:
                break
    if targetpath is None:
        return ids
    else:
        with open(targetpath, 'w') as file:
            file.write(','.join(ids))


# 4. Read TweetData file line by line.
def read_tweetData(filepath):

    with open(filepath, 'r') as file:
        for line in file:
            status = json.loads(line)
            print(status['place']['full_name'], ':', status['place']['country_code'])
            # print(json.dumps(status, indent=4)) # print


# 5. Quick validate whether TweetTrack file is correct or not.
def quicktest_file_ok(sourcepath):
    idcount = 0
    linecount = 0
    with open(sourcepath) as f:
        for line in f:
            jsondata = json.loads(line)
            if "id" in jsondata:
                idcount += 1
            linecount += 1

    print(idcount, linecount)
    print('Same line count and id count. File seems ok.')
