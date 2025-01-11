import pygame, sys, random
from solver import Solver
from particle import Particle
from rope import Rope, RopeParticle
from pygame import Vector2 as vec2
from timer import Timer

pygame.init()
# pygame.font.

WIDTH = 800
HEIGHT = 800

class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.solid_particles = []
        # self.solid_particles.append(Particle(4, "blue", vec2(200, 400), anchorpoint=True))
        # self.solid_particles.append(Particle(4, "blue", vec2(208, 400), anchorpoint=True))
        # self.solid_particles.append(Particle(4, "blue", vec2(216, 400), anchorpoint=True))
        # self.solid_particles.append(Particle(4, "blue", vec2(224, 400), anchorpoint=True))
        # self.solid_particles.append(Particle(4, "blue", vec2(232, 400), anchorpoint=True))
        radius = 4
        x, y = 200, 400
        for i in range(20):
            self.solid_particles.append(Particle(radius, "black", vec2(x+i * (radius*2), y), anchorpoint=True))

        # radius = 4
        # x, y = 500, 500
        # for i in range(20):
        #     self.solid_particles.append(Particle(radius, "black", vec2(x+i * (radius*2), y), anchorpoint=True))

        # self.solid_particles.append(Particle(10, "blue", vec2(240, 400), anchorpoint=True))
        # self.solid_particles.append(Particle(10, "blue", vec2(280, 400), anchorpoint=True))
        # self.solid_particles.append(Particle(10, "blue", vec2(320, 400), anchorpoint=True))

        self.display = pygame.Surface((WIDTH, HEIGHT))

        self.boundry_radius = 300
        self.boundry_pos = vec2(WIDTH/2, HEIGHT/2)
        self.circle = False
        self.debug = False
        self.color_mode = True
        self.use_velo_color = True


        self.grid_count = 100

        # vec2(250, 200)
        # vec2(250, 200), vec2(340, 220)
        self.rope1 = Rope([], rope_radius=4, length=40, color=(0, 255, 0), use_velocity_color=True, spawnPos=vec2(200, 200))
        # self.rope2 = Rope([], rope_radius=4, length=30, color="orange", use_velocity_color=False, spawnPos=vec2(320, 300))
        self.rope3 = Rope([vec2(400, 300)], rope_radius=4, length=20, color=(245, 147, 217), use_velocity_color=True, spawnPos=vec2(400, 400))

        # self.rope3 = Rope([vec2(620, 250), vec2(520, 250)], rope_radius=4, length=10, color="orange")

        # particle for particle in self.rope.rope_particles
        # particle for particle in self.solid_particles
        initial_particles = []
        initial_particles += [ropeParticle for ropeParticle in self.rope1.rope_particles]
        # initial_particles += [ropeParticle for ropeParticle in self.rope2.rope_particles]
        initial_particles += [ropeParticle for ropeParticle in self.rope3.rope_particles]

        self.solver = Solver(initial_particles, self.boundry_radius, self.boundry_pos, 8, vec2(WIDTH, HEIGHT), self.circle, self.grid_count, self.debug)

        self.spawn_timer = Timer(10)
        self.spawn_timer.start(loop=True)
        self.max_objects = len(self.solver.particles) + 300

    def run(self):
        clicked = False
        # circle = True
        while True:
            self.screen.fill("gray")

            if self.circle:
                self.solver.bounding = "circle"
                pygame.draw.circle(self.screen, "white", self.boundry_pos, self.boundry_radius)

            if self.color_mode:
                self.screen.blit(self.display, (0, 0))

            dt = self.clock.tick(60) / 1000
            
            if self.debug:
                grid_size = (WIDTH/self.grid_count)
                for i in range(self.grid_count):
                    for j in range(self.grid_count):
                        x = i * grid_size
                        y = j * grid_size
                        pygame.draw.rect(self.screen, (0, 0, 0, 0), ((x, y), (grid_size, grid_size)), width=1)
            
            if self.color_mode:
                self.solver.update(self.display, dt)
            else:
                self.solver.update(self.screen, dt)

            self.render_text(self.clock.get_fps(), (255, 255, 0), (10, 0), 30)
            self.render_text(len(self.solver.particles), (255, 255, 0), (10, 30), 30)

            if self.spawn_timer.has_expired() and len(self.solver.particles) + 1 <= self.max_objects:
                random_radius = random.randint(5, 8)
                random_radius = 4
                if self.use_velo_color:
                    color = "blue"
                else:
                    color = self.generate_random_color()
                self.solver.particles.append(Particle(random_radius, color, vec2(WIDTH/2, HEIGHT/2), use_velocity_color=(True if self.use_velo_color else False)))
                self.solver.particles[-1].setVelocity(vec2(0, 0), dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = False
                
            if clicked:
                mouse_buttons = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if mouse_buttons[0]:
                    self.solver.mousePull(vec2(mouse_pos[0], mouse_pos[1]))
                if mouse_buttons[2]:
                    self.solver.mousePush(vec2(mouse_pos[0], mouse_pos[1]))

            
                        # self.render_text(f"{i};{j}", (255, 255, 0), (x, y), 10)

            
            pygame.display.update()

    def render_text(self, what, color, where, size):
        font = pygame.font.SysFont('Comic Sans MS', size)
        text = font.render(str(round(what, 2)) if isinstance(what, float) else str(what), 1, pygame.Color(color))
        self.screen.blit(text, where)

    def generate_random_color(self):
        # Generate random values for Red, Green, and Blue
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

if __name__ == "__main__":
    Simulation().run()

            