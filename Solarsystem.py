import pygame
import math
pygame.init()
WIDTH, HEIGHT = 10000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (118, 238, 198)
RED = (188, 39, 50)
FLOWERBLUE = (100,149,237)
DARKGOLDEN = (255, 185, 15)
BRICK = (156, 102, 31)
BURLYWOOD = (222, 184, 135)
LIGHTBLUE = (152, 245, 255)
LIGHTERBLUE = (122,197,205)

FONT = pygame.font.SysFont("comicsans", 16 )

class Planet:
    AU = 149.6e6 * 1000  #Astronimical unit
    G = 6.67428e-11      # Gravitional constant
    SCALE = 150 / AU
    TIMESTEP = 3600*24   #1day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        if len(self.orbit) >3:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points,1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1e3)} km", 1,WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_width()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance**2
        alpha = math.atan2(distance_y, distance_x)
        force_x = math.cos(alpha) * force
        force_y = math.sin(alpha) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)

            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
def main():
    run = True
    clock = pygame.time.Clock()
    sun = Planet(0, 0, 35, YELLOW, 1.98892 * (1e30))  # in kg
    sun.sun = True
    earth = Planet(-1 * Planet.AU, 0, 16,  BLUE, 5.9742 * 1e24)    # in kg
    earth.y_vel = 29.783 * 1e3
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 1e23)     # in kg
    mars.y_vel = 24.077 * 1e3
    mercury = Planet(0.387 * Planet.AU, 0, 8, FLOWERBLUE, 3.30 * 1e23)   # in kg
    mercury.y_vel = -47.4 * 1e3
    venus = Planet(0.723 * Planet.AU, 0, 13, DARKGOLDEN, 4.8685 * 1e24)  # in kg
    venus.y_vel = -35.02 * 1e3
    jupiter = Planet(4.98* Planet.AU, 0, 24, BRICK, 1.898 * 1e27) # in kg
    jupiter.y_vel = -13.06 * 1e3
    saturn = Planet(9.8 * Planet.AU, 0, 20, BURLYWOOD, 3.798 * 10e18)
    saturn.y_vel = -9.68 * 1e3
    uranus = Planet(19.7 * Planet.AU, 0, 17, LIGHTBLUE, 8.681 * 1e25)
    uranus.y_vel = -6.80 * 1e3
    neptune = Planet(29.9 * Planet.AU, 0 , 16.8, LIGHTERBLUE, 1.024 * 1e26)
    neptune.y_vel = -5.45 *1e3
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
    while run:
        clock.tick(100)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        pygame.display.update()
    pygame.quit()

main()
