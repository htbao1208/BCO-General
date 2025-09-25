import random
from BCO_gen import BCO
from TSP import BCO_TSP

# ====== Hàm test cho General BCO ======
# f(x) = -(x-3)^2 + 9, cực đại tại x=3
def f1(sol):
    x = sol[0]
    return -(x - 3)**2 + 9

# ====== Sinh tọa độ ngẫu nhiên cho TSP ======
def random_coords(n, width=1000, height=1000, seed=42):
    random.seed(seed)
    return [(random.random()*width, random.random()*height) for _ in range(n)]

if __name__ == "__main__":
    print("=== Chạy Bee Colony Optimization (BCO) ===")
    print("1. General benchmark (f1(x) = -(x-3)^2 + 9)")
    print("2. Travelling Salesman Problem (TSP)")
    choice = input("Chọn chế độ (1 hoặc 2): ").strip()

    if choice == "1":
        print("\n--- BCO General ---")
        algo = BCO(fitness_function=f1,
                   B=10, NC=3,
                   max_iterations=15,
                   domain=(-10, 10), dim=1)

        best_sol, best_fit = algo.run(verbose=True)
        print("\n=== Kết quả cuối cùng (General) ===")
        print("Best solution =", best_sol, "Best fitness =", best_fit)

    elif choice == "2":
        print("\n--- BCO TSP ---")
        n_cities = 30
        coords = random_coords(n_cities, seed=42)  # giữ seed để tái lập kết quả
        bco = BCO_TSP(coords,
                      B=30,
                      max_iterations=500,
                      stagnation_limit=80,
                      seed=42)

        best_route, best_fit = bco.run(verbose=True)
        print("\n=== Kết quả cuối cùng (TSP) ===")
        print("Best tour length:", -best_fit)
        print("Best route (index):", best_route)

        # Xuất tour ra CSV để vẽ
        with open("tour.csv", "w", encoding="utf-8") as f:
            f.write("order,city_id,x,y\n")
            for order, cid in enumerate(best_route):
                x, y = coords[cid]
                f.write(f"{order},{cid},{x},{y}\n")
            first = best_route[0]
            fx, fy = coords[first]
            f.write(f"{len(best_route)},{first},{fx},{fy}\n")
        print("Đã ghi tour vào file tour.csv")

    else:
        print("Lựa chọn không hợp lệ!")