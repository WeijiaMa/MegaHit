import pygame
import random
import pygame.mixer
import time

class Structure(object):
	# Contains basic information needed to draw anything on the surface
	# topBoundary is the min y value of which everything is drawn
	# hitLineY is the y value of the hit line at the bottom
	def __init__(self, color, surface):
		self.color = color
		self.surface = surface
		self.topBoundary = 10
		self.hitLineY = 7/8 * surfaceHeight

class Frame(Structure):
	# Contains basic information needed to draw the frame and bars
	# numKey is the total number of columns, with a value of 4 or 6 or 8
	# leftSpace is the x value of the left most column
	def __init__(self, numKey, color, surface):
		super().__init__(color, surface)
		self.numKey = numKey
		self.barWidth = surfaceWidth / 2 / self.numKey
		self.barHeight = 2/5 * self.barWidth
		self.leftSpace = (surfaceWidth  - self.barWidth * (numKey + 1/5 * (numKey - 1))) / 4

	def draw(self):
		# Draw vertical frames
		for i in range(self.numKey + 1):
			pygame.draw.rect(surface, self.color, ((6/5 * i - 1/10) * self.barWidth +  self.leftSpace - 1/320 * surfaceWidth, self.topBoundary, 1/160 * surfaceWidth, surfaceHeight))
		# Draw bottom hit line
		pygame.draw.rect(surface, self.color, (1/16 * surfaceWidth, self.hitLineY, 7/8 * surfaceWidth, 1/160 * surfaceWidth))

	def setKey(self, numKey):
		if numKey == 8:
			return ["a", "s", "d", "f", "j", "k", "l", ";"]
		elif numKey == 6:
			return ["s", "d", "f", "j", "k", "l"]
		elif numKey == 4:
			return ["d", "f", "j", "k"]

	# Draw the 
	def drawKey(self, numKey):
		for i in range(numKey):
			textX = self.leftSpace + 2/5 * self.barWidth + 6/5 * i * self.barWidth
			textInRect(self.setKey(numKey)[i], self.color, (6/5 * i - 1/10) * self.barWidth +  self.leftSpace - 1/320 * surfaceWidth, self.hitLineY + 1/160 * surfaceWidth, 6/5 * self.barWidth, self.barHeight, 1)

class Bar(Frame):
	# column is the column the bar is in: ranging from 0 to numKey
	# speed is the speed the bar drops
	# the entire frame will take up slightly more than half of the width of the screen and placed in the centre
	def __init__(self, numKey, column, color, speed, surface):
		super().__init__(numKey, color, surface)
		self.column = column
		self.barX = self.column * self.barWidth * 6/5 + self.leftSpace
		self.barY = self.topBoundary
		self.speed = speed

	def getPosition(self):
		return [self.barX, self.barY]

	def barInColumn(self):
		# Returns a boolean whether the bar is above the bottom hit line
		return self.hitLineY - 20 < self.barY < self.hitLineY + 20

	def draw(self):
		# Draw the dropping bar
		rect = pygame.draw.rect(surface, pink, (self.barX, self.barY, self.barWidth, self.barHeight))
		self.barY += self.barHeight / 8 * self.speed

class Option(Structure):
	# Option "bottons" for the user to choose from
	def __init__(self, x, y, color, surface):
		super().__init__(color, surface)
		self.x = x
		self.y = y

	def draw(self):
		pygame.draw.rect(self.surface, self.color,(self.x, self.y, optionWidth, optionHeight))

class Song(object):
	# Attributes related to songs
	# bpm is beat per minute
	def __init__(self, name, bpm):
		self.name = name
		self.bpm = bpm
		self.sound = pygame.mixer.Sound("Song/" + self.name)
		self.freq = 60000//self.bpm

	# Play the song
	def play(self):
		self.sound.play()

	# Length of the song in miliseconds
	def length(self):
		return 1000 * self.sound.get_length()

	# Start the timing
	def start(self):
		pygame.time.set_timer(BARDROPEVENT, self.freq)

class Pic(object):
	# Draw an image on the side of the main game screen
	def __init__(self, image):
		self.image = image
		self.pic = pygame.image.load("Image/" + image)

	def drawPic(self):
		surface.blit(self.pic, (18/25 * surfaceWidth, 1/8 * surfaceHeight))

