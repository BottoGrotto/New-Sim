import pygame, math
from pygame import Vector2 as vec2
from particle import Particle

class Rope:
    def __init__(self, anchor_points, rope_radius, length, color, use_velocity_color, spawnPos):
        self.anchor_points = anchor_points
        self.rope_radius = rope_radius
        self.length = length
        self.color = color
        self.rope_particles = [RopeParticle(None, self.rope_radius, self.color, anchor_points[0], True, 0, use_velocity_color) if len(anchor_points) > 0 else RopeParticle(None, self.rope_radius, self.color, spawnPos, False, 0, use_velocity_color)]

        particle_pos = self.rope_particles[0].pos.copy()

        for i in range(length -1):
            if len(anchor_points) > 1:
                if i < length / 2:
                    particle_pos += vec2(self.rope_radius + self.rope_radius, self.rope_radius + self.rope_radius)
                else:
                    particle_pos += vec2(self.rope_radius + self.rope_radius, - self.rope_radius - self.rope_radius)

            else:
                if i < length / 2:
                    particle_pos += vec2(self.rope_radius, self.rope_radius + self.rope_radius)
                else:
                    particle_pos += vec2(self.rope_radius, -self.rope_radius - self.rope_radius)

            if i == 1:
                self.rope_particles[0].child = self.rope_particles[-1]

            self.rope_particles.append(RopeParticle(self.rope_particles[i], self.rope_radius, self.color, particle_pos.copy(), False, i, use_velocity_color))
            self.rope_particles[-2].child = self.rope_particles[-1]
        # print(length - len(anchor_points) - 1)
        # for i in range(1, length - (len(self.anchor_points) - 1)):
        #     # print(i, i-1)
        #     if len(anchor_points) > 1:
        #         particle_pos += vec2(self.rope_radius + self.rope_radius, 0)
        #         # self.rope_particles.append(RopeParticle(self.rope_particles[i-1], self.rope_radius, self.color, particle_pos.copy(), False, i))
        #         # self.rope_particles[-2].child = self.rope_particles[-1]
        #     else:
        #         particle_pos += vec2(0, self.rope_radius + self.rope_radius)
                # print(particle_pos)
            # self.rope_particles.append(RopeParticle(self.rope_particles[i-1], self.rope_radius, self.color, particle_pos.copy(), False, i))
            # self.rope_particles[-2].child = self.rope_particles[-1]

        if len(self.anchor_points) > 1:
            self.rope_particles[-1].anchorpoint = True
            self.rope_particles[-1].pos = anchor_points[1]
        # self.rope_particles[-1].anchorpoint = True
        # print([particle.pos for particle in self.rope_particles])

class RopeParticle(Particle):
    def __init__(self, parent, radius, color, pos, anchorpoint, index, use_velocity_color):
        super().__init__(radius, color, pos, anchorpoint=anchorpoint, use_velocity_color=use_velocity_color)
        self.parent = parent
        self.index = index
        self.is_rope = True
        self.child = None
        self.use_velocity_color = use_velocity_color

    def update(self, dt):
        # if self.parent and self.child:
        super().update(dt)
        if self.parent:
            dir = self.parent.pos - self.pos
            dist = math.sqrt(math.pow(dir.x, 2) + math.pow(dir.y, 2))
            max_dist = self.parent.radius + self.radius
            delta = 0.5 * (max_dist - dist)
            if dist > max_dist:
                if not self.parent.anchorpoint:
                    self.parent.pos += (dir / dist) * delta
                self.pos -= (dir / dist) * delta
        if self.child:
            dir = self.child.pos - self.pos
            dist = math.sqrt(math.pow(dir.x, 2) + math.pow(dir.y, 2))
            max_dist = self.child.radius + self.radius
            delta = 0.5 * (max_dist - dist)
            if dist > max_dist:
                if not self.child.anchorpoint:
                    self.child.pos += (dir / dist) * delta
                self.pos -= (dir / dist) * delta

    def speed_to_color(self):
        if self.use_velocity_color:
            # Calculate intensity based on velocity
            intensity = max(0.0, 1 - abs(self.getVelocity().magnitude()) / 5)  # Scale intensity between 0 and 1
            
            r, g, b = self.color
            
            

            # Adjust the RGB values based on the intensity
            new_r = int(r * intensity)
            new_g = int(g * intensity)
            new_b = int(b * intensity)
            
            return (new_r, new_g, new_b)


            # intensity = min(255, int((abs(self.getVelocity().magnitude())/ 5) * 255))
            # return (intensity, 255 - intensity, 0)
        else:
            return self.color

        # if self.child:
        #     dir = self.pos - self.child.pos
        #     dist = math.sqrt(math.pow(dir.x, 2) + math.pow(dir.y, 2))
        #     max_dist = self.child.radius + self.radius
        #     delta = 0.5 * (max_dist - dist)
        #     if dist > max_dist:
        #         if not self.child.anchorpoint:
        #             self.child.pos += (dir / dist) * delta
        #         self.pos -= (dir / dist) * delta
                # self.setVelocity(dir/dist, 1)
            