import pygame, math
from pygame import Vector2 as vec2
from particle import Particle

class Rope:
    def __init__(self, anchor_points, rope_radius, length, color):
        self.anchor_points = anchor_points
        self.rope_radius = rope_radius
        self.length = length
        self.color = color
        self.rope_particles = [RopeParticle(None, self.rope_radius, self.color, anchor_points[0], True, 0)]


        
        particle_pos = anchor_points[0].copy()
        # print(length - len(anchor_points) - 1)
        for i in range(1, length - (len(self.anchor_points) - 1)):
            # print(i, i-1)
            if len(anchor_points) > 1:
                particle_pos += vec2(self.rope_radius + self.rope_radius, 0)
                self.rope_particles.append(RopeParticle(self.rope_particles[i-1], self.rope_radius, self.color, particle_pos.copy(), False, i))
            else:
                particle_pos += vec2(0, self.rope_radius + self.rope_radius)
                # print(particle_pos)
                self.rope_particles.append(RopeParticle(self.rope_particles[i-1], self.rope_radius, self.color, particle_pos.copy(), False, i))

        # print([particle.pos for particle in self.rope_particles])

class RopeParticle(Particle):
    def __init__(self, parent, radius, color, pos, anchorpoint, index):
        super().__init__(radius, color, pos, anchorpoint=anchorpoint)
        self.parent = parent
        self.index = index

    def update(self, dt):
        if self.parent:
            super().update(dt)
            dir = self.parent.pos - self.pos
            dist = math.sqrt(math.pow(dir.x, 2) + math.pow(dir.y, 2))
            max_dist = self.parent.radius + self.radius
            delta = 0.5* (max_dist - dist)
            if dist > max_dist:
                if not self.parent.anchorpoint:
                    self.parent.pos += (dir / dist) * delta
                self.pos -= (dir / dist) * delta
                # self.setVelocity(dir/dist, 1)
            