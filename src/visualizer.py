import tkinter as tk
import random
from math import sqrt

def MST(pts):
    INF = float(10**10)
    def distance(u, v):
        return sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)

    V = len(pts)
    if V <= 1:
        return 0, list()

    cost =  [[distance(pts[i], pts[j]) for i in range(V)] for j in range(V)]
    min_cost = [INF for i in range(V)]
    min_cost[0] = 0
    min_edge = [(-1,-1) for i in range(V)]
    visited = [False for i in range(V)]

    score = 0
    edges = list()
    while True:
        best_v = -1
        best_cost = INF
        for t in range(V):
            if visited[t]:
                continue
            if min_cost[t] < best_cost:
                best_v = t
                best_cost = min_cost[t]
        if best_v == -1:
            break
        visited[best_v] = True
        if best_v > 0:
            edges.append(min_edge[best_v])
        score += best_cost
        for t in range(V):
            if min_cost[t] > cost[best_v][t]:
                min_cost[t] = cost[best_v][t]
                min_edge[t] = (best_v, t)

    return score, edges


class Visualizer:
    CANVAS_WIDTH = 640
    CANVAS_HEIGHT = 480
    POINT_SIZE = 10
    NUM_OF_RED_POINTS = 5

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TCO18 MMR1 Visualizer")

        self.draw_tk_objects()

    def draw_tk_objects(self):
        """ tkオブジェクトを配置 """
        ## キャンバス
        self.canvas = tk.Canvas(self.root,
                                width=self.CANVAS_WIDTH,
                                height=self.CANVAS_HEIGHT)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.pack()
        ## フレーム1
        frm = tk.LabelFrame(self.root,
                            text='設定',
                            relief='groove',
                            borderwidth=1)
        frm.pack(fill="both")
        b = tk.Button(frm, text='再描画',width=15)
        b.bind("<Button-1>", self.draw)
        b.pack(side='left')
        b = tk.Button(frm, text='座標出力',width=15)
        b.bind("<Button-1>", self.dump)
        b.pack(side='left')
        l = tk.Label(frm, text="jc:")
        l.pack(side='left')
        self.junction_cost = tk.Entry(frm)
        self.junction_cost.insert(tk.END,"0.0")
        self.junction_cost.pack(side='left')
        ## フレーム2
        frm = tk.LabelFrame(self.root, text='モード', relief='groove', borderwidth=1)
        frm.pack(fill="both")
        self.mode_label = tk.Label(frm, text="[MOVE]")
        self.mode_label.pack(side='left')
        b = tk.Button(frm, text='追加',width=15)
        b.bind("<Button-1>", self.add_mode)
        b.pack(side='left')
        b = tk.Button(frm, text='削除',width=15)
        b.bind("<Button-1>", self.erase_mode)
        b.pack(side='left')
        b = tk.Button(frm, text='移動',width=15)
        b.bind("<Button-1>", self.move_mode)
        b.pack(side='left')
        # スコア表示
        self.score_label = tk.Label(self.root, text="0.0")
        self.score_label.pack()

    def dump(self, ev):
        """ 座標情報の出力 """
        print("#red points")
        for id in self.canvas.find_withtag("cpoint"):
            coords = self.canvas.coords(id)
            posx = int((coords[2]-coords[0])/2 + coords[0])
            posy = int((coords[3]-coords[1])/2 + coords[1])
            print(str(posx) + " " + str(posy))
        print("#blue points")
        for id in self.canvas.find_withtag("jpoint"):
            coords = self.canvas.coords(id)
            posx = int((coords[2]-coords[0])/2 + coords[0])
            posy = int((coords[3]-coords[1])/2 + coords[1])
            print(str(posx) + " " + str(posy))

    def draw_line(self):
        """ 最小全域木の辺の表示(スコア情報も更新) """
        self.canvas.delete("line")
        lst = list()
        for id in self.canvas.find_withtag("cpoint"):
            coords = self.canvas.coords(id)
            posx = int((coords[2]-coords[0])/2 + coords[0])
            posy = int((coords[3]-coords[1])/2 + coords[1])
            lst.append((posx, posy))
        for id in self.canvas.find_withtag("jpoint"):
            coords = self.canvas.coords(id)
            posx = int((coords[2]-coords[0])/2 + coords[0])
            posy = int((coords[3]-coords[1])/2 + coords[1])
            lst.append((posx, posy))
        # 最小全域木の構築
        cost, edges = MST(lst)
        # スコア情報の更新
        cost += float(self.junction_cost.get()) * len(self.canvas.find_withtag("jpoint"))
        self.score_label['text'] = str(cost)
        # 辺の描画
        for edge in edges:
            self.canvas.create_line(lst[edge[0]][0], lst[edge[0]][1],
                                    lst[edge[1]][0], lst[edge[1]][1],
                                    tag="line")
        self.canvas.tag_lower("line")

    def draw(self, ev):
        """ 赤点(cities)の描画 """
        self.erase(ev)
        for i in range(self.NUM_OF_RED_POINTS):
            x = random.randint(0, self.CANVAS_WIDTH)
            y = random.randint(0, self.CANVAS_HEIGHT)
            id = self.canvas.create_oval(x-self.POINT_SIZE/2, y-self.POINT_SIZE/2,
                                         x+self.POINT_SIZE/2, y+self.POINT_SIZE/2,
                                         fill='#ff0000', tag="cpoint")
            self.canvas.tag_bind(id, "<Button1-Motion>", lambda ev,id=id:self.move(ev, id))
        self.draw_line()

    def move(self, ev, id):
        """ クリックされたオブジェクトの移動 """
        x = ev.x
        y = ev.y
        self.canvas.coords('current',
                           x-self.POINT_SIZE/2, y-self.POINT_SIZE/2,
                           x+self.POINT_SIZE/2, y+self.POINT_SIZE/2)
        self.draw_line()

    def erase(self, ev):
        """ キャンバス内のオブジェクトを全削除 """
        self.canvas.delete("cpoint")
        self.canvas.delete("jpoint")
        self.canvas.delete("line")
        self.draw_line()

    def add_mode(self, ev):
        """ 操作モードを「追加」モードにする """
        self.mode_label['text'] = "[ADD]"

    def erase_mode(self, ev):
        """ 操作モードを「削除」モードにする """
        self.mode_label['text'] = "[ERASE]"

    def move_mode(self, ev):
        """ 操作モードを「移動」モードにする """
        self.mode_label['text'] = "[MOVE]"

    def canvas_click(self, ev):
        """ キャンバス内でクリックされた時の処理 """
        if self.mode_label['text'] == "[ADD]":
            self.add_point(ev.x, ev.y)
        if self.mode_label['text'] == "[ERASE]":
            self.canvas.delete('current')
        self.draw_line()

    def add_point(self, x, y):
        """ 青点(junctions)の追加 """
        id = self.canvas.create_oval(x-self.POINT_SIZE/2, y-self.POINT_SIZE/2,
                                     x+self.POINT_SIZE/2, y+self.POINT_SIZE/2,
                                     fill='#0000ff', tag="jpoint")
        self.canvas.tag_bind(id, "<Button1-Motion>", lambda ev,id=id:self.move(ev, id))
        self.draw_line()

    def run(self):
        self.root.mainloop()


def main():
    vis = Visualizer()
    vis.run()

if __name__ == '__main__':
    main()
