##############################
#           setup            #
# 1 - pip install trueskill  #
# 2 - pip install requests   #
# 3 - enter data - email,pw, #
#     bot_programming, total #
# 4 - Run the code and       #
#     experience the magic.  #
#                   -by jrke #
##############################
import requests
from trueskill import Rating, rate_1vs1, quality_1vs1
import trueskill
import random
import time
#-----------------------------------------------------------------------------------------------------------
bot_programming = "coders-strike-back"#Bot programming (pretty id)
total_matches = 220 #Total matches to be played

email = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Enter your Codingame handle email-Id
pw = '********************'#Enter your Codingame handle password don't worry its secure
#-----------------------------------------------------------------------------------------------------------

match_cooldown = 5#time in seconds to halt after each match
url1 = 'https://www.codingame.com/services/TestSession/startTestSession'#start test session
url2 = 'https://www.codingame.com/services/TestSession/play'#play a match
url3 = 'https://www.codingame.com/services/CodingamerRemoteService/loginSiteV2'#logs in to the site
url4 = 'https://www.codingame.com/services/Leaderboards/getCompatibleAgentsLeaderboard'#gets compatible leaderboard
url5 = 'https://www.codingame.com/services/Puzzle/generateSessionFromPuzzlePrettyId'#generates session id and handle
url6 = 'https://www.codingame.com/services/user/logout'#logout

sess = requests.Session()
me = Rating(0, sigma = 10)
user = "NOT LOGGED YET"
handle = -1
puzzle = -1
code = "NONE"
language = "BASH"
divid = -1
leaderboard = []
players = []
total_players = 0
trueskill_leaderboard = []
my_rank = 1000

def login():
    global user
    user = sess.post(url3, json = [email, pw, True]).json()

def logout():
    global user
    sess.post(url6,json=[])
    user = "NOT LOGGED YET"

def generate_session():
    global handle
    handle = sess.post(url5,json = [user['success']['codinGamer']['userId'], bot_programming, False]).json()['handle']

def startTestSession():
    global puzzle
    puzzle = sess.post(url1, json = [str(handle)]).json()

def collect_data():
    global divid
    global language
    global code
    divid = puzzle['currentQuestion']['arena']['arenaCodinGamer']['divisionId']
    language = puzzle['currentQuestion']['answer']['programmingLanguageId']
    code = puzzle['currentQuestion']['answer']['code']

def collect_players():
    global leaderboard
    global total_players
    json = [{'divisionId':divid, 'roomIndex':0}, user['success']['codinGamer']['publicHandle']]
    leaderboard = sess.post(url4, json = json).json()['users']
    total_players = len(leaderboard)
    player = []
    for i in range(total_players):
        if leaderboard[i]['league']['divisionIndex'] == leaderboard[0]['league']['divisionIndex']:
            player.append(leaderboard[i])
    total_players = len(player)
    leaderboard = player

def create_trueskill():
    global trueskill_leaderboard
    for player in leaderboard:
        if player['pseudo'] != user['success']['codinGamer']['pseudo']:
            p = {"name":player['pseudo'], 'skill':Rating(mu = player['score'], sigma = .8), 'id':player['agentId']}
            trueskill_leaderboard.append(p)
    p = {'name':'me', 'skill':me, 'id':-1}
    trueskill_leaderboard.append(p)

def update_my_rank():
    global my_rank
    trueskill_leaderboard.sort(key = lambda a: a['skill'], reverse = True)
    for i in range(len(trueskill_leaderboard)):
        a = trueskill_leaderboard[i]
        if a['name'] == 'me':
            my_rank = i
            break

def get_random_opp_rank():
    total = total_players
    rank = random.randrange(max(0,my_rank-(total//8)), min(total,my_rank+min(7,total//12)))
    while rank == my_rank:
        rank = random.randrange(max(0,my_rank-(total//8)), min(total,my_rank+min(7,total//12)))
    return rank

def play(json):
    return sess.post('https://www.codingame.com/services/TestSession/play', json = json).json()

def run_submission():
    lose = win = tie = 0
    global my_rank
    print("S.no : Opponent name : Opponent rank : result : scores : your current rank : side : replay")
    for match in range(total_matches):
        opp_rank = get_random_opp_rank()
        player = trueskill_leaderboard[opp_rank]
        side = random.choice([0,1])
        agents = [0,1]
        agents[side] = trueskill_leaderboard[my_rank]['id']
        agents[1-side] = trueskill_leaderboard[opp_rank]['id']
        json = [handle,{"code":f"{code}", "programmingLanguageId":f"{language}","multi":{"agentsIds":agents,"gameOptions":None}}]
        data = play(json)
        try:
            scores = data['scores']
        except:
            print(data)
        if scores[side] > scores[1-side]:
            result = "WON"
            win += 1
            trueskill_leaderboard[my_rank]['skill'],trueskill_leaderboard[opp_rank]['skill'] = rate_1vs1(trueskill_leaderboard[my_rank]['skill'],trueskill_leaderboard[opp_rank]['skill'])
        elif scores[side] < scores[1-side]:
            result = "LOSE"
            lose += 1
            trueskill_leaderboard[opp_rank]['skill'],trueskill_leaderboard[my_rank]['skill'] = rate_1vs1(trueskill_leaderboard[opp_rank]['skill'],trueskill_leaderboard[my_rank]['skill'])
        elif scores[side] == scores[1-side]:
            result = "TIE"
            tie += 1
            trueskill_leaderboard[my_rank]['skill'],trueskill_leaderboard[opp_rank]['skill'] = rate_1vs1(trueskill_leaderboard[my_rank]['skill'],trueskill_leaderboard[opp_rank]['skill'],drawn = True)
        update_my_rank()
        sides = ['Left', 'Right']
        print(f"{match+1} : {player['name']} : {opp_rank+1} : {result} : {data['scores']} : {my_rank+1} : {sides[side]}, - https://www.codingame.com/share-replay/{data['gameId']}")
        time.sleep(match_cooldown)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("WINS  :  TIES  :  LOSES")
    print(f"{win}  : {tie}  :  {lose}")
    print(f"Your expected rank is near {my_rank+1}.")
    print(f"{round(win/total_matches*100)}% winrate")

if __name__ == "__main__":
    login()
    generate_session()
    startTestSession()
    collect_data()
    collect_players()
    create_trueskill()
    update_my_rank()
    run_submission()
    logout()
