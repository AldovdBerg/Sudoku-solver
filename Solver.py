## Part3, @Aldo van der Berg

## example input
"""
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

"""


def solve(block):
  find = findEmpty(block)
  if not find:
    return True
  else:
    row, col = find
  for i in range(1,10):
    if valid(bo, i, (row, col)):
      block[row][col] = i
      if solve(block):
        return True
      block[row][col] = 0
  return False
    
def valid(block, num, pos):
  # check row
  for i in range(len(block[0])):
    if block[pos[0]][i] == num and pos[i] != i:
      return False
  # check coulumn
  for i in range(len(bo)):
    if block[i][pos[1]] == num and pos[0] != i:
      return False
  # check box
  boxX = pos[1] // 3
  boxY = pos[0] //3
  for i in range(boxY*3, boxY*3+3):
    for j in range(boxX*3, boxY*3+3):
      if block[i][j] == num and (i,j) != pos:
        return False
  return True
  
def display(block):
  for i in range(len(block)):
    if i % 3 == 0 and i != 0:
      print("- - - - - - - - -")
    for j in range(len(block[0])):
      if j % 3 == 0 and j != 0:
        print(" | ", end = "")
      if j == 8:
        print(block[i][j])
      else:
        print(str(block[i][j]) + " ", end="")  
    
   
## @Kyle Kumm
def findEmpty(block):
    for i in range(len(block)):
            for j in range(len(block[0])):
                if block[i][j] == 0:
                    return (i, j)  # row, col
        return None


