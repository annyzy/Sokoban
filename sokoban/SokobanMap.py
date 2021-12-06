import copy
import numpy as np
import utilitiesLWB
#map中数值含义：      0:空白    1：墙     2：箱子位置    3：箱子目标    4：小人    5:箱子在目标上    6:小人在目标上
#map values：      0:null    1：wall     2：box    3：storage location    4：agent    5:box in storage   6:agent on storage
class SokobanMap:
    def __init__(self, walls,boxes,targets,agent,currMap):
        self.walls = walls
        self.boxes = boxes
        self.targets = targets
        self.agent = agent
        self.currMap = currMap

        # self.wallsORG = copy.deepcopy(walls)
        # self.boxesORG = copy.deepcopy(boxes)
        # self.targetsORG = copy.deepcopy(targets)
        # self.agentORG = copy.deepcopy(agent)
        # self.currMapORG = copy.deepcopy(currMap)

    # def resetGame(self):
    #     self.walls = copy.deepcopy(self.wallsORG)
    #     self.boxes = copy.deepcopy(self.boxesORG)
    #     self.targets = copy.deepcopy(self.targetsORG)
    #     self.agent = copy.deepcopy(self.agentORG)
    #     self.currMap = copy.deepcopy(self.currMapORG)
    #     print(self.currMapORG)
    #     print("====================")
    #     print(copy.deepcopy(self.currMapORG))

    def getTrainMaps(self):
        rows=self.currMap.shape[0]
        columns=self.currMap.shape[1]
        rslt=np.zeros((7,rows,columns))
        for row in range(rows):
            for col in range(columns):
                for element in range(7):
                    if self.currMap[row][col]==element:
                        rslt[element][row][col]=float(1)
        rslt = rslt.astype('float32')
        return rslt


    def getMapSize(self):
        return self.currMap.shape

    def getWallPositions(self):
        return self.walls

    def getBoxPositions(self):
        return self.boxes

    def getStorageLocation(self):
        return self.targets

    def getAgentPosition(self):
        return self.agent

    def getCurrMap(self):
        return self.currMap

    # direction：      0:上    1：右     2：下    3：左
    # direction：      0:Up    1：Right     2：Down    3：Left
    #返回的是数值：reward；返回的是None：move失败
    #return is number：reward; return is None：move failed
    def getReward(self,direction):
        reward=None
        currMap=self.currMap
        currRow=self.agent[0]
        currColumn=self.agent[1]
        currState=currMap[currRow][currColumn]
        if (direction == 0):
            targetRow=currRow-1
            targetColumn=currColumn
            targetNextRow=currRow-2
            targetNextColumn=currColumn
        elif (direction == 1):
            targetRow=currRow
            targetColumn=currColumn+1
            targetNextRow=currRow
            targetNextColumn=currColumn+2
        elif (direction == 2):
            targetRow=currRow+1
            targetColumn=currColumn
            targetNextRow=currRow+2
            targetNextColumn=currColumn
        elif (direction == 3):
            targetRow=currRow
            targetColumn=currColumn-1
            targetNextRow=currRow
            targetNextColumn=currColumn-2
        else:
            return "Wrong direction"
        if targetNextRow<0 or targetNextRow>=currMap.shape[0]:
            return None
        if targetNextColumn<0 or targetNextColumn>=currMap.shape[1]:
            return None
        targetState=currMap[targetRow][targetColumn]
        targetNextState=currMap[targetNextRow][targetNextColumn]
        if (targetState == 0):
            # 目标位置是空白
            # target position is null

            # 返回Reward
            # Return reward
            reward = -1
        elif(targetState == 1):
            # 目标位置是墙
            # target position is wall
            return None
        elif(targetState == 2):
            # 目标位置是箱子
            # target position is box
            if (targetNextState == 0 ):
                # 返回Reward
                # Return reward
                reward = -1
            elif ( targetNextState == 3):
                # 返回Reward
                # Return reward
                reward = 10
            else:
                return None
        elif(targetState == 3):
            # 目标位置是箱子目标
            # target position is storage location

            # 返回Reward
            # Return reward
            reward = -1
        elif(targetState == 5):
            # 目标位置是 箱子在目标上
            # target position is box in storage
            if (targetNextState == 0 ):
                # 返回Reward
                # Return reward
                reward = -10
            elif ( targetNextState == 3):
                # 返回Reward
                # Return reward
                reward = -1
            else:
                return None


        tempSokoban=self.move(direction)
        #check all-target
        if (utilitiesLWB.isAllTarget(tempSokoban)):
            print("all-target")
            return 100,tempSokoban
        #check deadlock
        if (utilitiesLWB.isDeadLock(tempSokoban)):
            return -100,tempSokoban

        # if reward==-1:
            # reward=-0.1
        return reward,tempSokoban

    # direction：      0:上    1：右     2：下    3：左
    # direction：      0:Up    1：Right     2：Down    3：Left
    #返回的是SokobanMap class：move成功；返回的是None：move失败
    #return is SokobanMap class：move successed; return is None：move failed
    def move(self,direction):
        tempSokoban=SokobanMap(copy.deepcopy(self.walls) , copy.deepcopy(self.boxes), copy.deepcopy(self.targets), copy.deepcopy(self.agent), copy.deepcopy(self.currMap))
        currMap=tempSokoban.getCurrMap()
        currRow=tempSokoban.agent[0]
        currColumn=tempSokoban.agent[1]
        currState=currMap[currRow][currColumn]
        if (direction == 0):
            targetRow=currRow-1
            targetColumn=currColumn
            targetNextRow=currRow-2
            targetNextColumn=currColumn
        elif (direction == 1):
            targetRow=currRow
            targetColumn=currColumn+1
            targetNextRow=currRow
            targetNextColumn=currColumn+2
        elif (direction == 2):
            targetRow=currRow+1
            targetColumn=currColumn
            targetNextRow=currRow+2
            targetNextColumn=currColumn
        elif (direction == 3):
            targetRow=currRow
            targetColumn=currColumn-1
            targetNextRow=currRow
            targetNextColumn=currColumn-2
        else:
            return None
        targetState=currMap[targetRow][targetColumn]
        targetNextState=currMap[targetNextRow][targetNextColumn]
        # map中数值含义：      0:空白    1：墙     2：箱子位置    3：箱子目标    4：小人    5:箱子在目标上    6:小人在目标上
        # map values：      0:null    1：wall     2：box    3：storage location    4：agent    5:box in storage   6:agent on storage
        if (targetState == 0):
            # 目标位置是空白
            # target position is null

            # 更新位置
            # update agent position
            tempSokoban.agent=[targetRow,targetColumn]
            # print(tempSokoban.agent)
            # 更新地图
            # update map
            currMap[targetRow][targetColumn]=4
            if (currState == 4):
                currMap[currRow][currColumn]=0
            elif (currState == 6):
                currMap[currRow][currColumn]=3
            tempSokoban.currMap=currMap

        elif(targetState == 1):
            # 目标位置是墙
            # target position is wall
            return None
        elif(targetState == 2):
            # 目标位置是箱子
            # target position is box
            if (targetNextState == 0 ):
                # 更新位置
                # update agent position
                boxes=tempSokoban.boxes
                tempSokoban.agent = [targetRow, targetColumn]
                boxIndex = boxes.index([targetRow, targetColumn])
                boxes[boxIndex]=[targetNextRow,targetNextColumn]
                tempSokoban.boxes=boxes
                # 更新地图
                # update map
                if (currState == 4):
                    currMap[currRow][currColumn]=0
                elif (currState == 6):
                    currMap[currRow][currColumn]=3
                currMap[targetRow][targetColumn]=4
                currMap[targetNextRow][targetNextColumn]=2
                tempSokoban.currMap=currMap
            elif ( targetNextState == 3):
                # 更新位置
                # update agent position
                boxes=tempSokoban.boxes
                tempSokoban.agent = [targetRow, targetColumn]
                boxIndex = boxes.index([targetRow, targetColumn])
                boxes[boxIndex]=[targetNextRow,targetNextColumn]
                tempSokoban.boxes=boxes
                # 更新地图
                # update map
                if (currState == 4):
                    currMap[currRow][currColumn]=0
                elif (currState == 6):
                    currMap[currRow][currColumn]=3
                currMap[targetRow][targetColumn]=4
                currMap[targetNextRow][targetNextColumn]=5
                tempSokoban.currMap=currMap
            else:
                return None
            # map中数值含义：      0:空白    1：墙     2：箱子位置    3：箱子目标    4：小人    5:箱子在目标上    6:小人在目标上
            # map values：      0:null    1：wall     2：box    3：storage location    4：agent    5:box in storage   6:agent on storage
        elif(targetState == 3):
            # 目标位置是箱子目标
            # target position is storage location

            # 更新位置
            # update agent position
            tempSokoban.agent=[targetRow,targetColumn]
            # 更新地图
            # update map
            currMap[targetRow][targetColumn]=6
            if (currState == 4):
                currMap[currRow][currColumn]=0
            elif (currState == 6):
                currMap[currRow][currColumn]=3
            tempSokoban.currMap=currMap
            # 返回Reward
            # Return reward
        elif(targetState == 5):
            # 目标位置是 箱子在目标上
            # target position is box in storage
            if (targetNextState == 0 ):
                # 更新位置
                # update agent position
                boxes=tempSokoban.boxes
                tempSokoban.agent = [targetRow, targetColumn]
                boxIndex = boxes.index([targetRow, targetColumn])
                boxes[boxIndex]=[targetNextRow,targetNextColumn]
                tempSokoban.boxes=boxes
                # 更新地图
                # update map
                if (currState == 4):
                    currMap[currRow][currColumn]=0
                elif (currState == 6):
                    currMap[currRow][currColumn]=3
                currMap[targetRow][targetColumn]=6
                currMap[targetNextRow][targetNextColumn]=2
                tempSokoban.currMap=currMap
            # map中数值含义：      0:空白    1：墙     2：箱子位置    3：箱子目标    4：小人    5:箱子在目标上    6:小人在目标上
            # map values：      0:null    1：wall     2：box    3：storage location    4：agent    5:box in storage   6:agent on storage
            elif ( targetNextState == 3):
                # 更新位置
                # update agent position
                boxes=tempSokoban.boxes
                tempSokoban.agent = [targetRow, targetColumn]
                boxIndex = boxes.index([targetRow, targetColumn])
                boxes[boxIndex]=[targetNextRow,targetNextColumn]
                tempSokoban.boxes=boxes
                # 更新地图
                # update map
                if (currState == 4):
                    currMap[currRow][currColumn]=0
                elif (currState == 6):
                    currMap[currRow][currColumn]=3
                currMap[targetRow][targetColumn]=6
                currMap[targetNextRow][targetNextColumn]=5
                tempSokoban.currMap=currMap
            else:
                return None
        return tempSokoban
