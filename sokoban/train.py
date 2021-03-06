import utilitiesLWB
from SokobanMap import SokobanMap
import matplotlib.pyplot as plt
from setupDQN import Agent
import numpy as np

actionToWord= {
    0: "U",
    1: "R",
    2: "D",
    3: "L"
}

def outputBestActions(name,actions,rewards):
    i = 0
    # print(actions)
    while True:
        try:
            if (actions[i] == actions[i + 2] and abs(actions[i] - actions[i + 1]) == 2 and rewards[i] != 10 and rewards[i] != 100 and rewards[i + 1] != 10 and rewards[i + 1] != 100):
                actions.pop(i)
                actions.pop(i)
                rewards.pop(i)
                rewards.pop(i)
                # print(actions)
            else:
                i = i + 1
        except:
            break
    with open("./result/"+name+".txt", "w") as txt_file:
        txt_file.write(str(len(actions)))
        for action in actions:
            txt_file.write(" "+actionToWord[action])  # works with any number of elements in a line

def plot_learning_curve(x,scores,epsilons,filename,lines=None):
    fig=plt.figure()
    ax=fig.add_subplot(111,label="1")
    ax2=fig.add_subplot(111,label="2",frame_on=False)
    ax.plot(x,epsilons,color="C0")
    ax.set_xlabel("Training Steps", color="C0")
    ax.set_ylabel("Epsilon", color="C0")
    ax.tick_params(axis='x', colors = "C0")
    ax.tick_params(axis='y', colors="C0")
    N = len(scores)
    running_avg = np.empty(N)
    for t in range(N):
        running_avg[t] = np.mean(scores[max(0, t - 20): (t + 1)])

    ax2.scatter(x, running_avg, color="C1")
    ax2.axes.get_xaxis().set_visible(False)
    ax2.yaxis.tick_right()
    ax2.set_ylabel('Score',color="C1")
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='y', colors="C1")
    if lines is not None:
        for line in lines:
            plt.axvline(x=line)

    plt.savefig(filename)

