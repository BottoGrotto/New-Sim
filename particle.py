import pygame, math, time
from pygame import Vector2 as vec2


class Particle:
    def __init__(self, radius: float, color, pos: vec2, accel=vec2(10, 10), anchorpoint=False, use_velocity_color=True):
        self.radius = radius
        self.color = color
        self.anchorpoint = anchorpoint
        self.pos = pos
        self.last_pos = pos.copy()
        self.accel = accel
        self.is_rope = False
        self.use_velocity_color = use_velocity_color

    def __eq__(self, other):
        if not isinstance(other, Particle):
            return NotImplemented
        return self.pos == other.pos and self.last_pos == other.last_pos
    
    def speed_to_color(self):
        if self.use_velocity_color:
            intensity = min(255, int((abs(self.getVelocity().magnitude())/ 5) * 255))
            return (intensity, 0, 255 - intensity)
        else:
            return self.color

    def render(self, surf):
        pygame.draw.circle(surf, self.color if self.anchorpoint else self.speed_to_color(), self.pos, self.radius)


    def update(self, dt: float):
        displacement = self.pos - self.last_pos
        self.last_pos = self.pos.copy()
        self.pos += displacement + self.accel * math.pow(dt, 2)
        self.accel = vec2()

    def accelerate(self, a: vec2):
        self.accel += a

    def setVelocity(self, v, dt):
        self.last_pos = self.pos - (v * dt)

    def addVelocity(self, v, dt):
        self.last_pos -= v * dt

    def getVelocity(self):
        return self.pos - self.last_pos
    


    