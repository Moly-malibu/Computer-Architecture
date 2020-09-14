from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: TreeNode, desired_sum: int) -> List[List[int]]:
        # Edge cases
        if not root:
            return []
        
        # Setting up variables
        q = deque()
        q.append((root, [root.val]))
        output = []
        
        # tree traversal
        while len(q) > 0:
            # Using destructuring to label what comes off from popping
            curr_node, curr_path = q.popleft()
            
            # If at a leaf node, check to see if the sums are equal
            if not curr_node.right and not curr_node.left and sum(curr_path) == desired_sum:
                output.append(curr_path)
            
            # Add the right and left nodes to the stack
            if curr_node.right:
                path_copy = curr_path[:]
                path_copy.append(curr_node.right.val)
                q.append((curr_node.right, path_copy))
                
            if curr_node.left:
                path_copy = curr_path[:]
                path_copy.append(curr_node.left.val)
                q.append((curr_node.left, path_copy))
                
        return output