import sys
import os
import requests
import json 
import configparser as ConfigParser

def main():

	print("================= HEROES OF THE STORM API v1.0 =================")
	print("================================================================\n\n")

	if len(sys.argv) > 1:
		if sys.argv[1] == "-info":
			if len(sys.argv) > 2:
				player_info(sys.argv[2])
			else:
				player_info(parse_config(), 0)
		elif sys.argv[1] == "-help":
			help()
	else:
		loop()

def parse_config():

	config = ConfigParser.ConfigParser()
	config.read("config.txt")

	options = config.options("PLAYER_STATS")
	for option in options:
		if option == "player_battletag":
			battletag = config.get("PLAYER_STATS", option)
			return battletag

	print("PLAYER_BATTLETAG need to be initialize.")
	exit()

def loop():

	print("-(1) Heroes list")
	print("-(2) Map list")
	print("-(3) Player info")
	print("-(4) Specific heroes info")
	print("-(5) Exit")
	inp = int(input("Choice : "))

	if inp == 1:
		heroes_list()
	elif inp == 2:
		map_list()
	elif inp == 3:
		player_info()
	elif inp == 4:
		specific_heroes_info()
	elif inp == 5:
		print("Thank's for using HeroesAPI. See you soon !")
		exit()
	else:
		print("I don't understand your choice, please try again.")
		loop()

def heroes_list():

	heroes_list = requests.get("https://api.hotslogs.com/Public/Data/Heroes")
	data_heroes = json.loads(heroes_list.text)

	heroes_type = input("Which type (All, Assassin, Specialist, Support, Tank) : ")

	if heroes_type == "All":
		heroes_list_all(data_heroes)
	elif heroes_type != "Assassin" and heroes_type != "Specialist" and heroes_type != "Support" and heroes_type != "Tank":
		print("Type undefined, try again.")
		exit()
	else:
		heroes_list_by_type(data_heroes, heroes_type)

	loop()

def specific_heroes_info():

	heroes_name = input("Enter the hero name : ")
	
	if(os.path.exists("Heroes/"+heroes_name+".json")):
		with open("Heroes/"+heroes_name+".json", "rb") as fin:
			content = json.load(fin)
	else:
		print("File " + heroes_name + ".json not found.")

	print("============================"+heroes_name.upper()+"============================")
	print("Basic abilities : ")
	print("\t"+content['Abilities']['Q'])
	print("\t"+content['Abilities']['Z'])
	print("\t"+content['Abilities']['E'])
	print("\n")
	print("Heroic Abilities : ")
	print("\t"+content['Heroic Abilities']['R1'])
	print("\t"+content['Heroic Abilities']['R2'])
	print("\n")
	print("Tier 1 : ")
	for talent in content['Tier 1']:
		print("\t"+talent['Name']+" : "+talent['Description'])

def heroes_list_all(data_heroes):

	print("-------------------------------")
	for heroes in data_heroes:
		name_length = len(heroes['PrimaryName'])
		space = ""
		for i in range(name_length, 16):
			space += " "

		group_length = len(heroes['Group'])
		space2 = ""
		for i in range(group_length, 10):
			space2 += " "

		print("|"+heroes['PrimaryName'] + space + " | " + heroes['Group'] + space2 + "|")
	print("-------------------------------")

def heroes_list_by_type(data_heroes, group_type):

	print("-------------------------------")
	for heroes in data_heroes:
		if(heroes['Group'] == group_type):
			name_length = len(heroes['PrimaryName'])
			space = ""
			for i in range(name_length, 16):
				space += " "

			group_length = len(heroes['Group'])
			space2 = ""
			for i in range(group_length, 10):
				space2 += " "

			print("|"+heroes['PrimaryName'] + space + " | " + heroes['Group'] + space2 + "|")
	print("-------------------------------")

def map_list():
	
	maps_list = requests.get("https://api.hotslogs.com/Public/Data/Maps")
	data_maps = json.loads(maps_list.text)

	for maps in data_maps:
		print(maps['PrimaryName'])

	loop()

