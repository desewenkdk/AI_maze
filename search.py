###### Write Your Library Here ###########
import pygame
from maze import Maze as maze
from collections import deque
from queue import PriorityQueue
import heapq
import collections
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

        # if already visited - don't search
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

            #at here, adj node's parent node is updated to minimum F valued node(maybe?)
            adj_node = Node(current_node, adj)

            # if adjacent node is already discarded - don't search further...
            if adj_node in discard:
                continue 

            adj_node.g = current_node.g+1
            adj_node.h = manhatten_dist(adj,end_point)

            adj_node.f = adj_node.g + adj_node.h

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
def stage2_heuristic(cur_point, end_points):
    #mst using prim's method
    
    MSTedges = []
    start_index = 0
    
    #num: cur:0, end_points:1,2,3,4
    points = []
    points.append(cur_point)
    points.extend(end_points)
    visited = [0] * (len(end_points)+1)
    #print(visited)
    #list : [distance, u, v], represents edge
    # Edge stored list initialization, points are current, and end-points to visit
    edges = collections.defaultdict(list)
    calculated_sum_dist = 0

    for i in range(len(points)):
        for j in range(i,len(points)):
            edges[i].append([manhatten_dist(points[i], points[j]), i, j])
            edges[j].append([manhatten_dist(points[i], points[j]), j, i])
    
    visited[start_index] = 1
    candidate_next_edge = edges[start_index][:]

    #make edges to min-heap!!
    heapq.heapify(candidate_next_edge)

    while candidate_next_edge:
        
        dist, u, v = heapq.heappop(candidate_next_edge)#u: curr, v:next

        #1. check vertex visited, add visited & mst, update total distance sum
        if visited[v] == 0:
            visited[v] = 1
            MSTedges.append([u,v])
            calculated_sum_dist += dist

        #2. find adjacent edges, add to pq if not make circle
        for adj_edge in edges[v]:
            
            if visited[adj_edge[2]] == 0:
                #pq.push(adj_edge)
                
                heapq.heappush(candidate_next_edge, adj_edge)
    return calculated_sum_dist

def astar_four_circles(maze):
    """
    [문제 03] 제시된 stage2의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage2_heuristic function을 직접 정의하여 사용해야 한다.)
    """

    end_points=maze.circlePoints()
    end_points.sort()
    left_end_points = end_points[:]

    path=[]

    ####################### Write Your Code Here ################################
    start_point = maze.startPoint()
    start_node = Node(None, start_point)

    candidate = [start_node]
    discard = []
    object_visited_cnt = 0
    object_visited_list = [0] * len(end_points)

    while candidate:
        current_node = candidate[0]

        #find least f value node
        for node in candidate:
            if node.f < current_node.f:
                current_node = node

        candidate.remove(current_node)
        discard.append(current_node)

        #Goal check
        if maze.isObjective(current_node.location[0],current_node.location[1]):
            object_visited_list[object_visited_cnt] = 1
            object_visited_cnt += 1

        #record route when reach to one of end point.
            
            path_node = current_node
            while(path_node.parent is not None):
                path.append(path_node.location)
                t = path_node.parent
                path_node = t

        #remove visited end point, to build new MST without visited end point!!
            for end_point in left_end_points:
                if end_point == current_node.location:
                    left_end_points.remove(end_point)
                    break

            if len(left_end_points) <= 0:
                print("no left end points")
                if object_visited_cnt == len(end_points):
                    print("all end points are visited")
                    candidate.append(current_node)
                    break
            
        cur_row = current_node.location[0]
        cur_col = current_node.location[1]
        for adj in maze.neighborPoints(cur_row, cur_col):

            #at here, adj node's parent node is updated to minimum F valued node(maybe?)
            adj_node = Node(current_node, adj)

            # if adjacent node is already discarded - don't search further...
            if adj_node in discard:
                continue 

            adj_node.g = current_node.g+1
            adj_node.h = stage2_heuristic(adj,left_end_points)

            adj_node.f = adj_node.g + adj_node.h

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



