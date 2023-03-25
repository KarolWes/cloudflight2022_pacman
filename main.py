import math
import queue


def pacman1():
    for i in range(1, 6):
        f = open('level1_' + str(i) + '.in', 'r')
        n = f.readline()
        counter = 0
        for line in f:
            for char in line:
                if char == 'C':
                    counter += 1
        out = open('level1_' + str(i) + '.out', 'w')
        out.write(str(counter))
        out.close()
        print(counter)


def pacman2():
    for i in range(1, 6):
        f = open('data/level2_' + str(i) + '.in', 'r')
        n = int(f.readline())
        mapa = []
        counter = 0
        for _ in range(n):
            mapa.append(f.readline())
        y, x = map(int, f.readline().split())
        com_count = int(f.readline())
        coms = f.readline()
        print(coms)

        x -= 1
        y -= 1
        coins = []
        for let in coms:
            if let == 'U':
                y -= 1
            if let == 'D':
                y += 1
            if let == 'R':
                x += 1
            if let == 'L':
                x -= 1
            if mapa[y][x] == 'C':
                coins.append((y, x))

        set_coins = set(coins)
        ans = len(set_coins)

        out = open('data/level2_' + str(i) + '.out', 'w')
        out.write(str(ans))
        out.close()
        print(ans)


def pacman3():
    for m in range(1, 8):
        f = open('data/level3_' + str(m) + '.in', 'r')
        #f = open('data/level3_example.in', 'r')
        n = int(f.readline())
        mapa = []
        coins = []
        ghost_pos = []
        ghost_coms = []
        alive = True

        for _ in range(n):
            mapa.append(f.readline())
        y, x = map(int, f.readline().split())
        x -= 1
        y -= 1
        com_len = int(f.readline())
        coms = f.readline()
        ghosts = int(f.readline())
        ghost_pos.append([y, x])
        ghost_coms.append(coms)
        for _ in range(ghosts):
            g_y, g_x = map(int, f.readline().split())
            g_y -= 1
            g_x -= 1
            ghost_pos.append([g_y, g_x])
            _ = int(f.readline())
            ghost_coms.append(f.readline())

        for i in range(com_len):
            for j in range(ghosts + 1):
                if ghost_coms[j][i] == 'U':
                    ghost_pos[j][0] -= 1
                if ghost_coms[j][i] == 'D':
                    ghost_pos[j][0] += 1
                if ghost_coms[j][i] == 'R':
                    ghost_pos[j][1] += 1
                if ghost_coms[j][i] == 'L':
                    ghost_pos[j][1] -= 1
            for j in range(1, ghosts + 1):
                if ghost_pos[0] == ghost_pos[j]:
                    alive = False
            if not alive:
                break
            if mapa[ghost_pos[0][0]][ghost_pos[0][1]] == 'C':
                coins.append((ghost_pos[0][0], ghost_pos[0][1]))

        set_coins = set(coins)
        ans = len(set_coins)

        out = open('data/level3_' + str(m) + '.out', 'w')
        out.write(str(ans))
        out.write(' YES' if alive else ' NO')
        out.close()
        print(ans)
        print(alive)

def shortest_dist(y, x, mapa):
    visited = [[False for j in range(len(mapa))] for i in range(len(mapa))]
    stack = [[y, x]]
    p = []
    while len(stack):
        s = stack[-1]
        stack.pop()
        if not visited[s[0]][s[1]]:
            print(s, end=' ')
            p.append(s)
            visited[s[0]][s[1]] = True
        adj = []
        if mapa[s[0]][s[1]+1] != 'W' and mapa[s[0]][s[1]+1] != 'G':
            adj.append([s[0], s[1]+1])
        if mapa[s[0]][s[1] - 1] != 'W' and mapa[s[0]][s[1] - 1] != 'G':
            adj.append([s[0], s[1]-1])
        if mapa[s[0] + 1][s[1]] != 'W' and mapa[s[0] + 1][s[1]] != 'G':
            adj.append([s[0]+1, s[1]])
        if mapa[s[0] - 1][s[1]] != 'W' and mapa[s[0] - 1][s[1]] != 'G':
            adj.append([s[0]-1, s[1]])
        for node in adj:
            if not visited[node[0]][node[1]]:
                stack.append(node)

    return p

def shortest_dist_two_points(start, end, mapa):
    queue = [[start]]
    
    while queue:
        path = queue.pop(0)
        u = path[-1]
        adj = []
        if mapa[u[0]][u[1] + 1] != 'W' and mapa[u[0]][u[1] + 1] != 'G':
            adj.append([u[0], u[1] + 1])
        if mapa[u[0]][u[1] - 1] != 'W' and mapa[u[0]][u[1] - 1] != 'G':
            adj.append([u[0], u[1] - 1])
        if mapa[u[0] + 1][u[1]] != 'W' and mapa[u[0] + 1][u[1]] != 'G':
            adj.append([u[0] + 1, u[1]])
        if mapa[u[0] - 1][u[1]] != 'W' and mapa[u[0] - 1][u[1]] != 'G':
            adj.append([u[0] - 1, u[1]])
        for neighbour in adj:
            new_path = list(path)
            new_path.append(neighbour)
            queue.append(new_path)
            if neighbour == end:
                return new_path
    return

