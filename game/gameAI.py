#! /usr/bin/env python
## Javier Huertas (2017-18)
## Alejandro Cervantes (2017-18)
## Based on code from:
## Daniel Borrajo (2016-17)
## To be used with python2.7
## Open source. Distributed as-is

import random
import time
import re

import os
import sys
import pygame


# IA code that performs simple searches for a solution
# We have to provide the state representation in this domain
# We have to provide the list of feasible actions in this domain
# We have to provide the search algorithm that stores the current solution
# We have to extract the action that corresponds to the next step
# We have to check that the provided state matches the expected state
from gameSearch import searchSolution,searchInfo

# my code
import behavior
import maps

#import yaml
#with open("config.yml", 'r') as ymlfile:
#    configuration = yaml.load(ymlfile)

sys.path.append(os.path.abspath("../student"))
import config
configuration = config.configuration


text_size = configuration['text_size']
tile_size = configuration['tile_size']

# aux vars
tracep = False
cycle = 0
done = False
winner = False

# Behaviour related vars
# it can be static, fsm, random or greedy
behavior_npc = 'random'
fsm_state = 'init'

# IA 2017-18
ai201718=True # Activates the IA solution
aiPlan=None   # Stores the plan
basicAgent="drone"
aiMapText="Now running" 

def read_events(configuration, state):
    done=False
    if tracep:
        print("Reading events from keyboard")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state['inPause'] = not state['inPause']
                state['step'] = False
                continue
            if event.key == pygame.K_s:
#                state['step'] = not state['step']
                state['step'] = True
                state['inPause'] = False
                continue
    return done, state

def init_mygame():
    global configuration
    random.seed(configuration['seed'])
    
    image_files = dict()
    for tilekey, tiledict in configuration['maptiles'].iteritems():
        image_files[tilekey]= tiledict['img']
    for tilekey, tiledict in configuration['agentTiles'].iteritems():
        image_files[tilekey]= tiledict
    
    aiBaseName = configuration['agentBaseTile']      

    # This must be consistent with the agent base locations
    state = {'prev_pos': configuration['agentInit']}

    state['inPause']=False
    state['step']=False
    
    plan = []

    debugMap=configuration['debugMap']
    
    # FSM
    fsm_state = 'init'
    steps_in_state = 0
    direccion_guardia = 'north'
   
    # map
    if configuration['type'] == 'random':
        map = maps.create_map(configuration, state, configuration['debug'])
    else:
        map, configuration = maps.read_map(configuration)
        
     # display
    screen_size = [configuration['map_size'][0] * tile_size, configuration['map_size'][1] * tile_size + text_size]
    screen = pygame.display.set_mode(screen_size)
    images = {f: pygame.transform.scale(pygame.image.load(image_files[f]).convert(),(tile_size - 5, tile_size - 5)) for f in image_files}

    state['prev_pos'] = configuration['agentInit']
    if configuration['save']:
        with open(configuration['file'], 'w') as f:
            f.write(maps.printable_map(map, configuration, False))

    maps.print_map(map, configuration, images, screen, state, tile_size, fsm_state, configuration['debug'],"Running search")
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # planner
    header = ""

    
    # --- In the IA201718 configuration we have planned in advance for the objective
    if ai201718:
        global aiPlan
        global aiMapText
        aiPlan,problem,result,use_viewer = searchSolution(map,configuration,state,aiBaseName,debugMap)
        
        if aiPlan:
            aiMapText = searchInfo(problem,result,use_viewer)
            print ("----------------------- STARTING SEARCH ---------------------")
            print("Retrieved a plan: {0}".format(aiPlan))
            state['searchOk']=True
            done=False
        else:
            aiMapText = "Search retrieved no plan for this problem"
            print("Search retrieved no plan for this problem")
            state['searchOk']=False


    return state, plan, screen_size, screen, images, map, configuration, clock, header, fsm_state, steps_in_state, direccion_guardia

def check_finish (state, configuration):
    done = False
    winner = False

    if ai201718 and len(aiPlan)==0:
        done=True
        winner = 'You'
    return done, winner

def move_npc(mapa, state, configuration, new_pos, fsm_state, steps_in_state, direccion_guardia, tracep):
    if tracep:
        print("Moving NPCs")
    if behavior_npc == 'random':
        mapa, state = behavior.random_behavior(mapa, state, configuration)
    elif behavior_npc == 'greedy':
        mapa, state = behavior.greedy_behavior(mapa, state, configuration, new_pos)
    elif behavior_npc == 'fsm':
        mapa, state, fsm_state, steps_in_state, direccion_guardia = behavior.fsm_behavior(mapa, state, configuration, new_pos, fsm_state, steps_in_state, direccion_guardia, tracep)
    return mapa, state, fsm_state, steps_in_state, direccion_guardia
    

