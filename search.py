###### Write Your Library Here ###########
import pygame
from maze import Maze as maze
from collections import deque


#########################################


def search(maze, func):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)


# -------------------- Stage 01: One circle - BFS Algorithm ------------------------ #

def bfs(maze):
    """
    [문제 01] 제시된 stage1의 맵 세가지를 BFS Algorithm을 통해 최단 경로를 return하시오.(20점)
    """
    start_point=maze.startPoint()

    path=[] #최단경로를 도착점부터 다시 저장해둘 리스트.
    stored_path = [[-1 for j in range(maze.cols)] for i in range(maze.rows) ]  #path[cur.row][cur.col] = paraent[row][col]

    ####################### Write Your Code Here ################################
    visited = [[False for j in range(maze.cols) ] for i in range(maze.rows)]
    queue = deque()
    
    queue.appendleft(start_point)
    stored_path[start_point[0]][start_point[1]] = (-1.1, -1.1)
    dest_row = -1
    dest_col = -1

    while(len(queue) > 0):
        current_point = queue.popleft()
        visited[current_point[0]][current_point[1]] = True

        neighbors = maze.neighborPoints(current_point[0], current_point[1])
        for point in neighbors:
            '''
            NO USE BECAUSE ALREADY IMPLEMENTED IN maze.choosemove()

            if maze.choosemove(point.row, point.col) == False:
                neighbors.remove(point) #no more way to move from given point.
            '''

            if maze.isObjective(point[0], point[1]):
                print("path found!!")
                stored_path[point[0]][point[1]] = (current_point[0],current_point[1])
                dest_row = point[0]
                dest_col = point[1]
                break
                
            elif visited[point[0]][point[1]] == True:
                neighbors.remove(point) #already visited
            
            else:
                stored_path[point[0]][point[1]] = (current_point[0], current_point[1])

        queue.extend(neighbors)


    row = dest_row
    col = dest_col
    while(row != 1.1 and col != -1,1):
        next_r = stored_path[row][col][0]
        next_c = stored_path[row][col][1]

        path.append((next_r, next_c))
        row = next_r
        col = next_c
    

    path = path.reverse #change order to depart from start point.
    return path

    ############################################################################



class Node:
    def __init__(self,parent,location):
        self.parent=parent
        self.location=location #현재 노드

        self.obj=[]

        # F = G+H
        self.f=0
        self.g=0
        self.h=0

    def __eq__(self, other):
        return self.location==other.location and str(self.obj)==str(other.obj)

    def __le__(self, other):
        return self.g+self.h<=other.g+other.h

    def __lt__(self, other):
        return self.g+self.h<other.g+other.h

    def __gt__(self, other):
        return self.g+self.h>other.g+other.h

    def __ge__(self, other):
        return self.g+self.h>=other.g+other.h


# -------------------- Stage 01: One circle - A* Algorithm ------------------------ #

def manhatten_dist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def astar(maze):

    """
    [문제 02] 제시된 stage1의 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.(20점)
    (Heuristic Function은 위에서 정의한 manhatten_dist function을 사용할 것.)
    """

    start_point=maze.startPoint()

    end_point=maze.circlePoints()[0]

    path=[]

    ####################### Write Your Code Here ################################

















    return path

    ############################################################################


# -------------------- Stage 02: Four circles - A* Algorithm  ------------------------ #



def stage2_heuristic():
    pass


def astar_four_circles(maze):
    """
    [문제 03] 제시된 stage2의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage2_heuristic function을 직접 정의하여 사용해야 한다.)
    """

    end_points=maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################


















    return path

    ############################################################################



# -------------------- Stage 03: Many circles - A* Algorithm -------------------- #

def mst(objectives, edges):

    cost_sum=0
    ####################### Write Your Code Here ################################













    return cost_sum

    ############################################################################


def stage3_heuristic():
    pass


def astar_many_circles(maze):
    """
    [문제 04] 제시된 stage3의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage3_heuristic function을 직접 정의하여 사용해야 하고, minimum spanning tree
    알고리즘을 활용한 heuristic function이어야 한다.)
    """

    end_points= maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################





















    return path

    ############################################################################
