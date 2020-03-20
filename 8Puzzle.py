import argparse

class Node:

    #----- Inicializa el nodo con pattern gfunction la localización en blanco y los movimientos usados para alcanzar un estado -----#
    def __init__(self,pattern,gfunc,move='start'):
        self.pattern = pattern
        self.gfunc = gfunc
        self.move = move
        for (row,i) in zip(pattern,range(3)):
            if 0 in row:
                self.blankloc=[i,row.index(0)]
                # print(self.blankloc[0],self.blankloc[1])

    #----- Función para chequear si los estados son iguales o nodos, elemento por elemento-----#
    def __eq__(self,other):
        if other==None:
            return False

        if isinstance(other,Node)!=True:
            raise TypeError

        for i in range(3):
            for j in range(3):
                if self.pattern[i][j]!=other.pattern[i][j]:
                    return False
        return True

    #----- Función para recobrar un elemento desde un nodo, como un array -----#
    def __getitem__(self,key):
        if isinstance(key,tuple)!=True:
            raise TypeError
        if len(key)!=2:
            raise KeyError

        return self.pattern[key[0]][key[1]]

    #----- Función para calcular hfunction acorde a la meta designada -----#

    def calc_hfunc(self,goal):
        self.hfunc = 0
        for i in range(3):
            for j in range(3):
                # print (i,j)
                if self.pattern[i][j]!=goal.pattern[i][j]:
                    self.hfunc+=1
        if self.blankloc != goal.blankloc:
            self.hfunc-=1   #Remueve un contador si la localización en blanco es desplazada debido al sobreestimo de la meta

        self.ffunc=self.hfunc+self.gfunc

        return self.hfunc,self.gfunc,self.ffunc

    #----- Función para mover el cuadro en blanco hacia la izquierda, de ser posible -----#
    def moveleft(self):
        if self.blankloc[1]==0:
            return None

        left = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
        left[self.blankloc[0]][self.blankloc[1]]=left[self.blankloc[0]][self.blankloc[1]-1]
        left[self.blankloc[0]][self.blankloc[1]-1]=0

        return Node(left,self.gfunc+1,'left')

    #----- Función para mover el cuadro en blanco hacia la derecha, de ser posible -----#
    def moveright(self):
        if self.blankloc[1]==2:
            return None

        right = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
        right[self.blankloc[0]][self.blankloc[1]]=right[self.blankloc[0]][self.blankloc[1]+1]
        right[self.blankloc[0]][self.blankloc[1]+1]=0

        return Node(right,self.gfunc+1,'right')

    #----- Función para mover el cuadro en blanco hacia arriba, de ser posible -----#
    def moveup(self):
        if self.blankloc[0]==0:
            return None

        up = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
        up[self.blankloc[0]][self.blankloc[1]]=up[self.blankloc[0]-1][self.blankloc[1]]
        up[self.blankloc[0]-1][self.blankloc[1]]=0

        return Node(up,self.gfunc+1,'up')

    #----- Función para mover el cuadro en blanco hacia abajo, de ser posible -----#
    def movedown(self):
        if self.blankloc[0]==2:
            return None

        down = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
        down[self.blankloc[0]][self.blankloc[1]]=down[self.blankloc[0]+1][self.blankloc[1]]
        down[self.blankloc[0]+1][self.blankloc[1]]=0

        return Node(down,self.gfunc+1,'down')

    #----- Función para verificar y realizar todos los movimientos de acuerdo con la posibilidad y si el próximo movimiento está cerca o no -----#
    #----- cierra el nodo actual y todos los demás para poder abrir una lista -----#
    def moveall(self,game):
        left = self.moveleft()
        left = None if game.isclosed(left) else left
        right = self.moveright()
        right = None if game.isclosed(right) else right
        up = self.moveup()
        up = None if game.isclosed(up) else up
        down = self.movedown()
        down = None if game.isclosed(down) else down

        game.closeNode(self)
        game.openNode(left)
        game.openNode(right)
        game.openNode(up)
        game.openNode(down)

        return left,right,up,down

    #----- Función para imprimir el array -----#
    def print(self):
        print(self.move+str(self.gfunc))
        print(self.pattern[0])
        print(self.pattern[1])
        print(self.pattern[2])

