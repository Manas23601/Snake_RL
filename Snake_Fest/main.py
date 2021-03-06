import numpy as np
import matplotlib
import gym
import gym_snake
from  my_module import initialize_q, learn
import os
import settings

#Making the environment
env = gym.make('snake-v0')
env.grid_size = [30,30]
env.unit_size = 10
env.unit_gap = 1
env.snake_size = 1
env.n_snakes = 2
env.n_foods = 2 


# Training settings
epsilon = 0.1
alpha = 0.7
discount = 0.5
num_of_episodes = 150
max_moves_per_episode = 350

max_epsilon  = 1
min_epsilon = 0.1
epsilon_decay_rate = 0.01

initialize_q.initialise_q_table(settings.files['q_values'], "qvalue_1.json")


def gameloop(max_moves_per_episode):
    episode_reward = 0
    learner = learn.learn(epsilon, alpha, discount, env.grid_size, env)
    controller = env.controller
    # all snake bodies list of deque
    for move in range(max_moves_per_episode):
        snakes = controller.snakes
        foods = controller.grid.foods
        direction = learner.act(snakes[0],foods[0])
        env.render()
        board, reward, done, info = env.step(direction)
        reward1 = learner.UpdateQValues(reward)
        episode_reward += reward
        if reward == -1:
            break
    initialize_q.SaveQvalues(settings.files['q_values'], "qvalue_1.json", learner.q_table)
    return episode_reward


episode_reward = []
for episode in range(num_of_episodes):
    observation = env.reset()
    episode_reward.append(gameloop(max_moves_per_episode))
    print("game {0} score:".format(episode+1), episode_reward[-1])
    if episode > 100:
        epsilon = 0
    # epsilon = min_epsilon + epsilon * np.exp(-epsilon_decay_rate * (100 + episode))
    

