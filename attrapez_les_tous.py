import requests
import random
import time
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

# List of all Pokemon types and their score modifiers against other types
type_advantages = {
    'normal': {'rock': 0.5, 'ghost': 0.0, 'steel': 0.5},
    'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2.0, 'ice': 2.0, 'bug': 2.0, 'rock': 0.5, 'dragon': 0.5, 'steel': 2.0},
    'water': {'fire': 2.0, 'water': 0.5, 'grass': 0.5, 'ground': 2.0, 'rock': 2.0, 'dragon': 0.5},
    'electric': {'water': 2.0, 'electric': 0.5, 'grass': 0.5, 'ground': 0.0, 'flying': 2.0, 'dragon': 0.5},
    'grass': {'fire': 0.5, 'water': 2.0, 'grass': 0.5, 'poison': 0.5, 'ground': 2.0, 'flying': 0.5, 'bug': 0.5, 'rock': 2.0, 'dragon': 0.5, 'steel': 0.5},
    'ice': {'fire': 0.5, 'water': 0.5, 'grass': 2.0, 'ice': 0.5, 'ground': 2.0, 'flying': 2.0, 'dragon': 2.0, 'steel': 0.5},
    'fighting': {'normal': 2.0, 'ice': 2.0, 'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 2.0, 'ghost': 0.0, 'dark': 2.0, 'steel': 2.0, 'fairy': 0.5},
    'poison': {'grass': 2.0, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0.0, 'fairy': 2.0},
    'ground': {'fire': 2.0, 'electric': 2.0, 'grass': 0.5, 'poison': 2.0, 'flying': 0.0, 'bug': 0.5, 'rock': 2.0, 'steel': 2.0},
    'flying': {'electric': 0.5, 'grass': 2.0, 'fighting': 2.0, 'bug': 2.0, 'rock': 0.5, 'steel': 0.5},
    'psychic': {'fighting': 2.0, 'poison': 2.0, 'psychic': 0.5, 'dark': 0.0, 'steel': 0.5},
    'bug': {'fire': 0.5, 'grass': 2.0, 'fighting': 0.5, 'poison': 0.5, 'flying': 0.5, 'psychic': 2.0, 'ghost': 0.5, 'dark': 2.0, 'steel': 0.5, 'fairy': 0.5},
    'rock': {'fire': 2.0, 'ice': 2.0, 'fighting': 0.5, 'ground': 0.5, 'flying': 2.0, 'bug': 2.0, 'steel': 0.5},
    'ghost': {'normal': 0.0, 'psychic': 2.0, 'ghost': 2.0, 'dark': 0.5},
    'dragon': {'dragon': 2.0, 'steel': 0.5, 'fairy': 0.0},
    'dark': {'fighting': 0.5, 'psychic': 2.0, 'ghost': 2.0, 'dark': 0.5, 'fairy': 0.5},
    'steel': {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2.0, 'rock': 2.0, 'steel': 0.5, 'fairy': 2.0},
    'fairy': {'fire': 0.5, 'fighting': 2.0, 'poison': 0.5, 'dragon': 2.0, 'dark': 2.0, 'steel': 0.5}
}

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
            'speed': data['stats'][5]['base_stat'],
            'type': [t['type']['name'] for t in data['types']],
            'sprite': data['sprites']['front_default']
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
            time.sleep(0.5)
        
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
            winner = battle(pokemon_list[i], pokemon_list[i+1], round_number)
            next_round.append(winner)
            time.sleep(1)
        pokemon_list = next_round
        round_number += 1

    champion = pokemon_list[0]
    print(f"\n--- The Champion is {champion['name'].capitalize()}! ---")
    display_winner(champion)

def battle(pokemon1, pokemon2, round_number):
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

    for type1 in pokemon1['type']:
        for type2 in pokemon2['type']:
            # Checking if the type and the modifier against the other type is present in type_advantage
            # If not, there is not modifier for the current type against the other current type
            if type1 in type_advantages and type2 in type_advantages[type1]:
                score1 *= type_advantages[type1][type2]
            if type2 in type_advantages and type1 in type_advantages[type2]:
                score2 *= type_advantages[type2][type1]

    print(f"{pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}!")
    display_battle(pokemon1, pokemon2, score1, score2, round_number)

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
        
def display_battle(pokemon1, pokemon2, score1, score2, round_number):
    window = tk.Tk()
    window.geometry("1000x200")
    window.title("Pokémon Battle")

    round_label = tk.Label(window, text=f"Round {round_number}", font=("Arial, 18"))
    round_label.pack()
    
    url1 = pokemon1['sprite']
    url2 = pokemon2['sprite']
    # Opening the pictures from the URL and allows to read them online
    image1 = Image.open(BytesIO(urllib.request.urlopen(url1).read()))
    image2 = Image.open(BytesIO(urllib.request.urlopen(url2).read()))
    # Converting the pictures to display them on Tkinter 
    photo1 = ImageTk.PhotoImage(image1)
    photo2 = ImageTk.PhotoImage(image2)

    # Displaying the first Pokemon picture
    img_label1 = tk.Label(window, image=photo1)
    img_label1.pack(side="left", padx=10)
    # Displaying the second Pokemon picture
    img_label2 = tk.Label(window, image=photo2)
    img_label2.pack(side="right", padx=10)

    label = tk.Label(window, text=f"{pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}!", font=("Arial", 16))
    label.pack()

    type_label1 = tk.Label(window, text=f"Type: {', '.join(pokemon1['type'])}", font=("Arial", 12))
    type_label1.pack(side="left", padx=10, pady=10)

    type_label2 = tk.Label(window, text=f"Type: {', '.join(pokemon2['type'])}", font=("Arial", 12))
    type_label2.pack(side="right", padx=10, pady=10)

    score_label = tk.Label(window, text=f"{pokemon1['name'].capitalize()}: {score1:.2f} vs {pokemon2['name'].capitalize()}: {score2:.2f}", font=("Arial", 14))
    score_label.pack()

    winner_name = pokemon1['name'].capitalize() if score1 > score2 else pokemon2['name'].capitalize()
    winner_label = tk.Label(window, text=f"Winner: {winner_name}", font=("Arial", 14))
    winner_label.pack()

    # Attendre un peu avant de fermer la fenêtre pour que l'utilisateur ait le temps de voir le résultat
    window.after(5000, window.destroy)
    window.mainloop()

def display_winner(champion):
    window = tk.Tk()
    window.geometry("1000x200")
    window.title("Tournament Winner")

    url = champion['sprite']
    # Opening the picture from the URL and allows to read it online
    image = Image.open(BytesIO(urllib.request.urlopen(url).read()))
    # Converting the picture to display it on Tkinter 
    photo = ImageTk.PhotoImage(image)
    # Displaying the winner picture
    img_label = tk.Label(window, image=photo)
    img_label.pack(pady=10)

    label = tk.Label(window, text=f"The winner is {champion['name'].capitalize()}!", font=("Arial", 16))
    label.pack()

    type_label = tk.Label(window, text=f"Type: {', '.join(champion['type'])}", font=("Arial", 14))
    type_label.pack()

    # Attendre un peu avant de fermer la fenêtre pour que l'utilisateur ait le temps de voir le résultat
    window.after(5000, window.destroy)
    window.mainloop()

def display_start():
    window = tk.Tk()
    window.geometry("1000x200")
    window.title("Starting Pokémon tournament...")

    label = tk.Label(window, text="Choosing the Pokémon, please wait...", font=("Arial", 16))
    label.pack()

    # Attendre un peu avant de fermer la fenêtre pour que l'utilisateur ait le temps de voir le résultat
    window.after(3000, window.destroy)
    window.mainloop()

if __name__ == "__main__":
    display_start()
    run_tournament(create_pokemon_list())
