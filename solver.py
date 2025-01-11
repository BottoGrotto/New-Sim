import math, time
from pygame import Vector2 as vec2
import pygame
from rope import RopeParticle




class Solver:
    def __init__(self, particles, boundary_radius, boundary_pos, sub_steps, window_size, circle, grid_size, debug):
        self.particles = particles
        self.gravity = vec2(0, 1000)
        self.boundary_radius = boundary_radius
        self.boundary_pos = boundary_pos
        self.window_size = window_size
        self.grid_size = grid_size
        self.grid_box_size = window_size/grid_size
        self.debug = debug
        # print(self.grid_box_size)

        # self.grid = {}
        # for i in range(grid_size):
        #     for j in range(grid_size):
        #         self.grid[f'{i};{j}'] = []

        self.grid = list(range(grid_size))
        for i in range(grid_size):
            self.grid[i] = list(range(grid_size))
            for j in range(grid_size):
                self.grid[i][j] = []

        self.updateGrid()
        # self.grid_empty = self.grid.copy()
        # print(self.grid)

        self.box_around = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0))

        self.bounding = circle

        self.sub_steps = sub_steps
        self.step_dt = 1/60


    def checkCollisions(self, surf):
        num_objects = len(self.particles)
        start = time.time()

        for i in range(num_objects):
            obj1 = self.particles[i]

            row = int(obj1.pos.x/self.grid_box_size.x)
            col = int(obj1.pos.y/self.grid_box_size.y)
            
            for neighbor in self.box_around:
                neighbor_pos = (row + neighbor[0], col + neighbor[1])
                if neighbor_pos[0] > self.grid_size -1 or neighbor_pos[0] < 0 or neighbor_pos[1] > self.grid_size -1 or neighbor_pos[1] < 0:
                    continue
                # if self.grid[]
                # print(neighbor_pos, f"{row + neighbor[0]};{col + neighbor[1]}")
                if self.debug:
                    rect = ((neighbor_pos[0] * self.grid_box_size.x, neighbor_pos[1] * self.grid_box_size.y), (self.grid_box_size.x, self.grid_box_size.y))
                    if neighbor == (0, 0):
                        pygame.draw.rect(surf, (255, 255, 0), rect)
                    else:
                        pygame.draw.rect(surf, (209, 209, 29), rect)
                    

                # key = f"{neighbor_pos[0]};{neighbor_pos[1]}"

                if not self.grid[neighbor_pos[0]][neighbor_pos[1]]:
                    continue
                
                for j in self.grid[neighbor_pos[0]][neighbor_pos[1]]:
                    if i == j:
                        continue
                    obj2 = self.particles[j]
                    v = obj1.pos - obj2.pos
                    dist_squared = v.x * v.x + v.y * v.y
                    min_dist_squared = (obj1.radius + obj2.radius) ** 2
                    if dist_squared < min_dist_squared:
                        dist = math.sqrt(dist_squared)

                    # dist = math.sqrt(math.pow(v.x, 2) + math.pow(v.y, 2))
                        min_dist = obj1.radius + obj2.radius
                    # if (dist < min_dist):
                        n = v / dist
                        total_mass = math.pow(obj1.radius, 2) + math.pow(obj2.radius, 2)
                        mass_ratio = math.pow(obj1.radius, 2) / total_mass
                        # mass_ratio = 0
                        delta = 0.5 * (min_dist - dist)
                        
                        # if not isinstance(obj1, RopeParticle) and not isinstance(obj2, RopeParticle):
                            # mvb =  + mvb2
                        if obj1.anchorpoint:
                            # n.normalize() * (1 - mass_ratio)
                            obj2.pos -= n.normalize() * obj2.getVelocity().magnitude() * delta
                        else:
                            obj1.pos += n * (1 - mass_ratio) * delta

                        if obj2.anchorpoint:

                            obj1.pos += n.normalize() * obj1.getVelocity().magnitude() * delta
                        else:
                            obj2.pos -= n * (1 - mass_ratio) * delta
                        
        end = time.time()
        # print(end - start)

                        
                # self.grid[f'{row};{col}'].append(partcile)



        # for i in range(num_objects):
        #     obj1 = self.particles[i]
        #     for j in range(num_objects):
        #         if (i == j):
        #             continue
        #         obj2 = self.particles[j]
        #         v = obj1.pos - obj2.pos
        #         dist = math.sqrt(math.pow(v.x, 2) + math.pow(v.y, 2))
        #         min_dist = obj1.radius + obj2.radius
        #         if (dist < min_dist):
        #             n = v / dist
        #             total_mass = math.pow(obj1.radius, 2) + math.pow(obj2.radius, 2)
        #             mass_ratio = math.pow(obj1.radius, 2) / total_mass
        #             delta = 0.5 * (min_dist - dist)

        #             obj1.pos += n * (1 - mass_ratio) * delta
        #             obj2.pos -= n * (1 - mass_ratio) * delta

    def mousePull(self, pos: vec2):
        for particle in self.particles:
            dir = pos - particle.pos
            dist = math.sqrt(math.pow(dir.x, 2) + math.pow(dir.y, 2))
            particle.accelerate(dir * max(0, 10 * (120 - dist)))

    def mousePush(self, pos: vec2):
        for particle in self.particles:
            dir = pos - particle.pos
            dist = math.sqrt(math.pow(dir.x, 2) + math.pow(dir.y, 2))
            particle.accelerate(dir * min(0, -10 * (120 - dist)))

    def render(self, surf):
        start = time.time()
        for particle in self.particles:
            particle.render(surf)
        end = time.time()
        # print(end - start)

    def applyGravity(self):
        for i, particle in enumerate(self.particles):
            if not particle.anchorpoint:
                particle.accelerate(self.gravity)
        # for i in range(len(self.particles)):
            # for j in range(len(self.particles)):
            #     if (i == j):
            #         continue
            #     obj1 = particle
            #     obj2 = self.particles[j]
            #     dir = obj1.pos - obj2.pos
            #     dist = math.sqrt(math.pow(dir.x, 2) + math.pow(dir.y, 2))
            #     particle.accelerate(dir * max(0, 2 * (2 - dist)))
            #     obj2.accelerate(dir * max(0, 2 * (2 - dist)))
        
        
    def updateObjects(self, dt):
        for particle in self.particles:
            if not particle.anchorpoint:
                particle.update(dt)

    def updateGrid(self):
        start = time.time()
        # self.grid = {}
        # for i in range(self.grid_size):
        #     for j in range(self.grid_size):
        #         self.grid[f'{i};{j}'] = []
        
        for row in self.grid:
            for cell in row:
                cell.clear()
        # self.grid = self.grid_empty.copy()
            
        for i, particle in enumerate(self.particles):
           row = int(particle.pos.x/self.grid_box_size.x)
           col = int(particle.pos.y/self.grid_box_size.y)
           self.grid[row][col].append(i)
        
        end = time.time()
        # print(end - start)
        # print(len(self.grid))
        #    except:
        #         print(row, col, particle.pos.x, particle.pos.y)

    def applyBoundary(self):
        for particle in self.particles:
            r = self.boundary_pos - particle.pos
            dist = math.sqrt(math.pow(r.x, 2) + math.pow(r.y, 2))
            if (dist > self.boundary_radius - particle.radius):
                n = r / dist
                tan = vec2(-n.y, n.x)
                vel = particle.getVelocity()
                # if particle.radius + 5 <= self.boundary_radius:
                #     particle.radius += 5
                projected_v_on_tan = (tan.dot(vel)/tan.dot(tan)) * tan

                particle.pos = self.boundary_pos - n * (self.boundary_radius - particle.radius)
                # (vel.x * tan.x + vel.y * tan.y) * tan
                particle.setVelocity(2 * projected_v_on_tan - vel, 1)
                
                # print(n, perp, vel, particle.pos, particle.getVelocity())
                # print(particle.getVelocity())
    
    def applyBorder(self):
        for particle in self.particles:
            dampening = 0.75
            pos = particle.pos.copy()
            npos = particle.pos.copy()
            vel = particle.getVelocity()

            dy = vec2(vel.x * dampening, -vel.y)
            dx = vec2(-vel.x, vel.y * dampening)

            if (pos.x < particle.radius or pos.x + particle.radius > self.window_size.x):
                if (pos.x < particle.radius):
                    npos.x = particle.radius
                if (pos.x + particle.radius > self.window_size.x):
                    npos.x = self.window_size.x - particle.radius
                particle.pos = npos.copy()
                particle.setVelocity(dx, 1.0)
            
            if (pos.y < particle.radius or pos.y + particle.radius > self.window_size.y):
                if (pos.y < particle.radius):
                    npos.y = particle.radius
                if (pos.y + particle.radius > self.window_size.y):
                    npos.y = self.window_size.y - particle.radius
                particle.pos = npos.copy()
                particle.setVelocity(dy, 1.0)


    def update(self, surf, dt):
        substep_dt = self.step_dt / self.sub_steps
        for i in range(self.sub_steps):
            self.applyGravity()
            self.updateObjects(substep_dt)
           
            # self.check_particle_collisions_multiprocessing()
            # self.check_particle_collisions_split_grid()
            self.checkCollisions(surf)

            if self.bounding:
                self.applyBoundary()
            else:
                self.applyBorder()

            self.updateGrid()



        self.render(surf)
