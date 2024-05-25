from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 8

# Начальная позиция
POSITION = (0, 0)

# Дефолтный цвет
DEFAULT_COLOR = (255, 255, 255)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """
    Функция обработки действий пользователя

    Обрабатывает нажатия клавиш, чтобы изменить направление движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject():
    """
    Родительский класс, методы и атрибуты которого
    наследуются в дочерних классах
    """

    def __init__(self, body_color=DEFAULT_COLOR, position=POSITION,
                 grid_size=GRID_SIZE, width=SCREEN_WIDTH,
                 height=SCREEN_HEIGHT) -> None:
        self.body_color = body_color
        self.position = position
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.center = ((self.width // 2), (self.height // 2))

    def draw(self):
        """
        Метод draw, предназначен для переопределения
        в дочерних классах, отвечает за отрисовку объектов на игровом поле
        """
        pass

    def reset(self):
        """
        Метод reset, предназначен для переопределения
        в дочерних классах, отвечает за сброс атрибутов объектов класса
        """


class Apple(GameObject):
    """
    Класс Apple, наследуется от родительского GameObject
    Отвечает за отрисовку яблока на игровом поле
    """

    def __init__(self, body_color=DEFAULT_COLOR, position=POSITION,
                 grid_size=GRID_SIZE, width=SCREEN_WIDTH,
                 height=SCREEN_HEIGHT) -> None:
        super().__init__(body_color, position, grid_size, width, height)
        self.position = self.randomize_position(
            self.width, self.height, self.grid_size)
        self.body_color = APPLE_COLOR

    def randomize_position(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                           grid_size=GRID_SIZE):
        """
        Метод randomize_position, генерирует случайные числа
        в пределах игрового поля и возвращает кортеж состоящий из X и Y
        координат яблока
        """
        position_x = (randint(0, width)) // grid_size * grid_size
        position_y = (randint(0, height)) // grid_size * grid_size
        self.position = position_x, position_y
        return self.position

    def draw(self):
        """Метод draw, отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """
        Метод reset, при столкновении змеи с собой,
        происходит перерисовка игрового поля,
        происходит генерация новых координат и отрисовка объекта
        """
        screen.fill((BOARD_BACKGROUND_COLOR))
        self.randomize_position()
        self.draw()


class Snake(GameObject):
    """
    Класс Snake, наследуется от родительского GameObject
    Отвечает за отрисовку змейки на игровом поле
    """

    def __init__(self, body_color=DEFAULT_COLOR, position=POSITION,
                 grid_size=GRID_SIZE, width=SCREEN_WIDTH,
                 height=SCREEN_HEIGHT) -> None:
        super().__init__(body_color, position, grid_size, width, height)
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.last = None
        self.positions = [self.center]
        self.direction = choice([UP, RIGHT, LEFT, DOWN])
        self.next_direction = None

    def draw(self):
        """Метод draw, отрисовывает змейку на игровой поверхности"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        """Отрисовка основания змейки"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента змеи"""
        if self.last:
            self.positions.pop()
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод, отвечающий за обновление направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод move, отвечающий за отрисовку движения змейки"""
        head_pos = self.get_head_position()
        next_pos_x = (head_pos[0] + self.direction[0]
                      * self.grid_size) % SCREEN_WIDTH
        next_pos_y = (head_pos[1] + self.direction[1]
                      * self.grid_size) % SCREEN_HEIGHT
        self.positions.insert(0, (next_pos_x, next_pos_y))
        self.last = self.positions[-1]
        self.draw()

    def get_head_position(self):
        """Метод, отвечающий за определение основания змейки"""
        return self.positions[0]

    def is_eat_apple(self, apple_pos):
        """
        Метод, проверяющий съела ли змейка яблока,
        если true то змейка растет
        """
        if self.positions[0] == apple_pos:
            self.positions.insert(0, apple_pos)
            return True

    def reset(self):
        """
        При столкновении змейки с собой, происходит очищение позиций,
        и возврат к изначалной точке начала игры
        """
        self.positions.clear()
        self.positions.append(self.center)
        self.length = 1
        self.direction = choice([UP, RIGHT, LEFT, DOWN])


def main():
    """Основной цикл игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    apple.draw()
    snake.draw()

    while True:
        clock.tick(SPEED)
        snake.move()

        if snake.is_eat_apple(apple.position):
            apple.randomize_position()
            apple.draw()
            snake.length += 1
        handle_keys(snake)
        snake.update_direction()

        if snake.length > 4:
            if (snake.positions[0] in
                    snake.positions[(len(snake.positions) - 3) * -1:]):
                snake.reset()
                apple.reset()
        pygame.display.update()


if __name__ == '__main__':
    main()