# Define colors to be used in the game
black = (50, 50, 50)
white = (245, 245, 245)
pink = (255, 136, 136)
green = (0, 200, 0)
blue = (0, 0, 232)
grey = (150, 150, 150)


# Initialize the surface, font, timer and some other global constants
pygame.init()
surfaceWidth = 800
surfaceHeight = 600
surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
pygame.display.set_caption('Mega Hit')

font = []
for i in [60, 40, 30, 20]:
	font += [pygame.font.SysFont("comicsansms", surfaceWidth//i)]
clock = pygame.time.Clock()
FPS = 60
BARDROPEVENT = 25
optionWidth = 3/8 * surfaceWidth
optionHeight = 1/6 * surfaceHeight

# Draw text to the centre of the rectangle centred at [x,y], size is 0 to 3 with 3 being the largest
def textObject(text, color, size):
	for i in range(len(font)):
		textSurface = font[size].render(text, True, color)
	return textSurface, textSurface.get_rect()

# Draw text at x, y
def drawText(text, color, x, y, size):
	txt = font[size].render(text, True, color)
	surface.blit(txt, (x,y))

# Draw text in the centre of the screen, adjusting up and down by an amount of yDisplace
def textOnScreen(text, color, yDisplace, size):
	textSurf, textRect = textObject(text, color, size)
	textRect.center = (surfaceWidth / 2, surfaceHeight / 2 + yDisplace)
	surface.blit(textSurf, textRect)

# Draw text in the centre of a rect
def textInRect(text, color, rectX, rectY, rectWidth, rectHeight, size):
	textSurf, textRect = textObject(text, color, size)
	textRect.center = (rectX + rectWidth/2, rectY + rectHeight/2)
	surface.blit(textSurf, textRect)

# The start screen, printing out information the user need to play the game
def startScreen():
	startScreen = True
	key = None
	while startScreen:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				elif event.type == pygame.KEYDOWN:
					key = event.unicode

		surface.fill(white)
		textOnScreen("Welcome to Mega Hit", pink, - 1/4 * surfaceHeight, 3)
		textOnScreen("Choose a speed, number of keys and a song to play with", black, 0, 2)
		textOnScreen("Then hit the keys when the bars drop to the bottom line", black, 1/8 * surfaceHeight, 2)
		textOnScreen("Press S to start, P to pause and R to return to the menu", black, 1/4 * surfaceHeight, 2)
		if key == "s":
			startScreen = False
		pygame.display.update()

# Let the user choose the speed
def setSpeed():
	key = None
	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				elif event.type == pygame.KEYDOWN:
					key = event.unicode
		# Draw speed options
		surface.fill(white)
		textOnScreen("Choose a speed by pressing the respective number key:", black, -3/8 * surfaceHeight, 2)
		speedOption = []
		for i in range(3):
			speedOption += [Option(1/2 * surfaceWidth - 1/2 * optionWidth, 1/4 * surfaceHeight + (1/16 * surfaceHeight + optionHeight) * i, pink, surface)]
			speedOption[i].draw()
			textInRect(str(i + 1) + "X", white, speedOption[i].x, speedOption[i].y, optionWidth, optionHeight, 2)
		# Choose a speed
		for i in range(len(speedOption)):
			if key == str(i + 1):
				return i + 1
		pygame.display.update()

# Let the user choose the number of keys
def setKey(numKeys):
	key = None
	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				elif event.type == pygame.KEYDOWN:
					key = event.unicode
		# Draw options for the number of keys
		surface.fill(white)
		textOnScreen("Choose the number of keys by pressing the respective number key:", black, -3/8 * surfaceHeight, 1)
		keyOption = []
		for i in range(len(numKeys)):
			keyOption += [Option(1/2 * surfaceWidth - 1/2 * optionWidth, 1/4 * surfaceHeight + (1/16 * surfaceHeight + optionHeight) * i, pink, surface)]
			keyOption[i].draw()
			textInRect(str(numKeys[i]) + " Keys", white, keyOption[i].x, keyOption[i].y, optionWidth, optionHeight, 2)
		# Choose the number of keys
		for i in range(len(numKeys)):
			if key == str(numKeys[i]):
				return numKeys[i]
		pygame.display.update()

# Let the user choose the song
def setSong(songs, options):
	key = None
	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				elif event.type == pygame.KEYDOWN:
					key = event.unicode
		# Draw song options
		surface.fill(white)
		textOnScreen("Choose a song by pressing the respective alphabet key:", black, -3/8 * surfaceHeight, 2)
		songOption = []
		for i in range(len(songs)):
			songOption += [Option(1/12 * surfaceWidth + (1/12 * surfaceWidth + optionWidth) * (i // 3), 1/4 * surfaceHeight + (1/16 * surfaceHeight + optionHeight) * (i % 3), pink, surface)]
			songOption[i].draw()
			textInRect(str(options[i]) + ". " + songs[i].name, white, songOption[i].x, songOption[i].y, optionWidth, optionHeight, 0)
		# Choose a song
		for i in range(len(songs)):
			if key == options[i]:
				return songs[i]
		pygame.display.update()

# The main game screen
def mainGame(speed, numKey, song):
	song.play()
	song.start()
	key = None
	score = 0
	bar = []
	for i in range(numKey):
		bar += [[]]
	frame = Frame(numKey, grey, surface)
	picture = [Pic("josh1.png"), Pic("josh2.png"), Pic("josh3.png")]
	randPic = None
	clock.tick(FPS)
	initTime = pygame.time.get_ticks()
	currentTime = 0
	timePlayed = 0

	while timePlayed < song.length():
		# Draw the canvas
		surface.fill(white)
		frame.draw()
		frame.setKey(numKey)
		frame.drawKey(numKey)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				key = event.unicode
			else:
				key = None
			if event.type == BARDROPEVENT:
				# Initialize bars at random column when there is a beat
				randCol = random.randint(0, numKey - 1)
				bar[randCol] += [Bar(numKey, randCol, pink, speed, surface)]
				# Blit a random image of a figure to the screen
				randPic = picture[random.randint(0, len(picture) - 1)]

		# Return to menu
		if key == "r":
			game()
		# Draw bars
		for i in range(numKey):
			for j in range(len(bar[i])):
				if bar[i][j] != 0:
					bar[i][j].draw()

		# Undraw bars if hit at the hit line
		for i in range(numKey):
			for j in range(len(bar[i])):
				if bar[i][j] != 0:
					if key == frame.setKey(numKey)[i] and bar[i][j].barInColumn():
						bar[i][j] = 0
						score += 1
		if randPic != None:
			randPic.drawPic()
		# Update score
		drawText("Score: " + str(score), black, 4/5 * surfaceWidth, frame.topBoundary * 2, 2)
		currentTime = pygame.time.get_ticks()
		timePlayed = currentTime - initTime
		pygame.display.update()
	return score

# The game loop
def game():
	startScreen()
	gameOver = False
	while True:
		key = None
		numKey = 1
		# List of songs
		songs = [Song("Marry You - Bruno Mars.wav", 145), Song("I Will Wait - Mumford & Sons.wav", 131), Song("Closer - The Chainsmokers (feat. Halsey).wav", 95), Song("I Gotta Feeling - The Black Eyed Peas.wav", 128), Song("Wobble - Flo Rida.wav", 88), Song("Trucker's Hitch - Ylvis.wav", 128)]
		options = [chr(i) for i in range(ord('a'),ord('z')+1)]
		numKeys = [4, 6, 8]

		while gameOver == True:
			surface.fill(white)
			textOnScreen("Done!", black, - 1/6 * surfaceHeight, 3)
			textOnScreen("Score: " + str(score), black, - 1/50 * surfaceHeight, 3)
			textOnScreen("Press r to play again", black, 1/5 * surfaceHeight, 2)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					key = event.unicode
			if key == "r":
				game()
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					key = event.unicode
		speed = setSpeed()
		numKey = setKey(numKeys)
		song = setSong(songs, options)
		score = mainGame(speed, numKey, song)
		gameOver = True
	pygame.quit()
	quit()

game()