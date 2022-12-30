import gym

t=0
env = gym.make("CartPole-v1")
observation = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()
    
    # Something strange here env.step returns 5 values : observation, reward, terminated, truncated, info
    # A bug maybe ? -> See documentation
    observation, reward, terminated, truncated = env.step(action)
 
    #Printing the state while run goes
    print("Current action", action, "Current reward", reward)

    if terminated or truncated:
        print("Episode finished after {} timesteps".format(t+1))
        observation = env.reset()
env.close()
