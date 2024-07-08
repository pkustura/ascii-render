import math
import time
import os

# Cube properties
CUBE_SIZE = 2.0
SCREEN_SIZE = 40
SCALE = (SCREEN_SIZE - 4) * 0.5 / CUBE_SIZE

# Rotation speed
ROTATION_SPEED = 0.6

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    # Rotate around X-axis
    new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = new_y, new_z

    # Rotate around Y-axis
    new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
    new_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = new_x, new_z

    # Rotate around Z-axis
    new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
    new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
    x, y = new_x, new_y

    return x, y, z

def project(x, y, z):
    factor = SCALE / (4 + z)
    return int(x * factor + SCREEN_SIZE / 2), int(y * factor + SCREEN_SIZE / 2)

def render_cube(angle_x, angle_y, angle_z):
    cube = [
        [-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE], [CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE],
        [CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE], [-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE],
        [-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE], [CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE],
        [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE], [-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
    ]

    screen = [[' ' for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]

    for point in cube:
        x, y, z = rotate_point(*point, angle_x, angle_y, angle_z)
        x, y = project(x, y, z)
        if 0 <= x < SCREEN_SIZE and 0 <= y < SCREEN_SIZE:
            screen[y][x] = '@'

    # Draw edges
    edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
    for start, end in edges:
        x1, y1, z1 = rotate_point(*cube[start], angle_x, angle_y, angle_z)
        x2, y2, z2 = rotate_point(*cube[end], angle_x, angle_y, angle_z)
        x1, y1 = project(x1, y1, z1)
        x2, y2 = project(x2, y2, z2)
        
        # Simple line drawing algorithm
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        x, y = x1, y1
        n = 1 + dx + dy
        x_inc = 1 if x2 > x1 else -1
        y_inc = 1 if y2 > y1 else -1
        error = dx - dy
        dx *= 2
        dy *= 2

        while n > 0:
            if 0 <= x < SCREEN_SIZE and 0 <= y < SCREEN_SIZE:
                screen[y][x] = '#'
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
            n -= 1

    return '\n'.join(''.join(row) for row in screen)

def main():
    angle_x = angle_y = angle_z = 0
    try:
        while True:
            clear_screen()
            print(render_cube(angle_x, angle_y, angle_z))
            angle_x += ROTATION_SPEED * 0.05
            angle_y += ROTATION_SPEED * 0.03
            angle_z += ROTATION_SPEED * 0.07
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
