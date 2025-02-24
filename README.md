# Farm Resource Management Game

## Introduction
This project implements a farm resource management game using the Q-learning algorithm. The game simulates a farm environment where players must make optimal decisions to maximize crop yields and profits within a 7-day cycle. The game incorporates elements of resource management, crop growth cycles, random weather conditions, and market price fluctuations.

## Features
- **Game Design**: Clear objectives, rules, and well-defined state space, action space, and reward function.
- **Q-learning Implementation**: Utilizes the Q-learning algorithm to train an agent that learns optimal strategies through multiple episodes.
- **User Interface**: A basic interactive UI built with Tkinter for player interaction.
- **Random Events**: Weather conditions and market prices change randomly, adding complexity to decision-making.

## Getting Started

### Prerequisites
- Python 3.x
- Numpy library (`pip install numpy`)
- Tkinter library (usually included with Python)
- Pillow library (`pip install pillow`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/farm-resource-management-game.git
   ```
2. Navigate to the project directory:
   ```bash
   cd farm-resource-management-game
   ```
3. Install the required libraries (if not already installed):
   ```bash
   pip install numpy pillow
   ```

### Running the Game
1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the game script:
   ```bash
   python farm_game.py
   ```
4. The game window will open, allowing you to interact with the game using the provided buttons.

## Game Mechanics

### Game Objectives
- Maximize crop yields and profits within a 7-day simulation cycle.
- Make optimal decisions in resource allocation, planting, and harvesting.

### Game Rules
- **Daily Operations**: Players can buy resources, plant crops, harvest, or take no action each day.
- **Crop Characteristics**: Two types of crops (tomatoes and carrots) with different growth cycles, resource requirements, and rewards.
- **Resource Management**: Initial supply of seeds, fertilizer, and water. Resources can be purchased at a cost.
- **Random Events**: Weather conditions (sunny, rainy, stormy) and market prices change randomly each day.

### State Space
- Comprises resource quantities, crop growth stages, weather condition, and market price.

### Action Space
- Actions include buying seeds, fertilizer, water, planting tomatoes or carrots, harvesting, and doing nothing.

### Reward Function
- Rewards and penalties are assigned based on actions taken, resource management, and environmental conditions.

## Q-learning Algorithm
- **Learning Rate**: Controls the step-size of Q-value updates.
- **Discount Factor**: Balances the importance of current and future rewards.
- **Ɛ - Greedy Exploration Strategy**: Balances exploration and exploitation during training.

## User Interface
- **Information Display Area**: Shows current game state information.
- **Action Button Area**: Contains buttons for performing actions.
- **Reward Display Area**: Displays the total reward obtained in real-time.

## Evaluation Results
- The agent learns effective strategies over multiple episodes, resulting in increased total rewards.
- Parameters such as learning rate, discount factor, and exploration rate significantly impact the learning process.

## Future Work
- **Game Content**: Add more crop types, resources, and complex random events.
- **Algorithm Optimization**: Improve state-space representation for better efficiency.
- **User Experience**: Enhance UI aesthetics and interaction fluency, add operation prompts, and incorporate visual elements.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

Enjoy playing the Farm Resource Management Game!
