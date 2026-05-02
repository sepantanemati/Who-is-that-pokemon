from flask import Flask , request, render_template, jsonify, Blueprint, redirect, url_for, session
import requests
import random

hard_mode = Blueprint('hard_mode', __name__)    

base_url = "https://pokeapi.co/api/v2/pokemon/"

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
    answer_text = request.args.get('msg', "")

    if "hard_point" not in session:
        session["hard_point"] = 10
    if "hard_record" not in session:
        session["hard_record"] = 0
    if "hard_name" not in session:
        image, name = get_info()
        session["hard_image"] = image
        session["hard_name"] = name

    if request.method == "POST":
        guessed_name = request.form.get("gs")
        
        if "enter" in request.form:
            if session["hard_point"] <= 0:
                answer_text = f"you are out of points"
                session["hard_image"] = "https://i.postimg.cc/Xv00JJYr/GAME-OVER.png" 
                session["hard_name"] = "GAMEOVER"
            elif guessed_name.lower() == session["hard_name"].lower():
                answer_text = f"you got it right, his name was:{session['hard_name']}"
                image, name = get_info()
                session["hard_image"] = image
                session["hard_name"] = name
                session["hard_point"] += 1    
                if session["hard_point"] > session["hard_record"]:
                    session["hard_record"] = session["hard_point"]
            else:
                answer_text = f"wrong its name was:{session['hard_name']}"
                image, name = get_info()
                session["hard_image"] = image
                session["hard_name"] = name
                session["hard_point"] -= 1
                
        elif "restart" in request.form:
            session["hard_point"] = 10
            image, name = get_info()
            session["hard_image"] = image
            session["hard_name"] = name
            
        return redirect(url_for('hard_mode.send_info_hard', msg=answer_text))       
        
    return render_template("hard.html", 
                           answer=answer_text, 
                           pokemonimage=session.get('hard_image'), 
                           score=session.get('hard_point'), 
                           best=session.get('hard_record'))


    

