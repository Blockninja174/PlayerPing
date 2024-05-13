import requests, json, os, time, tqdm

def get_players_from_server():
    url = "https://api.mcstatus.io/v2/status/java/n111.pufferfish.host:25565"
    response = requests.get(url)
    data = json.loads(response.text)
    return get_clean_names(data)

def get_clean_names(json_data):
    clean_names = []

    if 'players' in json_data and 'list' in json_data['players']:
        for player in json_data['players']['list']:
            if 'name_clean' in player:
                clean_names.append(player['name_clean'])
    return clean_names
os.system('cls')
'''
while True:
    print("Players online: ")
    print(get_players_from_server())
    # Status Bar
    for i in tqdm.tqdm(range(5), desc="Refresh"):
        time.sleep(1)
    os.system('cls')'''