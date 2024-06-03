from player import Player
import time
bot = Player()
bot.setName("[GOOOL] Idiot")
bot.adjustSettings()
bot.enterMultiplayer()
games = bot.getCurrentGames()
print(games)
bot.waitForGame(["PVE", "FFA"])
bot.chooseStartLocation()
time.sleep(1000)

'''
Idiot
Novice
Beginner
Amateur
Learner
Pupil
Apprentice
Student
Initiate
Recruit
Rookie
Newcomer
Freshman
Junior
Aspirant
Candidate
Contender
Probationer
Trainee
Adept
Proficient
Skilled
Capable
Competent
Qualified
Accomplished
Veteran
Seasoned
Experienced
Practiced
Masterful
Expert
Virtuoso
Prodigy
Maestro
Savant
Genius
Luminary
Paragon
Grandmaster
'''