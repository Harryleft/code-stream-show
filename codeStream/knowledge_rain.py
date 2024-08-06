import pygame
import random
import sys
import pygame.freetype
from codeStream import config


class KnowledgeRain:
    """
    A class to create and manage a 'knowledge rain' game using Pygame.

    This class handles the creation, movement, and display of knowledge points
    falling from the top of the screen, as well as user interactions.
    """

    def __init__(self, width, height, knowledge_points, fullscreen=False):
        """
        Initialize the KnowledgeRain game.

        Args:
            width (int): The width of the game window.
            height (int): The height of the game window.
            knowledge_points (dict): A dictionary of knowledge points and
                                     their explanations.
            fullscreen (bool): Whether to run the game in fullscreen mode.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("考研知识代码流，你的无聊陪伴助手")

        # Define colors
        self.BLACK = config.BLACK
        self.GREEN = config.GREEN
        self.WHITE = config.WHITE

        # Set up fonts
        self.font = (
            pygame.freetype.SysFont("simsun", config.FONT_SIZE)
            if "simsun" in pygame.freetype.get_fonts()
            else pygame.freetype.Font(None, config.FONT_SIZE)
        )
        self.large_font = (
            pygame.freetype.SysFont("simsun", config.LARGE_FONT_SIZE)
            if "simsun" in pygame.freetype.get_fonts()
            else pygame.freetype.Font(None, config.LARGE_FONT_SIZE)
        )

        self.clock = pygame.time.Clock()

        # Initialize game variables
        self.raindrops = []
        self.speed = 2
        self.density = 10
        self.paused = False

        # Set up grid for managing raindrop positions
        self.grid_size = config.FONT_SIZE * 2
        self.grid_width = self.width // self.grid_size
        self.grid_height = self.height // self.grid_size
        self.grid = [
            [False for _ in range(self.grid_height)] for _ in range(self.grid_width)
        ]

        # Set up knowledge points
        self.knowledge_points = knowledge_points
        self.knowledge_list = list(self.knowledge_points.keys())
        self.knowledge_index = 0
        self.active_knowledge = set()

    def get_text_width(self, text):
        """
        Get the width of a text string when rendered with the current font.

        Args:
            text (str): The text to measure.

        Returns:
            int: The width of the text in pixels.
        """
        return self.font.get_rect(text)[2]

    def get_next_knowledge(self):
        """
        Get the next unused knowledge point from the list.

        Returns:
            str: The next unused knowledge point, or None if all are in use.
        """
        start_index = self.knowledge_index
        while True:
            knowledge = self.knowledge_list[self.knowledge_index]
            self.knowledge_index = (self.knowledge_index + 1) % len(self.knowledge_list)
            if knowledge not in self.active_knowledge:
                return knowledge
            if self.knowledge_index == start_index:
                # If all knowledge points are on screen, return None
                return None

    def find_empty_cell(self, text_width):
        """
        Find an empty cell at the top of the grid for a new raindrop.

        Args:
            text_width (int): The width of the text to be placed.

        Returns:
            tuple: (x, y, cells) coordinates and number of cells needed,
            or None if no space found.
        """
        cells_needed = (text_width + self.grid_size - 1) // self.grid_size
        start_x = random.randint(0, self.grid_width - cells_needed)

        # Check from random start point to the right
        for x in range(start_x, self.grid_width - cells_needed + 1):
            if all(not self.grid[x + i][0] for i in range(cells_needed)):
                return x, 0, cells_needed

        # If not found, check from the left to the start point
        for x in range(0, start_x):
            if all(not self.grid[x + i][0] for i in range(cells_needed)):
                return x, 0, cells_needed

        return None

    def is_overlapping(self, new_drop):
        """
        Check if a new raindrop overlaps with existing ones.

        Args:
            new_drop (list): The new raindrop to check.

        Returns:
            bool: True if overlapping, False otherwise.
        """
        new_rect = self.font.get_rect(new_drop[3])
        new_rect.topleft = (new_drop[0], new_drop[1])
        for drop in self.raindrops:
            existing_rect = self.font.get_rect(drop[3])
            existing_rect.topleft = (drop[0], drop[1])
            if new_rect.colliderect(existing_rect):
                return True
        return False

    def create_raindrop(self):
        """
        Create a new raindrop with a knowledge point.

        Returns: list: A new raindrop [x, y, speed, knowledge, grid_x,
        grid_y, cells], or None if unable to create.
        """
        knowledge = self.get_next_knowledge()
        if knowledge is None:
            return None

        text_width = self.get_text_width(knowledge)
        cell_info = self.find_empty_cell(text_width)
        if cell_info is None:
            return None

        x, y, cells = cell_info
        for i in range(cells):
            self.grid[x + i][y] = True

        real_x = x * self.grid_size
        real_y = 0  # Start from the top of the screen
        speed = random.uniform(self.speed * 0.5, self.speed * 1.5)
        self.active_knowledge.add(knowledge)
        return [real_x, real_y, speed, knowledge, x, y, cells]

    def update_raindrops(self):
        """
        Update the positions of all raindrops and remove those that are
        off-screen.
        """
        if not self.paused:
            raindrops_to_remove = []
            for drop in self.raindrops:
                old_grid_y = drop[5]
                drop[1] += drop[2]  # Update actual y coordinate
                new_grid_y = int(drop[1] // self.grid_size)

                if new_grid_y != old_grid_y:
                    if new_grid_y >= self.grid_height:
                        # If raindrop goes off the screen, mark it for removal
                        for i in range(
                            drop[6]
                        ):  # drop[6] stores the number of cells occupied by
                            # this raindrop
                            self.grid[drop[4] + i][
                                old_grid_y
                            ] = False  # Clear old position
                        self.active_knowledge.discard(drop[3])
                        raindrops_to_remove.append(drop)
                    else:
                        # Update grid state
                        for i in range(drop[6]):
                            self.grid[drop[4] + i][old_grid_y] = False
                            self.grid[drop[4] + i][new_grid_y] = True
                        drop[5] = new_grid_y

            # Remove raindrops that are off the screen
            for drop in raindrops_to_remove:
                self.raindrops.remove(drop)
                new_drop = self.create_raindrop()
                if new_drop:
                    self.raindrops.append(new_drop)

    def draw_raindrops(self):
        """
        Draw all raindrops on the screen.
        """
        for drop in self.raindrops:
            text_surface, _ = self.font.render(drop[3], self.GREEN)
            self.screen.blit(text_surface, (drop[0], drop[1]))

    def adjust_density(self, change):
        """
        Adjust the density of raindrops within defined limits.

        Args:
            change (int): The amount to change the density by.
        """
        self.density = max(
            config.DENSITY_MIN, min(config.DENSITY_MAX, self.density + change)
        )
        print(f"当前密度：{self.density}")

    def show_detail(self, knowledge):
        """
        Display detailed information about a selected knowledge point.

        Args:
            knowledge (str): The knowledge point to display details for.
        """
        self.paused = True
        detail_surface = pygame.Surface((self.width, self.height))
        detail_surface.fill(self.BLACK)

        title, _ = self.large_font.render(knowledge, self.GREEN)
        detail_surface.blit(title, (config.TEXT_X_OFFSET, config.TEXT_X_OFFSET))

        explanation = self.knowledge_points[knowledge]
        max_width = self.width - config.TEXT_MAX_WIDTH_OFFSET

        lines = []
        if "\n" in explanation:
            # If newlines exist, split by newline
            paragraphs = explanation.split("\n")
            for paragraph in paragraphs:
                words = paragraph.split()
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if self.font.get_rect(test_line)[2] < max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                lines.append("")  # Add empty line between paragraphs
        else:
            # If no newlines, split by character
            current_line = ""
            for char in explanation:
                test_line = current_line + char
                if self.font.get_rect(test_line)[2] < max_width:
                    current_line += char
                else:
                    lines.append(current_line)
                    current_line = char
            lines.append(current_line)

        y_offset = config.TEXT_Y_OFFSET

        def render_text():
            """Render the explanation text on the detail surface."""
            line_height = self.font.get_sized_height(config.FONT_SIZE)
            detail_surface.fill(self.BLACK)
            detail_surface.blit(title, (config.TEXT_X_OFFSET, config.TEXT_X_OFFSET))
            y = y_offset
            for line in lines:
                if y + line_height > self.height - config.TEXT_Y_OFFSET:
                    break
                text, _ = self.font.render(line, self.WHITE)
                detail_surface.blit(text, (config.TEXT_X_OFFSET, y))
                y += line_height
            exit_text, _ = self.font.render("点击任意位置返回", self.GREEN)
            detail_surface.blit(
                exit_text,
                (
                    self.width - config.TEXT_EXIT_X_OFFSET,
                    self.height - config.TEXT_EXIT_Y_OFFSET,
                ),
            )
            self.screen.blit(detail_surface, (0, 0))
            pygame.display.flip()

        render_text()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        waiting = False

        self.paused = False

    def run(self):
        """
        Run the main game loop.
        """
        print("开始运行知识雨...")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.key == pygame.K_UP:
                        self.speed = min(config.SPEED_MAX, self.speed + 0.5)
                    elif event.key == pygame.K_DOWN:
                        self.speed = max(config.SPEED_MIN, self.speed - 0.5)
                    elif event.key == pygame.K_RIGHT:
                        self.adjust_density(1)
                    elif event.key == pygame.K_LEFT:
                        self.adjust_density(-1)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    print(f"速度: {self.speed:.1f}, 密度: {self.density}")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for drop in self.raindrops:
                        text_surface, _ = self.font.render(drop[3], self.GREEN)
                        text_rect = text_surface.get_rect(topleft=(drop[0], drop[1]))
                        if text_rect.collidepoint(event.pos):
                            self.show_detail(drop[3])
                            break

            self.screen.fill(self.BLACK)

            # Manage raindrop density
            if len(self.raindrops) < self.density:
                new_drop = self.create_raindrop()
                if new_drop:
                    self.raindrops.append(new_drop)
            elif len(self.raindrops) > self.density:
                drop = self.raindrops.pop()
                for i in range(drop[6]):
                    self.grid[drop[4] + i][drop[5]] = False
                self.active_knowledge.discard(drop[3])

            self.update_raindrops()
            self.draw_raindrops()

            pygame.display.flip()
            self.clock.tick(config.CLOCK_TICK)

        pygame.quit()