def player_info(battletag="none", looping=1):

	if battletag == "none":
		battletag = input("Enter your battletag (Name_1234) : ")

	player = requests.get("https://api.hotslogs.com/Public/Players/2/"+battletag);

	if player.text=="null":
		print("Player unavailable, please try again.")
		loop()

	player_json = json.loads(player.text)
	leaderboard = player_json['LeaderboardRankings']
	qm_mmr = str(leaderboard[0]['CurrentMMR'])
	hl_mmr = str(leaderboard[1]['CurrentMMR'])
	tl_mmr = str(leaderboard[2]['CurrentMMR'])
	ud_mmr = str(leaderboard[3]['CurrentMMR'])

	qm_rank = str(leaderboard[0]['LeagueRank'])
	hl_rank = str(leaderboard[1]['LeagueRank'])
	tl_rank = leaderboard[2]['LeagueRank']
	ud_rank = str(leaderboard[3]['LeagueRank'])

	tl_rank_s = convert_mmr_to_rank(tl_rank)

	print("----------------- Player  info -----------------\n")
	print("       | QuickMatch| HeroLeague| TeamLeague | Unranked|")
	print("|RANK  | "+qm_rank+"      | "+hl_rank+"      | "+tl_rank_s+"| "+ud_rank+"    |")
	print("|MMR   | "+qm_mmr+"      | "+hl_mmr+"      | "+tl_mmr+"       | "+ud_mmr+"    |\n")

	if looping == 1:
		loop()
	else:
		exit()

def convert_mmr_to_rank(tl_rank):

	if tl_rank < 200:
		tl_rank_s = "Bronze 5   "
	elif tl_rank > 200 and tl_rank < 400:
		tl_rank_s = "Bronze 4   "
	elif tl_rank > 400 and tl_rank < 600:
		tl_rank_s = "Bronze 3   "
	elif tl_rank > 600 and tl_rank < 800:
		tl_rank_s = "Bronze 2   "
	elif tl_rank > 800 and tl_rank < 1000:
		tl_rank_s = "Bronze 1   "
	elif tl_rank > 1000 and tl_rank < 1200:
		tl_rank_s = "Argent 5   "
	elif tl_rank > 1200 and tl_rank < 1400:
		tl_rank_s = "Argent 4   "
	elif tl_rank > 1400 and tl_rank < 1600:
		tl_rank_s = "Argent 3   "
	elif tl_rank > 1600 and tl_rank < 1800:
		tl_rank_s = "Argent 2   "
	elif tl_rank > 1800 and tl_rank < 2000:
		tl_rank_s = "Argent 1   "
	elif tl_rank > 2000 and tl_rank < 2200:
		tl_rank_s = "Gold 5     "
	elif tl_rank > 2200 and tl_rank < 2400:
		tl_rank_s = "Gold 4     "
	elif tl_rank > 2400 and tl_rank < 2600:
		tl_rank_s = "Gold 3     "
	elif tl_rank > 2600 and tl_rank < 2800:
		tl_rank_s = "Gold 2     "
	elif tl_rank > 2800 and tl_rank < 3000:
		tl_rank_s = "Gold 1     "
	elif tl_rank > 3000 and tl_rank < 3200:
		tl_rank_s = "Platinium 5"
	elif tl_rank > 3200 and tl_rank < 3400:
		tl_rank_s = "Platinium 4"
	elif tl_rank > 3400 and tl_rank < 3600:
		tl_rank_s = "Platinium 3"
	elif tl_rank > 3600 and tl_rank < 3800:
		tl_rank_s = "Platinium 2"
	elif tl_rank > 3800 and tl_rank < 4000:
		tl_rank_s = "Platinium 1"
	elif tl_rank > 4000 and tl_rank < 4200:
		tl_rank_s = "Diamond 5  "
	elif tl_rank > 4200 and tl_rank < 4400:
		tl_rank_s = "Diamond 4  "
	elif tl_rank > 4400 and tl_rank < 4600:
		tl_rank_s = "Diamond 3  "
	elif tl_rank > 4600 and tl_rank < 4800:
		tl_rank_s = "Diamond 2  "
	elif tl_rank > 4800 and tl_rank < 5000:
		tl_rank_s = "Diamond 1  "
	elif tl_rank > 5000:
		tl_rank_s = "Master     "
	else:
		tl_rank_s = "None           "

	return tl_rank_s

def help():

	print("<==== HELP ====>")
	print("\t-info : <battletag>\tDirectly show player info")
	print("\t-help :            \tShow help")

	exit()

main()