import math


def get_appromixate_dimension(dimension, factor):
    sections = dimension / factor
    weight = sections % 1
    if weight < 0.5:
        return math.floor(sections) * factor
    else:
        return math.ceil(sections) * factor


def get_standard_image_dimensions(dimensions, factor):
    old_width, old_height = dimensions
    new_width = get_appromixate_dimension(old_width, factor)
    new_height = get_appromixate_dimension(old_height, factor)
    return new_width, new_height


# Small Scale Dimensions are gotten after standardizing
def get_small_scale_dimensions(dimensions, factor):
    big_width, big_height = get_standard_image_dimensions(dimensions, factor)
    small_width = int(big_width / factor)
    small_height = int(big_height / factor)
    return small_width, small_height
