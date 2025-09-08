# Custom Queue (used only for tree construction)
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


# Build binary tree using input
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


# DFS Preorder traversal (recursive)
def dfs_preorder(root):
    result = []

    def dfs(node):
        if not node:
            return
        result.append(node.val)  # Visit root
        dfs(node.left)           # Visit left subtree
        dfs(node.right)          # Visit right subtree

    dfs(root)
    return result


# Run the build and DFS
if __name__ == "__main__":
    root = build_tree()
    print("\nDFS (Preorder) Traversal of the tree:")
    print(dfs_preorder(root))
