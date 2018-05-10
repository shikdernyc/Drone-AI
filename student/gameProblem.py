'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''
from simpleai.search import SearchProblem
import simpleai.search


class GameProblem(SearchProblem):
    # Object attributes, can be accessed in the methods below
    MAP = None
    POSITIONS = None
    INITIAL_STATE = None
    GOAL = None
    CONFIG = None
    AGENT_START = None
    # will contain all the maps tile we have visited
    VISITED = set()

    # --------------- Common functions to a SearchProblem -----------------
    def actions(self, state):
        '''
        Returns a LIST of the actions that may be executed in this state
        '''
        actions = []
        return actions

    def get_nesw_tiles(self, state):
        '''
        Get the available tiles/paths the drone is able to move to
        '''
        x = state[0]
        y = state[1]
        north = self.return_tile(x, y-1)
        east = self.return_tile(x+1, y)
        south = self.return_tile(x, y+1)
        west = self.return_tile(x-1, y)

    def return_tile(self, x, y):
        '''
        Returns the tile position or null if at the edge of the map
        '''
        try:
            north = self.MAP[x][y]
        except IndexError:
            north = 'null'
        try:
            east = self.MAP[x][y]
        except IndexError:
            east = 'null'
        try:
            south = self.MAP[x][y]
        except IndexError:
            south = 'null'
        try:
            west = self.MAP[x][y]
        except IndexError:
            west = 'null'
        return {"North" : north, "East" : east, "South" : south, "West" : west}

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        state_final = 0
        return state_final

    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        return True

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

    def setup(self):
        print('\nMAP: ', self.MAP, '\n')
        print('POSITIONS: ', self.POSITIONS, '\n')
        print('CONFIG: ', self.CONFIG, '\n')
        initial_state = 0
        final_state = 0
        algorithm = simpleai.search.astar
        return initial_state, final_state, algorithm

    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

    def getAttribute(self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string

           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes = self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self, map, positions, conf, aiBaseName):
        # Loads the problem attributes: self.AGENT_START, self.POSITIONS,etc.
        if self.mapInitialization(map, positions, conf, aiBaseName):
            initial_state, final_state, algorithm = self.setup()
            self.INITIAL_STATE = initial_state
            self.GOAL = final_state
            self.ALGORITHM = algorithm
            super(GameProblem, self).__init__(self.INITIAL_STATE)
            return True
        else:
            return False
    # END initializeProblem

    def mapInitialization(self, map, positions, conf, aiBaseName):
        # Creates lists of positions from the configured map
        # The initial position for the agent is obtained from the first and only aiBaseName tile
        self.MAP = map
        self.POSITIONS = positions
        self.CONFIG = conf

        if 'agentInit' in conf.keys():
            self.AGENT_START = tuple(conf['agentInit'])
        else:
            if aiBaseName in self.POSITIONS.keys():
                if len(self.POSITIONS[aiBaseName]) == 1:
                    self.AGENT_START = self.POSITIONS[aiBaseName][0]
                else:
                    # print(
                        # '-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}", found several at {1}'.format(
                            # aiAgentName, mapaPosiciones[aiAgentName]))
                    return False
            else:
                print('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}"'.format(
                    aiBaseName))
                return False
        return True
