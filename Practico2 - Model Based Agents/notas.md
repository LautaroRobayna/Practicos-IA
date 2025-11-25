# Project 2 notes

## What is a Model-Based Agent?

### Definition

A **Model-Based Agent** maintains an internal state that represents the current condition of the world. It uses:
- A **model** of how the world works (transition model) to predict future states
- A **sensor** to update its internal state based on observations
- **Decision rules** to choose actions based on the internal state

Unlike simple reflex agents that only react to current observations, model-based agents can handle partial observability and make better decisions by tracking world state over time.



![alt text](https://www.doc.ic.ac.uk/project/examples/2005/163/g0516334/images/snapshot12.png)

As we can see in the image, we have a series of steps to implement a Model-Based Utility Agent.

### Steps to Implement a Utility-Based Agent for this Project

1. **Define Discrete States**
   - Create state space: `FRIO_EXTREMO`, `FRIO`, `OBJETIVO`, `CALOR`, `CALOR_EXTREMO`
   - Define temperature ranges for each state
   - Use `Enum` for type safety

2. **Implement Sensor (Perception Function)**
   - Maps continuous temperature observation → discrete state
   - Checks which temperature range contains the observation

3. **Create Transition Model**
   - Predicts next state given current temperature and action
   - Estimates: `future_temp ≈ current_temp + action`
   - Uses sensor to convert predicted temperature → predicted state

4. **Define Utility Function**
   - Assigns numeric value to each state (higher = better)
   - For this problem: penalize distance from goal (0°C)
   - Example: `utility = -abs(temperature)` maximizes at 0°

5. **Implement Utility-Based Decision Making**
   - For each possible action (-3 to +3):
     - Use transition model to predict resulting state
     - Calculate utility of that state
   - Choose action that maximizes expected utility

6. **Test and Compare**
   - Run agent in environment
   - Plot temperature over time
   - Compare metrics (mean temperature, MAE) with Reflex Agent