def decode(p, mapa):
    base = p[0]

    new_path = []
    for tup in p[1:]:
        x_dif = base[1] - tup[1]
        y_dif = base[0] - tup[0]
        if x_dif == 1 and y_dif == 0:
            new_path.append('L')
        elif x_dif == -1 and y_dif == 0:
            new_path.append('R')
        elif x_dif == 0 and y_dif == 1:
            new_path.append('U')
        elif x_dif == 0 and y_dif == -1:
            new_path.append('D')
        else:
            small_path = shortest_dist_two_points(base, tup, mapa)
            for coord in small_path[1:]:
                x_dif = base[1] - coord[1]
                y_dif = base[0] - coord[0]
                if x_dif == 1 and y_dif == 0:
                    new_path.append('L')
                elif x_dif == -1 and y_dif == 0:
                    new_path.append('R')
                elif x_dif == 0 and y_dif == 1:
                    new_path.append('U')
                elif x_dif == 0 and y_dif == -1:
                    new_path.append('D')
                base = coord[:]
        base = tup[:]
    # small_path = shortest_dist_two_points(p[-1], p[0], mapa)
    # for coord in small_path[1:]:
    #     x_dif = base[1] - coord[1]
    #     y_dif = base[0] - coord[0]
    #     if x_dif == 1 and y_dif == 0:
    #         new_path.append('L')
    #     elif x_dif == -1 and y_dif == 0:
    #         new_path.append('R')
    #     elif x_dif == 0 and y_dif == 1:
    #         new_path.append('U')
    #     elif x_dif == 0 and y_dif == -1:
    #         new_path.append('D')
    #     base = coord[:]
    return new_path



def pacman4():
    for i in range(1, 6):
        f = open('data/level4_' + str(i) + '.in', 'r')
        #f = open('data/level4_example.in', 'r')
        n = int(f.readline())
        mapa = []
        counter = 0
        for _ in range(n):
            mapa.append(f.readline())
        y, x = map(int, f.readline().split())
        com_count = int(f.readline())
        coms = f.readline()
        print(coms)

        x -= 1
        y -= 1


        aws_tab = decode(shortest_dist(y,x,mapa), mapa)
        ans = ''
        for el in aws_tab:
            ans += el
        print(ans)


        out = open('data/level4_' + str(i) + '.out', 'w')
        out.write(str(ans))
        out.close()
        print(ans)


def ghost_positions(ghosts, ghost_pos, ghost_coms):
    ans = []
    for i in range(ghosts):
        pos = [ghost_pos[i]]
        for j in range(len(ghost_coms[i])):
            if ghost_coms[i][j] == 'U':
                pos.append([pos[-1][0] - 1, pos[-1][1]])
            if ghost_coms[i][j] == 'D':
                pos.append([pos[-1][0] + 1, pos[-1][1]])
            if ghost_coms[i][j] == 'R':
                pos.append([pos[-1][0], pos[-1][1] + 1])
            if ghost_coms[i][j] == 'L':
                pos.append([pos[-1][0], pos[-1][1] - 1])
        for j in range(len(ghost_coms[i])-2, 0, -1):
            pos.append(pos[j])
        ans.append(pos)
    return ans



def shortest_dist_two_points_upd(start, end, mapa, ghost_maps):
    explored = []
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        u = path[-1]
        max_len = len(ghost_maps[0])
        step = (len(path))%max_len
        act_ghosts = [line[step] for line in ghost_maps]
        if u not in explored:
            adj = []
            if mapa[u[0]][u[1] + 1] != 'W' and [u[0], u[1] + 1] not in act_ghosts:
                adj.append([u[0], u[1] + 1])
            if mapa[u[0]][u[1] - 1] != 'W' and [u[0],u[1] - 1] not in act_ghosts:
                adj.append([u[0], u[1] - 1])
            if mapa[u[0] + 1][u[1]] != 'W' and [u[0] + 1,u[1]] not in act_ghosts:
                adj.append([u[0] + 1, u[1]])
            if mapa[u[0] - 1][u[1]] != 'W' and [u[0] - 1,u[1]] not in act_ghosts:
                adj.append([u[0] - 1, u[1]])
            for neighbour in adj:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == end:
                    return new_path
            explored.append(u)
    return


def pacman5():
    for m in range(1, 6):
        f = open('data/level5_' + str(m) + '.in', 'r')
        # f = open('data/level5_example.in', 'r')
        n = int(f.readline())
        mapa = []
        counter = 0
        for _ in range(n):
            mapa.append(f.readline())
        y, x = map(int, f.readline().split())

        x -= 1
        y -= 1


        for i in range(n):
            for j in range(n):
                if mapa[i][j] == 'C':
                    coin = [i, j]
        ghost_pos = []
        ghost_coms = []
        ghosts = int(f.readline())
        for _ in range(ghosts):
            g_y, g_x = map(int, f.readline().split())
            g_y -= 1
            g_x -= 1
            ghost_pos.append([g_y, g_x])
            _ = int(f.readline())
            ghost_coms.append(f.readline())
        tmp = shortest_dist_two_points_upd([y,x], coin, mapa, ghost_positions(ghosts, ghost_pos, ghost_coms))
        aws_tab = decode(tmp, mapa)
        ans = ''
        for el in aws_tab:
            ans += el
        print(ans)


        out = open('data/level5_' + str(m) + '.out', 'w')
        out.write(str(ans))
        out.close()
        print(ans)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pacman5()
