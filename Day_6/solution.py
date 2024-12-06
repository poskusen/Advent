board = {} # (True for obstacle, True for visited)
pos_guard = [0,0]

guard_direction = 0 #[0,1] - up, [1,0] - right, [0,-1] - down, [-1,0] - left)
visisted_amount = 0


with open('input.txt', 'rb') as file:
    row = 0
    col = 0
    for line in file:
        board[row] = {}
        for spot in line:
            spot = chr(spot)
            board[row][col] = [spot == '#', False, [[0,0]]]
            if spot in ['v', '<', '>', '^']:
                pos_guard = [row, col]
                board[row][col][1] = True
                visisted_amount += 1
                if spot == 'v':
                    guard_direction = [-1,0]
                elif spot == '^':
                    guard_direction = [1,0]
                elif spot == '<':
                    guard_direction = [0,-1]
                else:
                    guard_direction = [0,1]
            col += 1
        row += 1
        col = 0

class walk_along():
    def __init__(self, board, pos_guard, guard_direction):
        self.board = board
        self.pos_guard = pos_guard
        self.guard_direction = guard_direction
        
    def test_cyclical(self):
        return self.solve()
        

    def new_direction(self, direction):
        if direction == [0,1]:
            return [1, 0]
        elif direction == [1,0]:
            return [0,-1]
        elif direction == [0,-1]:
            return [-1,0]
        else:
            return [0,1]

    def add_list(self, list1, list2):
        re_list = [0 for _ in list1]
        for i in range(len(list1)):
            re_list[i] = list1[i] - list2[i]
        return re_list
            

    def walk_along_direction(self, direction, spot):
        end_walk = False
        while not end_walk:
            new_spot = self.add_list(spot, direction)
            if new_spot[0] in self.board and new_spot[1] in self.board[new_spot[0]]:
                if direction in self.board[new_spot[0]][new_spot[1]][2]:
                    return True, spot, not end_walk, 0
                elif self.board[new_spot[0]][new_spot[1]][0]:
                    end_walk = True
                    direction = self.new_direction(direction)
                
                else:
                    self.board[new_spot[0]][new_spot[1]][2].append(direction)
                    spot = new_spot
            else:
                return False, spot, not end_walk, 0
        
        return direction, spot, not end_walk, 1

    def solve(self):
        success = 1
        end_the_walk = False    
        while not end_the_walk and success == 1:
            self.guard_direction, self.pos_guard, self.end_the_walk, success = self.walk_along_direction(self.guard_direction, self.pos_guard)
        return self.guard_direction
        
        
amount = 0
for i in range(0, len(board)):
    for j in range(0, len(board[0])):
        print(len(board))
        if not [i, j] == pos_guard and not board[i][j][0]:
            new_board = board
            new_board[i][j][0] = True
            walk_object = walk_along(new_board, pos_guard, guard_direction)
            if walk_object.test_cyclical():
                amount += 1
    print(amount)

print(f'Cykliska: {amount}')
        