import random
import time


# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (59, 130, 246)
LIGHT_BLUE = (96, 165, 250)
RED = (239, 68, 68)
LIGHT_RED = (248, 113, 113)
YELLOW = (250, 204, 21)
GRAY = (30, 30, 30)
GREEN = (34, 197, 94)

# 게임 설정
GRID_SIZE = 20
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 100  # 점수판 공간

# 화면 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("스네이크 배틀")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Snake:
    def __init__(self, x, y, color, light_color):
        self.body = [(x, y)]
        self.direction = (0, 0)
        self.color = color
        self.light_color = light_color
        self.alive = True
    
    def move(self, current_length):
        if not self.alive or self.direction == (0, 0):
            return
        
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_SIZE, (head_y + dy) % GRID_SIZE)
        
        self.body.insert(0, new_head)
        # 시간에 따른 길이로 제한
        if len(self.body) > current_length:
            self.body.pop()
    
    def check_collision(self, other_snake):
        if not self.alive:
            return False
        
        head = self.body[0]
        
        # 자기 몸과 충돌
        if head in self.body[1:]:
            return True
        
        # 상대 뱀과 충돌
        if head in other_snake.body:
            return True
        
        return False
    
    def draw(self, surface):
        if not self.alive:
            return
        
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + 100, CELL_SIZE - 2, CELL_SIZE - 2)
            if i == 0:
                pygame.draw.rect(surface, self.color, rect, border_radius=3)
                # 머리에 빛나는 효과
                pygame.draw.rect(surface, self.color, rect, 2, border_radius=3)
            else:
                pygame.draw.rect(surface, self.light_color, rect, border_radius=2)

def generate_food(snake1, snake2):
    while True:
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if food not in snake1.body and food not in snake2.body:
            return food

