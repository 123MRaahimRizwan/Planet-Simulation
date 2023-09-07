import pygame
import math
pygame.init()

WIDTH, HEIGHT = 900,900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulator")
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (188,39,50)
DARK_GREY = (144,143,143)
YELLOWISH_WHITE = (240,172,15)
YELLOWISH = (242,220,160)
BLACK = (0,0,0)

class Planet:
    # This planet class will contain the information about the planets
    # AU means astronomical unit it will simplify our math
    AU = 149.6e6 * 1000 # here 149.6e6 is in km and *by 1000 converts km to m
    G = 6.67428e-11 # gravitational constant
    SCALE = 200 / AU # 1AU = 100px
    TIMESTEP = 3600*24 # This represents 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH/ 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))
            
            pygame.draw.lines(window, self.color, False, updated_points, 2)
        pygame.draw.circle(window, self.color, (x,y), self.radius)

    def attraction(self, other):
        other_x , other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance**2 # This is the Newton's law equation
        theta = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(theta) # Fx=Fcos(T)
        force_y = force * math.sin(theta) # Fy=Fsin(T)

        return force_x, force_y
    
    def update_position(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet: #This checks if we are calculating force with ourselves with will give a zero division error
                continue
            fx, fy = self.attraction(planet)
            total_force_x += fx
            total_force_y += fy

        self.x_vel += total_force_x / self.mass * self.TIMESTEP #  a = F/m
        self.y_vel += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP # S=vt
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742 * 10**24) # -1 AU means to the left
    earth.y_vel = 29.783 * 1000 # 29.783 is km/s and *1000 gives us m/s

    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387*Planet.AU, 0, 8, DARK_GREY, 0.330*10**24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723*Planet.AU, 0, 14, YELLOWISH_WHITE, 4.8685*10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(-2.120*Planet.AU, 0, 18, YELLOWISH, 1.898*10**27)
    jupiter.y_vel = 13.06 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter]

    while run:
        clock.tick(60)
        WINDOW.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)
        pygame.display.update()
    pygame.quit()

main()