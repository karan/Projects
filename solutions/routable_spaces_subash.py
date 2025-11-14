# Routable Spaces - Solution by Subash
# Problem #130
#
# Task:
# Given point pairs, generate routes between every pair of points
# while staying inside the bounding rectangle and avoiding path crossing.

def get_bounding_box(point_pairs):
    xs = []
    ys = []
    for (x1, y1), (x2, y2) in point_pairs:
        xs += [x1, x2]
        ys += [y1, y2]
    return min(xs), min(ys), max(xs), max(ys)


def manhattan_route(start, end, occupied):
    """
    Simple Manhattan path routing:
    Goes horizontal first then vertical.
    Avoids crossing by checking occupied coordinates.
    """

    (x1, y1) = start
    (x2, y2) = end

    path = []

    # Horizontal movement
    step = 1 if x2 > x1 else -1
    for x in range(x1, x2, step):
        if (x, y1) in occupied:
            # shift the route upward to avoid crossing
            y1 += 1
        path.append((x, y1))

    # Vertical movement
    step = 1 if y2 > y1 else -1
    for y in range(y1, y2, step):
        if (x2, y) in occupied:
            # shift the route rightward to avoid crossing
            x2 += 1
        path.append((x2, y))

    path.append(end)
    return path


def route_all(point_pairs):
    minx, miny, maxx, maxy = get_bounding_box(point_pairs)

    occupied = set()
    all_routes = []

    for (p1, p2) in point_pairs:
        route = manhattan_route(p1, p2, occupied)

        # prevent crossing: mark all used coordinates
        for pt in route:
            occupied.add(pt)

        all_routes.append(route)

    return all_routes


# --------------------------
# Example usage
# --------------------------

if __name__ == "__main__":
    pairs = [
        ((1, 1), (5, 5)),
        ((2, 4), (7, 2)),
        ((3, 3), (6, 6))
    ]

    routes = route_all(pairs)

    print("Generated Routes:")
    for r in routes:
        print(r)
