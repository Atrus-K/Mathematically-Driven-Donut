import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning 3D Cube")

# Define cube vertices
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define cube edges
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
]

# Rotation functions
def rotateX(x, y, z, angle):
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    y_new = y * cosa - z * sina
    z_new = y * sina + z * cosa
    return x, y_new, z_new

def rotateY(x, y, z, angle):
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x_new = z * sina + x * cosa
    z_new = z * cosa - x * sina
    return x_new, y, z_new

def rotateZ(x, y, z, angle):
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x_new = x * cosa - y * sina
    y_new = x * sina + y * cosa
    return x_new, y_new, z

def project(x, y, z, width, height, fov, distance):
    factor = fov / (distance + z)
    x_new = x * factor + width / 2
    y_new = -y * factor + height / 2
    return int(x_new), int(y_new)

# Main loop
A = 0
B = 0
C = 0
clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill((0, 0, 0))

    # Cube rotation and projection
    projected_points = []
    fov = 500  # Field of view
    distance = 5  # Distance from camera

    for vertex in vertices:
        x, y, z = vertex
        # Apply rotations around X, Y, and Z axes
        x, y, z = rotateX(x, y, z, A)
        x, y, z = rotateY(x, y, z, B)
        x, y, z = rotateZ(x, y, z, C)
        # Project 3D coordinates into 2D
        x, y = project(x, y, z, width, height, fov, distance)
        projected_points.append((x, y))

    # Draw cube edges
    for edge in edges:
        pygame.draw.line(screen, (255, 255, 255), projected_points[edge[0]], projected_points[edge[1]], 2)

    # Update display
    pygame.display.flip()

    # Increment rotation angles
    A += 1  # Rotate around X-axis
    B += 1  # Rotate around Y-axis
    C += 1  # Rotate around Z-axis

    # Frame rate
    clock.tick(60)