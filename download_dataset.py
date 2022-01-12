import os
import subprocess
from subprocess import PIPE
import json
import time


def pull_tweets(tweetIDs,media_ids,destination,auth,tracker):

    # elements of the tweet curl request; see Twitter's docs for more information
    twitter_command = "curl 'https://api.twitter.com/2/tweets?"
    ids = "ids="
    expansions = "&expansions=attachments.media_keys&media.fields=media_key,preview_image_url,url'"
    full_auth = " -H 'Authorization: Bearer " + auth + "'"

    # put all tweet-IDs in the id parameter string
    for id in tweetIDs:
        ids += str(id) + ','

    # send request to twitter for tweets and interpret the response as a dictionary
    command = twitter_command + ids[:len(ids) - 1] + expansions + full_auth
    comp_process = subprocess.run(command,stdout=PIPE, stderr=PIPE,shell=True)
    tweet_dict = eval(comp_process.stdout)

    # check for keys to avoid program crash
    if 'includes' in tweet_dict.keys():
        if 'media' in tweet_dict['includes'].keys():

            # for each live image
            for item in tweet_dict['includes']['media']:

                if 'media_key' in item.keys() and 'url' in item.keys():
                    # make sure this is an image in our dataset
                    if item['media_key'][len(item['media_key']) - 4 :] in media_ids:

                        wgetCommand = "wget -O " + item['media_key'] + ".jpg " + item['url']
                        comp_process = subprocess.run(wgetCommand,stdout=PIPE, stderr=PIPE,shell=True)


                        # check for errors in wget process
                        if type(comp_process.stdout) == bytes:
                            if comp_process.stdout.decode('utf-8') == "":
                                # print("Success -> Moving Image")
                                # successful download -> increase tracker
                                tracker += 1

                                # move file to appropriate sub folder
                                mv_image = "mv " + item['media_key'] + ".jpg " + destination
                                comp_process = subprocess.run(mv_image,stdout=PIPE, stderr=PIPE,shell=True)

                            else:
                                print("Could not download -> Error below")
                                print(comp_process.stdout)
                else:
                    print("media_key or url not in item dictionary")
        else:
            print("Media key not in dictionary")

    # twitter only allows 900 requests every 15 minutes, if we hit that error
    # sleep for a minute then try again with the same parameters; this section
    # will be called until the "Too many requests error is resolved"
    elif "Too Many Requests" in comp_process.stdout.decode('utf-8'):
        print("Overran rate limits")
        print("You can only request 900 requests  every 15 minutes, going to sleep for 1 min before trying again zzz...")
        time.sleep(60)
        pull_tweets(tweetIDs,media_ids,destination,auth,tracker)
    else:
        print("Includes not in dictionary: Error below")
        print(comp_process.stdout)
    return tracker

"""
For simplicity, it is easier to process mask and unmasked images separately.
This method takes the dictionary containing both and returns them separated
into two directories.

@param dict -> the dictionary containing mask and no mask entries to be separated
@returns an array containing a mask and no mask dictionary
"""
def seperate_dict(dict):
    mask = {}
    no_mask = {}
    for key in dict:
        if dict[key][1] == 'mask':
            mask[key] = dict[key]
        elif dict[key][1] == 'no_mask':
            no_mask[key] = dict[key]
    return [mask,no_mask]


