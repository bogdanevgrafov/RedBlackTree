import random
import time

RED = True
BLACK = False


class Node:
    def __init__(self, key):
        self.key = key
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.NIL = Node(0)
        self.NIL.color = BLACK
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = None

        self.root = self.NIL
        self.ops = 0

    def reset_ops(self):
        self.ops = 0

    def left_rotate(self, x):
        y = x.right
        self.ops += 1

        x.right = y.left
        self.ops += 1
        if y.left != self.NIL:
            y.left.parent = x
            self.ops += 1

        y.parent = x.parent
        self.ops += 1
        if x.parent is None:
            self.root = y
            self.ops += 1
        elif x == x.parent.left:
            x.parent.left = y
            self.ops += 1
        else:
            x.parent.right = y
            self.ops += 1

        y.left = x
        x.parent = y
        self.ops += 2

    def right_rotate(self, x):
        y = x.left
        self.ops += 1

        x.left = y.right
        self.ops += 1
        if y.right != self.NIL:
            y.right.parent = x
            self.ops += 1

        y.parent = x.parent
        self.ops += 1
        if x.parent is None:
            self.root = y
            self.ops += 1
        elif x == x.parent.right:
            x.parent.right = y
            self.ops += 1
        else:
            x.parent.left = y
            self.ops += 1

        y.right = x
        x.parent = y
        self.ops += 2

    def insert(self, key):
        self.reset_ops()
        start = time.perf_counter()

        node = Node(key)
        node.color = RED
        node.left = self.NIL
        node.right = self.NIL

        y = None
        x = self.root

        while x != self.NIL:
            self.ops += 1
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
            self.ops += 1
        elif node.key < y.key:
            y.left = node
            self.ops += 1
        else:
            y.right = node
            self.ops += 1

        self.fix_insert(node)
        return self.ops, time.perf_counter() - start

    def fix_insert(self, k):
        while k.parent is not None and k.parent.color == RED:
            self.ops += 1
            gp = k.parent.parent

            if k.parent == gp.left:
                u = gp.right
                self.ops += 1

                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    gp.color = RED
                    k = gp
                    self.ops += 3
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                        self.ops += 1

                    k.parent.color = BLACK
                    gp.color = RED
                    self.right_rotate(gp)
                    self.ops += 2
            else:
                u = gp.left
                self.ops += 1

                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    gp.color = RED
                    k = gp
                    self.ops += 3
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                        self.ops += 1

                    k.parent.color = BLACK
                    gp.color = RED
                    self.left_rotate(gp)
                    self.ops += 2

        self.root.color = BLACK
        self.ops += 1

    def search(self, key):
        self.reset_ops()
        start = time.perf_counter()

        current = self.root
        while current != self.NIL:
            self.ops += 1
            if key == current.key:
                return current, self.ops, time.perf_counter() - start
            if key < current.key:
                current = current.left
            else:
                current = current.right

        return None, self.ops, time.perf_counter() - start

    def delete(self, key):
        self.reset_ops()
        start = time.perf_counter()

        z = self.root
        while z != self.NIL:
            self.ops += 1
            if key == z.key:
                break
            if key < z.key:
                z = z.left
            else:
                z = z.right

        if z == self.NIL:
            return self.ops, time.perf_counter() - start

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
            self.ops += 1
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
            self.ops += 1
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            self.ops += 1

            if y.parent == z:
                x.parent = y
                self.ops += 1
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                self.ops += 2

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            self.ops += 3

        if y_original_color == BLACK:
            self.fix_delete(x)
            self.ops += 1

        return self.ops, time.perf_counter() - start

    def fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            self.ops += 1

            if x == x.parent.left:
                s = x.parent.right

                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    s = x.parent.right
                    self.ops += 3

                if s.left.color == BLACK and s.right.color == BLACK:
                    s.color = RED
                    x = x.parent
                    self.ops += 2
                else:
                    if s.right.color == BLACK:
                        s.left.color = BLACK
                        s.color = RED
                        self.right_rotate(s)
                        s = x.parent.right
                        self.ops += 4

                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
                    self.ops += 5
            else:
                s = x.parent.left

                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    s = x.parent.left
                    self.ops += 3

                if s.right.color == BLACK and s.left.color == BLACK:
                    s.color = RED
                    x = x.parent
                    self.ops += 2
                else:
                    if s.left.color == BLACK:
                        s.right.color = BLACK
                        s.color = RED
                        self.left_rotate(s)
                        s = x.parent.left
                        self.ops += 4

                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
                    self.ops += 5

        x.color = BLACK
        self.ops += 1

    def transplant(self, u, v):
        self.ops += 1
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
            self.ops += 1
        else:
            u.parent.right = v
            self.ops += 1
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
            self.ops += 1
        return node


def run_experiment():
    tree = RBTree()
    data = random.sample(range(1_000_000), 10_000)

    insert_ops = 0
    insert_time = 0.0
    for x in data:
        ops, t = tree.insert(x)
        insert_ops += ops
        insert_time += t

    avg_insert_ops = insert_ops / len(data)
    avg_insert_time = insert_time / len(data)

    search_sample = random.sample(data, 100)
    search_ops = 0
    search_time = 0.0
    for x in search_sample:
        _, ops, t = tree.search(x)
        search_ops += ops
        search_time += t

    avg_search_ops = search_ops / len(search_sample)
    avg_search_time = search_time / len(search_sample)

    delete_sample = random.sample(data, 1000)
    delete_ops = 0
    delete_time = 0.0
    for x in delete_sample:
        ops, t = tree.delete(x)
        delete_ops += ops
        delete_time += t

    avg_delete_ops = delete_ops / len(delete_sample)
    avg_delete_time = delete_time / len(delete_sample)

    print("INSERT:")
    print(f"  avg ops: {avg_insert_ops:.2f}")
    print(f"  avg time: {avg_insert_time:.6f}")

    print("\nSEARCH:")
    print(f"  avg ops: {avg_search_ops:.2f}")
    print(f"  avg time: {avg_search_time:.6f}")

    print("\nDELETE:")
    print(f"  avg ops: {avg_delete_ops:.2f}")
    print(f"  avg time: {avg_delete_time:.6f}")

if __name__ == "__main__":
    run_experiment()