from helpers import read_input, begin_part_one, begin_part_two, solution
import numpy as np


def process_inputs(inputs: list[str]):
    return np.array([[int(y) for y in list(x)] for x in inputs])


def get_lowpoints(heights):
    """
    Find every point in a 2D array of heights that is lower
    than all its adjacent points, including points on the edges.
    """
    rows, cols = heights.shape
    lowpoints = []
    for i in range(rows):
        for j in range(cols):
            is_vert_low = False
            if i == 0 or heights[i - 1, j] > heights[i, j]:
                if (i == rows - 1) or heights[i, j] < heights[i + 1, j]:
                    is_vert_low = True
            is_horiz_low = False
            if j == 0 or heights[i, j - 1] > heights[i, j]:
                if (j == cols - 1) or heights[i, j] < heights[i, j + 1]:
                    is_horiz_low = True
            if is_horiz_low and is_vert_low:
                # print(f"{i, j} is low")
                lowpoints.append([i, j])
    return lowpoints


def expand(point, heights):
    """
    For a point in an array of heights, find any adjacent points
    that are higher than it, excluding the number 9.
    """
    i, j = point
    rows, cols = heights.shape
    expanded_points = []
    # expand in the vertical direction
    if i > 0 and heights[i - 1, j] > heights[i, j] and heights[i - 1, j] != 9:
        expanded_points.append([i - 1, j])
    if (i < rows - 1) and heights[i, j] < heights[i + 1, j] and heights[i + 1, j] != 9:
        expanded_points.append([i + 1, j])
    # expand in the horizontal direction
    if j > 0 and heights[i, j - 1] > heights[i, j] and heights[i, j - 1] != 9:
        expanded_points.append([i, j - 1])
    if (j < cols - 1) and heights[i, j] < heights[i, j + 1] and heights[i, j + 1] != 9:
        expanded_points.append([i, j + 1])
    return expanded_points


def get_basins(heights):
    """
    In a 2D array of heights, compute all "basins", defined as a mutually
    adjacent set of points that all flow downhill to a single low point,
    but excluding the number 9 (the highest point).

    Returns an array of basins, where a basin is an array of position
    indices (i,j) in the heights array.
    """
    lowpoints = get_lowpoints(heights)
    basins = []
    for lowpoint in lowpoints:
        # expand point to build up the basin
        basin = [lowpoint]
        while True:
            new_basin = basin
            # expand each point in the basin
            for point in basin:
                expanded = expand(point, heights)
                for expanded_point in expanded:
                    if expanded_point not in basin:
                        new_basin.append(expanded_point)
            if len(new_basin) == len(basin):
                break
            else:
                basin = new_basin
        basins.append(basin)
    return basins


inputs = read_input("./inputs/day9.txt")
heightmap = process_inputs(inputs)
print(heightmap)


begin_part_one()
lowpoints = get_lowpoints(heightmap)
solution(np.sum(lowpoints) + len(lowpoints))


begin_part_two()
basins = get_basins(heightmap)
basin_sizes = sorted([len(basin) for basin in basins], reverse=True)
print("Basin sizes: ", basin_sizes)

solution(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
