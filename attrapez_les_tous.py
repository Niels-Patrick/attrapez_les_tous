import requests
import random
import time

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon_info(pokemon_id):
    '''
    Fetches the information of the Pokémon which id has been passed as parameter

    Parameters:
    pokemon_id: the id of the fetched pokemon

    Return:
    A dictionary containing the name, hp, attack, defense and speed of the Pokémon
    '''
    try:
        url = f"{POKEAPI_BASE_URL}{pokemon_id}"
        response = requests.get(url)
        response.raise_for_status()  # Checking if the requests worked
        data = response.json()
        # Fetching the import stats for battles
        return {
            'name': data['name'],
            'hp': data['stats'][0]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'speed': data['stats'][5]['base_stat']
        }
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
    return None

def create_pokemon_list():
    '''
    Creates the list of the 16 chosen Pokemon for the tournament

    Return:
    list_pokemon: contains all 16 chosen Pokemon
    '''
    list_pokemon = []

    try:
        for i in range(0, 16):
            list_pokemon.append(get_pokemon_info(random.randint(1, 1025)))
            time.sleep(1)
        
        return list_pokemon
    except:
        print("An error occurred.")

def run_tournament(pokemon_list):
    '''
    Starts the tournament process, chosing 2 Pokemon for each 1v1 battle, and keeping only
    the winners in the Pokemon list. There will be as much rounds as needed to keep only one Pokemon
    in the list, who will be the tournament winner.

    Parameters:
    pokemon_list: a list containing the 16 chosen Pokemon
    '''
    round_number = 1
    while len(pokemon_list) > 1:
        print(f"\n--- Round {round_number} ---")
        next_round = []
        for i in range(0, len(pokemon_list), 2):
            winner = battle(pokemon_list[i], pokemon_list[i+1])
            next_round.append(winner)
            time.sleep(1)
        pokemon_list = next_round
        round_number += 1

    champion = pokemon_list[0]
    print(f"\n--- The Champion is {champion['name'].capitalize()}! ---")

def battle(pokemon1, pokemon2):
    '''
    The 1v1 battle process, based on each Pokemon stats

    Parameters:
    pokemon1: the first chosen Pokemon for the battle
    pokemon2: the second chosen Pokemon for the battle

    Return:
    pokemon1 OR pokemon2 depending on the result of the battle
    '''
    # Calculating the score of each Pokemon based on their stats
    score1 = (pokemon1['attack'] + pokemon1['hp'] + pokemon1['speed']) - pokemon2['defense']
    score2 = (pokemon2['attack'] + pokemon2['hp'] + pokemon2['speed']) - pokemon1['defense']

    print(f"{pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}!")

    # Determining the winner
    if score1 > score2:
        print(f"{pokemon1['name'].capitalize()} wins!")
        return pokemon1
    elif score2 > score1:
        print(f"{pokemon2['name'].capitalize()} wins!")
        return pokemon2
    else:
        # If they are at a stale, the Pokemon with the highest speed wins
        if pokemon1['speed'] > pokemon2['speed']:
            print(f"{pokemon1['name'].capitalize()} wins by speed tie!")
            return pokemon1
        else:
            print(f"{pokemon2['name'].capitalize()} wins by speed tie!")
            return pokemon2

if __name__ == "__main__":
    print("The Pokemon tournament will begin!")
    time.sleep(1)
    print("Choosing the Pokemon...")
    run_tournament(create_pokemon_list())
