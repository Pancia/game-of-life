import time
import json
import os

#consider switching to outputting to GUI for learning purposes
def main():
    test = str(raw_input("test_run?[y/N] "))
    if test != "" and test in "Yy":
        play_game_of_life(max_size=10, num_iters=25, sleep_time=.2)
    else:
        try:
            play_game_of_life(
                int(raw_input("max_size? ")),
                int(raw_input("num_iters? ")),
                float(raw_input("sleep_time? ")))
        except ValueError, ve:
            print "\tERROR: "+str(ve)
            print "\tTRY AGAIN"
            main()

def play_game_of_life(max_size, num_iters, sleep_time):
    game_board = GameBoard(max_size)
    if str(raw_input("add_creature?[Y/n] ")) in "yY":
        while True:
            creature_name = str(raw_input("creature_name? "))
            if creature_name in ["stop", "done"]:
                break
            try:
                game_board.add_creature(GameCreature(creature_name))
                break
            except ValueError, ve:
                print str(ve)
    if str(raw_input("create creature?[Y/n]")) in "yY":
        print "enter \"stop\", \"done\", or \"save\" when finished"
        print "enter \"print\" to display currect creation"
        print "enter \"save\" to store current creation"
        points = []
        while True:
            i = raw_input("i? ").lower()
            if i in ["stop", "done"]:
                break;
            elif i in ["print"]:
                game_board.print_game_board()
                continue
            elif i in ["save"]:
                GameCreature.save_creature(str(raw_input("name? ")), points)
                break
            j = raw_input("j? ").lower()
            if j in ["stop", "done"]:
                break;
            game_board.toggle_cell(int(i), int(j))
            points.append([i,j])

    game_board.print_game_board()
    for q in range(num_iters):
        game_board.update_game_board()
        game_board.print_game_board()
        time.sleep(sleep_time)
    end = raw_input("end?[y/N] ")
    if end == "" or end not in "yY":
        main()

class GameBoard():
    live_cell = 'x'
    dead_cell = ' '

    def __init__(self, max_size):
        self.max_size = max_size
        self.game_board = [[self.dead_cell for i in range(max_size)] for j in range(max_size)]
        self.num_live_cells = 0

    def add_creature(self, creature, x=0, y=0):
        for i, j in creature.get_cells():
            self.toggle_cell(int(i)+x, int(j)+y, True)

    def update_game_board(self):
        if self.num_live_cells == 0:
            return
        new_game_board = GameBoard(self.max_size)
        new_game_board.num_live_cells = self.num_live_cells
        new_game_board.game_board = [row[:] for row in self.game_board]

        for i in range(self.max_size):
            for j in range(self.max_size):
                num_neighbors = self.get_neighbor_count(i, j)
                if self.game_board[i][j] == self.live_cell:
                    if num_neighbors < 2 or num_neighbors > 3:
                        new_game_board.toggle_cell(i, j)
                else:
                    if num_neighbors == 3:
                        new_game_board.toggle_cell(i, j)

        self.game_board = new_game_board.game_board

    def get_neighbor_count(self, i, j):
        count = 0
        temp = self.max_size-1
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x==0 and y==0:
                    continue
                if i+x < 0: 
                    i_x = temp
                elif i+x > temp:
                    i_x = 0
                else:
                    i_x = i+x
                if j+y < 0:
                    j_y = temp
                elif j+y > temp:
                    j_y = 0
                else:
                    j_y = j+y
                if self.game_board[i_x][j_y] == self.live_cell:
                    count += 1
        return count

    def print_game_board(self):
        print ""
        for i in range(self.max_size):
            buf = ""
            sep = ""
            for j in range(self.max_size):
                buf += self.game_board[i][j] + "|"
                sep += "--"
            print buf
            print sep       
        print ""

    def toggle_cell(self, i, j, to_alive=None):
        try:
            if to_alive == None:
                if self.game_board[i][j] == self.live_cell:
                    self.game_board[i][j] = self.dead_cell
                    self.num_live_cells -= 1
                else:
                    self.game_board[i][j] = self.live_cell
                    self.num_live_cells += 1
            else:
                if to_alive:
                    self.game_board[i][j] = self.live_cell
                    self.num_live_cells += 1
                else:
                    self.game_board[i][j] = self.dead_cell
                    self.num_live_cells -= 1
        except IndexError, e:
            print str(e) + "; max_size is " + str(max_size)

class GameCreature():
    def __init__(self, name):
        self.creature_type = name
        self.creature_types = GameCreature.get_all_creatures()
        print self.creature_types

        if name in self.creature_types:
            self.cells = self.creature_types[name]
        else:
            raise TypeError(name + " is not a stored creature type")

    @staticmethod
    def get_all_creatures():
        with open("creatures.json", "r") as in_file:
            return json.load(in_file)

    @staticmethod
    def save_creature(name, points):
        creature_types = GameCreature.get_all_creatures()
        creature_types[str(name)] = points
        with open("creatures.json", "r+") as out_file:
            json.dump(creature_types, out_file, indent=4)
        print creature_types

    def get_cells(self):
        return self.cells

if __name__ == "__main__":
    main()
