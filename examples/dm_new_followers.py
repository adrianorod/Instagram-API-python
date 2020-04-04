# encoding: utf-8

import json
import os
import time
# import imageio
# imageio.plugins.ffmpeg.download()
from InstagramAPI import InstagramAPI

##### CONFIGURATION TO USE #####
login = "login"
password = "password"
messages = [
    "Type message one here",
    "Type message two here",
    "Type message three here",
]
messageIndex = 0
sentCount = 0
##### CONFIGURATION TO USE #####

api = InstagramAPI(login, password)

if (api.login()):
    
    user_id = api.username_id

    #getting total followers function
    def getTotalFollowers(api, user_id):
        """
        Returns the list of followers of the user.
        It should be equivalent of calling api.getTotalFollowers from InstagramAPI
        """
        followers = []
        next_max_id = True
        while next_max_id:
            # first iteration hack
            if next_max_id is True:
                next_max_id = ''
            _ = api.getUserFollowers(user_id, maxid=next_max_id)
            followers.extend(api.LastJson.get('users', []))
            next_max_id = api.LastJson.get('next_max_id', '')
        return followers

    def sendMessage(user_name, user_pk):
        if(messageIndex == 3):
            messageIndex = 0
        else:
            messageIndex = messageIndex + 1
        print("New follower founded: " + str(user_name) + ". Sendind message version " + str(messageIndex) + " !")
        messageToSend = "Hi, @" + user_name + '! ' + messages[messageIndex]
        api.direct_message(messageToSend, user_pk)

    while True:    
        print("Checking if you have new followers... Please, wait.")

        followers = getTotalFollowers(api, user_id)

        # verifying if had the list of followers created
        if(os.path.isfile('./dm_new_followers.json')):
            with open('./dm_new_followers.json') as json_file:  
                data = json.load(json_file)
                hasNewUser = False
                for newUser in followers: # for each user founded, we verify if exists in the list of followers
                    userReceivedMessage = False
                    for user in data:
                        if(newUser['pk'] == user['pk']): # if exists, we set the variable to True
                            userReceivedMessage = True
                    if(userReceivedMessage == False): # if not exists, the variable will be False and we sent the message and save in the list of followers
                        sendMessage(newUser['username'], newUser['pk'])
                        data.append(newUser)
                        with open('./dm_new_followers.json', 'w') as outfile:  
                            json.dump(data, outfile, indent=4)
                        hasNewUser = True
                        if (sentCount == 10):
                            sentCount = 0
                            time.sleep(10*60)
                        else:
                            sentCount = sentCount + 1
                            time.sleep(60)
                if(hasNewUser == False):
                    print("Theres no new followers.")
                    time.sleep(10*60)
        else:
            print("How its the first time that you run the script, we'd created a backup of your actual followers.")
            with open('./dm_new_followers.json', 'w') as outfile:  
                json.dump(followers, outfile, indent=4)
            time.sleep(10*60)

else:
    print("Can't login")