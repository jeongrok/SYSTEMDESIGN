class Player:
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker


class Board:
    def __init__(self, size):
        self.size = size
        self.reset(size)
    

    def reset(self, size):
        self.board = [['' for x in range(size)].copy() for y in range(size)]
        self.rowCounts = {}
        self.colCounts = {}
        self.diagCounts = {}


    # places the marker on the board and returns True if the game ended
    def place(self, player, x, y):
        marker = player.marker
        if self.board[y][x] != '' or x not in range(self.size) or y not in range(self.size):
            raise ValueError
        else:
            self.board[y][x] = marker

            self.rowCounts[y] = self.rowCounts.get(y, {})
            self.rowCounts[y][marker] = self.rowCounts[y].get(marker, 0) + 1
            if self.rowCounts[y][marker] == self.size:
                return True

            self.colCounts[x] = self.colCounts.get(x, {})
            self.colCounts[x][marker] = self.colCounts[x].get(marker, 0) + 1
            if self.colCounts[x][marker] == self.size:
                return True

            if x == y:
                self.diagCounts["forward"] = self.diagCounts.get("forward", {})
                self.diagCounts["forward"][marker] = self.diagCounts["forward"].get(marker, 0) + 1
                if self.diagCounts["forward"][marker] == self.size:
                    return True

            if x + y + 1 == self.size:
                self.diagCounts["backward"] = self.diagCounts.get("backward", {})
                self.diagCounts["backward"][marker] = self.diagCounts["backward"].get(marker, 0) + 1
                if self.diagCounts["backward"][marker] == self.size:
                    return True
            
            return False
    
    def print_board(self):
        for r in self.board:
            print('|'.join(r))
            print('-'* (self.size*2-1))


class Game:
    def __init__(self, player1, player2, board) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
    

    def playGame(self):
        currTurn = 1
        gameDone = False
        while not gameDone:
            currPlayer = self.player1 if currTurn %2 == 1 else self.player2
            if currPlayer == self.player1:
                print("Player 1 Turn")
            else:
                print("Player 2 Turn")
            x = int(input("Write x position of marker"))
            y = int(input("Write y position of marker"))
            result = self.board.place(currPlayer, x, y)
            self.board.print_board()
            if result:
                gameDone = True
                print(f"{currPlayer.name} wins!")
            else:
                currTurn += 1
    

mike = Player("Big mike", "x")
musk = Player("Elon Musk", "o")
board = Board(3)
game = Game(mike, musk, board)

game.playGame()