'''

Erweitere die Implementierung der Klasse für gerichtete Graphen um eine
Mehode, die die Knoten des Graphen topologisch sortiert und in einer
Liste zurückgibt. Der Graph soll durch den Aufruf der Methode nicht
verändert werden! Achte darauf, dass die Methode auch für zyklische 
Graphen nicht in eine Endlosschleife gerät. [3 Punkte]

'''

from collections import defaultdict, deque

from random import randint

with open("names.txt") as f:
    namen = [l.strip() for l in f.readlines()]


class DirectedGraph:
    def __init__(self):
        self.matrix = defaultdict(set)
    def add_edge(self, src, tgt):
        self.matrix[src].add(tgt)
    def has_edge(self, src, tgt):
        return tgt in self.matrix[src]
    def edges(self):
        l =  []
        for k in self.matrix.keys():
            for t in self.matrix[k]:
                l.append((k,t))
        return l
    def nodes(self):
        s = set(self.matrix)
        for x in self.matrix.values():
            s.update(x)
        return s
    def indeg(self, node):
        count = 0
        for out in self.matrix.values():
            if node in out:
                count += 1
        return count
    def outdeg(self, node):
        return len(self.matrix[node])
    def neighbors(self, node):
        return self.matrix[node]

    def namedcopy(self):
        if len(self.nodes())>len(namen):
            raise Exception #zu viele Knoten.
        namen_ = list(namen)
        matr = defaultdict(set)
        assign = dict()
        for (node,val) in self.matrix.items():

            if node not in assign:
                name = namen_.pop(randint(0,len(namen_)-1))
                assign[node] = name
            m = set()
            for e in val:
                if e in assign:
                    m.add(assign[e])
                else:
                    name = namen_.pop(randint(0,len(namen_)-1))
                    assign[e] = name
                    m.add(name)
            matr[assign[node]] = m
        g = DirectedGraph()
        g.matrix = matr
        return g
    
    def has_cycle(self):
        stack = list(self.nodes())
        visited = set()
        done = set()
        while len(stack)>0:
            current = stack.pop()
            if current in visited:
                return True
            visited.add(current)
            if len(self.neighbors(current) - done)==0:
                done.update(visited)
                visited = set()
            stack.extend(self.neighbors(current)-done)
        return False
    
    def dfs(self, node):
        stack = [node]
        done = set()
        while len(stack)>0:
            current = stack.pop()
          #  print("visited",current)
            if current in done:
                continue
            done.add(current)
            yield current
            stack.extend(self.neighbors(current))
            
    def bfs(self, node):
        que = deque([node])
        done = set()
        while len(que)>0:
            current = que.popleft()
           # print("visited",current)
            if current in done:
                continue
            done.add(current)
            yield current
            que.extend(self.neighbors(current))

    def indegs(self):
        indegs = {x:0 for x in self.matrix.keys()}
        for out in self.matrix.values():
             for node in out:
                 indegs[node] = 1 + indegs.get(node,0)
        return indegs
    # Topologische Sortierung
    def tsort(self):
        if self.has_cycle():
            return None
        d = self.indegs()
        result = []
        removed = 0
        while removed<len(d):
            for node, indeg in d.items():
                if node and indeg == 0:
                    removed +=1
                    result.append(node)
                    d[node] = None
                    for child in self.neighbors(node):
                        d[child] -=1
        return result

    def fairytale(self):
        l = deque(self.tsort())
        tale = "Es war einmal "+ str(l[0])
        while len(l)>0:
            current = l.popleft()
            kinder = list(self.matrix[current])
            if self.outdeg(current) == 0:
                tale += " und "+str(current)+" starb kinderlos"
            if self.outdeg(current) == 1:
                tale +=" und "+str(current) +" hatte ein Kind, nämlich "+str(kinder[0])
            elif self.outdeg(current) > 1:
                tale +=" und "+str(current) +" hatte " + str(self.outdeg(current))+" Kinder, nämlich "
                for i in range(0,len(kinder)-1):
                    tale += str(kinder[i]) + ","
                tale= tale[:-1] +" und "+str(kinder[-1])
            
        return tale+"."

g = DirectedGraph()
g.add_edge(1,2)
g.add_edge(2,4)
g.add_edge(2,3)
g.add_edge(3,4)

n = g.namedcopy()



