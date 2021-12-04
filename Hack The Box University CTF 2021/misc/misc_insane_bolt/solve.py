from collections import deque
import re
import time

from pwn import *

fire = "🔥"
gem = "💎"
nut = "🔩"
robot = "🤖"
skull = "☠️"


def build_graph(grid):
    graph = {}
    max_row = len(grid)
    max_col = len(grid[0])
    
    for y, row in enumerate(grid):
        for x, el in enumerate(row):
            if el == robot:
                start = (x, y)
            if el == gem:
                end = (x, y)

            adj = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
            adj = [(x, y) for x, y in adj if x>=0 and x<max_col and y>=0 and y<max_row]
            adj = [(x, y) for x, y in adj if grid[y][x] == nut or grid[y][x] == gem]
            graph[(x, y)] = adj
    
    return start, end, graph


def bfs(start, end, graph):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        s, path = queue.popleft() 
        visited.add(s)

        for adj in graph[s]:
            if adj == end:
                return path + [adj]

            if adj not in visited:
                queue.append((adj, path + [adj]))


def convert_to_dlr(path):
    output = []
    for p1, p2 in zip(path, path[1:]):
        if p1[1] == p2[1]:
            if p1[0] > p2[0]:
                output.append("L")
            else:
                output.append("R")
        else:
            output.append("D")

    return "".join(output)


io = remote("64.227.40.93", 32584)
io.recv()
io.sendline(b"2")

for i in range(500):
    idx = 3 if i > 0 else 1

    grid = io.recv().decode().split("\n")
    print(f"Round {i}:")
    print("\n".join(grid[:2]) + "\n")
    grid = [re.split("\s+", line) for line in grid[idx:-2]] 

    start, end, graph = build_graph(grid)
    path = bfs(start, end, graph)
    res = convert_to_dlr(path)

    io.sendline(res.encode())
    time.sleep(0.15)

io.interactive()