"""
Twitter only allows a user to pull 100 tweets at a time; this function separates
out tweets into batches of 100 before calling pull_tweets on that batch

@param mask -> a dictionary containing relevant information on each masked image
@param no_mask -> a dictionary containing relevant information on each unmasked image
@param train_or_test -> a string of either "Training" or "Testing" that tells
                        the pull_tweets function which directory to place an
                        image in
@param tracker -> an integer to track the number of successful downloads
@returns the integer value of successful downloads
"""
def batch_pull(mask,no_mask,train_or_test,tracker):

    # number of items per batch
    batch_tracker = 0

    # arrays of each batches' tweet IDs and media ids
    batch_ids = []
    batch_media = []

    # go through each tweet in the mask dictionary
    for key in mask:
        # grab the dictionary entry in consideration
        item = mask[key]

        # add tweet and media keys to the batch list till we reach 100
        if batch_tracker < 100:
            batch_ids.append(key)
            batch_media.append(item[0])
            batch_tracker += 1

        # grab 100 tweets and reset
        if batch_tracker == 100:
            testing_tracker = pull_tweets(batch_ids,batch_media, "Twitter_Img_Dataset/" + train_or_test + "/mask/",auth,tracker)
            batch_ids = []
            batch_media = []
            batch_tracker = 0


    # go through each tweet in the mask dictionary
    for key in no_mask:
        # grab the dictionary entry in consideration
        item = no_mask[key]

        # add tweet and media keys to the batch till we reach 100
        if batch_tracker < 100:
            batch_ids.append(key)
            batch_media.append(item[0])
            batch_tracker += 1

        # grab 100 tweets and reset
        if batch_tracker == 100:
            tracker = pull_tweets(batch_ids,batch_media, "Twitter_Img_Dataset/" + train_or_test+ "/no_mask/",auth,tracker)
            batch_ids = []
            batch_media = []
            batch_tracker = 0

    # return the number of successful downloads
    return tracker


# inform user of what is going to happen
print("This script will create a training and testing directory on your computer and download GBs of images; is that ok?")
user_ok = input("Enter Yes or No: ")

if user_ok.lower() == "yes" or user_ok.lower() == "y":

    # have the user input their token and test it before proceeding
    auth = input("Enter your bearer token (Use no spaces or extra characters - just copy paste): ")

    test_auth = "curl 'https://api.twitter.com/2/tweets' -H 'Authorization: Bearer " + auth + "'"
    comp_process = subprocess.run(test_auth,stdout=PIPE, stderr=PIPE,shell=True)

    # bearer token incorrect -> inform user
    if "Unauthorized" in comp_process.stdout.decode('utf-8'):
        print("There was an error with your bearer token. Make sure it is correct (watch out for newlines)")

    # success; proceed with download
    else:
        print("Authentication Successful; Starting Downloads. This will take a while ")

        # make directories for train and test set
        make_dirs = "mkdir Twitter_Img_Dataset/ && mkdir Twitter_Img_Dataset/Training/ && mkdir Twitter_Img_Dataset/Testing/ && mkdir Twitter_Img_Dataset/Training/mask && mkdir Twitter_Img_Dataset/Training/no_mask && mkdir Twitter_Img_Dataset/Testing/mask && mkdir Twitter_Img_Dataset/Testing/no_mask"
        comp_process = subprocess.run(make_dirs,stdout=PIPE, stderr=PIPE,shell=True)


        # load json files for train and test set
        with open('training.json') as f:
                data = f.read()
        with open('testing.json') as f:
                data1 = f.read()
        training = json.loads(data)
        testing = json.loads(data1)

        # get mask and no mask images all in 1 dictionary for train and test_tracker
        training_seperated_dict = seperate_dict(training)
        testing_seperated_dict = seperate_dict(testing)

        # create variables to keep track of successful downloads
        training_tracker = 0
        testing_tracker = 0

        # in batches of 100 tweets, download training and testing images
        training_tracker = batch_pull(training_seperated_dict[0],training_seperated_dict[1],"Training",training_tracker)
        testing_tracker = batch_pull(testing_seperated_dict[0],testing_seperated_dict[1],"Testing",testing_tracker)

        # print out results to console
        print()
        print("__Summary Training__")
        print("Images downloaded: ", training_tracker)
        print("Images available when authors downloaded images in Summer of 2021: ", len(training.keys()))
        print("Number of Twitter Images no longer available: ", len(training.keys()) - training_tracker)

        print()
        print("__Summary Testing__")
        print("Images downloaded: ", testing_tracker)
        print("Images available when authors downloaded images in Summer of 2021: ", len(testing.keys()))
        print("Number of Twitter Images no longer available: ", len(testing.keys()) - testing_tracker)

else:
    print("Come back when you are ready :) ")
