from random import randint


class Game():

    def __init__(self, screen_width: int = 10, screen_height: int = 10) -> None:
        self.state =  {
            'players': {},
            'fruits': {},
            'screen': {
                'width': screen_width,
                'height': screen_height
            }
        }
        self.observers = []

    def subscribe(self, function):
        self.observers.append(function)

    def notfity_all(self, message):
        for observer in self.observers:
            observer(message)

    def add_player(self, player_id: str, player_x: int = None, player_y: int = None) -> None:
        self.state['players'][player_id] = {
            'x': randint(0, self.state['screen']['width'] - 1) if player_x is None else player_x,
            'y': randint(0, self.state['screen']['width'] - 1) if player_y is None else player_y,
            'score': 0,
        }

        self.notfity_all({
            'type': 'add-player',
            'playerId': player_id,
            'playerX': self.state['players'][player_id]['x'],
            'playerY': self.state['players'][player_id]['y'],
        })

    def remove_player(self, player_id: str) -> None:
        del self.state['players'][player_id]

        self.notfity_all({'type': 'remove-player', 'playerId': player_id})

    def add_fruit(self, fruit_id: str = None, fruit_x: int = None, fruit_y: int = None) -> None:
        fruit_id = randint(0, 10000) if fruit_id is None else fruit_id 
        fruit_x = randint(0, self.state['screen']['width'] - 1) if fruit_x is None else fruit_x 
        fruit_y = randint(0, self.state['screen']['width'] - 1) if fruit_y is None else fruit_y
        self.state['fruits'][fruit_id] = {
            'x': fruit_x,
            'y': fruit_y
        }

        self.notfity_all({'type': 'add-fruit', 'fruitId': fruit_id, 'fruitX': fruit_x, 'fruitY': fruit_y})

    def remove_fruit(self, fruit_id: str) -> None:
        del self.state['fruits'][fruit_id]

        self.notfity_all({'type': 'remove-fruit', 'fruitId': fruit_id})

    def player_action(self, player_id: str, action: str) -> None:
        player = self.state['players'][player_id]
        if action == "ArrowUp":
            player['y'] = max(player['y'] - 1, 0)
        elif action == "ArrowRight":
            player['x'] = min(player['x'] + 1, self.state['screen']['width'] - 1)
        elif action == "ArrowDown":
            player['y'] = min(player['y'] + 1, self.state['screen']['height'] - 1)
        elif action == "ArrowLeft":
            player['x'] = max(player['x'] - 1, 0)
        else:
            print('Action not implemented')
        self.state['players'][player_id] = player        

        self.notfity_all({'type': 'move-player', 'playerId': player_id, 'keyPressed': action})
        self.check_colidion(player_id=player_id)

    def check_colidion(self, player_id: str) -> None:
        player = self.state['players'][player_id]
        remove_fruits = []
        for fruit in self.state['fruits']:
            if self.state['fruits'][fruit]['x'] == player['x'] and self.state['fruits'][fruit]['y'] == player['y']:
                remove_fruits.append(fruit)
        for fruit in remove_fruits:
            self.remove_fruit(fruit_id=fruit)
            self.state['players'][player_id]['score'] += 1

    def player_add_point(self, player_id: str) -> None:
        self.state['players'][player_id]['score'] += 1
        self.notfity_all({'type': 'add-point', 'playerId': player_id, 'score': self.state['players'][player_id]['score']})




