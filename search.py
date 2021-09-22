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

    # rows and cols are concludes wall, 0 and last row/col num means wall...
    # so, 0 will ignored, we use 1~row-1, 1~col-1 to coordinate
    stored_path = [[(-1,-1) for j in range(maze.cols - 1)] for i in range(maze.rows - 1) ]  #path[cur.row][cur.col] = paraent[row][col]

    ####################### Write Your Code Here ################################
    visited = [[False for j in range(maze.cols - 1) ] for i in range(maze.rows - 1)]
    queue = deque()
    
    queue.appendleft(start_point)
    stored_path[start_point[0]][start_point[1]] = (-11, -11)
    dest_row = -1
    dest_col = -1

    while(len(queue) > 0):
        current_point = queue.popleft()
    #    print("current point and queue before extend")
    #    print(current_point)
    #    print(queue)

        # if already visited - no search
        if visited[current_point[0]][current_point[1]]:
            continue

        visited[current_point[0]][current_point[1]] = True

        # Goal Check;
        if maze.isObjective(current_point[0], current_point[1]):
    #        print("path found!!")
            stored_path[point[0]][point[1]] = (current_point[0],current_point[1])
            dest_row = current_point[0]
            dest_col = current_point[1]
            break

        # expending nodes
        neighbors = maze.neighborPoints(current_point[0], current_point[1])

    #    print("n")
    #    print(neighbors)
        
        # https://devpouch.tistory.com/110
        # do not remove elements in list while looping....
        for point in neighbors[:]:
            '''
            NO USE BECAUSE ALREADY IMPLEMENTED IN maze.choosemove()

            if maze.choosemove(point.row, point.col) == False:
                neighbors.remove(point) #no more way to move from given point.
            ''' 
            if visited[point[0]][point[1]] == True:
    #            print("erased")
    #            print(point[0],point[1])
                neighbors.remove(point) #already visited
            
            else:
    #            print("first")
    #            print(point[0],point[1])
                stored_path[point[0]][point[1]] = (current_point[0], current_point[1])
    #            print(stored_path)
        queue.extend(neighbors)
    #    print("after extend")
    #    print(queue)

    
    row = dest_row
    col = dest_col
    i=0

    while(row != -11 and col !=-11):
        next_r = stored_path[row][col][0]
        next_c = stored_path[row][col][1]

        path.append((next_r, next_c))
        
        row = next_r
        col = next_c
        i +=1
        #
        #print(str(row) + "," + str(col))


    path.reverse() #change order to depart from start point.
    print(type(path))
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
    start_node = Node(None, start_point)
    end_point=maze.circlePoints()[0]

    path=[]

    ####################### Write Your Code Here ################################
    #   
    discard = []
    candidate = []

    current_node = start_node
    candidate.append(start_node)


    while len(candidate) > 0:
        current_node = candidate[0]

        for cand in candidate:
            if current_node.f > cand.f:
                current_node = cand

        candidate.remove(current_node)
        discard.append(current_node)

        if maze.isObjective(current_node.location[0], current_node.location[1]):    
            candidate.append(current_node)
            #print("Goal")
            #print(current_node.location[0], current_node.location[1])
            break

        cur_row = current_node.location[0]
        cur_col = current_node.location[1]
        for adj in maze.neighborPoints(cur_row, cur_col):

            adj_node = Node(current_node, adj)

            # if adjacent node is already discarded - don't search further...
            if adj_node in discard:
                continue 

            adj_node.g = current_node.g+1
            adj_node.h = manhatten_dist(adj,end_point)

            adj_node.f = adj_node.g + adj_node.h

            # https://info-lab.tistory.com/117
            # check element in list using if-in statement
            if adj_node in candidate:
                if adj_node.g >= current_node.g: #if adjacent node's g >= current: cannot be candidate
                    continue
            
            #only goal-direction positioned nodes can be candidate.
            candidate.append(adj_node)
                            
    path_node = candidate.pop()
    while(path_node.parent is not None):
        path.append(path_node.location)
        t = path_node.parent
        path_node = t
    path.reverse()
    #print(path)
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
