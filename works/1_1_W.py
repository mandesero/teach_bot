# x + y
# x and y - конъюнкция
# x or y - дизъюнкция
# int(not x) - отрицание
# int(x <= y) - импликация
# int(x == y) - равенство

# x y
# 0 0
# 0 1
# 1 0
# 1 1
# ¬x ∨ y ∨ (¬z ∧ w)

for x in range(0, 2):
    for y in range(0, 2):
        for w in range(0, 2):
            for z in range(0, 2):
                f = int(not x) or y or (int(not z) and w)
                if f == 0:
                    print(x, y, w, z, f)
