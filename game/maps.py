import pygame
import os.path
import re
import random

# Define some colors
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue      = ( 70,   70,   255)
myred    = ( 230,   30, 70)
black    = (   0,   0,   0)
background = black
disp     = (0, 0)

def create_map (configuration, state, tracep):
    if tracep:
        print("Creating map")
        
    basicTile=configuration['basicTile']
    basicMapConf= configuration['maptiles'][basicTile]
        
    terrainMap = [ [ [ basicMapConf['id'],0,
                 dict(basicMapConf['attributes'])]
               for x in range(configuration['map_size'][1])
             ] 
            for y in range(configuration['map_size'][0])]
    
    # Establish one base with the agent (others will be void)
    agentBaseTile=configuration['agentBaseTile']
    agentBaseMapData= [ configuration['maptiles'][agentBaseTile]['id'],0,dict(configuration['maptiles'][agentBaseTile]['attributes'])]
    terrainMap[state['prev_pos'][0]][state['prev_pos'][1]]=agentBaseMapData

    agentType=configuration['agentType']
    terrainMap[state['prev_pos'][0]][state['prev_pos'][1]][2]['agent']=agentType
    
    for tilekey, tiledict in configuration['maptiles'].iteritems():
        if 'num' in tiledict:
            terrainMap = fill_map(configuration, terrainMap, tiledict)
    return terrainMap

def fill_map(configuration,terrainMap,attribute):
    # Create walls
    basicTile=configuration['basicTile']
    
    for i in range(0,attribute['num']):
        a = random.randrange(0,configuration['map_size'][0])
        b = random.randrange(0,configuration['map_size'][1])
        while not(terrainMap[a][b][0] == configuration['maptiles'][basicTile]['id']):
            a = random.randrange(0,configuration['map_size'][0])
            b = random.randrange(0,configuration['map_size'][1])
        if 'attributes' in attribute.keys():
            tileAttributes = dict(attribute['attributes'])
        else:
            tileAttributes = None
            
        terrainMap[a][b] = [attribute['id'],i,tileAttributes]

    return terrainMap

def print_map(terrainMap, configuration, images, screen, state, tile_size, fsm_state, tracep ,show_text="Insert text here"):
    basicTile=configuration['basicTile']
    if tracep:
        print("Printing map")
    screen.fill(background)

    for i in range(0,configuration['map_size'][0]):
        for j in range (0,configuration['map_size'][1]):
            if terrainMap[i][j][0] == configuration['maptiles'][basicTile]['id']:
                d = [0, 0]
            else:
                d = disp

            rect = pygame.Rect(i * tile_size + d[0], j * tile_size + d[1], 1, 1)                
            
            if terrainMap[i][j][2]['agent'] is not None:
                image = images[terrainMap[i][j][2]['agent']]
            else:
                for tilekey, tiledict in configuration['maptiles'].iteritems():
                    if tiledict['id'] == terrainMap[i][j][0]:
                        image = images[tilekey]
            
            screen.blit(image, rect)
    if tracep:
        s = printable_map(terrainMap, configuration, False)
        print(s)
    rect1 = pygame.Rect((0, configuration['map_size'][1] * tile_size, 1, 1))
    rect2 = pygame.Rect((0, configuration['map_size'][1] * tile_size + 30, 1, 1))
    #font = pygame.font.SysFont(pygame.font.get_fonts()[6], 30)
    font = pygame.font.Font(None, 24)
    if state['inPause']:
        if state['step']:
                controlText="**** STEP MODE - PRESS 'S' TO STEP [SPACE: CONTINUE] ****"
        else:
                controlText="**** PAUSED - PRESS SPACE TO CONTINUE ['S' STEP] ****"
        controlColor=red
    else:
        controlText="**** RUNNING - FOLLOWING PLAN [SPACE: PAUSE] [S: STEP] ****"
        controlColor=blue
        
    rect1 = pygame.Rect((0, configuration['map_size'][1] * tile_size, 1, 1))
    text1 = font.render(controlText,1,controlColor)
    screen.blit(text1, rect1)
    
    l=1
    for show_line in show_text.split('\n'):
        rect2 = pygame.Rect((0, configuration['map_size'][1] * tile_size + 18*l, 1, 1))
        text2 = font.render(show_line,1,green)
        screen.blit(text2, rect2)
        l += 1

    pygame.display.flip()


def printable_map(terrainMap, configuration, screenp):
    s = ''
    for j in range (0,configuration['map_size'][1]):
        for i in range(0,configuration['map_size'][0]):
            if screenp:
                y = configuration['map_size'][1] - j - 1
            else: y = j
            
            if terrainMap[i][y][2]['agent'] == configuration["agentType"]:
                s+= configuration["agentMarker"]
            else:
                for tilekey, tiledict in configuration['maptiles'].iteritems():
                    if terrainMap[i][y][0] == tiledict['id']:
                        s += tiledict['marker']
        s = s + '\n'
    return s

def read_map(configuration):
    basicTile=configuration['basicTile']
    map_file= configuration['file']
    for tilekey, tiledict in configuration['maptiles'].iteritems():
        if 'num' in tiledict:
            tiledict['num'] = 0
    
    allowed = configuration["agentMarker"]
    for tilekey, tiledict in configuration["maptiles"].iteritems():
        allowed += tiledict['marker']
    
    allowed = "([" + allowed + "]*)\n"
    
    with open(map_file, 'r') as f:
        lines = re.findall(allowed,f.read())
        
    configuration['map_size'][1] = len(lines)
    configuration['map_size'][0] = len(lines[0])

    basicTile=configuration['basicTile']
    basicMapConf= configuration['maptiles'][basicTile]
        
    terrainMap = [ [ [ basicMapConf['id'],0,
                 dict(basicMapConf['attributes'])]
               for x in range(configuration['map_size'][1])
             ] 
            for y in range(configuration['map_size'][0])]

    column = -1
    for line in lines:
        row = -1
        column = column + 1
        for char in line:
            row = row + 1
            if char == configuration["agentMarker"] :
                terrainMap[row][column][2]["agent"] = configuration["agentType"]
                terrainMap[row][column][0] = configuration["maptiles"]["drone-base"]["id"]
                configuration["agentInit"] = [row,column]
            else:
                for tilekey, tiledict in configuration['maptiles'].iteritems():
                    if char == tiledict['marker']:
                        terrainMap[row][column][0] = tiledict['id']
                        if 'num' in tiledict.keys():
                            configuration['maptiles'][tilekey]['num'] += 1
                            terrainMap[row][column][1] =  configuration['maptiles'][tilekey]['num'] 
                        if 'attributes' in tiledict.keys():
                            terrainMap[row][column][2] = dict(tiledict['attributes'])

            
    return terrainMap, configuration
