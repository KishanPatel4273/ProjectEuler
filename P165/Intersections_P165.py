import math

def cross(A: tuple[int, int], B: tuple[int, int]) -> int:
    return A[0] * B[1] - B[0] * A[1]

def sub(A: tuple[int, int], B: tuple[int, int]) -> tuple[int, int]:
    return (A[0] - B[0], A[1] - B[1])

def add(A: tuple[int, int], B: tuple[int, int]) -> tuple[int, int]:
    return (A[0] + B[0], A[1] + B[1])

def reduce(A: tuple[int, int]) -> tuple[int, int]:
    gcd = math.gcd(A[0], A[1])
    if A[0] < 0 and A[1] < 0:
        return (-A[0] // gcd, -A[1] // gcd)
    return (A[0] // gcd, A[1] // gcd)


def true_intersection(A, B, C, D):
    r1 = sub(A, B)
    r2 = sub(C, D)
    r1xr2 = cross(r1, r2)
    if r1xr2 == 0:
        return False
    
    # r1 * u + B = r2 * v + D
    
    # r1 x [r1 * u + B = r2 * v + D]
    # r1xB = r1xr2 * v + r1xD
    # r1x(B-D)= r1xr2 * v
    b_d = sub(B, D)
    
    v = reduce((cross(r1, b_d), r1xr2))

    # r2 x [r1 * u + B = r2 * v + D]
    # r2xr1 * u +  r2 x B = r2 x D
    # r2xr1 * u = r2 x (D - B)
    # -r1xr2 * u = -r2 x (B - D)
    # r1xr2 * u = r2 x (B - D)
    u = reduce((cross(r2, b_d), r1xr2))

    
    # 0 <= u,v <= 1 -> intersection
    # u,v = 0 or 1 then end point
    if not ((0 < u[1] and 0 <= u[0] <= u[1]) or (u[1] < 0 and u[1] <= u[0] <= 0)):
        return False
    if not ((0 < v[1] and 0 <= v[0] <= v[1]) or (v[1] < 0 and v[1] <= v[0] <= 0)):
        return False
    
    if u[0] == 0 or  u[0] == u[1]:
        return False
    if v[0] == 0 or  v[0] == v[1]:
        return False
    

    # r1 * u + B = r2 * v + D
    pu1x = reduce((r1[0] * u[0] + B[0] * u[1], u[1]))
    pu1y = reduce((r1[1] * u[0] + B[1] * u[1], u[1]))

    pv1x = reduce((r2[0] * v[0] + D[0] * v[1], v[1]))
    pv1y = reduce((r2[1] * v[0] + D[1] * v[1], v[1]))

    assert((pu1x, pu1y) == (pv1x, pv1y))
    
    return (pu1x, pu1y)

def solve():
    
    s0 = 290797
    s = [s0]
    t = []

    for n in range(5_000 * 4):
        s_n = (s[-1]*s[-1]) % 50515093
        s.append(s_n)
        t.append(s_n % 500)
    
    res = []
    for i in range(5_000):
        for j in range(5_000):
            if i == j:
                continue
            
            pi = 4*i
            pj = 4*j
            r = true_intersection(
                (t[pi], t[pi + 1]), (t[pi + 2], t[pi + 3]),
                (t[pj], t[pj + 1]), (t[pj + 2], t[pj + 3]))
            
            if not r == False:
                res.append(r)
    print(f'number of true intersections {len(res)}, unique : {len(set(res))}')

solve()