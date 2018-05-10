configuration = {
"text_size": 150,
"tile_size": 60,
"type": "load", #"random"
"seed": None,
"file": "./map.txt",
"map_size": [10, 4],
"delay": 0.1,
"debugMap": False,
"debug": False,
"save": False, #True
"hazards": False,
"basicTile": "desert",
"agentInit":  [2, 1],
"agentBaseTile": "drone-base",
"agentType": "drone",
"agentMarker": "A",
"agentTiles": {
       "drone":"game/graphics/agents/drone.png"
     },
"maptiles": {
    "desert": {
        "img": "game/graphics/terrains/desert100.png",
        "id":  "desert",
        "marker": 'D',
        "attributes":
             {"agent":None,"cost": 1}
        },
    "desert-traversed": {
        "img": "game/graphics/terrains/desertTraversed100.png",
        "id":  "desert-traversed",
        "marker": 'd',
        "attributes":
             {"agent":None,"cost": 1}
        },
    "plains": {
        "img": "game/graphics/terrains/plains100.png",
        "id":  "plains",
        "marker": 'P',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1}
        },
    "plains-traversed": {
        "img": "game/graphics/terrains/plainsTraversed100.png",
        "id":  "plains-traversed",
        "marker": 'p',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1}
        },
    "hills": {
        "img": "game/graphics/terrains/hills100.png",
        "id":  "hills",
        "marker": 'H',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1},
        },
    "hills-traversed": {
        "img": "game/graphics/terrains/hillsTraversed100.png",
        "id":  "hills-traversed",
        "marker": 'h',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1},
        },
    "forest": {
        "img": "game/graphics/terrains/forest100.png",
        "id":  "forest",
        "marker": 'F',
        "num": 5,
        "attributes":
             {"agent":None,"cost": 1},
        },
    "forest-traversed": {
        "img": "game/graphics/terrains/forestTraversed100.png",
        "id":  "forest-traversed",
        "marker": 'f',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1},
        },
    "sea": {
        "img": "game/graphics/terrains/sea100.png",
        "id":  "sea",
        "marker": 'S',
        "num": 1,
        "attributes":
             {"agent":None,"blocked": True}
        },
    "sea-traversed": {
        "img": "game/graphics/terrains/seaTraversed100.png",
        "id":  "sea-traversed",
        "marker": 's',
        "num": 0,
        "attributes":
             {"agent":None,"blocked": True}
        },
    "goal": {
        "img": "game/graphics/locations/camera100.png",
        "id":  "goal",
        "marker": 'G',
        "num": 4,
        "attributes":
             {"agent":None,"cost": 1},
        },
    "goal-traversed": {
        "img": "game/graphics/locations/cameraTraversed100.png",
        "id":  "goal-traversed",
        "marker": 'g',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1},
        },
    "drone-base": {
        "img": "game/graphics/locations/droneBase100.png",
        "id":  "drone-base",
        "marker": 'B',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1},
        },
    "drone-base-traversed": {
        "img": "game/graphics/locations/droneBaseTraversed100.png",
        "id":  "drone-base-traversed",
        "marker": 'b',
        "num": 0,
        "attributes":
             {"agent":None,"cost": 1},
        }
     }
}
