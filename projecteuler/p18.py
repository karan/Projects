from Queue import PriorityQueue

def getval(coords):
    return grid[coords[0]][coords[1]]

fin = open('p18.in', 'r')
grid = [line.split(" ") for line in fin.read().split("\n")][:-1]
grid = [map(int, line) for line in grid]

q = PriorityQueue()
q.put([-grid[0][0],(0,0)])
while not q.empty():
    node = q.get()
    print node
    if node[1][0] == len(grid)-1:
        print node
        break
    else:
        for o in range(2):
            q.put([node[0]-grid[node[1][0]+1][node[1][1]+o],(node[1][0]+1,node[1][1]+o)])
