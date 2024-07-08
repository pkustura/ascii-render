import math
import time
import os

# Cube properties
CUBE_SIZE = 1.0
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 40  # Reduced height to account for ASCII aspect ratio
CAMERA_DISTANCE = 5

# ASCII character aspect ratio (approximately 2:1 height to width)
ASPECT_RATIO = 2.0

# Rotation speed
ROTATION_SPEED = 0.1

# ASCII character palette for depth
PALETTE = ' .:!/r(l1Z4H9W8$@'
PALETTE_SIZE = len(PALETTE) - 1

# Depth mapping steepness
DEPTH_STEEPNESS = 2.0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    # Rotate around X-axis
    y, z = y * math.cos(angle_x) - z * math.sin(angle_x), y * math.sin(angle_x) + z * math.cos(angle_x)
    
    # Rotate around Y-axis
    x, z = x * math.cos(angle_y) + z * math.sin(angle_y), -x * math.sin(angle_y) + z * math.cos(angle_y)
    
    # Rotate around Z-axis
    x, y = x * math.cos(angle_z) - y * math.sin(angle_z), x * math.sin(angle_z) + y * math.cos(angle_z)
    
    return x, y, z

def project(x, y, z):
    factor = min(SCREEN_WIDTH, SCREEN_HEIGHT * ASPECT_RATIO) * CAMERA_DISTANCE / (4 * (z + CAMERA_DISTANCE))
    return int(x * factor + SCREEN_WIDTH / 2), int(y * factor / ASPECT_RATIO + SCREEN_HEIGHT / 2)

def map_depth_to_char(z):
    # Map z from [CAMERA_DISTANCE - CUBE_SIZE, CAMERA_DISTANCE + CUBE_SIZE] to [0, 1]
    normalized_z = 1 - (z - (CAMERA_DISTANCE - CUBE_SIZE)) / (2 * CUBE_SIZE)
    normalized_z = max(0, min(1, normalized_z))  # Clamp to [0, 1]
    
    # Apply depth steepness
    mapped_z = math.pow(normalized_z, DEPTH_STEEPNESS)
    
    # Map to character index
    char_index = int(mapped_z * PALETTE_SIZE)
    return PALETTE[char_index]

def render_cube(angle_x, angle_y, angle_z):
    screen = [[' ' for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    # Define cube vertices
    vertices = [
        (-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE), (CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE),
        (CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE), (-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE),
        (-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE), (CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE),
        (CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), (-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
    ]

    # Rotate and project vertices
    rotated_vertices = [rotate_point(x, y, z, angle_x, angle_y, angle_z) for x, y, z in vertices]
    projected_vertices = [project(x, y, z) for x, y, z in rotated_vertices]

    # Draw vertices on screen
    for x, y in projected_vertices:
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            screen[y][x] = '@'

    # Draw edges
    edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
    for start, end in edges:
        x1, y1 = projected_vertices[start]
        x2, y2 = projected_vertices[end]
        # Simple line drawing
        for t in range(100):
            x = int(x1 + (x2 - x1) * t / 100)
            y = int(y1 + (y2 - y1) * t / 100)
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                screen[y][x] = '#'

    # Draw a border around the screen
    for i in range(SCREEN_WIDTH):
        screen[0][i] = screen[SCREEN_HEIGHT-1][i] = '-'
    for i in range(SCREEN_HEIGHT):
        screen[i][0] = screen[i][SCREEN_WIDTH-1] = '|'

    return '\n'.join(''.join(row) for row in screen)

def main():
    angle_x = angle_y = angle_z = 0
    try:
        while True:
            clear_screen()
            cube = render_cube(angle_x, angle_y, angle_z)
            print(cube)
            print(f"Angles: x={angle_x:.2f}, y={angle_y:.2f}, z={angle_z:.2f}")
            angle_x += ROTATION_SPEED
            angle_y += ROTATION_SPEED * 0.7
            angle_z += ROTATION_SPEED * 0.5
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
