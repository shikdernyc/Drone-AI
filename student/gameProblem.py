'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''
from simpleai.search import SearchProblem
import simpleai.search
import math


class GameProblem(SearchProblem):
    # Object attributes, can be accessed in the methods below
    MAP = None
    POSITIONS = None
    INITIAL_STATE = None
    GOAL = None
    CONFIG = None
    AGENT_START = None

    # --------------- Common functions to a SearchProblem -----------------
    def actions(self, state):
        """
        Returns all possible actions for each state
        :param state: Current state
        :return: Array of possible action directions
        """
        if state[0] is self.INITIAL_STATE[0] and state[1] is self.INITIAL_STATE[1]:
            print(state)
        actions = []
        nesw = self.__get_nesw_tiles(state)
        for key, value in nesw.items():
            if value is None or value[0] is "sea":
                continue
            else:
                actions.append(key)
        return actions

    def result(self, state, action):
        """
        Returns the next state based on action taken
        :param state: Current State
        :param action: Action taken (N, S, E, W)
        :return: New State
        """
        # Indicates how the x and y value changes for each type of action
        action_for_state = {
            "North": [0, -1],
            "East": [1, 0],
            "South": [0, 1],
            "West": [-1, 0]
        }
        pics = state[2]
        new_x = state[0] + action_for_state[action][0]
        new_y = state[1] + action_for_state[action][1]
        next_tile_type = self.__return_tile(new_x, new_y)[0]
        if next_tile_type is 'goal' and (new_x, new_y) not in pics:
            pics = state[2] + ((new_x, new_y),)
        if next_tile_type == "drone-base" or next_tile_type == 'drone-base-traversed':
            battery = self.INITIAL_STATE[3]
        else:
            battery = state[3] - self.__return_tile(new_x, new_y)[2]['battery']
        return new_x, new_y, pics, battery

    def is_goal(self, state):
        """
        Indicates if goal has been met
        :param state: Current State
        :return: True if state is goal
        """
        return True if state == self.GOAL else False

    def cost(self, state, action, state2):
        """
        Calculates the cost between states
        :param state: Current State
        :param action: Action taken to change state
        :param state2: Next State
        :return:
        """
        return self.__get_state_tile(state2)[2]['cost'] # + self.__get_state_tile(state)[2]['cost']

    def heuristic(self, state):
        """
        Euclidean distance Heuristic between state and goal
        :param state: Current State
        :return: Cost produced by applying heuristic
        """
        delta_x = abs(self.GOAL[0] - state[0])
        delta_y = abs(self.GOAL[1] - state[0])
        distance = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
        pic_cost = len(self.GOAL[2]) - len(state[2])
        battery = math.pow(self.INITIAL_STATE[3] - state[3], 2)
        # battery = 0 if distance <= state[3] else float('inf')
        battery = float('inf') if state[3] <= 0 else battery
        # battery = state[3] / self.INITIAL_STATE[3]
        # battery = battery / self.INITIAL_STATE[3]
        # battery = 1 / (battery+0.01)
        return distance + pic_cost + battery

    def setup(self):
        # print '\nMAP: ', self.MAP, '\n'
        # print 'POSITIONS: ', self.POSITIONS, '\n'
        # print 'CONFIG: ', self.CONFIG, '\n'
        # initial_state = (self.AGENT_START[0], self.AGENT_START[1],len(self.POSITIONS['goal']),
        # self.MAP[self.AGENT_START[0]][self.AGENT_START[1]][0])
        # final_state= (self.AGENT_START[0], self.AGENT_START[1],0, self.MAP[self.AGENT_START[0]]
        # [self.AGENT_START[1]][0])
        battery_max = 14
        initial_state = (2, 1, ())
        initial_state = (2, 1, (),  battery_max)
        final_goals = tuple(self.POSITIONS['goal'])
        # final_state = (2, 1, final_goals)
        final_state = (2, 1, final_goals, battery_max)
        # algorithm = simpleai.search.breadth_first
        # algorithm = simpleai.search.depth_first
        # algorithm = simpleai.search.greedy
        algorithm = simpleai.search.astar
        return initial_state, final_state, algorithm

    def __get_nesw_tiles(self, state):
        """
        Retrieves North, South, East West tiles in respect to a state
        :param state: Given State
        :return: Dictionary containing map tiles of NSEW. Value of None indicates tile doesn't exists
        """
        x = state[0]
        y = state[1]
        north = self.__return_tile(x, y-1)
        east = self.__return_tile(x+1, y)
        south = self.__return_tile(x, y+1)
        west = self.__return_tile(x-1, y)
        return {"North": north, "East": east, "South": south, "West": west}

    def __return_tile(self, x, y):
        """
        Returns a map tile depending on x and y value in the map
        :param x: Map X coordinate
        :param y: Map Y coordinate
        :return: Map Tile of (x, y). Returns None if it doesn't exists
        """
        if x < 0 or y < 0:
            return None
        try:
            tile = self.MAP[x][y]
        except IndexError:
            tile = None
        return tile

    def __get_state_tile(self, state):
        """
        Returns current state's corresponding Map tile
        :param state: Current State
        :return: Current State Map Tile
        """
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