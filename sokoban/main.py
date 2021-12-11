import utilitiesLWB
import sys
from SokobanMap import SokobanMap
import matplotlib.pyplot as plt
from setupDQN import Agent
import numpy as np
import train
actionToWord= {
    0: "U",
    1: "R",
    2: "D",
    3: "L"
}

wordToAction= {
    "U":0,
    "R":1,
    "D":2,
    "L":3
}

if __name__ == '__main__':
    currFileName = "input-03"
    Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt(currFileName);
    utilitiesLWB.showMap(Sokoban.currMap)
    with open("./result/"+currFileName+"_4_of_"+str(len(Sokoban.targets))+".txt","r") as f:
        for line in f:
            firstLine = line.strip('\n')
            actions = firstLine.split(" ")
            actions.pop(0)
    score=0
    for i in range(len(actions)):
        action=wordToAction[actions[i]]
        print("----------------------Step#"+str(i+1)+"----------------------")
        print("Action: " + actions[i])

        reward, Sokoban = Sokoban.getReward(action)
        score += reward

        print("Reward: " + str(reward))
        print("Score: " + str(score))
        utilitiesLWB.showMap(Sokoban.currMap)
