import pygame
import random
import sys
import pygame.freetype
from codeStream import config


class KnowledgeRain:
    def __init__(self, width, height, knowledge_points, fullscreen=False):
        pygame.init()
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("考研知识代码流，你的无聊陪伴助手")

        self.BLACK = config.BLACK
        self.GREEN = config.GREEN
        self.WHITE = config.WHITE

        self.font = pygame.freetype.SysFont('simsun', config.FONT_SIZE) \
            if 'simsun' in pygame.freetype.get_fonts() else pygame.freetype.Font(None, config.FONT_SIZE)
        self.large_font = pygame.freetype.SysFont('simsun', config.LARGE_FONT_SIZE) \
            if 'simsun' in pygame.freetype.get_fonts() else pygame.freetype.Font(None, config.LARGE_FONT_SIZE)

        self.clock = pygame.time.Clock()

        self.raindrops = []
        self.speed = 2
        self.density = 10
        self.paused = False

        self.grid_size = config.FONT_SIZE * 2
        self.grid_width = self.width // self.grid_size
        self.grid_height = self.height // self.grid_size
        self.grid = [[False for _ in range(self.grid_height)] for _ in range(self.grid_width)]

        self.knowledge_points = knowledge_points
        self.knowledge_list = list(self.knowledge_points.keys())
        self.knowledge_index = 0
        self.active_knowledge = set()

    def get_text_width(self, text):
        return self.font.get_rect(text)[2]

    def get_next_knowledge(self):
        start_index = self.knowledge_index
        while True:
            knowledge = self.knowledge_list[self.knowledge_index]
            self.knowledge_index = (self.knowledge_index + 1) % len(self.knowledge_list)
            if knowledge not in self.active_knowledge:
                return knowledge
            if self.knowledge_index == start_index:
                return None  # 如果所有知识点都在屏幕上，返回None

    def find_empty_cell(self, text_width):
        cells_needed = (text_width + self.grid_size - 1) // self.grid_size
        start_x = random.randint(0, self.grid_width - cells_needed)

        for x in range(start_x, self.grid_width - cells_needed + 1):
            if all(not self.grid[x + i][0] for i in range(cells_needed)):
                return x, 0, cells_needed

        for x in range(0, start_x):
            if all(not self.grid[x + i][0] for i in range(cells_needed)):
                return x, 0, cells_needed

        return None

    def is_overlapping(self, new_drop):
        new_rect = self.font.get_rect(new_drop[3])
        new_rect.topleft = (new_drop[0], new_drop[1])
        for drop in self.raindrops:
            existing_rect = self.font.get_rect(drop[3])
            existing_rect.topleft = (drop[0], drop[1])
            if new_rect.colliderect(existing_rect):
                return True
        return False

    def create_raindrop(self):
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
        if not self.paused:
            raindrops_to_remove = []
            for drop in self.raindrops:
                old_grid_y = drop[5]
                drop[1] += drop[2]  # Update actual y coordinate
                new_grid_y = int(drop[1] // self.grid_size)

                if new_grid_y != old_grid_y:
                    if new_grid_y >= self.grid_height:
                        # If raindrop goes off the screen, mark it for removal
                        for i in range(drop[6]):  # drop[6] stores the number of cells occupied by this raindrop
                            self.grid[drop[4] + i][old_grid_y] = False  # Clear old position
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
        for drop in self.raindrops:
            text_surface, _ = self.font.render(drop[3], self.GREEN)
            self.screen.blit(text_surface, (drop[0], drop[1]))

    def adjust_density(self, change):
        self.density = max(config.DENSITY_MIN, min(config.DENSITY_MAX, self.density + change))
        print(f"当前密度：{self.density}")

    def show_detail(self, knowledge):
        self.paused = True
        detail_surface = pygame.Surface((self.width, self.height))
        detail_surface.fill(self.BLACK)

        title, _ = self.large_font.render(knowledge, self.GREEN)
        detail_surface.blit(title, (config.TEXT_X_OFFSET, config.TEXT_X_OFFSET))

        explanation = self.knowledge_points[knowledge]
        lines = []
        current_line = ""
        max_width = self.width - config.TEXT_MAX_WIDTH_OFFSET

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
            detail_surface.blit(exit_text,
                                (self.width - config.TEXT_EXIT_X_OFFSET, self.height - config.TEXT_EXIT_Y_OFFSET))
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