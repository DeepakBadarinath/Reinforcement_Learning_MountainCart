# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:35:14 2020

@author: deepa
"""

import numpy as np
import matplotlib.pyplot as plt
import gym
env = gym.make("MountainCar-v0")

LEARNING_RATE=0.1
DISCOUNT=0.95
EPISODES=25000

SHOW_EVERY=2000

epsilon=0.9
START_EPSILON_DECAYING=1
END_EPSILON_DECAYING=EPISODES//2
EPSILON_DECAYS_EVERY=10
epsilon_decay_value=epsilon/(END_EPSILON_DECAYING-START_EPSILON_DECAYING)



DISCRETE_OS_SIZE=[40]*len(env.observation_space.high)
discrete_os_win_size=(env.observation_space.high-env.observation_space.low)/DISCRETE_OS_SIZE
q_table=np.random.uniform(low=-2,high=0,size=((DISCRETE_OS_SIZE)+[env.action_space.n]))

ep_rewards=[]
aggr_ep_rewards={'ep':[], 'avg':[], 'min':[], 'max':[]}

def get_discrete_state(state):
    discrete_state= (state-env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(np.int))

discrete_state=get_discrete_state(env.reset())


for episode in range(EPISODES):
    episode_reward=0
    if episode%SHOW_EVERY==0:
        render=True
    else:
        render=False
        
    done=False
    while not done:
        if np.random.random()>epsilon:
            action=np.argmax(q_table[discrete_state])
        else:
            action=np.random.randint(env.action_space.n)
        new_state,reward,done,_=env.step(action)
        episode_reward+=reward
        #print(reward)
    
        new_discrete_state=get_discrete_state(new_state)
        if not done:
            max_future_q=np.max(q_table[new_discrete_state])
            current_q=q_table[discrete_state + (action, )]
        
            new_q= (1-LEARNING_RATE)*current_q + LEARNING_RATE * (reward+DISCOUNT*(max_future_q))
            q_table[discrete_state+(action, )]=new_q
        else:
            q_table[discrete_state+(action, )]=0
            #print(f"We made it on episode {episode}")
        if render==True:
            print(episode)
            env.render()
        
        if END_EPSILON_DECAYING>=episode>=START_EPSILON_DECAYING:
            epsilon-=epsilon_decay_value
    ep_rewards.append(episode_reward)
    if episode%SHOW_EVERY==0:
        average_reward=sum(ep_rewards[-SHOW_EVERY:])/len(ep_rewards[-SHOW_EVERY:])
        aggr_ep_rewards['ep'].append(episode)
        aggr_ep_rewards['avg'].append(average_reward)
        aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
        aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))
        
        print(f"Episode:{episode} avg:{average_reward} min {min(ep_rewards[-SHOW_EVERY:])} max {max(ep_rewards[-SHOW_EVERY:])}")
env.close()
    
    
plt.plot(aggr_ep_rewards['ep'],aggr_ep_rewards['avg'],label='avg')
plt.plot(aggr_ep_rewards['ep'],aggr_ep_rewards['max'],label='max')
plt.plot(aggr_ep_rewards['ep'],aggr_ep_rewards['min'],label='min')
plt.legend(loc=4)
plt.show()

done=False
while not done:
    action=np.argmax(q_table[discrete_state])
    new_state,reward,done,_=env.step(action)
    #print(reward)
    
    new_discrete_state=get_discrete_state(new_state)
    if not done:
        max_future_q=np.max(q_table[new_discrete_state])
        current_q=q_table[discrete_state + (action, )]
        
        new_q= (1-LEARNING_RATE)*current_q + LEARNING_RATE * (reward+DISCOUNT*(max_future_q))
        q_table[discrete_state+(action, )]=new_q
    else:
        q_table[discrete_state+(action, )]=0
        print("you win")
        env.render()
    
env.close()






