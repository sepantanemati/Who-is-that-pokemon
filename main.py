from flask import Flask , request, render_template, jsonify, redirect, url_for
from hardmode import hard_mode
from impossiblemode import imp_mode
import requests
import random
import os

app = Flask(__name__)

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


@app.route("/", methods=["POST", "GET"])



def send_info():
    global memory
    answer_text = request.args.get('msg', "")

    if memory["name"] == "":
        image, name = get_info()
        memory["image"] = image
        memory["name"] = name
    if request.method == "POST":
        guessed_name = request.form.get("gs",)
        if "enters" in request.form:
            if guessed_name.lower() == memory["name"].lower():
                answer_text = f"you got it right, his name was:{memory['name']}"
                image, name = get_info()
                memory["image"] = image
                memory["name"] = name
            else:
                answer_text = f"wrong its name was:{memory['name']}"
                image, name = get_info()
                memory["image"] = image
                memory["name"] = name
        return redirect(url_for('send_info', msg=answer_text, answer=answer_text))
    return render_template("index.html", answer=answer_text, pokemonimage=memory['image'])
app.register_blueprint(hard_mode)
app.register_blueprint(imp_mode)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    

