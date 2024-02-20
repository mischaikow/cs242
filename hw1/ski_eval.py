

class Node:
  def __init__(self, val, left=None, right=None) -> None:
    self.val = val
    self.left = left
    self.right = right

  def reduce(self):
    if self.left.val == 'I':
      self.val = self.right.val
      self.left = None
      self.right = None
    return self

  def print_flat(self):
    return ''

  def print_tree(self):
    print(self.val)
    if self.left:
      self.left.print_tree()
    if self.right:
      self.right.print_tree()


def eval(exp):
  eval_tree = build_tree(exp);
  #eval_tree.print_tree()
  eval_tree.reduce()
  eval_tree.print_flat()
  return exp


def build_tree(exp):
  root = Node(exp)
  stack = [root]
  while stack:
    node = stack.pop()
    split_1, split_2 = split_exp(node.val.strip())
    node.val = None
    node.left = Node(split_1)
    if len(split_1) > 1:
      stack.append(node.left)
    node.right = Node(split_2)
    if len(split_2) > 1:
      stack.append(node.right)
  return root


def split_exp(value):
  if value[-1] == ')':
    depth = 1
    for i in range(len(value)-2, -1, -1):
      if value[i] == ')':
        depth += 1
      elif value[i] == '(':
        depth -= 1

      if depth == 0:
        if i == 0:
          return split_exp(value[1:-1])
        else:
          return value[:i], value[i+1:-1]
  else:
    return value[:-2], value[-1]


def file_reader(file_name):
  input_file = open(file_name, 'r')
  inputs_raw = input_file.readlines()
  for i in range(len(inputs_raw)):
    inputs_raw[i] = inputs_raw[i].replace('\n', '')
  return inputs_raw

eval('S x y z')
eval('((S K) (K x))(S y)')
eval('(((S K) (K x))(S y))')