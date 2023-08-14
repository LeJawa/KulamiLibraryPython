from bash_color import Color, color


def formatted_bin(num: int, mask_size) -> str:
    bin_length = mask_size + 2
    return format(num, f"#0{bin_length}b")


def check_collision(shape_mask: int, target_mask: int, forced_mask_size=0) -> bool:
    if forced_mask_size != 0:
        mask_size = forced_mask_size
    else:
        mask_size = max(len(bin(target_mask)), len(bin(shape_mask))) - 2

    tile_mask_str = formatted_bin(shape_mask, mask_size)
    colored_tile_mask_str = ""
    for i in range(len(tile_mask_str)):
        if tile_mask_str[i] == "1":
            if tile_mask_str[i] == formatted_bin(target_mask, mask_size)[i]:
                colored_tile_mask_str += color(tile_mask_str[i], Color.RED)
            else:
                colored_tile_mask_str += color(tile_mask_str[i], Color.GREEN)
        else:
            colored_tile_mask_str += tile_mask_str[i]

    print(colored_tile_mask_str)
    print(formatted_bin(target_mask, mask_size))