class Game:

    #---- Inicializa el nodo con Inicio (start), Meta (goal), Una tabla con los nodos abiertos, Una tabla con los nodos cerrados y agrega el Inicio a un nodo cerrado ----#
    #---- Los nodos abiertos son una tabla basada en la función 'f function' Y los nodos cerrados son una tabla basada en la función 'h function' ----#
    def __init__(self,start,goal):    
        self.start = start
        self.goal = goal
        self.open = {}
        self.closed = {}
        _,_,ffunc = self.start.calc_hfunc(self.goal)
        self.open[ffunc] = [start]

    #---- Función para comprobar si el estado del nodo es cerrado o no ----#
    def isclosed(self,node):
        if node==None:  #retorna True si no hay nodo
            return True

        hfunc,_,_ = node.calc_hfunc(self.goal) #Calcula hfucntion para revisar en la tabla

        if hfunc in self.closed:
            for x in self.closed[hfunc]:
                if x==node:
                    return True

        return False

    #---- Función para agregar un nodo a la lista de cerrados y eliminarlo de la lista de nodos abiertos ----#
    def closeNode(self,node):
        if node==None:		#return back if no node
            return

        hfunc,_,ffunc= node.calc_hfunc(self.goal)
        self.open[ffunc].remove(node)   #Remueve de la lista ffunction para los nodos abiertos
        if len(self.open[ffunc])==0:
            del self.open[ffunc]    #Remueve el atributo para ffunction si su lista está vacía

        if hfunc in self.closed:
            self.closed[hfunc].append(node)
        else:
            self.closed[hfunc] = [node]

        return

    #---- Función para agregar un nodo a la lista de abiertos después de inicializarlos ----#
    def openNode(self,node):
        if node==None:
            return

        _,_,ffunc = node.calc_hfunc(self.goal)  #Calcula ffucntion para agregarlo a la lista de nodos que ffucntion agregó a la tabla
        if ffunc in self.open:
            self.open[ffunc].append(node)
        else:
            self.open[ffunc] = [node]

        return

    #---- Función para resolver el puzzle usando el algoritmo A* ----#
    def solve(self):

        presentNode = None

        while(presentNode!=self.goal):
            i=0
            while i not in self.open:
                i+=1                        #Busca en la lista lo que esté realcionado a 'ffunction' para tomar un nodo de esa lista
            presentNode = self.open[i][-1]
            presentNode.moveall(self)       #Expande ese nodo hacia nuevos posibles movimientos

    #---- Imprime la solución en dirección inversa desde la meta hacia el inicio ----#
        while presentNode.move!='start':
            presentNode.print()
            # do reverse move that what was done to reach the state to backtrack along the solution
            if presentNode.move == 'up':
                presentNode = presentNode.movedown()
            elif presentNode.move == 'down':
                presentNode = presentNode.moveup()
            elif presentNode.move == 'right':
                presentNode = presentNode.moveleft()
            elif presentNode.move == 'left':
                presentNode = presentNode.moveright()

            hfunc,_,_ = presentNode.calc_hfunc(self.goal)
            for i in self.closed[hfunc]:
                if i==presentNode:
                    presentNode = i

        return


if __name__ == '__main__':

    #----- Argumentos -----#
    parser = argparse.ArgumentParser()
    # parser.add_argument("--hfunc",help='Escoge 1 para la distancia Manhattan y 2 los Cuadros desplazados.',metavar='Heuristic Function', default='1')
    parser.add_argument("--startrow",help='Inicia los numeros en secuencia para el estado de inicio desde la fila 1 a la fila 3, separados por espacios (escribe 0 para el espacio en blanco).',type=int, nargs=9, metavar=('row1col1', 'row1col2', 'row1col3','row2col1','row2col2','row2col3','row3col1','row3col2','row3col3'), required=True)
    parser.add_argument("--goalrow",help='Inicia los numeros en secuencia para la meta desde la fila 1 a la fila 3, separados por espacios (escribe 0 para el espacio en blanco).',type=int, nargs=9, metavar=('row1col1','row1col2','row1col3','row2col1','row2col2','row2col3','row3col1','row3col2','row3col3'), required=True)

    args = parser.parse_args()

    x = [1,2,3,4,5,6,7,8,0]

    #----- Acepta si la entrada es correcta -----#

    assert set(x)==set(args.startrow)
    assert set(x)==set(args.goalrow)

    #----- Reformatea la entrada -----#

    startloc = [args.startrow[0:3],args.startrow[3:6],args.startrow[6:]]
    goalloc = [args.goalrow[0:3],args.goalrow[3:6],args.goalrow[6:]]

    #----- Inicializa el nodo de inicio y el nodo final -----#

    start = Node(startloc,0)
    goal = Node(goalloc,0,'goal')

    #----- Inicializa el puzzle -----#

    game = Game(start, goal)
    game.solve() #Solve Game