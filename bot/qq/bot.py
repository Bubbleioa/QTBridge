#
#

import os
import requests
import random
from receive import rev_msg
import api
import ini

while true:
    try:
        rev = rev_msg()
        if rev == None:
            continue
    except:
        continue

    if rev["post_type"] == "message":
        print(rev)
        if rev["message_type"] == "group":
            if rev['group_id'] == 747324697:
                id = rev[user_id]
                name = rev['sender']['nickname']
                message = rev['raw_message']
                #todo


        #elif rev["message_type"] == "private"