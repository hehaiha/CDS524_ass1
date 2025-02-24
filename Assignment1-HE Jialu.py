#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  

# Game parameters
SIMULATION_DAYS = 7
INITIAL_SEEDS = 10
INITIAL_FERTILIZER = 10
INITIAL_WATER = 10

# Crop information
CROPS = {
    "tomato": {
        "growth_cycle": 3,
        "seed_cost": 2,
        "fertilizer_need": 1,
        "water_need": 1,
        "reward": 10
    },
    "carrot": {
        "growth_cycle": 2,
        "seed_cost": 1,
        "fertilizer_need": 1,
        "water_need": 1,
        "reward": 5
    }
}

# Weather conditions
WEATHERS = ["sunny", "rainy", "stormy"]
WEATHER_PROB = [0.6, 0.3, 0.1]

# Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
INITIAL_EPSILON = 0.9
EPSILON_DECAY = 0.99

# State space and action space
def get_state(seeds, fertilizer, water, crops_growth, weather, market_price):
    return (seeds, fertilizer, water, tuple(crops_growth), weather, market_price)

ACTIONS = ["buy_seeds", "buy_fertilizer", "buy_water", "plant_tomato", "plant_carrot", "harvest", "do_nothing"]

# Initialize the Q-table
state_space_size = 20 * 20 * 20 * (len(CROPS) * 5) * len(WEATHERS) * 10
action_space_size = len(ACTIONS)
Q_TABLE = np.zeros((state_space_size, action_space_size))

# Reward function
def get_reward(state, action, next_state):
    seeds, fertilizer, water, crops_growth, weather, market_price = state
    next_seeds, next_fertilizer, next_water, next_crops_growth, next_weather, next_market_price = next_state
    reward = 0

    if action.startswith("buy_"):
        if action == "buy_seeds" and next_seeds > seeds:
            reward -= 3  # Cost of buying seeds
        elif action == "buy_fertilizer" and next_fertilizer > fertilizer:
            reward -= 2  # Cost of buying fertilizer
        elif action == "buy_water" and next_water > water:
            reward -= 1  # Cost of buying water
    elif action.startswith("plant_"):
        crop = action.split("_")[1]
        if all([crops_growth[i] == 0 for i in range(len(crops_growth))]):
            if CROPS[crop]["seed_cost"] <= seeds and CROPS[crop]["fertilizer_need"] <= fertilizer and CROPS[crop]["water_need"] <= water:
                reward -= CROPS[crop]["seed_cost"]  # Cost of planting
            else:
                reward -= 5  # Penalty for insufficient resources
    elif action == "harvest":
        for i, crop in enumerate(CROPS.keys()):
            if next_crops_growth[i] == CROPS[crop]["growth_cycle"]:
                reward += CROPS[crop]["reward"] * market_price  # Reward for harvesting
    elif action == "do_nothing":
        if weather == "stormy":
            for i in range(len(crops_growth)):
                if crops_growth[i] > 0:
                    reward -= 3  # Penalty for taking no action in stormy weather

    return reward

# ε - Greedy exploration strategy
def epsilon_greedy(state, epsilon):
    state_index = hash(state) % state_space_size
    if random.uniform(0, 1) < epsilon:
        return random.choice(ACTIONS)
    else:
        return ACTIONS[np.argmax(Q_TABLE[state_index])]

# Q-learning update
def q_learning_update(state, action, reward, next_state):
    state_index = hash(state) % state_space_size
    next_state_index = hash(next_state) % state_space_size
    action_index = ACTIONS.index(action)
    Q_TABLE[state_index, action_index] = (1 - LEARNING_RATE) * Q_TABLE[state_index, action_index] +                                          LEARNING_RATE * (reward + DISCOUNT_FACTOR * np.max(Q_TABLE[next_state_index]))
    # The Q-table update formula is Q(s, a) = Q(s, a) + α * (r + γ * max Q(s', a') - Q(s, a)), 
    # where α is the learning rate, γ is the discount factor, r is the reward, and s' is the next state."