# -------------------- Stage 03: Many circles - A* Algorithm -------------------- #

def mst(objectives, edges):

    MSTedges = []
    cost_sum=0
    started_index = 0

    ####################### Write Your Code Here ################################
    visited = [0] * (len(objectives)+1)
    visited[started_index] = 1
    candidate_next_edge = edges[started_index][:]
    #make (graph)edges to min-heap!!
    heapq.heapify(candidate_next_edge)

    while candidate_next_edge:
        
        #awesome python technique
        dist, u, v = heapq.heappop(candidate_next_edge)#u: curr, v:next

        #1. check vertex visited, add visited & mst, update total distance sum
        if visited[v] == 0:
            visited[v] = 1
            MSTedges.append([u,v])
            cost_sum += dist

        #2. find adjacent edges, add to pq if not make circle
        
        for adj_edge in edges[v]:
            
            if visited[adj_edge[2]] == 0:
                #pq.push(adj_edge)
                
                heapq.heappush(candidate_next_edge, adj_edge)

    return cost_sum

    ############################################################################


def stage3_heuristic(cur_point, end_points):
    #mst using prim's method
    
    MSTedges = []
    start_index = 0
    
    #num: cur:0, end_points:1,2,3,4,......many
    points = []
    points.append(cur_point)
    points.extend(end_points)
    
    #print(visited)
    #list : [distance, u, v], Graph initialization
    graph = collections.defaultdict(list)
    calculated_sum_dist = 0

    for i in range(len(points)):
        for j in range(i,len(points)):
            graph[i].append([manhatten_dist(points[i], points[j]), i, j])
            graph[j].append([manhatten_dist(points[i], points[j]), j, i])
    
    return mst(end_points, graph)


def astar_many_circles(maze):
    """
    [문제 04] 제시된 stage3의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage3_heuristic function을 직접 정의하여 사용해야 하고, minimum spanning tree
    알고리즘을 활용한 heuristic function이어야 한다.)
    """
    #######################################################
    # you can re-use function used to solve problem 03!!!!! because i already built MST-based heuristic function.
    # like this: return astar_four_circles(maze)
    end_points= maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################
    left_end_points = end_points[:]
    start_point = maze.startPoint()
    start_node = Node(None, start_point)

    candidate = [start_node]
    discard = []
    object_visited_cnt = 0
    object_visited_list = [0] * len(end_points)

    while candidate:
        current_node = candidate[0]

        #find least f value node
        for node in candidate:
            if node.f < current_node.f:
                current_node = node

        candidate.remove(current_node)
        discard.append(current_node)

        #Goal check
        if maze.isObjective(current_node.location[0],current_node.location[1]):
            object_visited_list[object_visited_cnt] = 1
            object_visited_cnt += 1

        #record route when reach to one of end point.
            
            path_node = current_node
            while(path_node.parent is not None):
                path.append(path_node.location)
                t = path_node.parent
                path_node = t

        #remove visited end point, to build new MST without visited end point!!
            for end_point in left_end_points:
                if end_point == current_node.location:
                    left_end_points.remove(end_point)
                    break

            if len(left_end_points) <= 0:
                print("no left end points")
                if object_visited_cnt == len(end_points):
                    print("all end points are visited")
                    candidate.append(current_node)
                    break
            
        cur_row = current_node.location[0]
        cur_col = current_node.location[1]
        for adj in maze.neighborPoints(cur_row, cur_col):

            #at here, adj node's parent node is updated to minimum F valued node(maybe?)
            adj_node = Node(current_node, adj)

            # if adjacent node is already discarded - don't search further...
            if adj_node in discard:
                continue 

            adj_node.g = current_node.g+1
            adj_node.h = stage2_heuristic(adj,left_end_points)

            adj_node.f = adj_node.g + adj_node.h

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
