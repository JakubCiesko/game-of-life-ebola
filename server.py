from game import Game

import asyncio

from sanic import Sanic
from sanic import request, response 


app = Sanic("GameOfLife")

app.static("/static", "./")

GAMES = {}

game_of_life_settings = {
        'life_symbol': "X",#live_cell_symbol,
        'death_symbol': "P", #dead_cell_symbol,
        'replay_key': 'x',
        'time_delay': 0.05, #time_delay,
        'file_path': 'C:/Users/Asus/Desktop/pandemic.txt',
        'threshold_values': {
            'underpopulation': 2,
            'survive': 4,
            'overpopulation': 3,
            'revive': 3,
            'ebola': True,
            'ebola-life': 15,
            'ebola-infection': 5,
            'initial-number-of-ebola-cells': 80,
            'number_of_cells': 1000
        },
        'width': 100,
        'height': 100
    }

async def load_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as input_file:
        return input_file.read()


@app.route("/")
async def returnsomething(request):
    index_site = await load_content("index.html")
    reply = response.html(index_site)
    game_id = request.cookies.get("game_id")
    if game_id:
        game, task = GAMES[game_id]
        task.cancel()
        del game
        reply.delete_cookie("game_id")
    return reply


@app.route("/get_cells")
async def get_cells_handler(request):
    game_id = request.cookies.get("game_id")
    reply = response.json({"error_message": "No simulation started"}, status=400)
    if game_id:
        game, task = GAMES[game_id]
        cells_coordinates = game.get_alive_cells_coordinates()
        reply =  response.json(cells_coordinates)
        if game.finished:
            task.cancel()
            reply.delete_cookie("game_id")
            del game 
    return reply
    

@app.route("/get_stats")
async def get_stats_handler(request):
    reply = response.json({"error_message": "No simulation started"}, status=400)
    game_id = request.cookies.get("game_id")
    if game_id:
        game, task = GAMES[game_id]
        data_collector = game.get_data_collector()
        stats = data_collector.get_SIR()
        reply = response.json(stats)
        if game.finished:
            task.cancel()
            reply.delete_cookie("game_id")
            del game 
    return reply

async def create_cookies(sanic_response, cookie_name: str, cookie_value, cookie_age = 36000, httponly = True):
    sanic_response.add_cookie(cookie_name, cookie_value, max_age=cookie_age, httponly=httponly)
    sanic_response.cookies[cookie_name] = cookie_value        # user_task.add_cookie("task_id", task_id)
    sanic_response.cookies[cookie_name].max_age = cookie_age  # user_task.cookies.get_cookie("task_id").max_age = 36000
    sanic_response.cookies[cookie_name].httponly = httponly   # user_task.cookies.get_cookie("task_id").httponly = True
    return sanic_response


@app.route("/set_settings", methods=["POST"])
async def settings_setter(request):
    if request.json:
        data = request.json 
        game_of_life_settings['threshold_values']['initial-number-of-ebola-cells'] = int(data["initialInfectedNumber"])
        game_of_life_settings['threshold_values']['number_of_cells'] = int(data['totalNumberOfCells'])
        game_of_life_settings['width'] = data['windowWidth'] if 10 <= data['windowWidth'] <= 250 else 100
        game_of_life_settings['height'] = data['windowHeight'] if 10 <= data['windowHeight'] <= 250 else 100
        game_of_life_settings['threshold_values']['underpopulation'] = int(data['underpopulation'])
        game_of_life_settings['threshold_values']['survive'] = int(data['survive'])
        game_of_life_settings['threshold_values']['overpopulation'] = int(data['overpopulation'])
        game_of_life_settings['threshold_values']['ebola'] = bool(data['ebola'])
        game_of_life_settings['threshold_values']['ebola-life'] = int(data['ebola_life'])
        game_of_life_settings['threshold_values']['ebola-infection'] = int(data['ebola_infection'])
    return response.json(data)


@app.route("/start_simluation")
async def start_simulation_hanlder(request):
    game_id = f"{len(GAMES)}"
    game = Game()
    game.set_settings(game_of_life_settings)
    game.create_game()
    task = asyncio.create_task(asyncio.to_thread(game.start_game))
    GAMES[game_id] = (game, task)
    user_task =  response.json({"game_id": game_id})
    user_task = await create_cookies(user_task, cookie_name="game_id", cookie_value=game_id)
    return user_task
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
