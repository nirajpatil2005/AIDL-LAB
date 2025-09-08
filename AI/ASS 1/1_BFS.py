# Custom Queue (simple FIFO using list with manual indexing)
class Queue:
    def __init__(self):
        self.items = []
        self.front_index = 0

    def is_empty(self):
        return self.front_index >= len(self.items)

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty.")
            return None
        item = self.items[self.front_index]
        self.front_index += 1
        return item


# Tree Node class
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# Build tree from user input using level-order traversal
def build_tree():
    root_val = int(input("Enter root node value: "))
    if root_val == -1:
        return None

    root = TreeNode(root_val)
    queue = Queue()
    queue.enqueue(root)

    while not queue.is_empty():
        current = queue.dequeue()

        print(f"\nEnter children for node {current.val}:")
        left_val = int(input("Left child (-1 for None): "))
        right_val = int(input("Right child (-1 for None): "))

        if left_val != -1:
            current.left = TreeNode(left_val)
            queue.enqueue(current.left)

        if right_val != -1:
            current.right = TreeNode(right_val)
            queue.enqueue(current.right)

    return root


# BFS traversal using custom Queue
def bfs_traversal(root):
    if not root:
        return []

    result = []
    queue = Queue()
    queue.enqueue(root)

    while not queue.is_empty():
        node = queue.dequeue()
        result.append(node.val)

        if node.left:
            queue.enqueue(node.left)
        if node.right:
            queue.enqueue(node.right)

    return result


# Run the tree building and BFS
if __name__ == "__main__":
    root = build_tree()
    print("\nBFS Traversal of the tree:")
    print(bfs_traversal(root))
