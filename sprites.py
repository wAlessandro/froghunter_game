
import os
import shutil
import typing


__all__ =[ 
    "SPRITE"
]

imagespath = os.path.join("sprites")

class TypeSprite(typing.TypedDict):
    playerright:str
    playerleft:str
    playeratackleft:str
    playeratackright:str
    hearticon:str
    damageicon:str

    frogboss:str
    sleepingfrogboss:str
    lakebackground:str
    frogbossicon:str
    
SPRITE:TypeSprite = {}

for dirs in os.listdir(imagespath):
    if os.path.isdir(os.path.join(imagespath, dirs)):
        pathdir = os.path.join(imagespath, dirs)
        for filed in os.listdir(pathdir):
            filedir = os.path.join(pathdir,filed)
            name, extension = os.path.splitext(filed)
            SPRITE[name] = filedir
    else:
        for dirs in os.listdir(imagespath):
            filedir = os.path.join(imagespath, dirs)
            print(filedir)
            name, extension = os.path.splitext(dirs)
            SPRITE[name] = filedir
if __name__ == "__main__":
    for item in SPRITE.values():
        print(item)
    