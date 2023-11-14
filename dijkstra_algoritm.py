#Anggota Kelompok
#FADJRI ADHA PUTRA K (1301190395)
#RAFIF ZHAFIR DHIYAUL HAQ (1301194383)
#DIAZ WAHYU BRILIAND (1301194131)

class DijkstraNodeDecorator:
    
    def __init__(self, node):
        self.node = node
        self.prov_dist = float('inf')
        self.hops = []

    def index(self):
        return self.node.index

    def data(self):
        return self.node.data
    
    def update_data(self, data):
        self.prov_dist = data['prov_dist']
        self.hops = data['hops']
        return self

class BinaryTree:

    def __init__(self, nodes = []):
        self.nodes = nodes

    def root(self):
        return self.nodes[0]
    
    def iparent(self, i):
        return (i - 1) // 2
    
    def kiri(self, i):
        return 2*i + 1

    def kanan(self, i):
        return 2*i + 2

    def left(self, i):
        return self.node_at_index(self.kiri(i))
    
    def right(self, i):
        return self.node_at_index(self.kanan(i))

    def parent(self, i):
        return self.node_at_index(self.iparent(i))

    def node_at_index(self, i):
        return self.nodes[i]

    def size(self):
        return len(self.nodes)

class MinHeap(BinaryTree):

    def __init__(self, nodes, is_less_than = lambda a,b: a < b, get_index = None, update_node = lambda node, newval: newval):
        BinaryTree.__init__(self, nodes)
        self.order_mapping = list(range(len(nodes)))
        self.is_less_than, self.get_index, self.update_node = is_less_than, get_index, update_node
        self.min_heapify()

    def min_heapify_subtree(self, i):

        size = self.size()
        kiri = self.kiri(i)
        kanan = self.kanan(i)
        imin = i
        if( kiri < size and self.is_less_than(self.nodes[kiri], self.nodes[imin])):
            imin = kiri
        if( kanan < size and self.is_less_than(self.nodes[kanan], self.nodes[imin])):
            imin = kanan
        if( imin != i):
            self.nodes[i], self.nodes[imin] = self.nodes[imin], self.nodes[i]

            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[imin])] = imin
                self.order_mapping[self.get_index(self.nodes[i])] = i
            self.min_heapify_subtree(imin)



    def min_heapify(self):
        for count in range(len(self.nodes), -1, -1):
            self.min_heapify_subtree(count)

    def min(self):
        return self.nodes[0]

    def pop(self):
        min = self.nodes[0]
        if self.size() > 1:
            self.nodes[0] = self.nodes[-1]
            self.nodes.pop()

            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[0])] = 0
            self.min_heapify_subtree(0)
        elif self.size() == 1: 
            self.nodes.pop()
        else:
            return None

        if self.get_index is not None:
            self.order_mapping[self.get_index(min)] = None
        return min

    def decrease_key(self, i, val):
        self.nodes[i] = self.update_node(self.nodes[i], val)
        iparent = self.iparent(i)
        while( i != 0 and not self.is_less_than(self.nodes[iparent], self.nodes[i])):
            self.nodes[iparent], self.nodes[i] = self.nodes[i], self.nodes[iparent]

            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[iparent])] = iparent
                self.order_mapping[self.get_index(self.nodes[i])] = i
            i = iparent
            iparent = self.iparent(i) if i > 0 else None

    def index_of_node_at(self, i):
        return self.get_index(self.nodes[i])

class Node:
  
    def __init__(self, data, indexloc = None):
        self.data = data
        self.index = indexloc

class Graph: 


    def __init__(self, nodes):
        self.adj_list = [ [node, []] for node in nodes ]
        panjang = len(nodes)
        for count in range(panjang):
            nodes[count].index = count


    def connect_dir(self, node1, node2, weight = 1):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)

        self.adj_list[node1][1].append((node2, weight))

    def connect(self, node1, node2, weight = 1):
        self.connect_dir(node1, node2, weight)
        self.connect_dir(node2, node1, weight)

    
    def connections(self, node):
        node = self.get_index_from_node(node)
        return self.adj_list[node][1]
    
    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node harus integer")
        if isinstance(node, int):
            return node
        else:
            return node.index

    def dijkstra(self, src):
        
        src_index = self.get_index_from_node(src)

        dnodes = [ DijkstraNodeDecorator(nodeedge[0]) for nodeedge in self.adj_list ]

        dnodes[src_index].prov_dist = 0
        dnodes[src_index].hops.append(dnodes[src_index].node)

        is_less_than = lambda a, b: a.prov_dist < b.prov_dist
        get_index = lambda node: node.index()
        update_node = lambda node, data: node.update_data(data)

        heap = MinHeap(dnodes, is_less_than, get_index, update_node)

        min_list = []

        while heap.size() > 0:

            min_decorated_node = heap.pop()
            min_dist = min_decorated_node.prov_dist
            hops = min_decorated_node.hops
            min_list.append([min_dist, hops])
            

            connections = self.connections(min_decorated_node.node)

            for (inode, weight) in connections: 
                node = self.adj_list[inode][0]
                heap_location = heap.order_mapping[inode]
                if(heap_location is not None):
                    tot_dist = weight + min_dist
                    if tot_dist < heap.nodes[heap_location].prov_dist:
                        hops_cpy = list(hops)
                        hops_cpy.append(node)
                        data = {'prov_dist': tot_dist, 'hops': hops_cpy}
                        heap.decrease_key(heap_location, data)

        return min_list 

a = Node('a')
b = Node('b')
c = Node('c')
d = Node('d')
e = Node('e')
f = Node('f')

tree = Graph([a,b,c,d,e,f])

tree.connect(a,b,5)
tree.connect(a,c,10)
tree.connect(a,e,2)
tree.connect(a,d,9)
tree.connect(a,f,10)
tree.connect(b,a,6)
tree.connect(b,c,2)
tree.connect(b,d,4)
tree.connect(b,e,4)
tree.connect(b,f,8)
tree.connect(c,a,7)
tree.connect(c,b,1)
tree.connect(c,d,7)
tree.connect(c,e,9)
tree.connect(c,f,10)
tree.connect(d,e,3)
tree.connect(d,a,5)
tree.connect(d,b,3)
tree.connect(d,c,8)
tree.connect(d,f,10)
tree.connect(e,a,9)
tree.connect(e,b,8)
tree.connect(e,c,5)
tree.connect(e,d,4)
tree.connect(e,f,5)
tree.connect(f,a,9)
tree.connect(f,b,5)
tree.connect(f,c,5)
tree.connect(f,d,6)
tree.connect(f,e,2)

print([(weight, [n.data for n in node]) for (weight, node) in tree.dijkstra(d)])