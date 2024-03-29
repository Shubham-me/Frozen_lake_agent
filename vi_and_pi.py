### MDP Value Iteration and Policy Iteration

import numpy as np
import gym
import time
from lake_envs import *

#
import random as rn
#
np.set_printoptions(precision=3)

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""

def policy_evaluation(P, nS, nA, policy, gamma, tol):
	"""Evaluate the value function from a given policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.
	tol: float
		Terminate policy evaluation when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS]
		The value function of the given policy, where value_function[s] is
		the value of state s
	"""

	##(probability, nextstate, reward, terminal)
	value_function = np.zeros(nS)
	prev_value_function = np.zeros(nS)

	diff = 1
	while(diff >= tol):
		new_value_function = np.zeros(nS)
		for i in range(nS):
			value = 0
			action = policy[i]
			for j in range(len(P[i][action])):
				value = value + P[i][action][j][0]*(P[i][action][j][2] +  gamma*(value_function[P[i][action][j][1]]))
			new_value_function[i] = value 
		diff = abs(new_value_function[0]-value_function[0])	
		for i in range(nS):
			if(abs(new_value_function[i]-value_function[i]) > diff):
				diff = abs(new_value_function[i]-value_function[i])
			prev_value_function[i] = value_function[i]
			value_function[i] = new_value_function[i]
	return value_function

def policy_improvement(P, nS, nA, value_from_policy, policy, gamma):
	"""Given the value function from policy improve the policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.

	Returns
	-------
	new_policy: np.ndarray[nS]
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""

	new_policy = np.zeros(nS, dtype='int')
	##(probability, nextstate, reward, terminal)
	for i in range(nS):
		max_value = 0
		for j in range(len(P[i][0])):
			max_value = max_value + P[i][0][j][0]*(P[i][0][j][2] + gamma*(value_from_policy[P[i][0][j][1]]))
		for j in range(1,nA):
			value = 0
			for k in range(len(P[i][j])):
				value = value + P[i][j][k][0]*(P[i][j][k][2] + gamma*(value_from_policy[P[i][j][k][1]]))
			if(value > max_value):
				max_value = value
		action = []
		for j in range(nA):
			value = 0
			for k in range(len(P[i][j])):
				value = value + P[i][j][k][0]*(P[i][j][k][2] + gamma*(value_from_policy[P[i][j][k][1]]))
			if(value == max_value):
				action.append(j)
			
		new_policy[i] = action[rn.randint(0,len(action)-1)]		
	return new_policy


def policy_iteration(P, nS, nA, gamma, tol):
	"""Runs policy iteration.

	You should call the policy_evaluation() and policy_improvement() methods to
	implement this method.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		tol parameter used in policy_evaluation()
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

	
	value_function = np.zeros(nS)
	prev_value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)


	value_function = policy_evaluation(P,nS,nA,policy,gamma,tol)
	prev_value_function = policy_evaluation(P,nS,nA,policy,gamma,tol)
	##(probability, nextstate, reward, terminal)
	diff = 1
	null = 1
	while(diff >= tol or null == 1):
		policy = policy_improvement(P,nS,nA,value_function,policy,gamma)
		new_value_function = policy_evaluation(P,nS,nA,policy,gamma,tol)
		diff = abs(new_value_function[0] - value_function[0])
		for i in range(1,nS):
			if(abs(new_value_function[i] - value_function[i]) > diff):
				diff = abs(new_value_function[i] - value_function[i])
		for i in range(nS):
			prev_value_function[i] = value_function[i]
			value_function[i] = new_value_function[i]
		null = 1	
		for i in range(nS):
			if(value_function[i] != 0):
				null = 0
	return value_function, policy

def value_iteration(P, nS, nA, gamma, tol):
	"""
	Learn value function and policy by using value iteration method for a given
	gamma and environment.

	Parameters:
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		Terminate value iteration when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

	value_function = np.zeros(nS)
	prev_value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	diff = 1
	new_value_function = np.zeros(nS)
	while(diff >= tol):
		for i in range(nS):
			max_value = 0
			for j in range(len(P[i][0])):
				max_value = max_value + P[i][0][j][0]*(P[i][0][j][2] + gamma*(value_function[P[i][0][j][1]]))
			for j in range(1,nA):
				value = 0
				for k in range(len(P[i][j])):
					value = value + P[i][j][k][0]*(P[i][j][k][2] + gamma*(value_function[P[i][j][k][1]])) 
				if(value > max_value):
					max_value = value	
			new_value_function[i] = max_value
		diff = 0	
		for i in range(nS):
			if(abs(new_value_function[i] - value_function[i]) > diff):
				diff = abs(new_value_function[i] - prev_value_function[i])
			prev_value_function[i] = value_function[i]
			value_function[i] = new_value_function[i]

	for i in range(nS):
		max_value = 0
		for j in range(len(P[i][0])):
			max_value = max_value + P[i][0][j][0]*(P[i][0][j][2] + gamma*(value_function[P[i][0][j][1]]))
		for j in range(1,nA):
			value = 0
			for k in range(len(P[i][j])):
				value = value + P[i][j][k][0]*(P[i][j][k][2] + gamma*(value_function[P[i][j][k][1]])) 
			if(value > max_value):
				max_value = value	
		action = []
		for j in range(nA):
			value = 0
			for k in range(len(P[i][j])):
				value = value + P[i][j][k][0]*(P[i][j][k][2] + gamma*(value_function[P[i][j][k][1]]))
			if(value == max_value):
				action.append(j)
		policy[i] = action[rn.randint(0,len(action)-1)]						
	return value_function, policy

def render_single(env, policy, max_steps=100):
  """
    This function does not need to be modified
    Renders policy once on environment. Watch your agent play!

    Parameters
    ----------
    env: gym.core.Environment
      Environment to play on. Must have nS, nA, and P as
      attributes.
    Policy: np.array of shape [env.nS]
      The action to take at a given state
  """

  episode_reward = 0
  ob = env.reset()
  for t in range(max_steps):
    env.render()
    time.sleep(0.25)
    a = policy[ob]
    ob, rew, done, _ = env.step(a)
    episode_reward += rew
    if done:
      break
  env.render();
  if not done:
    print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
  else:
    print("Episode reward: %f" % episode_reward)
    


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":

	# comment/uncomment these lines to switch between deterministic/stochastic environments
	env = gym.make("Deterministic-8x8-FrozenLake-v0")
	
	#env = gym.make("Stochastic-4x4-FrozenLake-v0")
	print(env.P)
	for i in range(len(env.P)):
		print("STATE =",i)
		for j in range(len(env.P[i])):
			print(" ACTION =",j)
			for k in range(len(env.P[i][j])):
				print("  ",end = "")
				print(env.P[i][j][k])
	print("\n" + "-"*25 + "\nBeginning Policy Iteration\n" + "-"*25)

	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, 0.9, 1e-8)
	render_single(env, p_pi, 100)
	
	print("\n" + "-"*25 + "\nBeginning Value Iteration\n" + "-"*25)
	
	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-8)
	render_single(env, p_vi, 100)
	