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
    VISITED = []
    VISITED_STATES = []

    # --------------- Common functions to a SearchProblem -----------------
    def actions(self, state):
        if state is not self.INITIAL_STATE:
            current_tile = self.__get_state_tile(state)
            self.VISITED.append(current_tile)
            self.VISITED_STATES.append(state)
        # Returns a LIST of the actions that may be executed in this state
        actions = []
        nesw = self.__get_nesw_tiles(state)
        for key, value in nesw.items():
            if value is None or value[0] is "sea" or value in self.VISITED:
                # TODO: Add a check for visited
                continue
            else:
                actions.append(key)
        return actions

    def result(self, state, action):
        # Returns the state reached from this state when the given action is executed
        # Indicates how the x and y value changes for each type of action
        action_for_state = {
            # NESW: [x, y]
            "North": [0, -1],
            "East": [1, 0],
            "South": [0, 1],
            "West": [-1, 0]
        }
        new_x = state[0] + action_for_state[action][0]
        new_y = state[1] + action_for_state[action][1]
        next_tile_type = self.__return_tile(new_x, new_y)[0]
        return (new_x, new_y, state[2] - 1) if next_tile_type is 'goal' else (new_x, new_y, state[2])

    def is_goal(self, state):
        return True if state == self.GOAL else False

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        return self.__get_state_tile(state)[2]['cost'] + self.__get_state_tile(state2)[2]['cost']

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        # missing = len(self.GOAL) - len(state)
        return 0

    def setup(self):

        print '\nMAP: ', self.MAP, '\n'
        print 'POSITIONS: ', self.POSITIONS, '\n'
        print 'CONFIG: ', self.CONFIG, '\n'

        # initial_state = (self.AGENT_START[0], self.AGENT_START[1],len(self.POSITIONS['goal']), self.MAP[self.AGENT_START[0]][self.AGENT_START[1]][0])
        # final_state= (self.AGENT_START[0], self.AGENT_START[1],0, self.MAP[self.AGENT_START[0]][self.AGENT_START[1]][0])
        initial_state = (2, 1, 4)
        final_state = (2, 1, 0)
        algorithm = simpleai.search.astar

        return initial_state, final_state, algorithm

    def __get_nesw_tiles(self, state):
        # Get the keys/values of tiles around the drone's current position
        x = state[0]
        y = state[1]
        north = self.__return_tile(x, y-1)
        east = self.__return_tile(x+1, y)
        south = self.__return_tile(x, y+1)
        west = self.__return_tile(x-1, y)
        return {"North": north, "East": east, "South": south, "West": west}

    def __return_tile(self, x, y):
        # Returns the tile position or null if at the edge of the map
        try:
            tile = self.MAP[x][y]
        except IndexError:
            tile = None
        return tile

    def __get_state_tile(self, state):
        return self.MAP[state[0]][state[1]]
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
                    print (
                        '-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}", found several at {1}'.format(
                            aiAgentName, mapaPosiciones[aiAgentName]))
                    return False
            else:
                print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}"'.format(
                    aiBaseName))
                return False

        return True
