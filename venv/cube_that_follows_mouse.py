import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Cube Following Mouse")

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

def project(x, y, z, width, height, fov, distance):
    factor = fov / (distance + z)
    x_new = x * factor + width / 2
    y_new = -y * factor + height / 2
    return int(x_new), int(y_new)

# Main loop
clock = pygame.time.Clock()
fov = 500  # Field of view
distance = 5  # Distance from camera

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill((0, 0, 0))

    # Get mouse position and map to rotation angles
    mouse_x, mouse_y = pygame.mouse.get_pos()
    A = (mouse_y - height / 2) * 0.1  # Control rotation around X-axis
    B = (mouse_x - width / 2) * 0.1   # Control rotation around Y-axis

    # Cube rotation and projection
    projected_points = []

    for vertex in vertices:
        x, y, z = vertex
        # Apply rotations around X and Y axes based on mouse movement
        x, y, z = rotateX(x, y, z, A)
        x, y, z = rotateY(x, y, z, B)
        # Project 3D coordinates into 2D
        x, y = project(x, y, z, width, height, fov, distance)
        projected_points.append((x, y))

    # Draw cube edges
    for edge in edges:
        pygame.draw.line(screen, (255, 255, 255), projected_points[edge[0]], projected_points[edge[1]], 2)

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)