if __name__ == '__main__':
    currFileName="input-05b"
    Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt(currFileName);
    # Sokoban = utilitiesLWB.loadMapFromTxt(currFileName)
    utilitiesLWB.showMap(Sokoban.currMap)
    mapSize=Sokoban.getMapSize()
    agent = Agent(gamma=0.9999, epsilon=1, batch_size=96, n_actions=4, eps_end=0.1, input_dims=(1,7,*mapSize), lr=0.001,chkpt_dir="saved_model/",name=currFileName)
    try:
        agent.load_models()
        print('... checkpoint loaded ...')
    except:
        print('... checkpoint failed ...')
    scores,eps_history=[],[]
    reportPeriod=1
    n_games=1000
    stepLimit = 2500
    M=mapSize[0]
    N=mapSize[1]
    overAllSteps=[]
    overAllStepCt=0

    lastAction=-99
    lastReward=-9999
    recordNumOfTargets=-1;
    recordStepCt=stepLimit*2;
    for i in range(n_games):
        trackActions=[]
        trackRewards=[]
        numOfTargets=0
        score=0
        done=False
        Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt(currFileName)
        # Sokoban = utilitiesLWB.loadMapFromTxt(currFileName)
        # utilitiesLWB.showMap(Sokoban.currMap)
        observation3= Sokoban.getTrainMaps()
        observation3 = observation3.reshape((1,1,7,M,N))

        # agent.predict(observation3)
        # # utilitiesLWB.showMap(Sokoban.currMap)
        # print("Step: "+str(overAllStepCt))
        # print("---------------------------")

        stepCt=0
        actions=[]
        while not done:
            actions = [0, 1, 2, 3]
            action = agent.choose_action(observation3)
            overAllStepCt += 1
            stepCt += 1

            try:
                reward,tempSokoban = Sokoban.getReward(action)
                # moved
                trackActions.append(action)
                trackRewards.append(reward)
                if (i == n_games - 1):
                    print("=============================")
                    print(score)
                    utilitiesLWB.showMap(tempSokoban.currMap)
            except:
                # blocked by something
                reward = -50
                agent.store_trasition(observation3, action, reward, observation3, done)
                overAllStepCt += 1
                stepCt += 1
                actions.pop(action)
                position=0
                while True:
                    try:
                        reward, tempSokoban = Sokoban.getReward(actions[position])
                        position+=1
                    except:
                        actions.pop(position)
                    if (position>=len(actions)):
                        break
                action = np.random.choice(actions)
                reward, tempSokoban = Sokoban.getReward(action)
                trackActions.append(action)
                trackRewards.append(reward)
            score += reward

            observation_ = tempSokoban.getTrainMaps()
            observation_ = observation_.reshape((1, 1, 7, M, N))

            if (reward == -100):
                #deadlock
                agent.store_trasition(observation3, action, reward, observation_, done)
                overAllStepCt += 1
                stepCt += 1
                actions.pop(actions.index(action))
                trackActions.pop(len(trackActions)-1)
                trackRewards.pop(len(trackRewards)-1)
                position = 0
                # utilitiesLWB.showMap(Sokoban.currMap)
                while True:
                    try:
                        reward, tempSokoban = Sokoban.getReward(actions[position])
                        if (reward==-100):
                            actions.pop(position)
                        else:
                            position += 1
                    except:
                        actions.pop(position)
                    if (position >= len(actions)):
                        break
                if (len(actions)==0):
                    done=True
                    continue
                else:
                    action = np.random.choice(actions)
                    reward, tempSokoban = Sokoban.getReward(action)
                    trackActions.append(action)
                    trackRewards.append(reward)
                    observation_ = Sokoban.getTrainMaps()
                    observation_ = observation_.reshape((1, 1, 7, M, N))
            if (len(actions)>1 and abs(action-lastAction)==2 and lastReward!=100 and lastReward!=max(10,100/len(Sokoban.boxes))):
                done = False
                trackActions.pop(len(trackActions)-1)
                trackRewards.pop(len(trackRewards)-1)
                continue
                # overAllStepCt += 1
                # stepCt += 1
                # actions.pop(actions.index(action))
                # action = np.random.choice(actions)
                # print(action)
                # reward, tempSokoban = Sokoban.getReward(action)
                # observation_ = Sokoban.getTrainMaps()
                # observation_ = observation_.reshape((1, 1, 7, M, N))
            lastAction=action
            lastReward=reward
            Sokoban = tempSokoban
            # print(stepCt)
            if (reward == 10):
                reward=max(10,100/len(Sokoban.boxes))
                numOfTargets+=1
            if (reward == 100):
                numOfTargets += 1
                print("+++++++++++++++++++++target stepCt "+str(stepCt)+"+++++++++++++++++++++")
                done = True
            agent.store_trasition(observation3, action, reward, observation_, done)

            # if (overAllStepCt > 3):
            #     observation0 = observation1
            # if (overAllStepCt > 2):
            #     observation1 = observation2
            # if (overAllStepCt > 1):
            #     observation2 = observation3
            observation3 = observation_

            if (overAllStepCt%5000==1):
                agent.learn(True)
            else:
                agent.learn(False)
            if stepCt >= stepLimit:
                done = True

        scores.append(score)

        overAllSteps.append(overAllStepCt)

        eps_history.append(agent.epsilon)

        avg_score=np.mean(scores[-100:])

        if (i % reportPeriod == 0):
            print('episode ',i,
                  '|score %.2f' % score,
                  '|average score %.2f' % avg_score,
                  '|epsilon %.2f' % agent.epsilon,
                  '| moved %.0f steps' % stepCt,
                  '|total steps %.0f' % overAllStepCt,
                  '| %.0f target hit' % numOfTargets)
            agent.save_models()

        if (i % (reportPeriod*5) == 0):
            plot_learning_curve(overAllSteps, scores, eps_history, currFileName + "_curve")

        if (numOfTargets>=1 and numOfTargets>recordNumOfTargets):
            recordNumOfTargets=numOfTargets;
            outputBestActions(currFileName+"_"+str(recordNumOfTargets)+"_of_"+str(len(Sokoban.targets)),trackActions,trackRewards)
            recordStepCt=stepCt
        elif (numOfTargets==recordNumOfTargets and stepCt < recordStepCt):
            recordStepCt=stepCt
            outputBestActions(currFileName + "_" + str(recordNumOfTargets) + "_of_" + str(len(Sokoban.targets)),trackActions, trackRewards)

