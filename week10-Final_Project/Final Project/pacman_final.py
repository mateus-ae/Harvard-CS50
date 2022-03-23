import pygame
import random


pygame.init()

WIDTH = 900
HEIGHT = 720

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_BLUE = (131, 238, 255)
ORANGE = (255, 131, 0)
PINK = (255, 53, 184)

GRID = {'rows': 30, 'columns': 28}
# Cell size will be 600 px // 30 = 20px
CELL_SIZE = HEIGHT // GRID['rows']
# Speed will be measured in how many cells in the grid pacman will advance
SPEED = 1
# Text font for the game
FONT = pygame.font.SysFont("arial", 22, True, False)

# Ghost's movement keys
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4


screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)


class Background:
    def __init__(self, size, pacman_instance):
        self.pacman = pacman_instance
        self.characters = []
        self.game_state = "play"
        # Defines the ratio for the ghost's direction change
        self.direction_shift = 0
        self.size = size
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
        # Define starting score (It's -1 because pacman starts)
        self.score = 0
        # Define maximum score:
        self.max_score = self.get_max_score()
        # Define player's lives
        self.player_lives = 3

    def get_max_score(self):
        # Based on the how many '1' are in the matrix
        max_score = 0

        for row in self.matrix:
            for content in row:
                if content == 1:
                    max_score += 1

        return max_score

    def add_character(self, character):
        # Add pacman and ghosts
        self.characters.append(character)

    def draw_row(self, row_number, row_content):
        # Draw the game background based on the rows of the matrix
        for column_number, column_content in enumerate(row_content):
            x = column_number * self.size
            y = row_number * self.size

            if column_content == 2:
                color = BLUE
            else:
                color = BLACK

            pygame.draw.rect(screen, color, (x, y, self.size, self.size))

            if column_content == 1:
                pygame.draw.circle(screen, YELLOW, (x + self.size // 2, y + self.size // 2), self.size // 10)

    def change_game_state(self, state):
        # Game states - Play, Pause, Game Over, Win
        self.game_state = state

    def draw(self, screen):
        # Draw any state of the game
        if self.game_state == "play":
            self.draw_game(screen)
        elif self.game_state == "pause":
            self.draw_game(screen)
            self.draw_pause(screen)
        elif self.game_state == "gameover":
            self.draw_game(screen)
            self.draw_gameover(screen)
        elif self.game_state == "win":
            self.draw_game(screen)
            self.draw_win(screen)

    def draw_player_info(self, screen):
        # Draw lives and score
        x_position = (self.size * GRID['columns']) + 30
        y_position = 50
        score_img = FONT.render(f"Score: {self.score}", True, YELLOW)
        lives_img = FONT.render(f"Lives: {self.player_lives}", True, YELLOW)
        screen.blit(score_img, (x_position, y_position))
        screen.blit(lives_img, (x_position, y_position + 50))

    def draw_win(self, screen):
        # Draw winning text
        text_image = FONT.render("Y O U  W O N ! ! !", True, WHITE)
        text_initial_x_coordinate = (WIDTH - text_image.get_width()) // 2
        text_initial_y_coordinate = (HEIGHT - text_image.get_height()) // 2
        screen.blit(text_image, (text_initial_x_coordinate, text_initial_y_coordinate))

    def draw_gameover(self, screen):
        # Draw gameover text
        text_image = FONT.render("G A M E  O V E R", True, WHITE)
        text_initial_x_coordinate = (WIDTH - text_image.get_width()) // 2
        text_initial_y_coordinate = (HEIGHT - text_image.get_height()) // 2
        screen.blit(text_image, (text_initial_x_coordinate, text_initial_y_coordinate))

    def draw_pause(self, screen):
        # Draw pause text
        text_image = FONT.render("P A U S E", True, WHITE)
        text_initial_x_coordinate = (WIDTH - text_image.get_width()) // 2
        text_initial_y_coordinate = (HEIGHT - text_image.get_height()) // 2
        screen.blit(text_image, (text_initial_x_coordinate, text_initial_y_coordinate))

    def draw_game(self, screen):
        # Draw every row of the game
        for row_number, row_content in enumerate(self.matrix):
            self.draw_row(row_number, row_content)

        self.draw_player_info(screen)

    def get_directions(self, row, column):
        # Define possible movements for the ghost
        directions = []

        if self.matrix[row - 1][column] != 2:
            directions.append(UP)

        if self.matrix[row + 1][column] != 2:
            directions.append(DOWN)

        if self.matrix[row][column - 1] != 2:
            directions.append(LEFT)

        if self.matrix[row][column + 1] != 2:
            directions.append(RIGHT)

        return directions

    def game_actions(self):
        # Define possible actions for each state of the game
        if self.game_state == "play":
            self.validate_movement()
        elif self.game_state == "pause":
            self.pause_game()
        elif self.game_state == "gameover":
            self.end_game()

    def end_game(self):
        pass

    def validate_movement(self):
        # It takes any of the characters for movement validation
        for character in self.characters:
            row = int(character.row)
            col = int(character.column)
            row_movement_attempt = int(character.row_movement_attempt)
            col_movement_attempt = int(character.col_movement_attempt)
            directions = self.get_directions(row, col)

            # Decide which direction ghost should take

            if len(directions) >= 3 and self.direction_shift == 0:
                character.decide_direction(directions)
            self.direction_shift += 1

            if self.direction_shift == 3:
                self.direction_shift = 0

            # Defines life loss when pacman hits a ghost
            if (
                    isinstance(character, Ghost) and character.row == self.pacman.row
                    and character.column == self.pacman.column
            ):
                self.player_lives -= 1

                if self.player_lives <= 0:
                    self.change_game_state("gameover")
                else:
                    self.pacman.row = 1
                    self.pacman.column = 1

            else:
                if (
                        0 <= col_movement_attempt < GRID['columns'] and 0 <= row_movement_attempt < GRID['rows']
                        and self.matrix[row_movement_attempt][col_movement_attempt] != 2
                ):
                    character.allow_movement()

                    if isinstance(character, Pacman) and self.matrix[row][col] == 1:
                        self.score += 1
                        self.matrix[row][col] = 0
                        if self.score >= self.max_score:
                            self.change_game_state("win")

                else:
                    character.deny_movement(directions)

    def pause_game(self):
        pass

    def event_action(self, events):
        # Control events for the background
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if self.game_state == "play":
                        self.change_game_state("pause")
                    else:
                        self.change_game_state("play")


class Pacman:
    def __init__(self, size):
        # Pacman starts at row 1, col 1
        self.row = 1
        self.column = 1
        # Define Pacman's size
        self.x_center = WIDTH // 2
        self.y_center = HEIGHT // 2
        self.size = size
        self.radius = self.size // 2
        # Pacman starts with no movement
        self.x_movement = 0
        self.y_movement = 0
        # Create movement attempt variables. They will be validated to allow the movement through the background
        # Validation is made by the Background class
        self.col_movement_attempt = self.column
        self.row_movement_attempt = self.row
        # Variables for controlling pacman's mouth opening
        self.mouth_opening = 0
        self.open_mouth_movement = 3

    def move(self):
        # Define where pacman is trying to go
        self.row_movement_attempt = self.row + self.y_movement
        self.col_movement_attempt = self.column + self.x_movement

        self.x_center = self.column * self.size + self.radius
        self.y_center = self.row * self.size + self.radius

    def allow_movement(self):
        # Allow movement if pacman tries to go to a valid position
        self.row = self.row_movement_attempt
        self.column = self.col_movement_attempt

    def deny_movement(self, directions):
        # Denies movement if pacman tries to go to a invalid position
        self.row_movement_attempt = self.row
        self.col_movement_attempt = self.column

    def draw(self, screen):
        # Draw Pacman
        pygame.draw.circle(screen, YELLOW, (self.x_center, self.y_center), self.radius)

        # Control pacman's mouth
        self.mouth_opening += self.open_mouth_movement
        if self.mouth_opening >= self.radius:
            self.open_mouth_movement = -3
        elif self.mouth_opening <= 0:
            self.open_mouth_movement = 3

        # Draw Pacman's mouth
        start_coordinate = (self.x_center, self.y_center)
        first_lip = (self.x_center + self.radius, self.y_center - (self.mouth_opening * 0.50))
        second_lip = (self.x_center + self.radius, self.y_center + (self.mouth_opening * 0.50))
        mouth_coordinates = (start_coordinate, first_lip, second_lip)

        pygame.draw.polygon(screen, BLACK, mouth_coordinates)

        # Draw Pacman's eye
        eye_x = int(self.x_center + self.radius / 3)
        eye_y = int(self.y_center - self.radius / 2)
        eye_radius = int(self.radius / 6)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), eye_radius)

    def event_action(self, events):
        # Control events for pacman
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.x_movement = SPEED
                elif e.key == pygame.K_LEFT:
                    self.x_movement = -SPEED
                elif e.key == pygame.K_UP:
                    self.y_movement = -SPEED
                elif e.key == pygame.K_DOWN:
                    self.y_movement = SPEED
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or pygame.K_LEFT:
                    self.x_movement = 0
                if e.key == pygame.K_UP or pygame.K_DOWN:
                    self.y_movement = 0

    def decide_direction(self, directions):
        return


