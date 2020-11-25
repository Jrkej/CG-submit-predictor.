# CG-submit-predictor.
It will predict your rank in CG leaderboard if you submit your code saved in CG IDE.
# Introduction
After ending of fall challenge i was thinking that how can the speed of submits can be increased,So here is my one of idea.

# Requirements
For this you need python3 + 2 modules of python

1 - trueskill
2 - requests

in windows you can do it via pip-
pip install trueskill
pip install requests

for other OS i am not aware of them but you are smart enough to install it.

# NOTE - IF YOU HAVE CHANGED YOUR CODE IN CG IDE SO YOU HAVE TO PLAY A MATCH TO SAVE THAT CODE ON CG.

# Running the code
Download submission.py from this respitory - https://github.com/Jrkej/CG-submit-predictor./blob/main/submission.py
open it and enter your credentials in line 20 and 21-

email = 'xxxxxxxxxxxxxxxxxxxxxxxx' #Enter your Codingame handle email-Id
pw = '*******************'#Enter your Codingame handle password don't worry its secure

and then you have to enter pretty id of bot programming you have to predict your submission for on line 17 -
bot_programming = "x-y-z"#Bot programming (pretty id)
pretty id is nothing just its made of small letters and spaces are replaced '-' so for 'Coders Strike Back' it will be 'coders-strike-back'

Now comes amount of total matches to play, For a accurate result check how many battles does default submission plays on an average(like for 'Coders strike Back' legend league its nearly 220 battles per submit) and change number of battles on line 18th-
total_matches = X #Total matches to be played

Bingo everything is ready now you can Run the code, It will print data for each match in the form of -
match_number:opponent nickname:opponent rank:result(WON,LOSE,TIE):scores:your current rank:side:replay link

# Benefits

-It can used for checking that is my code in IDE is better than my code in arena.
-It can reduce the amount of submits if this becomes familiar with every codingamer.
-No Bot verification Captchas on many spam submits unlike CodinGame ;)
-It gives you an good estimate of rank of your bot in IDE cause it uses 'TRUESKILL' which is used by CG as well for submission.

# Limitations

-As we can only fetch 1000 players from CG so it won't be able to predict your rank if your bot level is below those 1000 bots' level so it will show you your rank as 1001.
-This tool is not yet available for Contest cause the APIs are different as far as i know (I will make it available for Contest also when the tool will also work for contest)

# Exceptions

-This tool brokes for platinum rift episode 1 and episode 2 also i will fix it if i got the problem.
-In case you decreased match_cooldown time in seconds on line 24th in submission.py it can cause error in middle of running code it will say that many battles have been played in very less time,Due to CG.

# Further additions
Later i will make this tool available for contest as well cause we faced slow submits in contest.

For any suggestions or if you find any bug in the code please tell me, or don't hesitate to make PR for fixed version :)