def draw_text(surface, text, x, y, font_obj, color=WHITE):
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def main():
    # 게임 변수
    snake1 = Snake(3, 10, BLUE, LIGHT_BLUE)
    snake2 = Snake(16, 10, RED, LIGHT_RED)
    snake1.direction = (1, 0)
    snake2.direction = (-1, 0)
    
    food_list = [generate_food(snake1, snake2) for _ in range(3)]
    
    scores = [0, 0]
    game_state = "playing"  # playing, gameover, menu
    round_start_time = time.time()
    current_length = 1
    winner_text = ""
    game_winner = None
    
    running = True
    
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_state == "menu" or game_state == "gameover":
                    if event.key == pygame.K_SPACE:
                        if game_winner:
                            scores = [0, 0]
                            game_winner = None
                        
                        # 게임 재시작
                        snake1 = Snake(3, 10, BLUE, LIGHT_BLUE)
                        snake2 = Snake(16, 10, RED, LIGHT_RED)
                        snake1.direction = (1, 0)
                        snake2.direction = (-1, 0)
                        food_list = [generate_food(snake1, snake2) for _ in range(3)]
                        game_state = "playing"
                        round_start_time = time.time()
                        current_length = 1
                        winner_text = ""
                    elif event.key == pygame.K_r:
                        scores = [0, 0]
                        game_winner = None
                        game_state = "menu"
                
                # 플레이어 1 (WASD)
                if game_state == "playing":
                    if event.key == pygame.K_w and snake1.direction != (0, 1):
                        snake1.direction = (0, -1)
                    elif event.key == pygame.K_s and snake1.direction != (0, -1):
                        snake1.direction = (0, 1)
                    elif event.key == pygame.K_a and snake1.direction != (1, 0):
                        snake1.direction = (-1, 0)
                    elif event.key == pygame.K_d and snake1.direction != (-1, 0):
                        snake1.direction = (1, 0)
                    
                    # 플레이어 2 (방향키)
                    if event.key == pygame.K_UP and snake2.direction != (0, 1):
                        snake2.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake2.direction != (0, -1):
                        snake2.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake2.direction != (1, 0):
                        snake2.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake2.direction != (-1, 0):
                        snake2.direction = (1, 0)
        
        # 게임 로직
        if game_state == "playing":
            # 시간에 따른 뱀 길이 계산 (2초마다 1칸)
            elapsed_time = time.time() - round_start_time
            round_time = int(elapsed_time)
            current_length = int(elapsed_time / 2) + 1
            
            # 뱀 이동
            snake1.move(current_length)
            snake2.move(current_length)
            
            # 먹이 먹기
            if snake1.body[0] in food_list:
                food_list.remove(snake1.body[0])
                scores[0] += 10
                if scores[0] >= 500:
                    game_state = "gameover"
                    game_winner = 1
                    winner_text = "플레이어 1 최종 승리!"
                food_list.append(generate_food(snake1, snake2))
            
            if snake2.body[0] in food_list:
                food_list.remove(snake2.body[0])
                scores[1] += 10
                if scores[1] >= 500:
                    game_state = "gameover"
                    game_winner = 2
                    winner_text = "플레이어 2 최종 승리!"
                food_list.append(generate_food(snake1, snake2))
            
            # 충돌 체크
            if snake1.check_collision(snake2):
                kill_bonus = 50 + (round_time * 2)
                scores[1] += kill_bonus
                if scores[1] >= 500:
                    game_state = "gameover"
                    game_winner = 2
                    winner_text = "플레이어 2 최종 승리!"
                else:
                    game_state = "gameover"
                    winner_text = f"플레이어 2 라운드 승리! +{kill_bonus}점"
            
            if snake2.check_collision(snake1):
                kill_bonus = 50 + (round_time * 2)
                scores[0] += kill_bonus
                if scores[0] >= 500:
                    game_state = "gameover"
                    game_winner = 1
                    winner_text = "플레이어 1 최종 승리!"
                else:
                    game_state = "gameover"
                    winner_text = f"플레이어 1 라운드 승리! +{kill_bonus}점"
        
        # 그리기
        screen.fill(BLACK)
        
        # 점수판
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 100))
        
        # 점수
        draw_text(screen, f"플레이어 1: {scores[0]}", WIDTH // 4, 30, font, BLUE)
        draw_text(screen, f"플레이어 2: {scores[1]}", WIDTH * 3 // 4, 30, font, RED)
        draw_text(screen, "목표: 500점", WIDTH // 2, 60, small_font, YELLOW)
        
        if game_state == "playing":
            kill_bonus = 50 + (round_time * 2)
            draw_text(screen, f"시간: {round_time}초 | 킬: {kill_bonus}점 | 길이: {current_length}", 
                     WIDTH // 2, 85, small_font, WHITE)
        
        # 게임판 배경
        pygame.draw.rect(screen, GRAY, (0, 100, WIDTH, HEIGHT - 100))
        
        # 먹이
        for food_x, food_y in food_list:
            pygame.draw.circle(screen, YELLOW, 
                             (food_x * CELL_SIZE + CELL_SIZE // 2, 
                              food_y * CELL_SIZE + CELL_SIZE // 2 + 100), 
                             CELL_SIZE // 2 - 2)
        
        # 뱀
        snake1.draw(screen)
        snake2.draw(screen)
        
        # 게임 오버 화면
        if game_state == "gameover":
            overlay = pygame.Surface((WIDTH, HEIGHT - 100))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 100))
            
            draw_text(screen, winner_text, WIDTH // 2, HEIGHT // 2 - 20, font, GREEN)
            if game_winner:
                draw_text(screen, "스페이스: 새 게임 | R: 점수 초기화", 
                         WIDTH // 2, HEIGHT // 2 + 30, small_font, WHITE)
            else:
                draw_text(screen, "스페이스: 다음 라운드 | R: 점수 초기화", 
                         WIDTH // 2, HEIGHT // 2 + 30, small_font, WHITE)
        
        if game_state == "menu":
            overlay = pygame.Surface((WIDTH, HEIGHT - 100))
            overlay.set_alpha(220)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 100))
            
            draw_text(screen, "스네이크 배틀", WIDTH // 2, HEIGHT // 2 - 60, font, GREEN)
            draw_text(screen, "플레이어 1: W/A/S/D", WIDTH // 2, HEIGHT // 2 - 10, small_font, BLUE)
            draw_text(screen, "플레이어 2: 방향키", WIDTH // 2, HEIGHT // 2 + 20, small_font, RED)
            draw_text(screen, "스페이스를 눌러 시작!", WIDTH // 2, HEIGHT // 2 + 60, small_font, YELLOW)
        
        pygame.display.flip()
        clock.tick(10)  # 10 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()
