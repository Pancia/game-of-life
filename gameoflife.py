import time

#consider switching to outputting to GUI for learning purposes
def main():
	test = str(raw_input("test_run?[Y/n] "))
	if test in "Yy ":
		play_game_of_life(6, 13, .3, True)
	else:
		try:
			play_game_of_life(
				int(raw_input("max_size? ")),
				int(raw_input("num_iters? ")),
				float(raw_input("sleep_time? ")),
				False)
		except ValueError, ve:
			print "\tERROR: "+str(ve)
			print "\tTRY AGAIN"
			main()

#add self.num_live_cells 
def play_game_of_life(max_size, num_iters, sleep_time, is_test_run):
	game_board = GameBoard(max_size)
	if not is_test_run:
		if str(raw_input("add_glider?[Y/n] ")) in "yY":
			game_board.add_creature(GameCreature("glider"), 0, 0)
		else:
			print "enter \"stop\" or \"done\" when finished"
			while True:
				i = raw_input("i? ")
				if i in ["stop", "done"]:
					break;
				j = raw_input("j? ")
				if j in ["stop", "done"]:
					break;
				game_board.set_cell_to(int(i), int(j), True)
	else:
		game_board.add_creature(GameCreature("glider"), 0, 0)

	game_board.print_game_board()
	for q in range(num_iters):
		game_board.update_game_board()
		game_board.print_game_board()
		time.sleep(sleep_time)
	end = raw_input("end?[Y/n] ")
	if end not in "yY":
		main()

class GameBoard():
	live_cell = 'x'
	dead_cell = ' '

	def __init__(self, max_size):
		self.max_size = max_size
		self.game_board = [[self.dead_cell for i in range(max_size)] for j in range(max_size)]
		self.num_live_cells = 0

	def add_creature(self, creature, x, y): 
		for i, j in creature.get_cells():
			self.set_cell_to(x+i, y+j, True)

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
						new_game_board.set_cell_to(i, j, False)
				else:
					if num_neighbors == 3:
						new_game_board.set_cell_to(i, j, True)

		self.game_board = new_game_board.game_board

	def get_neighbor_count(self, i, j):
		count = 0
		for x in range(-1, 2):
			for y in range(-1, 2):
				if x==0 and y==0:
					continue
				if i+x < 0: 
					i_x = self.max_size-1
				elif i+x > self.max_size-1:
					i_x = 0
				else:
					i_x = i+x
				if j+y < 0:
					j_y = self.max_size-1
				elif j+y > self.max_size-1:
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

	def set_cell_to(self, i, j, alive):
		try:
			if alive:
				self.game_board[i][j] = self.live_cell
				self.num_live_cells += 1
			else:
				self.game_board[i][j] = self.dead_cell
				self.num_live_cells -= 1

		except IndexError, e:
			print str(e) + "; max_size is " + str(max_size)

#how to implement prompting and saving (persistently) user created creatures?
class GameCreature():
	glider_cells = [[0,0], [1,1], [1,2], [2,1], [0,2]]

	def __init__(self, creature_type):
		self.creature_type = creature_type
		if self.creature_type == "glider":
			self.cells = self.glider_cells
		else: #ie default
			self.cells = self.glider_cells

	def get_cells(self):
		return self.cells

if __name__ == "__main__":
	main()
