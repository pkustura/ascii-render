import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Cube Renderer")

# Define cube vertices
vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
])

# Define cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
    (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
]

# Create a z-buffer
z_buffer = np.full((height, width), float('inf'))

def rotate_x(theta):
    return np.array([
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)]
    ])

def rotate_y(theta):
    return np.array([
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)]
    ])

def rotate_z(theta):
    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])

def project(point):
    z = point[2] + 5
    f = 200 / z
    return int(point[0] * f + width / 2), int(point[1] * f + height / 2), z

running = True
clock = pygame.time.Clock()
angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen and z-buffer
    screen.fill((0, 0, 0))
    z_buffer.fill(float('inf'))

    # Rotate the cube
    rotation = rotate_x(angle) @ rotate_y(angle * 0.8) @ rotate_z(angle * 1.2)
    rotated = vertices @ rotation

    # Project 3D points to 2D
    projected = [project(point) for point in rotated]

    # Draw the edges
    for edge in edges:
        start = projected[edge[0]]
        end = projected[edge[1]]
        
        # Simple z-buffer check
        if start[2] < z_buffer[start[1], start[0]] and end[2] < z_buffer[end[1], end[0]]:
            pygame.draw.line(screen, (255, 255, 255), (start[0], start[1]), (end[0], end[1]))
            
            # Update z-buffer (simplified, just updating endpoints)
            z_buffer[start[1], start[0]] = start[2]
            z_buffer[end[1], end[0]] = end[2]

    pygame.display.flip()
    clock.tick(60)
    angle += 0.02

pygame.quit()
