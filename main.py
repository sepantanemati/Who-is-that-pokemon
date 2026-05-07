from flask import Flask , request, render_template, jsonify, redirect, url_for, session
from hardmode import hard_mode
from impossiblemode import imp_mode
import requests
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_key_123")

base_url = "https://pokeapi.co/api/v2/pokemon/"

pokemon_list = [
    # --- GENERATIE 1 (KANTO) ---
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
    "gengar", "onix", "drowzee", "hypno", "krabby", "kingler", "voltorb",
    "electrode", "exeggcute", "exeggutor", "cubone", "marowak", "hitmonlee", 
    "hitmonchan", "lickitung", "koffing", "weezing", "rhyhorn", "rhydon", 
    "chansey", "tangela", "kangaskhan", "horsea", "seadra", "goldeen", 
    "seaking", "staryu", "starmie", "mr-mime", "scyther", "jynx", 
    "electabuzz", "magmar", "pinsir", "tauros", "magikarp", "gyarados", 
    "lapras", "ditto", "eevee", "vaporeon", "jolteon", "flareon", 
    "porygon", "omanite", "omastar", "kabuto", "kabutops", "aerodactyl", 
    "snorlax", "articuno", "zapdos", "moltres", "dratini", "dragonair", 
    "dragonite", "mewtwo", "mew",

    # --- GENERATIE 2 (JOHTO) ---
    "chikorita", "bayleef", "meganium", "cyndaquil", "quilava", "typhlosion",
    "totodile", "croconaw", "feraligatr", "sentret", "furret", "hoothoot",
    "noctowl", "ledyba", "ledian", "spinarak", "ariados", "crobat", "chinchou",
    "lanturn", "pichu", "cleffa", "igglybuff", "togepi", "togetic", "natu",
    "xatu", "mareep", "flaaffy", "ampharos", "bellossom", "marill", "azumarill",
    "sudowoodo", "politoed", "hoppip", "skiploom", "jumpluff", "aipom",
    "sunkern", "sunflora", "yanma", "wooper", "quagsire", "espeon", "umbreon",
    "murkrow", "slowking", "misdreavus", "unown", "wobbuffet", "girafarig",
    "pineco", "forretress", "dunsparce", "gligar", "steelix", "snubbull",
    "granbull", "qwilfish", "scizor", "shuckle", "heracross", "sneasel",
    "teddiursa", "ursaring", "slugma", "magcargo", "swinub", "piloswine",
    "corsola", "remoraid", "octillery", "delibird", "mantine", "skarmory",
    "houndour", "houndoom", "kingdra", "phanpy", "donphan", "porygon2",
    "stantler", "smeargle", "tyrogue", "hitmontop", "smoochum", "elekid",
    "magby", "miltank", "blissey", "raikou", "entei", "suicune", "larvitar",
    "pupitar", "tyranitar", "lugia", "ho-oh", "celebi",

    # --- GENERATIE 3 (HOENN) ---
    "treecko", "grovyle", "sceptile", "torchic", "combusken", "blaziken",
    "mudkip", "marshtomp", "swampert", "poochyena", "mightyena", "zigzagoon",
    "linoone", "wurmple", "silcoon", "beautifly", "cascoon", "dustox",
    "lotad", "lombre", "ludicolo", "seedot", "nuzleaf", "shiftry", "taillow",
    "swellow", "wingull", "pelipper", "ralts", "kirlia", "gardevoir",
    "surskit", "masquerain", "shroomish", "breloom", "slakoth", "vigoroth",
    "slaking", "nincada", "ninjask", "shedinja", "whismur", "loudred",
    "exploud", "makuhita", "hariyama", "azurill", "nosepass", "skitty",
    "delcatty", "sableye", "mawile", "aron", "lairon", "aggron", "meditite",
    "medicham", "electrike", "manectric", "plusle", "minun", "volbeat",
    "illumise", "roselia", "gulpin", "swalot", "carvanha", "sharpedo",
    "wailmer", "wailord", "numel", "camerupt", "torkoal", "spoink", "grumpig",
    "spinda", "trapinch", "vibrava", "flygon", "cacnea", "cacturne", "swablu",
    "altaria", "zangoose", "seviper", "lunatone", "solrock", "barboach",
    "whiscash", "corphish", "crawdaunt", "baltoy", "claydol", "lileep",
    "cradily", "anorith", "armaldo", "feebas", "milotic", "castform",
    "kecleon", "shuppet", "banette", "duskull", "dusclops", "tropius",
    "chimecho", "absol", "wynaut", "snorunt", "glalie", "spheal", "sealeo",
    "walrein", "clamperl", "huntail", "gorebyss", "relicanth", "luvdisc",
    "bagon", "shelgon", "salamence", "beldum", "metang", "metagross",
    "regirock", "regice", "registeel", "latias", "latios", "kyogre",
    "groudon", "rayquaza", "jirachi", "deoxys-normal"
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
    answer_text = request.args.get('msg', "")

    if "name" not in session:
        image, name = get_info()
        session["image"] = image
        session["name"] = name
    if request.method == "POST":
        guessed_name = request.form.get("gs",)
        if "enters" in request.form:
            if guessed_name.lower() == session["name"].lower():
                answer_text = f"you got it right, his name was:{session['name']}"
                image, name = get_info()
                session["image"] = image
                session["name"] = name
            else:
                answer_text = f"wrong its name was:{session['name']}"
                image, name = get_info()
                session["image"] = image
                session["name"] = name
        return redirect(url_for('send_info', msg=answer_text))
    return render_template("index.html", answer=answer_text, pokemonimage=session.get('image'))

app.register_blueprint(hard_mode)
app.register_blueprint(imp_mode)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
