Maze-game

A Python maze game adapted from a base Sokoban implementation. The core push-crate mechanics and level-loading structure of Sokoban were reworked into maze navigation, with custom levels and a sprite map for rendering.

How It Works


The game loads level layouts from plain text map files (maze.txt, map1.txt)

spritemap.bin supplies the tile/sprite graphics used to render the maze

Gameplay logic — movement, collision, and level state — builds on the original Sokoban engine (level11_sokoban (5).py), adapted for maze traversal instead of crate-pushing

How It Works


The game loads level layouts from plain text map files (maze.txt, map1.txt)

Gameplay logic — movement, collision, and level state — builds on the original Sokoban engine (level11_sokoban (5).py), adapted for maze traversal instead of crate-pushing

