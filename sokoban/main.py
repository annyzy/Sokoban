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

    #
    # mapSize = Sokoban.getMapSize()
    # agent = Agent(gamma=0.9999, epsilon=1, batch_size=256, name=currFileName,n_actions=4, eps_end=0.1, input_dims=(1, 7, *mapSize),
    #               lr=0.001, chkpt_dir="saved_model/")
    # try:
    #     agent.load_models()
    #     print('... checkpoint loaded ...')
    # except:
    #     print('... checkpoint failed ...')
    #     utilitiesLWB.showMap(Sokoban.currMap)
    #     sys.exit(0)
    #
    #
    # M = mapSize[0]
    # N = mapSize[1]
    # while True:
    #     Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt(currFileName);
    #     score = 0
    #     done = False
    #     actions=[]
    #     rewards=[]
    #     stepLimit = 5000
    #     stepCt=0
    #     while not done:
    #         observation = Sokoban.getTrainMaps()
    #         observation = observation.reshape((1, 1, 7, M, N))
    #         action = agent.predict(observation)
    #         try:
    #             reward,Sokoban = Sokoban.getReward(action)
    #             stepCt+=1
    #             score += reward
    #             actions.append(action)
    #             rewards.append(reward)
    #
    #             # print("--------------------------------------------------")
    #             # print("Action: "+actionToWord[action])
    #             # print("Reward: "+str(reward))
    #             # print("Score: "+str(score))
    #             # utilitiesLWB.showMap(Sokoban.currMap)
    #             if (reward==100 or reward==-100 or stepCt==stepLimit):
    #                 done=True
    #         except:
    #             None
    #     break
    #     if (reward==100):
    #         break
    #
    # rslt=[]
    # # print(actions)
    # i = 0
    # while True:
    #     try:
    #         if (actions[i] == actions[i + 2] and abs(actions[i]-actions[i+1])==2 and rewards[i] != 10 and rewards[i] != 100 and rewards[i + 1] != 10 and rewards[
    #             i + 1] != 100):
    #             actions.pop(i)
    #             actions.pop(i)
    #             rewards.pop(i)
    #             rewards.pop(i)
    #             # print(actions)
    #         else:
    #             i=i+1
    #     except:
    #         break
    # # print(actions)
    #
    # Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt(currFileName);
    # utilitiesLWB.showMap(Sokoban.currMap)
    # score=0
    # for action in actions:
    #     reward, Sokoban = Sokoban.getReward(action)
    #     score += reward
    #     print("--------------------------------------------------")
    #     print("Action: "+actionToWord[action])
    #     print("Reward: "+str(reward))
    #     print("Score: "+str(score))
    #     utilitiesLWB.showMap(Sokoban.currMap)
