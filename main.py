from BCO_gen import BCO

# Ví dụ: f(x) = -(x-3)^2 + 9 (cực đại tại x = 3)
def f1(sol):
    x = sol[0]
    return -(x - 3)**2 + 9

if __name__ == "__main__":
    algo = BCO(fitness_function=f1, B=10, NC=3, max_iterations=15, domain=(-10, 10), dim=1)
    best_sol, best_fit = algo.run()
    print("\n=== Kết quả cuối cùng ===")
    print("Best solution =", best_sol, "Best fitness =", best_fit)
