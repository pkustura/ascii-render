import math
import time
import os

# Cube properties
CUBE_SIZE = 1.0
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 40
CAMERA_DISTANCE = 5

# ASCII character aspect ratio (approximately 2:1 height to width)
ASPECT_RATIO = 2.0

# Rotation speed
ROTATION_SPEED = 0.1

# ASCII character palette for depth (from darkest to lightest)
# PALETTE = ' .:-=+*#%@'
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

def calculate_normal(face_vertices):
    v1 = [face_vertices[1][i] - face_vertices[0][i] for i in range(3)]
    v2 = [face_vertices[2][i] - face_vertices[0][i] for i in range(3)]
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

def normalize(vector):
    magnitude = math.sqrt(sum(v * v for v in vector))
    return [v / magnitude for v in vector] if magnitude != 0 else vector

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def map_depth_to_char(z, normal, light_dir):
    # Normalize z to [0, 1] range
    normalized_z = 1 - (z - (CAMERA_DISTANCE - CUBE_SIZE)) / (2 * CUBE_SIZE)
    normalized_z = max(0, min(1, normalized_z))
    
    # Calculate lighting intensity
    light_intensity = max(0, dot_product(normalize(normal), light_dir))
    
    # Combine depth and lighting
    shading = (normalized_z + light_intensity) / 2
    
    # Apply depth steepness
    shading = math.pow(shading, DEPTH_STEEPNESS)
    
    # Map to character index
    char_index = int(shading * PALETTE_SIZE)
    return PALETTE[min(char_index, PALETTE_SIZE)]

def interpolate_z(x, y, triangle, z_values):
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]
    
    det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if abs(det) < 1e-6:
        return (z_values[0] + z_values[1] + z_values[2]) / 3
    
    w1 = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
    w2 = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
    w3 = 1 - w1 - w2
    
    return w1 * z_values[0] + w2 * z_values[1] + w3 * z_values[2]

def point_in_triangle(x, y, triangle):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign((x, y), triangle[0], triangle[1])
    d2 = sign((x, y), triangle[1], triangle[2])
    d3 = sign((x, y), triangle[2], triangle[0])

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def render_cube(angle_x, angle_y, angle_z):
    zbuffer = [[float('inf')] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
    screen = [[' ' for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    vertices = [
        (-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE), (CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE),
        (CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE), (-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE),
        (-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE), (CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE),
        (CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), (-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
    ]

    faces = [
        (0, 1, 2, 3), (5, 4, 7, 6), (1, 5, 6, 2),
        (4, 0, 3, 7), (4, 5, 1, 0), (3, 2, 6, 7)
    ]

    light_dir = normalize([1, -1, 1])  # Light direction

    rotated_vertices = [rotate_point(x, y, z, angle_x, angle_y, angle_z) for x, y, z in vertices]
    projected_vertices = [project(x, y, z) for x, y, z in rotated_vertices]

    faces_rendered = 0
    points_rendered = 0

    for face_index, face in enumerate(faces):
        face_vertices = [rotated_vertices[i] for i in face]
        projected_face = [projected_vertices[i] for i in face]

        normal = calculate_normal(face_vertices)
        
        if normal[2] <= 0:  # Back-face culling
            continue

        min_x = max(0, min(x for x, _ in projected_face))
        max_x = min(SCREEN_WIDTH - 1, max(x for x, _ in projected_face))
        min_y = max(0, min(y for _, y in projected_face))
        max_y = min(SCREEN_HEIGHT - 1, max(y for _, y in projected_face))

        points_inside = 0
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                triangle1 = projected_face[:3]
                triangle2 = [projected_face[0], projected_face[2], projected_face[3]]
                
                if point_in_triangle(x, y, triangle1):
                    z = interpolate_z(x, y, triangle1, [v[2] for v in face_vertices[:3]])
                    points_inside += 1
                elif point_in_triangle(x, y, triangle2):
                    z = interpolate_z(x, y, triangle2, [face_vertices[0][2], face_vertices[2][2], face_vertices[3][2]])
                    points_inside += 1
                else:
                    continue

                if z < zbuffer[y][x]:
                    zbuffer[y][x] = z
                    screen[y][x] = map_depth_to_char(z, normal, light_dir)
                    points_rendered += 1

        faces_rendered += 1

    # print(f"Faces rendered: {faces_rendered}, Points rendered: {points_rendered}")

    return '\n'.join(''.join(row) for row in screen)

def main():
    angle_x = angle_y = angle_z = 0
    try:
        while True:
            clear_screen()
            cube = render_cube(angle_x, angle_y, angle_z)
            print(cube)
            # print(f"Angles: x={angle_x:.2f}, y={angle_y:.2f}, z={angle_z:.2f}")
            angle_x += ROTATION_SPEED
            angle_y += ROTATION_SPEED * 0.7
            angle_z += ROTATION_SPEED * 0.5
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
