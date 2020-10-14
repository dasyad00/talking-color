from collections import namedtuple

monochrome_bounds_saturation = (0, 15)
white_bounds_value = (95, 100)
black_bounds_value = (0, 25)

colored_bounds_saturation = (monochrome_bounds_saturation[1], 100)
colored_bounds_value = (black_bounds_value[1], white_bounds_value[0])

ColorRGB = namedtuple("ColorRGB", ["R", "G", "B"])
ColorHSV = namedtuple("ColorHSV", ["H", "S", "V"])
