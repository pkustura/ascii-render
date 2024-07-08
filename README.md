# z-buf ascii renderer

## Simple cube demo (ascii-3d-cube.py)

Simply clone the directory and run the program with `python3 ascii-3d-cube.py`

Have fun playing with the parameters!

- Modify the PALETTE string to use different ASCII characters for shading.
- Adjust DEPTH_STEEPNESS to change how quickly the shading changes with depth.
- Change the light_dir vector to alter the lighting direction.`

## Loading .obj models (ascii-3d-obj-renderer.py)

You can load and view your own models: `python3 ascii-3d-obj-renderer.py path/to/obj`

-It only supports vertex (v) and face (f) data from the OBJ file. Texture coordinates, normals, and other data are ignored.
-It assumes triangular or quadrilateral faces. More complex polygons may not render correctly.
-Very complex models with many faces may render slowly or cause performance issues due to the nature of ASCII rendering.

