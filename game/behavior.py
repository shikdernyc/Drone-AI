import random

max_fsm_state = 5

def fsm_behavior(mapa, state, configuration, position, fsm_state, steps_in_state, direccion_guardia, tracep):
    if tracep:
        print("FSM state: "+fsm_state)
    if fsm_state == 'init':
        close = close_by(mapa, configuration, position)
        steps_in_state = 0
        if close:
            fsm_state = 'persigue'
        else:
            direccion_guardia = choose_direction()
            fsm_state = 'guardia'
    elif fsm_state == 'persigue':
        mapa, state = greedy_behavior(mapa, state, configuration, position)
        steps_in_state = steps_in_state + 1
        close = close_by(mapa, configuration, position)
        if not(close) or (steps_in_state > max_fsm_state):
            steps_in_state = 0
            fsm_state = 'random'
    elif fsm_state == 'random':
        mapa, state = random_behavior(mapa, state, configuration)
        steps_in_state = steps_in_state + 1
        close = close_by(mapa, configuration, position)
        if close:
            fsm_state = 'persigue'
        elif steps_in_state > max_fsm_state:
            steps_in_state = 0
            direccion_guardia = choose_direction()
            fsm_state = 'guardia'
    elif fsm_state == 'guardia':
        if tracep:
            print("Direction: " + direccion_guardia)
        mapa, state = guardia_behavior(mapa, state, configuration, direccion_guardia)
        steps_in_state = steps_in_state + 1
        close = close_by(mapa, configuration, position)
        if close:
            fsm_state = 'persigue'
        elif steps_in_state > max_fsm_state:
            steps_in_state = 0
            fsm_state = 'random'
    return mapa, state, fsm_state, steps_in_state, direccion_guardia

def choose_direction():
    r = random.randrange(0,4)
    if r == 0:
        direccion_guardia = 'north'
    elif r == 1:
        direccion_guardia = 'south'
    elif r == 2:
        direccion_guardia = 'west'
    else:
        direccion_guardia = 'east'
    return direccion_guardia

# we could change -1 and 1 for bigger radii
# position is the position of Mario
def close_by(mapa, configuration, position):
    close = False
    for i in range(-1,1):
        for j in range (-1,1):
            x = i + position[0]
            y = j + position[1]
            if x >= 0 and x < configuration['map_size'][0] and y >= 0 and y < configuration['map_size'][1] and mapa[x][y][0] == 'bad':
                close = True
    return close

# def close_by(mapa, configuration['map_size'], position):
#     close = False
#     for i in range(0,configuration['map_size'][0]):
#         for j in range (0,configuration['map_size'][1]):
#             if mapa[i][j][0] == 'bad':
#                 if abs(position[0] - i) <= 1 and abs(position[1] - j) <= 1:
#                     close = True
#     return close
    
def random_behavior(mapa, state, configuration):
    for i in range(0,configuration['map_size'][0]):
        for j in range (0,configuration['map_size'][1]):
            if mapa[i][j][0] == 'bad':
                x = i + random.randrange(-1,2)
                y = j + random.randrange(-1,2)
#                 print("x: "+str(x)+" y: "+str(y))
                if x >= 0 and x < configuration['map_size'][0] and y >= 0 and y < configuration['map_size'][1]:
                    mapa, state = move_bad(mapa,state,i,j,x,y)
    return mapa, state


def greedy_behavior(mapa, state, configuration, new_pos):
    for i in range(0,configuration['map_size'][0]):
        for j in range (0,configuration['map_size'][1]):
            if mapa[i][j][0] == 'bad':
                dif = new_pos[0] - i
                if (dif > 0 and i < configuration['map_size'][0] - 1):
                    x = i + 1
                elif i > 0:
                    x = i - 1
                else:
                    x = i
                dif = new_pos[1] - j
                if (dif > 0 and j < configuration['map_size'][0] - 1):
                    y = j + 1
                elif j > 0:
                    y = j - 1
                else:
                    y = j
                # print("x: "+str(x)+" y: "+str(y))
                if (not(x == i) or not(y == j)):
                    mapa, state = move_bad(mapa,state,i,j,x,y)
    return mapa, state

def guardia_behavior(mapa, state, configuration, direccion_guardia):
    bads_moved = []
    for i in range(0,configuration['map_size'][0]):
        for j in range (0,configuration['map_size'][1]):
            if mapa[i][j][0] == 'bad' and not(mapa[i][j][1] in bads_moved):
                bads_moved = bads_moved + [mapa[i][j][1]]
                if direccion_guardia == 'north':
                    if j < configuration['map_size'][1]-1:
#                         print(str(mapa[i][j][1])+" *** i: "+str(i)+" j+1: "+str(j+1))
                        mapa, state = move_bad(mapa,state,i,j+1,i,j)
                elif direccion_guardia == 'south':
                    if j > 0:
#                         print(str(mapa[i][j][1])+" *** i: "+str(i)+" j+1: "+str(j-11))
                        mapa, state = move_bad(mapa,state,i,j-1,i,j)
                elif direccion_guardia == 'east':
                    if i < configuration['map_size'][0]-1:
#                         print(str(mapa[i][j][1])+" *** i+1: "+str(i+1)+" j: "+str(j))
                        mapa, state = move_bad(mapa,state,i+1,j,i,j)
                elif direccion_guardia == 'west':
                    if i > 0:
#                         print(str(mapa[i][j][1])+" *** i-1: "+str(i-1)+" j: "+str(j))
                        mapa, state = move_bad(mapa,state,i-1,j,i,j)
    return mapa, state

def move_bad (mapa, state, oldx, oldy, newx, newy):
    if mapa[newx][newy][0] == 'empty':
        mapa[newx][newy] = ['bad', mapa[oldx][oldy][1]]
        mapa[oldx][oldy] = ['empty']
        state['bad-positions'].remove([oldx,oldy])
        state['bad-positions'].insert(0,[newx,newy])
    elif (mapa[newx][newy][0] == 'eat' and state['bad_knives'] >= 1):
        state['points'] = state['points'] - 1
        state['bad_eats'][mapa[newx][newy][1]] = state['bad_eats'][mapa[newx][newy][1]] + 1
        mapa[newx][newy] = ['bad', mapa[oldx][oldy][1]]
        mapa[oldx][oldy] = ['empty']
        state['bad-positions'].remove([oldx,oldy])
        state['bad-positions'].insert(0,[newx,newy])
    elif mapa[newx][newy][0] == 'knife':
        state['bad_knives'] = state['bad_knives'] + 1
        mapa[newx][newy] = ['bad', mapa[oldx][oldy][1]]
        mapa[oldx][oldy] = ['empty']
        state['bad-positions'].remove([oldx,oldy])
        state['bad-positions'].insert(0,[newx,newy])
    return mapa, state
