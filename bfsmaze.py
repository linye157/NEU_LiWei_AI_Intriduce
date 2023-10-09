import tkinter as tk
import time
import queue
import math

x0 = y0 = i = 0
my_num = 12  #正方形个数
my_width = 32  #单位方块长度
allnum = my_width * my_num
x_man=y_man=1
x_ball=5
y_ball=6

map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1],
       [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
       [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
       [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1],
       [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
       [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
       [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

class pacman:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=allnum, height=allnum, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.master = master
    def draw(self):
        for x in map:
            for y in x:
                global i
                if y:
                    self.canvas.create_rectangle(x0 + i % my_num * my_width, y0 + int(i / my_num) * my_width,
                                                 my_width + i % my_num * my_width,
                                                 my_width + int(i / my_num) * my_width,
                                                 fill='blue', outline='')
                    i += 1
                else:
                    i += 1
        self.pacman = self.canvas.create_arc(x_man * 32, y_man * 32, (x_man + 1) * 32, (y_man + 1) * 32,
                                             fill="yellow", extent=270, start=45)
        self.pacman2 = self.canvas.create_arc(x_man * 32, y_man * 32, (x_man + 1) * 32, (y_man + 1) * 32, fill="yellow", extent=340, start=10)
        self.ball = self.canvas.create_oval(x_ball * 32, y_ball * 32, (x_ball + 1) * 32, (y_ball + 1) * 32,
                                            fill="red")
    def moveto(self,i, j):
        # self.canvas.coords(self.pacman, j * 32, i * 32, (j + 1) * 32, (i + 1) * 32)
        self.canvas.itemconfig([self.pacman, self.pacman2][not i % 2], state="hidden")
        self.canvas.itemconfig([self.pacman, self.pacman2][i % 2], state="normal")
        self.canvas.moveto([self.pacman, self.pacman2][i % 2],j * 32, i * 32)
        self.master.update()
        time.sleep(0.5)

    def mark(self,i, j):
        self.canvas.create_rectangle(j * 32, i * 32, (j + 1) * 32, (i + 1) * 32, fill="red")

    def g_cost(self,x, y):
        g_cost = abs(x - x_man) + abs(y - y_man)
        return g_cost

    def f_cost(self,x, y):
        f_cost = self.g_cost(x, y) + math.sqrt(math.pow(x - y_ball, 2) + math.pow(y - x_ball, 2))
        return f_cost

    def maze_path_dfs(self, x1, y1):
        self.draw()
        maze=map
        stack = []
        stack2=[]
        stack.append([x1, y1])
        while stack:
            curNode = stack[-1]
            self.moveto(curNode[0], curNode[1])
            self.mark(curNode[0], curNode[1])
            if curNode[0] == y_ball and curNode[1] == x_ball:
                print(stack2)
                break
            flag = False
            for dir in self.dirs:
                nextNode = [0, 0]
                nextNode[0] = dir[0] + curNode[0]
                nextNode[1] = dir[1] + curNode[1]
                if maze[nextNode[0]][nextNode[1]] == 0:
                    flag = True
                    maze[nextNode[0]][nextNode[1]] = 2
                    stack.append(nextNode)
                    break
            if not flag:
                maze[nextNode[0]][nextNode[1]] = 2
                stack2.append(stack.pop())

    def maze_path_bfs(self,x1, y1):
        self.draw()
        queue = []
        allqueue = []
        maze=map
        queue.append([x1, y1])
        maze[x1][y1] = 2
        while queue:
            curNode = queue[0]
            self.moveto(curNode[0], curNode[1])
            self.mark(curNode[0], curNode[1])
            if curNode[0] == y_ball and curNode[1] == x_ball:
                print(allqueue)
                break
            flag = False
            for dir in self.dirs:
                nextNode = [0, 0]
                nextNode[0] = dir[0] + curNode[0]
                nextNode[1] = dir[1] + curNode[1]
                if maze[nextNode[0]][nextNode[1]] == 0:
                    maze[nextNode[0]][nextNode[1]] = 2
                    queue.append(nextNode)
                    flag = True
            if not flag:
                allqueue.append(queue.pop(0))

    def maze_path_usc(self,x1,y1):
        self.draw()
        q=queue.PriorityQueue()
        allq=[]
        maze=map
        q.put([0,x1,y1])
        maze[x1][y1] = 2
        while q :
            curNode=q.get()
            allq.append(curNode)
            self.moveto(curNode[1],curNode[2])
            self.mark(curNode[1],curNode[2])
            if curNode[1]==y_ball and curNode[2]==x_ball:
                print(allq)
                break
            for dir in self.dirs:
                nextNode = [0,0,0]
                nextNode[1]=dir[0]+curNode[1]
                nextNode[2]=dir[1]+curNode[2]
                if maze[nextNode[1]][nextNode[2]] == 0:
                    maze[nextNode[1]][nextNode[2]] = 2
                    nextNode[0]=self.g_cost(nextNode[1],nextNode[2])
                    q.put(nextNode)

    def maze_path_astar(self,x1, y1):
        self.draw()
        q = queue.PriorityQueue()
        maze=map
        allq = []
        q.put([0, x1, y1])
        maze[x1][y1] = 2
        while q:
            curNode = q.get()
            self.moveto(curNode[1], curNode[2])
            self.mark(curNode[1], curNode[2])
            allq.append(curNode)
            if curNode[1] == y_ball and curNode[2] == x_ball:
                print(allq)
                break
            for dir in self.dirs:
                nextNode = [0, 0, 0]
                nextNode[1] = dir[0] + curNode[1]
                nextNode[2] = dir[1] + curNode[2]
                if maze[nextNode[1]][nextNode[2]] == 0:
                    maze[nextNode[1]][nextNode[2]] = 2
                    nextNode[0] = self.f_cost(nextNode[1], nextNode[2])
                    q.put(nextNode)

def main():
    root = tk.Tk()
    root.title('实验1.1——20206470连顺')
    root.geometry(f"{allnum}x{allnum}")
    root.resizable(0, 0)
    ch=input("请选择搜索算法(1.深度优先 2.广度优先 3.一致代价 4.A*算法 其他.退出 )：")
    if ch=='1':
        pacman(root).maze_path_dfs(x_man,y_man)
        root.mainloop()
    elif ch=='2':
        pacman(root).maze_path_bfs(x_man,y_man)
        root.mainloop()
    elif ch=='3':
        pacman(root).maze_path_usc(x_man,y_man)
        root.mainloop()
    elif ch=='4':
        pacman(root).maze_path_astar(x_man,y_man)
        root.mainloop()
    else:exit(0)

if __name__ =="__main__":
    main()
