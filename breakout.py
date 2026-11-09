import pygame
import random

pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 600, 500

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
GRAY   = (160, 160, 160)   # warna blok putih setelah kena hit pertama
YELLOW = (255, 220, 50)    # kilatan flash saat kena hit

font = pygame.font.Font('freesansbold.ttf', 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

# to control the frame rate
clock = pygame.time.Clock()
FPS = 30


# Striker class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        # The rect variable is used to handle the placement
        # and the collisions of the object
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.striker = pygame.draw.rect(screen, 
                               self.color, self.strikerRect)

    # Used to render the object on the screen
    def display(self):
        self.striker = pygame.draw.rect(screen, 
                            self.color, self.strikerRect)

    # Used to update the state of the object
    def update(self, xFac):
        self.posx += self.speed*xFac

        # Restricting the striker to be in between the 
        # left and right edges of the screen
        if self.posx <= 0:
            self.posx = 0
        elif self.posx+self.width >= WIDTH:
            self.posx = WIDTH-self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    # Returns the rect of the object
    def getRect(self):
        return self.strikerRect


# Block Class
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100
        self.flash_timer = 0   # berapa frame tersisa untuk efek flash

        # The white blocks have the health of 200. So,
        # the ball must hit it twice to break
        if color == WHITE:
            self.health = 200
            self.max_health = 200
        else:
            self.health = 100
            self.max_health = 100

        # The rect variable is used to handle the placement
        # and the collisions of the object
        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.block = pygame.draw.rect(screen, self.color,
                                      self.blockRect)

    # ── gambar blok + efek visual kerusakan ──
    def display(self):
        if self.health <= 0:
            return

        # warna berubah kalau blok putih sudah kena sekali
        draw_color = self.color
        if self.color == WHITE and self.health < self.max_health:
            draw_color = GRAY   # tampak rusak / retak

        # flash kuning selama beberapa frame setelah kena hit
        if self.flash_timer > 0:
            draw_color = YELLOW
            self.flash_timer -= 1

        self.brick = pygame.draw.rect(screen, draw_color, self.blockRect)

        # ── garis retakan untuk blok putih yang sudah kena ──
        if self.color == WHITE and self.health < self.max_health:
            cx = self.posx + self.width  // 2
            cy = self.posy + self.height // 2
            crack_color = (80, 80, 80)
            # 3 garis retakan acak-tapi-konsisten
            pygame.draw.line(screen, crack_color,
                             (cx - 5, cy - 5), (cx + 8, cy + 6), 1)
            pygame.draw.line(screen, crack_color,
                             (cx + 8, cy + 6), (cx + 3, cy + self.height//2 - 1), 1)
            pygame.draw.line(screen, crack_color,
                             (cx - 5, cy - 5), (cx - 10, cy + 2), 1)

    # Used to decrease the health of the block
    def hit(self):
        self.health -= self.damage
        self.flash_timer = 4   # nyalain flash 4 frame

    # Used to get the rect of the object
    def getRect(self):
        return self.blockRect

    # Used to get the health of the object
    def getHealth(self):
        return self.health


# Ball Class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx,
                                 self.posy), self.radius)

    # Used to display the object on the screen
    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, 
                                 self.posy), self.radius)

    # Used to update the state of the object
    def update(self):
        self.posx += self.xFac*self.speed
        self.posy += self.yFac*self.speed

        # Reflecting the ball if it touches
        # either of the vertical edges
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1

        # Reflection from the top most edge of the screen
        if self.posy <= 0:
            self.yFac *= -1

        # If the ball touches the bottom most edge of 
        # the screen, True value is returned
        if self.posy >= HEIGHT:
            return True

        return False

    # Resets the position of the ball
    def reset(self):
        self.posx = 0
        self.posy = HEIGHT
        self.xFac, self.yFac = 1, -1

    # Used to change the direction along Y axis
    def hit(self):
        self.yFac *= -1

    # Returns the rect of the ball. In this case,
    # it is the ball itself
    def getRect(self):
        return self.ball

# Helper Functions

# Function used to check collisions between any two entities


def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True

    return False


# Function used to populate the blocks
def populateBlocks(blockWidth, blockHeight, 
                   horizontalGap, verticalGap):
    listOfBlocks = []

    for i in range(0, WIDTH, blockWidth+horizontalGap):
        for j in range(0, HEIGHT//2, blockHeight+verticalGap):
            listOfBlocks.append(
                Block(i, j, blockWidth, blockHeight, 
                      random.choice([WHITE, GREEN])))

    return listOfBlocks


# Once all the lives are over, this function waits until
# exit or space bar is pressed and does the corresponding action
def gameOver():
    gameOver = True

    while gameOver:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True


# Game Manager
def main():
    running = True
    lives = 3
    score = 0

    scoreText = font.render("score", True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (20, HEIGHT-10)

    livesText = font.render("Lives", True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (120, HEIGHT-10)

    striker = Striker(0, HEIGHT-50, 100, 20, 10, WHITE)
    strikerXFac = 0

    ball = Ball(0, HEIGHT-150, 7, 5, WHITE)

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    listOfBlocks = populateBlocks(
        blockWidth, blockHeight, horizontalGap, verticalGap)

    # Game loop
    while running:
        screen.fill(BLACK)
        screen.blit(scoreText, scoreTextRect)
        screen.blit(livesText, livesTextRect)

        scoreText = font.render("Score : " + str(score), True, WHITE)
        livesText = font.render("Lives : " + str(lives), True, WHITE)

        # If all the blocks are destroyed, then we repopulate them
        if not listOfBlocks:
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)

        # All the lives are over. So, the gameOver() function is called
        if lives <= 0:
            running = gameOver()

            while listOfBlocks:
                listOfBlocks.pop(0)

            lives = 3
            score = 0
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Collision check
        if(collisionChecker(striker.getRect(), ball.getRect())):
            ball.hit()
        for block in listOfBlocks:
            if(collisionChecker(block.getRect(), ball.getRect())):
                ball.hit()
                block.hit()

                if block.getHealth() <= 0:
                    listOfBlocks.pop(listOfBlocks.index(block))
                    score += 5

        # Update
        striker.update(strikerXFac)
        lifeLost = ball.update()

        if lifeLost:
            lives -= 1
            ball.reset()
            print(lives)

        # Display
        striker.display()
        ball.display()

        for block in listOfBlocks:
            block.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()