# This calculates the effect on the agent, basically calculating new_pos
# Actual movement takes place in do_move_agent
def plan_move_agent(actionName, mapa, state, configuration, new_pos, tracep):
    def moveup (state, configuration,new_pos):
        if state['prev_pos'][1] > 0:
            new_pos[1] = new_pos[1] - 1
        return new_pos, state
            
    def moveright (state, configuration,new_pos):
        if state['prev_pos'][0] < configuration['map_size'][0] - 1:
            new_pos[0] = new_pos[0] + 1
        return new_pos, state
        
    def movedown (state, configuration,new_pos):
        if state['prev_pos'][1] < configuration['map_size'][1] - 1:
            new_pos[1] = new_pos[1] + 1
        return new_pos, state
    
    def moveleft (state, configuration,new_pos):
        if state['prev_pos'][0] > 0:
            new_pos[0] = new_pos[0] - 1
        return new_pos, state
    
    def stay (state, configuration,new_pos):
        new_pos= state['prev_pos']
        return new_pos, state
    
    actionDefs = { 'North': moveup ,
                'East':  moveright,
                'South': movedown,
                'West':  moveleft,
                'default':  stay
              }
    
    if actionName in actionDefs.keys():
        f = actionDefs[actionName]
    else:
        f = actionDefs['default']
    
#    print ('Action name is {0}'.format(actionName))
    return f(state, configuration, new_pos)

# This executes a move for the agent, updating the state and managing colisions
# Calculations use the attributes of the map position
# Results are effects in the state and map, but may also reet new_pos (colision), etc.
def do_move_agent(state, mapa, new_pos):
    
    def step (state, mapa ,new_pos):
        old_pos = state['prev_pos']
        oldMapTileData=mapa[old_pos[0]][old_pos[1]]
        if oldMapTileData[0].find('traversed')<0:
            oldMapTileData[0]+='-traversed'
        agentState = oldMapTileData[2]['agent']
        oldMapTileData[2]['agent'] = None
        mapa[new_pos[0]][new_pos[1]][2]['agent'] = agentState
        return state, mapa, new_pos

    return step(state,mapa,new_pos)        
    

def init_game():
    global aiPlan # This variable stores the calculated solution
    global aiMapText # This variable stores a text obtained during the search

    pygame.init()
    cycle = 0
    winner = False

    state, plan, screen_size, screen, images, mapa, configuration, clock, header, fsm_state, steps_in_state, direccion_guardia = init_mygame()
    # If initialization returned state = None, then we are done
    done = not state['searchOk']

    if configuration['debugMap']:
        print ("-------------- INITIAL MAP -------------")
        print (mapa)
    
    # -------- Main Program Loop -----------
    state['inPause']=True
    displayText= aiMapText
    
    while not done:
        # --- Main event loop
        cycle = cycle + 1
        done, state = read_events(configuration, state)
        if done:
            continue
        
        new_pos = list(state['prev_pos'])

        # --- Game logic should go here

        # --- In the IA201718 configuration we have planned in advance for the objective
        # --- The plan is stored in a global (aiPlan)
        
        if ai201718 and len(aiPlan)>0 and not state['inPause']:
            nextElement = aiPlan.pop(0) 
            nextAction = nextElement[0]
            new_pos, state = plan_move_agent(nextAction,mapa, state, configuration, new_pos, configuration['debug'])
            nextActionData = nextElement[1]; # This field is reserved for plan step attributes (NOT USED YET)
            displayText= aiMapText
            if 'showText' in nextActionData.keys():
                displayText=nextActionData['showText'] + '\n' + aiMapText
            
        # These are the effects of the movement
        state,mapa,new_pos = do_move_agent(state,mapa,new_pos)  
        state['prev_pos'] = new_pos

        # --- Checking finish simulation
        done, winner = check_finish(state, configuration)

        # --- NPCs changes
        mapa, state, fsm_state, steps_in_state, direccion_guardia = move_npc(mapa, state, configuration, new_pos, fsm_state, steps_in_state, direccion_guardia, configuration['debug'])
        
        # --- Drawing code
        maps.print_map(mapa, configuration, images, screen, state, tile_size, fsm_state, configuration['debug'],show_text=displayText)
        
        # --- Limit to 60 frames per second
        clock.tick(60)
        time.sleep(configuration['delay'])
        if state['step']:
            state['inPause']=True
    
    if configuration['debugMap']:
        print ("-------------- FINAL MAP -------------")
        print (mapa)

    state['inPause']=True
    maps.print_map(mapa, configuration, images, screen, state, tile_size, fsm_state, configuration['debug'],show_text=aiMapText)
    while state['inPause']:
        done, state = read_events(configuration, state)

    pygame.quit()

# MAIN PROGRAM
init_game()
