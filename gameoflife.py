import time

def main():
    test = str(raw_input("test_run?[Y/n] "))
    if test in "Yy ":
        play(6, 10, .5, True)
    else:
        play(
            int(raw_input("max_size? ")),
            int(raw_input("num_iters? ")),
            float(raw_input("sleep_time? ")),
            False
        )

#upgrade game_board to class
#with fields, such as game_board, num_live_cells, etc,
#and functions, such as update_board(), make_cell_alive(), etc.
def play(max_size, num_iters, sleep_time, is_test_run):
    board = [[' '] * max_size] * max_size
    if not is_test_run:
        should_add_glider = str(raw_input("add_glider?[Y/n] ")).lower()
        if should_add_glider in "y ":
            add_glider(board, max_size);
        else:
            print "enter \"stop\" or \"done\" when finished"
            while True:
                i = raw_input("i? ")
                if i in ["stop", "done"]:
                    break;
                j = raw_input("j? ")
                if j in ["stop", "done"]:
                    break;
                make_alive(board, max_size, int(i), int(j))
    else:
        add_glider(board, max_size)

    print_game_of_life(board, max_size)
    for q in range(num_iters):
        board = update_game_board(board, max_size)
        print_game_of_life(board, max_size)
        time.sleep(sleep_time)
    end = raw_input("end")

#refactor to class/subclass
#and add starting location, rather than set board position
def add_glider(board, max_size): #ADD: (i, j):
    for i, j in [[0,0], [1,1], [1,2], [2,1], [0,2]]:
        make_alive(board, max_size, i, j)

def update_game_board(board, max_size):
    new_board = [row[:] for row in board]
    for i in range(max_size):
        for j in range(max_size):
            num_neighbors = get_neighbor_count(board, max_size, i, j)
            if board[i][j] == 'x':
                if num_neighbors < 2 or num_neighbors > 3:
                    new_board[i][j] = ' '
            else:
                if num_neighbors == 3:
                    new_board[i][j] = 'x'
    return new_board

# MAKE SURE THIS DOES WHAT YOU WANT IT TO.
# I'VE RAN IT AND IT GIVES ME A DIFFERENT OUPUT.
# I'M GOING TO BED. HAPPY EASTER, OR WHATEVER.
def get_neighbor_count(board, max_size, i, j):
    count = 0
    for x in [-1, 0, 1]:
        y = 0
        if x+i >= max_size or x+i < 0:
            x = 0
        if j+2 >= max_size:
            y = -1
        count += board[i+x][j-1:j+2+y].count('x')
    return count

def print_game_of_life(board, max_size):
    print ""
    for i in range(max_size):
        buf = ""
        sep = ""
        for j in range(max_size):
            buf += board[i][j] + "|"
            sep += "--"
        print buf
        print sep   
    print ""

#either add method or add to this
#func to make_dead if already alive
def make_alive(board, max_size, i, j):
    try:
        board[i][j] = 'x'
    except IndexError, e:
        print str(e) + "; max_size is " + str(max_size)

if __name__ == "__main__":
    main()
