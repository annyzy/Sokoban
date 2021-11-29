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
            return 100
        #check deadlock
        if (utilitiesLWB.isDeadLock(tempSokoban)):
            return -100

        return reward

    # direction：      0:上    1：右     2：下    3：左
    # direction：      0:Up    1：Right     2：Down    3：Left
    #返回的是SokobanMap class：move成功；返回的是None：move失败
    #return is SokobanMap class：move successed; return is None：move failed
    def move(self,direction):
        tempSokoban=SokobanMap(self.walls, self.boxes, self.targets, self.agent, self.currMap)
        currMap=tempSokoban.getCurrMap()
        agent=tempSokoban.getAgentPosition()
        currRow=agent[0]
        currColumn=agent[1]
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