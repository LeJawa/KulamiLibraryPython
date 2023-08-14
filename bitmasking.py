"""
This file contains functions for checking collisions between tiles.
"""

from bash_color import Color, colorize


def formatted_bin(num: int, mask_size) -> str:
    """Return the binary representation of a number with a specified length."""
    bin_length = mask_size + 2
    return format(num, f"#0{bin_length}b")


def check_collision(shape_mask: int, target_mask: int, forced_mask_size=0) -> bool:
    """
    Check if two masks collide and prints them to the terminal.
    Returns True if they collide, False otherwise.
    """
    if forced_mask_size != 0:
        mask_size = forced_mask_size
    else:
        mask_size = max(len(bin(target_mask)), len(bin(shape_mask))) - 2

    tile_mask_str = formatted_bin(shape_mask, mask_size)
    colored_tile_mask_str = ""
    for i, tile_mask_char in enumerate(tile_mask_str):
        if tile_mask_char == "1":
            if tile_mask_char == formatted_bin(target_mask, mask_size)[i]:
                colored_tile_mask_str += colorize(tile_mask_char, Color.RED)
            else:
                colored_tile_mask_str += colorize(tile_mask_char, Color.GREEN)
        else:
            colored_tile_mask_str += tile_mask_char

    print(colored_tile_mask_str)
    print(formatted_bin(target_mask, mask_size))
