import time

def main():
	test = str(raw_input("test_run?[Y/n] "))
	if test in "Yy ":
		play_game_of_life(6, 10, .5, True)
	else:
		play_game_of_life(
			int(raw_input("max_size? ")),
			int(raw_input("num_iters? ")),
			float(raw_input("sleep_time? ")),
			False
		)

#upgrade game_board to class
#with fields, such as game_board, num_live_cells, etc,
#and functions, such as update_board(), make_cell_alive(), etc.
def play_game_of_life(max_size, num_iters, sleep_time, is_test_run):
	game_board = [[' ' for i in range(max_size)] for j in range(max_size)]
	if not is_test_run:
		should_add_glider = str(raw_input("add_glider?[Y/n] ")).lower()
		if should_add_glider in "y ":
			add_glider(game_board, max_size);
		else:
			print "enter \"stop\" or \"done\" when finished"
			while True:
				i = raw_input("i? ")
				if i in ["stop", "done"]:
					break;
				j = raw_input("j? ")
				if j in ["stop", "done"]:
					break;
				make_alive(game_board, max_size, int(i), int(j))
	else:
		add_glider(game_board, max_size)

	print_game_of_life(game_board, max_size)
	for q in range(num_iters):
		game_board = update_game_board(game_board, max_size)
		print_game_of_life(game_board, max_size)
		time.sleep(sleep_time)
	end = raw_input("end")

#refactor to class/subclass
#and add starting location, rather than set board position
def add_glider(game_board, max_size): #ADD: (i, j):
	for i, j in [[0,0], [1,1], [1,2], [2,1], [0,2]]:
		make_alive(game_board, max_size, i, j)

def update_game_board(game_board, max_size):
	new_game_board = [row[:] for row in game_board]
	for i in range(max_size):
		for j in range(max_size):
			num_neighbors = get_neighbor_count(game_board, max_size, i, j)
			if game_board[i][j] == 'x':
				if num_neighbors < 2 or num_neighbors > 3:
					new_game_board[i][j] = ' '
			else:
				if num_neighbors == 3:
					new_game_board[i][j] = 'x'
	return new_game_board

def get_neighbor_count(game_board, max_size, i, j):
	count = 0
	for x in range(-1, 2):
		for y in range(-1, 2):
			if x==0 and y==0:
				continue
			if i+x < 0: 
				i_x = max_size-1
			elif i+x > max_size-1:
				i_x = 0
			else:
				i_x = i+x
			if j+y < 0:
				j_y = max_size-1
			elif j+y > max_size-1:
				j_y = 0
			else:
				j_y = j+y
			if game_board[i_x][j_y] == 'x':
				count += 1
	return count

def print_game_of_life(game_board, max_size):
	print ""
	for i in range(max_size):
		buf = ""
		sep = ""
		for j in range(max_size):
			buf += game_board[i][j] + "|"
			sep += "--"
		print buf
		print sep	
	print ""

#either add method or add to this
#func to make_dead if already alive
def make_alive(game_board, max_size, i, j):
	try:
		game_board[i][j] = 'x'
	except IndexError, e:
		print str(e) + "; max_size is " + str(max_size)

if __name__ == "__main__":
	main()