# Train the agent
epsilon = INITIAL_EPSILON
for episode in range(1000):
    seeds = INITIAL_SEEDS
    fertilizer = INITIAL_FERTILIZER
    water = INITIAL_WATER
    crops_growth = [0] * len(CROPS)
    weather = random.choices(WEATHERS, weights=WEATHER_PROB)[0]
    market_price = random.randint(1, 10)
    total_reward = 0

    for day in range(SIMULATION_DAYS):
        state = get_state(seeds, fertilizer, water, crops_growth, weather, market_price)
        action = epsilon_greedy(state, epsilon)

        # Execute the action
        if action == "buy_seeds":
            seeds += 1
            fertilizer -= 3
        elif action == "buy_fertilizer":
            fertilizer += 1
            water -= 2
        elif action == "buy_water":
            water += 1
            seeds -= 1
        elif action == "plant_tomato":
            if seeds >= CROPS["tomato"]["seed_cost"] and fertilizer >= CROPS["tomato"]["fertilizer_need"] and water >= CROPS["tomato"]["water_need"]:
                seeds -= CROPS["tomato"]["seed_cost"]
                fertilizer -= CROPS["tomato"]["fertilizer_need"]
                water -= CROPS["tomato"]["water_need"]
                crops_growth[0] = 1
        elif action == "plant_carrot":
            if seeds >= CROPS["carrot"]["seed_cost"] and fertilizer >= CROPS["carrot"]["fertilizer_need"] and water >= CROPS["carrot"]["water_need"]:
                seeds -= CROPS["carrot"]["seed_cost"]
                fertilizer -= CROPS["carrot"]["fertilizer_need"]
                water -= CROPS["carrot"]["water_need"]
                crops_growth[1] = 1
        elif action == "harvest":
            for i, crop in enumerate(CROPS.keys()):
                if crops_growth[i] == CROPS[crop]["growth_cycle"]:
                    crops_growth[i] = 0
        elif action == "do_nothing":
            pass

        # Update crop growth
        for i in range(len(crops_growth)):
            if crops_growth[i] > 0:
                if weather != "stormy":
                    crops_growth[i] += 1
                else:
                    if random.random() < 0.5:
                        crops_growth[i] = 0  # Storm may destroy crops

        # Update weather and market price
        weather = random.choices(WEATHERS, weights=WEATHER_PROB)[0]
        market_price = random.randint(1, 10)

        next_state = get_state(seeds, fertilizer, water, crops_growth, weather, market_price)
        reward = get_reward(state, action, next_state)
        total_reward += reward

        q_learning_update(state, action, reward, next_state)

    epsilon *= EPSILON_DECAY

# Game UI
class FarmGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Resource Management Game")

        self.seeds = INITIAL_SEEDS
        self.fertilizer = INITIAL_FERTILIZER
        self.water = INITIAL_WATER
        self.crops_growth = [0] * len(CROPS)
        self.weather = random.choices(WEATHERS, weights=WEATHER_PROB)[0]
        self.market_price = random.randint(1, 10)
        self.day = 1
        self.total_reward = 0

        # Display information
        self.info_label = tk.Label(root, text=self.get_info_text())
        self.info_label.pack(pady=10)

        # Action buttons
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(pady=10)
        for action in ACTIONS:
            tk.Button(self.action_frame, text=action, command=lambda a=action: self.take_action(a)).pack(side=tk.LEFT, padx=5)

        # Reward display
        self.reward_label = tk.Label(root, text=f"Total Reward: {self.total_reward}")
        self.reward_label.pack(pady=10)

    def get_info_text(self):
        return f"Day {self.day}/{SIMULATION_DAYS}\n"                f"Seeds: {self.seeds}, Fertilizer: {self.fertilizer}, Water: {self.water}\n"                f"Crops Growth: {self.crops_growth}\n"                f"Weather: {self.weather}, Market Price: {self.market_price}"

    def take_action(self, action):
        state = get_state(self.seeds, self.fertilizer, self.water, self.crops_growth, self.weather, self.market_price)

        # Execute the action
        if action == "buy_seeds":
            self.seeds += 1
            self.fertilizer -= 3
        elif action == "buy_fertilizer":
            self.fertilizer += 1
            self.water -= 2
        elif action == "buy_water":
            self.water += 1
            self.seeds -= 1
        elif action == "plant_tomato":
            if self.seeds >= CROPS["tomato"]["seed_cost"] and self.fertilizer >= CROPS["tomato"]["fertilizer_need"] and self.water >= CROPS["tomato"]["water_need"]:
                self.seeds -= CROPS["tomato"]["seed_cost"]
                self.fertilizer -= CROPS["tomato"]["fertilizer_need"]
                self.water -= CROPS["tomato"]["water_need"]
                self.crops_growth[0] = 1
        elif action == "plant_carrot":
            if self.seeds >= CROPS["carrot"]["seed_cost"] and self.fertilizer >= CROPS["carrot"]["fertilizer_need"] and self.water >= CROPS["carrot"]["water_need"]:
                self.seeds -= CROPS["carrot"]["seed_cost"]
                self.fertilizer -= CROPS["carrot"]["fertilizer_need"]
                self.water -= CROPS["carrot"]["water_need"]
                self.crops_growth[1] = 1
        elif action == "harvest":
            for i, crop in enumerate(CROPS.keys()):
                if self.crops_growth[i] == CROPS[crop]["growth_cycle"]:
                    self.crops_growth[i] = 0
        elif action == "do_nothing":
            pass

        # Update crop growth
        for i in range(len(self.crops_growth)):
            if self.crops_growth[i] > 0:
                if self.weather != "stormy":
                    self.crops_growth[i] += 1
                else:
                    if random.random() < 0.5:
                        self.crops_growth[i] = 0  # Storm may destroy crops

        # Update weather and market price
        self.weather = random.choices(WEATHERS, weights=WEATHER_PROB)[0]
        self.market_price = random.randint(1, 10)

        next_state = get_state(self.seeds, self.fertilizer, self.water, self.crops_growth, self.weather, self.market_price)
        reward = get_reward(state, action, next_state)
        self.total_reward += reward

        q_learning_update(state, action, reward, next_state)

        # Update the UI
        self.info_label.config(text=self.get_info_text())
        self.reward_label.config(text=f"Total Reward: {self.total_reward}")

        self.day += 1
        if self.day > SIMULATION_DAYS:
            messagebox.showinfo("Game Over", f"Game Over! Total Reward: {self.total_reward}")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game_ui = FarmGameUI(root)
    root.mainloop()