class Ghost:
    def __init__(self, color, size):
        self.column = 13
        self.row = 15
        self.speed = SPEED
        self.direction = DOWN
        self.size = size
        self.color = color
        # Create movement attempt variables. They will be validated to allow the movement through the background
        # Validation is made by the Background class
        self.col_movement_attempt = self.column
        self.row_movement_attempt = self.row

    def draw(self, screen):
        # Breaks cell into 8 porttions and defines ghost initial position reference
        cell_portion = self.size // 8
        x_initial_position = self.column * self.size
        y_initial_position = self.row * self.size

        # Define the coordinates for the ghost drawing
        ghost_draw_coordinates = [
            (x_initial_position, y_initial_position + self.size),
            (x_initial_position + cell_portion, y_initial_position + 3 * cell_portion),
            (x_initial_position + 2 * cell_portion, y_initial_position + cell_portion),
            (x_initial_position + 3 * cell_portion, y_initial_position),
            (x_initial_position + 5 * cell_portion, y_initial_position),
            (x_initial_position + 6 * cell_portion, y_initial_position + cell_portion),
            (x_initial_position + 7 * cell_portion, y_initial_position + 3 * cell_portion),
            (x_initial_position + self.size, y_initial_position + self.size),
            (x_initial_position + 7 * cell_portion, y_initial_position + 7 * cell_portion),
            (x_initial_position + 6 * cell_portion, y_initial_position + self.size),
            (x_initial_position + 5 * cell_portion, y_initial_position + 7 * cell_portion),
            (x_initial_position + 4 * cell_portion, y_initial_position + self.size),
            (x_initial_position + 3 * cell_portion, y_initial_position + 7 * cell_portion),
            (x_initial_position + 2 * cell_portion, y_initial_position + self.size),
            (x_initial_position + cell_portion, y_initial_position + 7 * cell_portion)
        ]

        # Draw the ghost
        pygame.draw.polygon(screen, self.color, ghost_draw_coordinates)

        # Define the ghost's eyes
        eye_external_radius = cell_portion * 0.9
        eye_internal_radius = cell_portion // 2

        left_eye_x = int(x_initial_position + cell_portion * 2.5)
        left_eye_y = int(y_initial_position + cell_portion * 2.5)

        right_eye_x = int(x_initial_position + cell_portion * 5.5)
        right_eye_y = int(y_initial_position + cell_portion * 2.5)

        # Draw the ghost's  left eye
        pygame.draw.circle(screen, WHITE, (left_eye_x, left_eye_y), eye_external_radius)
        pygame.draw.circle(screen, BLACK, (left_eye_x, left_eye_y), eye_internal_radius)

        # Draw the ghost's right eye
        pygame.draw.circle(screen, WHITE, (right_eye_x, right_eye_y), eye_external_radius)
        pygame.draw.circle(screen, BLACK, (right_eye_x, right_eye_y), eye_internal_radius)

    def move(self):
        # Defines where the ghost is trying to move to.
        if self.direction == UP:
            self.row_movement_attempt -= self.speed
        elif self.direction == DOWN:
            self.row_movement_attempt += self.speed
        elif self.direction == LEFT:
            self.col_movement_attempt -= self.speed
        elif self.direction == RIGHT:
            self.col_movement_attempt += self.speed

    def change_direction(self, directions):
        # Randomly pics a direction for a ghost
        self.direction = random.choice(directions)

    def decide_direction(self, directions):
        # Decides where the ghost should move to
        self.change_direction(directions)

    def allow_movement(self):
        # Allow a ghost's movement if it tries to go to a valid position
        self.row = self.row_movement_attempt
        self.column = self.col_movement_attempt

    def deny_movement(self, directions):
        # Denies a ghost's movement if it tries to go to an invalid positon
        self.row_movement_attempt = self.row
        self.col_movement_attempt = self.column

        self.change_direction(directions)


if __name__ == "__main__":
    # Define the scale for all the characters and background
    cell_size = CELL_SIZE

    # Create characters and background
    pacman = Pacman(cell_size)
    ghost1 = Ghost(RED, cell_size)
    ghost2 = Ghost(LIGHT_BLUE, cell_size)
    ghost3 = Ghost(ORANGE, cell_size)
    ghost4 = Ghost(PINK, cell_size)
    background = Background(cell_size, pacman)

    characters = [pacman, ghost1, ghost2, ghost3, ghost4]

    for character in characters:
        background.add_character(character)

    while True:
        # Rules
        for character in characters:
            character.move()

        background.game_actions()

        # Draw Background and Pacman
        screen.fill(BLACK)
        background.draw(screen)

        for character in characters:
            character.draw(screen)

        pygame.display.update()
        pygame.time.delay(100)

        # Listen for events
        events = pygame.event.get()

        pacman.event_action(events)
        background.event_action(events)

