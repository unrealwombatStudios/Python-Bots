import praw
import time
import sys
import re

# "Tell" reddit what this bot is going to do.
user_agent = "I am telling you PI /u/TellMePiBOT"
r = praw.Reddit(user_agent=user_agent)

# loging in to reddit.
r.login()
print("Bot is logging in...")


# Array with names of subreddits the bot should visit.
subs_to_check = ["learnmath", "math", "cheatatmathhomework", "homeworkhelp", "askmath", "mathematics",
                 "mathbooks", "physicsbooks", "matheducation", "casualmath", "puremathematics", "mathpics",
                 "mathematica", "matlab", "statistics", "LaTeX"]
# Words that a comment has to contain to tricker the bot.
words_to_match = ["3.141", "3.14", "3.141", "3.1415", "3.14159", "3,14", "3,141", "3,1415", "3,14159", "pi", 
                  "PI", "Pi", "pI"]
# The bot will replay with this answer if he is trickered.
message_to_reply_with = "PI:  3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606355881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537105079227968925 \n \n  I am a stupid bot that replied to you comment because I think your mentioned PI. "

# Max number of submissions the bot should check
numb_of_submissions_to_check = 500
# In the cache are IDs of comments stored where the bot already replied.
cache = []

# This methode checks if the parameter can be a float
def canStringBeFloat(pWord):
    try:
        float(pWord)
        return True
    except ValueError:
        return False


# This methode checks if a comment contains any of the words in the array.
def contains(comment):
    matched = False
    splited = comment.split()
    for word in  words_to_match:
        for split in splited:
            # Here we remove the punctuation in the word if the word insnt a number.
            if not canStringBeFloat(split):
                out = "".join(c for c in split if c not in ('!','.',':'))
            else:
                out = split

            if word == out:
                matched = True

    return matched

# This is the main methode. It checks all the comments of the submissions in the threads who are stored 
# in the array.
def run_bot():
    #For every subreddit in the array
    for subName in subs_to_check:
        print("The subreddit '"+subName+"' is going to be checked...")
        subreddit = r.get_subreddit(subName)
        submissions = subreddit.get_hot(limit = numb_of_submissions_to_check)

        # For every submission in the subreddit.
        for submission in submissions:
            comments = submission.comments
            print("Checking a submission...")

            # For every Comment in the submission.
            for comment in comments:
                print("Checking a comment...")
                # Extracting the text from a comment.
                comment_text = comment.body
                isMatch = contains(comment_text)

                # If the ID is not jet stored in the cache and if the bot found PI in the comment.
                if comment.id not in cache and isMatch:
                    print("-----------------------------------------")
                    print("The bot found pi and is now trying to reply")

                    # If a subreaddit only allows the bot to replie every X minutes but the bot replied under X
                    # than an exception will be lunched. The bot will automatically wait for the default time of 
                    # the subreddit.
                    try:
                        # The bot replies here with our message.
                        comment.reply(message_to_reply_with)
                        print("Bot replied!")
                        # The comment ID is stored in cache.
                        cache.append(comment.id)
                        # The bot upvotes the comment where he found the word pi.
                        comment.upvote() 
                        print("Bot upvoted the post!")
                        print("-----------------------------------------")
                    except praw.errors.RateLimitExceeded as error:
                        print '\tSleeping for %d seconds' % error.sleep_time
                        time.sleep(error.sleep_time)


# The bot will never stopp looking for the word pi.
while True:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    run_bot()
    print("The bot is now going to sleep for 10 sec...")
    time.sleep(10)
