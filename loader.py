import csv

class Cell:
  'Class for our cell should contain a value and a bool'
  def __init__ (self, value):
    self.value = value 
    self.visited = False



class Labyrinth:
  'Class for our labyrinth data structure'
  def __init__(self, seed, width, height, entrance, exit, maze):
    self.seed = seed
    self.width = width
    self.height = height
    self.entrance = entrance
    self.exit = exit
    self.maze = maze
    
  def showLab(self):
    print (f"Lab has seed {self.seed}")
    print(f"The height is {self.height} the width is {self.width}")
    print (f"The lab entrance is located at {self.entrance}")
    print (f"The lab exit is located at {self.exit}")    
    for i, sublist in enumerate(self.maze):
     for j, item in enumerate(sublist):
        print(f"{item.value}")
        #print(f"The bool located at [{i}][{j}] is {item.visited}")

  def __getitem__(self, index):
        return self.maze[index]

  
def load_prop(fileName):
    with open(fileName) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=" ")
      line_count = 0
      maze = []

      for row in csv_reader:
        if line_count == 0:
          print ("First line of the file is the seed")
          print (row)
          line_count += 1
          seed = int(row[0])
          print (seed)
        elif line_count == 1:
          print(row)
          print(f"The height is {row[0]} the width is {row[1]}")
          height = int(row[0])
          width = int(row[1])
          line_count += 1
        elif line_count == 2:
          print (row)
          entrance = int(row[0])
          exit = int(row[1])
          line_count += 1
        else:
          #print ("Time to load the cells")
          rowList = []
          #print (row)
          values = row[0].split(',')
          for value in values:
            newCell = Cell(value) 
            #print (value)
            rowList.append(newCell)
          maze.append(rowList)

    return seed, height, width, entrance, exit, maze

def number_to_walls(number):
  mask = 15
  extract = number&mask
  return format(int(bin(extract)[2:],2),'04b')
   

def dfs(maze,startrow,startcol):
  global solutionRute
 
  if startcol == (maze.exit-1) and startrow == (len(maze.maze)-1):
    print(f"Exit found at [{(len(maze.maze)-1)}][{(maze.exit-1)}]")
    maze[startrow][startcol].visited = True
    #solutionRute = generateSolution(maze)
    print(solutionRute)
    return True #we found the exit
  
  if (maze[startrow])[startcol].visited:
    print('Weve been here, stopping')
    return False #We already been here
  
  maze[startrow][startcol].visited = True
  solutionRute.append((startrow,startcol))
  print(f"The value of [{startrow}][{startcol}] is {(maze[startrow][startcol].value)} and the boolean is {maze[startrow][startcol].visited}")
  walls = number_to_walls(int(maze.maze[startrow][startcol].value))

  if int(walls[0]) == 0 and maze.maze[startrow][startcol-1].visited == False:
    print(startrow,startcol)
    print("Going West")
    if dfs(maze, startrow, startcol-1):
      return True
  if int(walls[1]) != 1 and maze.maze[startrow][startcol+1].visited == False:
    print(startrow,startcol)
    print("Going East")
    if dfs(maze, startrow, startcol+1):
      return True
  if int(walls[2]) != 1 and maze.maze[startrow+1][startcol].visited == False:
    print(startrow,startcol)
    print("Going South")
    if dfs(maze, startrow+1, startcol):
      return True
  if int(walls[3]) != 1 and maze.maze[startrow-1][startcol].visited == False:
    print(startrow,startcol)
    print("Going North")
    if dfs(maze, startrow-1, startcol):
      return True
  '''  
  found = dfs(maze, startrow+1, startcol) or \
          dfs(maze, startrow, startcol-1) or \
          dfs(maze, startrow, startcol+1) or \
          dfs(maze, startrow-1, startcol)
  return found
  '''
  return False

def pruneMaze(maze):
  count = 0
  print("initiating pruning")
  for rowCounter,row in enumerate(maze.maze):
    for colCounter, cell in enumerate(row):
      if int(cell.value) == 7:
        cell.value = 15
        maze.maze[rowCounter][colCounter-1].value = int(maze.maze[rowCounter][colCounter-1].value)+4    
        count = count + 1
      if int(cell.value) == 11:
        cell.value = 15
        maze.maze[rowCounter][colCounter+1].value = int(maze.maze[rowCounter][colCounter+1].value)+8    
        count = count + 1 
      if int(cell.value) == 13:
        cell.value = 15
        maze.maze[rowCounter+1][colCounter].value = int(maze.maze[rowCounter+1][colCounter].value)+1    
        count = count + 1 
      if int(cell.value) == 14:
        cell.value = 15
        maze.maze[rowCounter-1][colCounter].value = int(maze.maze[rowCounter-1][colCounter].value)+2    
        count = count + 1 
  while count:
    print(f"Pruning complete. # of nodes pruned {count}")
    count = pruneMaze(maze)
  
  return count

def iterativ_dfs(maze, row, col):
  solutions = []
  stack = []
  startrow = 0
  startcol = maze.entrance-1
  goalrow = maze.height-1
  goalcol = maze.exit-1
  stack.append((startrow,startcol,'start'))
  solutions.append((startrow,startcol,'start'))
  print(f"initiating iterative dfs with entrance [0][{startcol}] and exit [{goalrow}][{goalcol}]")
  #modify startnode to wall north off
  maze.maze[startrow][startcol].value = int(maze.maze[startrow][startcol].value)+1
  while stack:
    row,col, direction = stack.pop()
    print(f"Entering row {row} col {col}")
    cell = maze.maze[row][col]
    if cell.visited != True:
      cell.visited = True
      #solutions.append((row,col,direction))
      if row == goalrow and col ==  goalcol:
        print("Congratulations you found the exit")
        solutions.append((row,col,'exit'))
        return solutions
      walls = number_to_walls(int(maze.maze[row][col].value))
      print(walls)
      if int(walls[0]) == 0:
        solutions.append((row,col,direction))
        stack.append((row,col-1,'west'))
      if int(walls[1]) == 0:
        solutions.append((row,col,direction))        
        stack.append((row,col+1,'east'))
      if int(walls[2]) == 0:
        solutions.append((row,col,direction))
        stack.append((row+1,col,'south'))
      if int(walls[3]) == 0:
        solutions.append((row,col,direction))
        stack.append((row-1,col,'north'))
      solutions.remove((row,col,direction))

def generateSolution(maze):
  solution = []
  for row in maze.maze:
    rowList = []
    for cell in row:
      if cell.visited:
        rowList.append(1)
      else: 
        rowList.append(0)
    solution.append(rowList)
  return solution


#def printSolution()

solutionRute = []
myMaze = Labyrinth(*load_prop("5x5_32736.dat"))
#myMaze.showLab()
#dfs(myMaze,0, (myMaze.entrance-1))
pruneMaze(myMaze)
solution = iterativ_dfs(myMaze, 0,myMaze.entrance-1)
#print(solution)
print(list(dict.fromkeys(solution)))
#print(solution)

#dfs(myMaze,0, (myMaze.entrance-1))

#number_to_walls(9)
#mySolution = generateSolution(myMaze)
#for row in solutionRute:
 # print (row)



  #base case
  #end condition
