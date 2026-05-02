from flask import Flask , request, render_template, jsonify, Blueprint, redirect, url_for
import requests
import random

hard_mode = Blueprint('hard_mode', __name__)    
point = 10
record = 0
base_url = "https://pokeapi.co/api/v2/pokemon/"
memory = {"name": "", "image": ""}


pokemon_list = [
    "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
    "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree",
    "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot", "rattata",
    "raticate", "spearow", "fearow", "ekans", "arbok", "pikachu", "raichu",
    "sandshrew", "sandslash", "nidoran-f", "nidorina", "nidoqueen", "nidoran-m",
    "nidorino", "nidoking", "clefairy", "clefable", "vulpix", "ninetales",
    "jigglypuff", "wigglytuff", "zubat", "golbat", "oddish", "gloom", "vileplume",
    "paras", "parasect", "venonat", "venomoth", "diglett", "dugtrio", "meowth",
    "persian", "psyduck", "golduck", "mankey", "primeape", "growlithe", "arcanine",
    "poliwag", "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam", "machop",
    "machoke", "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool",
    "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash", "slowpoke",
    "slowbro", "magnemite", "magneton", "farfetchd", "doduo", "dodrio", "seel",
    "dewgong", "grimer", "muk", "shellder", "cloyster", "gastly", "haunter",
    "gengar", "onix", "drowzee", "hypno", "krabby", "kingler", "voltorb"
]
def randomchoice():
    rndmname = random.choice(pokemon_list)
    return rndmname

def get_info():
    rndmname = randomchoice()
    response = requests.get(f"{base_url}{rndmname}")
    data = response.json()

    image = data['sprites']['other']['official-artwork']['front_default']
    return image, rndmname


@hard_mode.route("/hardmode", methods=["POST", "GET"])



def send_info_hard():
    global record
    global point
    global memory
    answer_text = request.args.get('msg', "")

    if memory["name"] == "":
        image, name = get_info()
        memory["image"] = image
        memory["name"] = name
    if request.method == "POST":
        guessed_name = request.form.get("gs",)
        if "enter" in request.form:
            if point == 0:
                answer_text = f"you are out of points"
                memory["image"] = "https://i.postimg.cc/Xv00JJYr/GAME-OVER.png" 
                memory["name"] = "GAMEOVER"
            elif guessed_name.lower() == memory["name"].lower():
                answer_text = f"you got it right, his name was:{memory["name"]}"
                image, name = get_info()
                memory["image"] = image
                memory["name"] = name
                point += 1    
                if point > record :
                    record = point
            
            else:
                answer_text = f"wrong its name was:{memory["name"]}"
                image, name = get_info()
                memory["image"] = image
                memory["name"] = name
                point -= 1
        elif "restart" in request.form:
            point = 10
        return redirect(url_for('hard_mode.send_info_hard', msg=answer_text, answer=answer_text))       
    return render_template("hard.html", answer=answer_text, pokemonimage=memory["image"], score = point,best = record)


    

