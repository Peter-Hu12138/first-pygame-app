def get_distance(c):
    return c[0] ** 2 + c[1] ** 2

def quad_map(z, c):
    return ((z[0] ** 2 - z[1] ** 2) + c[0], 2 * z[0] * z[1] + c[1])

def is_candidate(c, z=(0,0), n=10):
    if n == 0:
        return -100 < get_distance(quad_map(z, c)) < 100
    else:
        return is_candidate(c, quad_map(z, c), n - 1)