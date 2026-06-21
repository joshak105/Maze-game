from kepoco import display, buttonB, buttonU, buttonD, buttonL, buttonR
from uctypes import addressof


@micropython.viper
def mem_cpy(dst: ptr8, src: ptr8, src_len: uint):
    for i in range(int(src_len)):
        dst[i] = src[i]

@micropython.viper
def mem_cpy_masked(dst: ptr8, src: ptr8, src_len: uint, mask: ptr8):
    for i in range(int(src_len)):
        dst[i] = (dst[i] & (255 - mask[i])) | (src[i] & mask[i])



with open("/Exercises/level11_sokoban/spritemap.bin", "rb") as f:
    sprite_map = f.read()


sprite_ptr = addressof(sprite_map)
foreground_ptr = addressof(display.buffer)
background_ptr = addressof(display.shading)

blank = sprite_ptr
character = sprite_ptr + 112
crate = sprite_ptr + 96
crate_mask = sprite_ptr + 104
dot = sprite_ptr + 88




tile_meta_data = {
    " ": (False, blank, 1),                    
    "o": (False, sprite_ptr + 8, 1),           
    ".": (True,  sprite_ptr + 16, 1),          
    "x": (True,  sprite_ptr + 24, 1),          
    "#": (True,  sprite_ptr + 32, 1),          
    "~": (False, sprite_ptr + 40, 4),          
    "_": (True,  sprite_ptr + 40, 4),        
    "?": (False, sprite_ptr + 72, 2),          
    "s": (False, sprite_ptr + 184, 1),         
    "k": (False, sprite_ptr + 184 + 8, 1),     
    "b": (False, sprite_ptr + 184 + 16, 1),    
    "a": (False, sprite_ptr + 184 + 24, 1),    
    "n": (False, sprite_ptr + 184 + 32, 1),    

    "*": (False, dot, 1),                      
    "c": (False, crate, 1),                   
    "C": (False, crate_mask, 1),               
    "&": (False, character, 1),                
    ">": (True,  sprite_ptr + 120, 2),         
    "<": (True,  sprite_ptr + 136, 2),         
    "^": (True,  sprite_ptr + 152, 2),         
    "v": (True,  sprite_ptr + 168, 2),         
}



def load_map(filename):
    global exit_tile

    with open("/Exercises/level11_sokoban/" + filename, "rt") as f:

        
        game_map = []
        for _ in range(5):
            line = f.readline()
            

            line = line.rstrip("\n")

            
            if len(line) < 9:
                line = line + " " * (9 - len(line))
            elif len(line) > 9:
                line = line[:9]

            row = [tile_meta_data.get(ch, tile_meta_data[" "]) for ch in line]
            game_map.append(row)

        
        line = f.readline()
        while line and line.strip().lower() != "player start":
            line = f.readline()
        

        pos_line = f.readline()
        
        px_str, py_str = pos_line.strip().split(",")
        player = (int(px_str), int(py_str))

        
        line = f.readline()
        while line and line.strip().lower() not in ("exit", "goal", "goals"):
            line = f.readline()
        

        exit_line = f.readline()
        
        ex_str, ey_str = exit_line.strip().split(",")
        exit_tile = (int(ex_str), int(ey_str))

    return game_map, player, exit_tile



game_map, player, exit_tile = load_map("maze.txt")


def is_passable(pos):
    x, y = pos
    if x < 0 or x > 8 or y < 0 or y > 4:  
        return False
    return game_map[y][x][0]  



assert is_passable(player), "Player start must be on a passable tile"
ex, ey = exit_tile
assert is_passable(exit_tile), "Exit must be on a passable tile"


def move(dx, dy):
    """
    Maze movement: no crates, no pushing.
    Player moves one tile at a time if the tile is passable.
    """
    global player
    move_to = (player[0] + dx, player[1] + dy)
    if is_passable(move_to):
        player = move_to
        return True
    return False


move_count = 0
display.setFPS(20)
display.enableGrayscale()
tick = 0

while not buttonB.justPressed():  
    needs_redraw = (tick % 6) == 0
    check_win = False

    
    if buttonU.justPressed():
        if move(0, -1):
            needs_redraw = True
            check_win = True
            move_count += 1

    elif buttonD.justPressed():
        if move(0, +1):
            needs_redraw = True
            check_win = True
            move_count += 1

    elif buttonL.justPressed():
        if move(-1, 0):
            needs_redraw = True
            check_win = True
            move_count += 1

    elif buttonR.justPressed():
        if move(+1, 0):
            needs_redraw = True
            check_win = True
            move_count += 1

    
    if needs_redraw:
        display.fill(display.BLACK)
        ani_tick = tick // 6

        
        for r, row in enumerate(game_map):
            
            for (passable, tile, ani), o in zip(row, range(r * 72, 72 * 5, 8)):
                ani_idx = ani_tick % ani
                if passable:
                    mem_cpy(background_ptr + o, tile + ani_idx * 8, 8)
                else:
                    mem_cpy(foreground_ptr + o, tile + ani_idx * 8, 8)

        
        ex, ey = exit_tile
        offset = ex * 8 + ey * 72
        mem_cpy_masked(background_ptr + offset, blank, 8, dot)
        mem_cpy_masked(foreground_ptr + offset, dot, 8, dot)

        
        p_x, p_y = player
        offset_p = p_x * 8 + p_y * 72
        mem_cpy_masked(background_ptr + offset_p, blank, 8, character)
        mem_cpy_masked(foreground_ptr + offset_p, character, 8, character)

    display.update()
    tick += 1

    
    if check_win and player == exit_tile:
        print("You escaped the maze!")
        print(f"{move_count=}")
        break