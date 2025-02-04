# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        """oldValues = util.Counter()
        for i in range(self.iterations):
            states = self.mdp.getStates()
            for currentState in states:
                if self.mdp.isTerminal(currentState):
                    continue
                actions = self.mdp.getPossibleActions(currentState)
                if not actions:
                    values[state] = 0
                vList = []

                for action in actions:
                    nextStatesAndProbs = self.mdp.getTransitionStatesAndProbs(currentState, action)
                    temp = 0
                    for (nextState, prob) in nextStatesAndProbs:
                        r = self.mdp.getReward(currentState, action, nextState)
                        temp += prob * (r + self.discount * self.values[nextState])
                    vList.append(temp)
                oldValues[currentState] = max(vList)
                    #print "state", currentState, "nextState", nextState ,"reward", r, "prob",prob, "value", oldValues[currentState]
            self.values = oldValues"""
        for iteration in xrange(self.iterations):
            values = self.values.copy()
            for state in self.mdp.getStates():
                actions = self.mdp.getPossibleActions(state)
                if not actions:
                    values[state] = 0
                else:
                    values[state] = max(self.computeQValueFromValues(state, action) for action in actions)
            self.values = values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        """qValue = 0
        nextStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for (nextState, prob) in nextStatesAndProbs:
            r = self.mdp.getReward(state, action, nextState)
            qValue += prob * (r + self.discount * self.values[nextState])
        return qValue"""
        return sum(prob * (self.mdp.getReward(state, action, newState) + self.discount * self.getValue(newState)) \
            for newState, prob in self.mdp.getTransitionStatesAndProbs(state, action))
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        """if self.mdp.isTerminal(state):
            return None
        actions = self.mdp.getPossibleActions(state)
        values = {}
        for action in actions:
            values[action] = 0
            for (nextState, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
                r = self.mdp.getReward(state, action, nextState)
                values[action] += prob * (r + self.discount * self.values[nextState])

        return  max(zip(values.values(),values.keys()))[1]"""
        actions = self.mdp.getPossibleActions(state)
        if not actions:
            return None
        return max(actions, key = lambda x: self.computeQValueFromValues(state, x))
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        i = 0
        for iteration in xrange(self.iterations):
            i = i % len(states)
            actions = self.mdp.getPossibleActions(states[i])
            if not actions:
                self.values[states[i]] = 0
            else:
                self.values[states[i]] = max(self.computeQValueFromValues(states[i], action) for action in actions)
            i += 1

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        predecessors = {}
        for state in states:
            predecessors[state] = set([])
        for state in states:
            actions = self.mdp.getPossibleActions(state)
            if actions:
                for action in actions:
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        predecessors[nextState].add(state)
        pqueue = util.PriorityQueue()
        for i in xrange(len(states)):
            actions = self.mdp.getPossibleActions(states[i])
            if actions:
                newValue = max(self.computeQValueFromValues(states[i], action) for action in actions)
                diff = abs(newValue - self.values[states[i]])
                pqueue.push((states[i], newValue), -diff)
        for iteration in xrange(self.iterations):
            if pqueue.isEmpty():
                break
            state, newValue = pqueue.pop()
            self.values[state] = newValue
            for predecessor in predecessors[state]:
                actions = self.mdp.getPossibleActions(predecessor)
                if actions:
                    newValue = max(self.computeQValueFromValues(predecessor, action) for action in actions)
                    diff = abs(newValue - self.values[predecessor])
                    if diff > self.theta:
                        pqueue.push((predecessor, newValue), -diff)
