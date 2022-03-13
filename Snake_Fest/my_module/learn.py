from my_module import initialize_q
import random

import settings

import dataclasses

@dataclasses.dataclass
class GameState:
    distance: tuple
    position: tuple
    surroundings: str
    food: tuple


class learn(object):
    def __init__(self, epsilon, alpha, discount, grid_size, env):
        self.history = []
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = discount
        self.grid_length = grid_size[0]
        self.grid_width = grid_size[1]
        self.env = env
        self.q_table = initialize_q.LoadQvalues(settings.files["q_values"], "qvalue_1.json")

    def act(self, snake, food):
        state = self.findstate(snake, food)
        direction = 0
        
        # exploration or exploitation, epsilon greedy
        rand = random.uniform(0,1)
        if rand < self.epsilon:
            direction = self.env.action_space.sample()
        else:
            state_scores = self.q_table[self._GetStateStr(state)]
            direction = state_scores.index(max(state_scores))

        self.history.append({'state':state, 'action': direction})
        if direction == 0:
            direction = 3
        elif direction == 1:
            direction = 1
        elif direction == 2:
            direction = 0
        else:
            direction = 2

    
        return direction

    def UpdateQValues(self, reward1):
        history = self.history[::-1]
        reward = 0
        for i, h in enumerate(history[:-1]):
            if reward1 == -1: # Snake Died -> Negative reward
                state = self._GetStateStr(history[0]['state'])
                action = history[0]['action']
                reward = -10
                self.q_table[state][action] = (1-self.alpha) * self.q_table[state][action] + self.alpha * reward # Bellman equation - there is no future state since game is over
            else:
                s1 = h['state'] # current state
                s0 = history[i+1]['state'] # previous state
                a0 = history[i+1]['action'] # action taken at previous state
            
                x1 = s0.distance[0] # x distance at current state
                y1 = s0.distance[1] # y distance at current state
    
                x2 = s1.distance[0] # x distance at previous state
                y2 = s1.distance[1] # y distance at previous state

                if reward1 == 1:
                    reward = 10
                elif (abs(x1) > abs(x2) or abs(y1) > abs(y2)):
                    reward = 1  
                else:
                    reward = -1
                state_str = self._GetStateStr(s0)
                new_state_str = self._GetStateStr(s1)
                self.q_table[state_str][a0] = (1-self.alpha) * (self.q_table[state_str][a0]) + self.alpha * (reward + self.discount*max(self.q_table[new_state_str])) # Bellman equation
        return reward

    def findstate(self, snake, food):
        snake_head = snake.head
        dist_x = food[0] - snake_head[0]
        dist_y = food[1] - snake_head[1]

        if dist_x > 0:
            pos_x = '1' # Food is to the right of the snake
        elif dist_x < 0:
            pos_x = '0' # Food is to the left of the snake
        else:
            pos_x = 'NA' # Food and snake are on the same X file

        if dist_y > 0:
            pos_y = '3' # Food is below snake
        elif dist_y < 0:
            pos_y = '2' # Food is above snake
        else:
            pos_y = 'NA' # Food and snake are on the same Y file
        
        # moves in all direction
        sqs = [
            (snake_head[0]-1, snake_head[1]),   # left
            (snake_head[0]+1, snake_head[1]),   # right    
            (snake_head[0],                  snake_head[1]-1), #up
            (snake_head[0],                  snake_head[1]+1), #down
        ]
        
        surrounding_list = []
        for sq in sqs:
            if sq[0] < 0 or sq[1] < 0: # off screen left or top
                surrounding_list.append('1')
            elif sq[0] >= self.grid_length or sq[1] >= self.grid_width: # off screen right or bottom
                surrounding_list.append('1')
            elif sq in snake.body[0]: # part of tail
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        surroundings = ''.join(surrounding_list)
        return GameState((dist_x, dist_y), (pos_x, pos_y), surroundings, food)

    def _GetStateStr(self, state):
        return str((state.position[0],state.position[1],state.surroundings))
        