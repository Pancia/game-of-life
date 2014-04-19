import time

def main():
	assert 0 < 10
	play_game_of_life(
		int(raw_input("max_size? ")),
		int(raw_input("num_iters? ")),
		float(raw_input("sleep_time? "))
	)

#upgrade game_board to class
#with fields, such as num_live_cells
def play_game_of_life(max_size, num_iters, sleep_time):
	game_board = [[' ' for i in range(max_size)] for j in range(max_size)]
	if str(raw_input("add_glider? ")) == "yes":
		add_glider(game_board, max_size);
	else:
		print "enter \"stop\" or \"done\" when finished"
		while True:
			i = raw_input("i? ")
			if i == "stop" or i == "done":
				break;
			j = raw_input("j? ")
			if j == "stop" or j == "done":
				break;
			make_alive(game_board, max_size, int(i), int(j))

	print_game_of_life(game_board, max_size)
	for q in range(num_iters):
		game_board = update_game_board(game_board, max_size)
		print_game_of_life(game_board, max_size)
		time.sleep(sleep_time)
	end = raw_input("end")

#refactor to class/subclass
#and add starting location, rather than set board position
def add_glider(game_board, max_size): #ADD: (i, j):
	make_alive(game_board, max_size, 0, 0)
	make_alive(game_board, max_size, 1, 1)
	make_alive(game_board, max_size, 1, 2)
	make_alive(game_board, max_size, 2, 1)
	make_alive(game_board, max_size, 0, 2)

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
	#print ">>i:"+str(i)+"|j:"+str(j)
	for x in range(-1, 2):
		for y in range(-1, 2):
			#print "x:"+str(x)+"|y:"+str(y)
			if x==0 and y==0:
				continue
			if i+x < 0: #or i+x > max_size-1 or j+y < 0 or j+y > max_size-1:
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
			#print ">i+x:"+str(i+x)+"|j+y:"+str(j+y)
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
