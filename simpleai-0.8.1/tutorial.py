'''
    Blind search
     
    The following methods must be implemented for any problem
      actions: LIST of possible actions in a given state: (action1,action2,...)
      result: LIST (state,action)
      is_goal: TRUE is a given state is the goal state
      cost: cost of reaching a state s' by appling action a in a state s
      heuristic: heuristic value for a given state
 
    Problem 1:
      Initial state: A
      Actions: move to a connected state
      Goal: H
      Heuristic: no
      Algorithm: breadth-first
 
    Problem 2: 
      Initial state: A
      Actions: move to a connected state
      Goal: H
      Heuristic: no
      Algorithm: depth-first
 
'''
import os
import sys
 
from simpleai.search import SearchProblem
from simpleai.search.viewers import BaseViewer,ConsoleViewer,WebViewer
from simpleai.search import breadth_first,depth_first,astar,greedy
 
# CLASS MapProblem derivatives from SearchProblem
class MapProblem(SearchProblem):
    
    mapProblem=None
    final_state=None
 
    # --------------- Common methods to SearchProblem -----------------
    #
    def actions(self, state):
        
        '''Returns a LIST of the actions that may be executed in this state
        '''
        return 
 
    def result(self, state, action):
      
	'''Returns the state reached from this state when the given action is executed
        '''
        return 
 
    def is_goal(self, state):
        
       '''Returns true if state is the final state
       '''
       return 
    
    def cost(self, state, action, state2):
        
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        return 1
 
    def heuristic(self, state):
        
        '''Returns the heuristic for `state`
        '''
        return 0
 
 
# INIT mapExercise
 
def mapExercise(problem,algorithm,use_viewer=None):
     
    result = algorithm(problem,graph_search=True,viewer=use_viewer)
     
    print("Final state:" + result.state)
    print("Path: {0}".format(result.path()))
    print("Cost: {0}".format(getTotalCost(problem,result)))
     
    if use_viewer:
        stats = [{'name': stat.replace('_', ' '), 'value': value}
                         for stat, value in list(use_viewer.stats.items())]
         
        for s in stats:
            print ('{0}: {1}'.format(s['name'],s['value']))
             
 
    return result
 
def getTotalCost (problem,result):
    originState = problem.initial_state
    totalCost = 0
    for action,endingState in result.path():
        if action is not None:
            totalCost += problem.cost(originState,action,endingState)
            originState = endingState
    return totalCost
 
# END mapExercise
 

# -------------------------  SOLVING THE PROBLEM ----------------------
 
initial_state=
final_state=
 
map = 
 
problem = MapProblem(initial_state)
problem.mapProblem = map
problem.final_state = final_state
 
print '\nSolution using BFS'
mapExercise(problem,algorithm=breadth_first,use_viewer=None)
print '\nSolution using DFS'
mapExercise(problem,algorithm=depth_first,use_viewer=None)
