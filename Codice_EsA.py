from random import random
from timeit import default_timer
import sys
import numpy as np
import matplotlib.pyplot as plt




sys.setrecursionlimit(2**16)




def generate_random_iterable(stop):
    for i in range(stop):
        yield random()




def test_execution_time_tree(tree_classes):
    result = []
    
    print('random order')
    result.append(test(tree_classes, generate_random_iterable))
    
    print('ordered insert')
    result.append(test(tree_classes, range))
    
    return result

def test(tree_classes, generate_function):
    n = 1
    sizes = np.array([])
    heights = np.empty((len(tree_classes), 0))
    max_time = 0
    if generate_function == range:
        num_tests = 1
    else:
        num_tests = 8 # can be changed
    while max_time < 8: # can be changed
        n *= 2
        sizes.resize(sizes.size+1)
        sizes[-1] = n
        heights = np.hstack((heights, np.zeros((heights.shape[0], 1))))
        time_n = -default_timer()
        for k in range(num_tests):
            time = -default_timer()
            T = [tree_class() for tree_class in tree_classes]
            for i in generate_function(n):
                for j in range(len(tree_classes)):
                    T[j].insert(i)
            for j in range(len(tree_classes)):
                heights[j, -1] += T[j].get_height()
            time += default_timer()
            if time > max_time:
                max_time = time
        for j in range(len(tree_classes)):
            heights[j, -1] /= num_tests
        print(f'    n = {n}')
    return sizes, heights




class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.p = None

class ABR:
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        z = Node(key)
        self.insert_node(z)
    
    def insert_node(self, z):
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
    
    def get_height(self):
        return self.get_node_height(self.root)
    
    def get_node_height(self, x):
        if x is None:
            return 0
        else:
            return 1+max(self.get_node_height(x.left), self.get_node_height(x.right))
    
    def search(self, key):
        x = self.root
        while x is not None and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x
    
    def inorder(self):
        def _inorder(v):
            if v is None:
                return
            _inorder(v.left)
            print(v.key)
            _inorder(v.right)
        _inorder(self.root)




class RNNode(Node):
    def __init__(self, key, color='RED'):
        Node.__init__(self, key)
        self.color = color

class ARN(ABR):
    
    def insert(self, key):
        z = RNNode(key)
        self.insert_node(z)
        self.RN_insert_fixup(z)
    
    def RN_insert_fixup(self, z):
        
        def left_rotate(self, x):
            y = x.right
            x.right = y.left
            if y.left != None:
                y.left.p = x
            y.p = x.p
            if x.p == None:
                self.root = y
            elif x == x.p.left:
                x.p.left = y
            else:
                x.p.right = y
            y.left = x
            x.p = y
        
        def right_rotate(self, x):
            y = x.left
            x.left = y.right
            if y.right != None:
                y.right.p = x
            y.p = x.p
            if x.p == None:
                self.root = y
            elif x == x.p.right:
                x.p.right = y
            else:
                x.p.left = y
            y.right = x
            x.p = y
        
        while z.p is not None and z.p.color == 'RED':
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y is not None and y.color == 'RED':
                    z.p.color = 'BLACK'
                    y.color = 'BLACK'
                    z.p.p.color = 'RED'
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        left_rotate(self, z)
                    z.p.color = 'BLACK'
                    z.p.p.color = 'RED'
                    right_rotate(self, z.p.p)
            else:
                y = z.p.p.left
                if y is not None and y.color == 'RED':
                    z.p.color = 'BLACK'
                    y.color = 'BLACK'
                    z.p.p.color = 'RED'
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        right_rotate(self, z)
                    z.p.color = 'BLACK'
                    z.p.p.color = 'RED'
                    left_rotate(self, z.p.p)
        self.root.color = 'BLACK'




test = test_execution_time_tree((ABR, ARN))




def plot(test, labels, funcs):
    for i in range(len(test)):
        plt.figure(i+1)
        x = np.logspace(1, np.log2(test[i][0][-1]), num=np.log2(test[i][0][-1]), base=2)
        for j in range(len(test[i][1])):
            plt.plot(test[i][0], test[i][1][j], label=labels[j])
            coeff = test[i][1][j][-1] / funcs[j][i](x[-1])
            y = funcs[j][i](x) * coeff
            plt.plot(x, y, 'k--')

def end_plot(n):
    for i in range(n):
        plt.figure(i+1)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('tree size')
        plt.ylabel('tree height')
        plt.legend()

labels = ('binary search tree', 'red-black tree')

br_funcs = (lambda x: np.log(x), lambda x: x)
rn_funcs = (lambda x: np.log(x), lambda x: np.log(x))
funcs = (br_funcs, rn_funcs)

plot(test, labels, funcs)

end_plot(len(test))
