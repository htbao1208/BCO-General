import random


class Bee:
    #Đại diện cho một ong trong BCO.

    def __init__(self, solution=None, fitness=float("-inf")):
        self.solution = solution
        self.fitness = fitness


class BCO:
    """
    Bee Colony Optimization (BCO) - General

    Parameters
    ----------
    fitness_function : callable
        Hàm đánh giá (maximize), nhận list[float] → trả về float.
    B : int
        Số lượng ong.
    NC : int
        Số bước xây dựng trong mỗi forward pass.
    max_iterations : int
        Số vòng lặp tối đa.
    domain : tuple
        Miền giá trị (min, max) cho mỗi biến.
    dim : int
        Số chiều của nghiệm.
    """

    def __init__(self, fitness_function, B=20, NC=3,
                 max_iterations=50, domain=(-10, 10), dim=1):

        self.fitness_function = fitness_function
        self.B = B
        self.NC = NC
        self.max_iterations = max_iterations
        self.domain = domain
        self.dim = dim

        self.bees = []
        self.best_solution = None
        self.best_fitness = float("-inf")

    # Các hàm hỗ trợ

    def initialize(self):
        #Khởi tạo đàn ong với nghiệm ngẫu nhiên.
        self.bees = []
        for _ in range(self.B):
            sol = self.random_solution()
            fit = self.fitness_function(sol)
            bee = Bee(sol, fit)
            self.bees.append(bee)

            if fit > self.best_fitness:
                self.best_solution, self.best_fitness = sol, fit

    def random_solution(self):
        #Sinh nghiệm ngẫu nhiên.
        return [random.uniform(*self.domain) for _ in range(self.dim)]

    def constructive_move(self, solution):
        #Sinh bước di chuyển mới quanh nghiệm hiện tại."
        new_solution = []
        for x in solution:
            step = random.uniform(-1, 1)
            val = max(self.domain[0], min(self.domain[1], x + step))
            new_solution.append(val)
        return new_solution

    def forward_pass(self, bee):
        #Mỗi ong mở rộng nghiệm trong NC bước.
        sol = bee.solution[:]
        for _ in range(self.NC):
            candidate = self.constructive_move(sol)
            if self.fitness_function(candidate) > self.fitness_function(sol):
                sol = candidate
        fit = self.fitness_function(sol)
        return Bee(sol, fit)

    def loyalty_probability(self, fitness, best_fitness):
        #Xác suất ong trung thành tiếp tục khám phá nghiệm riêng.
        if best_fitness == 0:
            return 0.5
        return fitness / (best_fitness + 1e-9)

    def select_recruiters(self, bees):
        #Chọn recruiters dựa trên chất lượng nghiệm.
        scores = [bee.fitness for bee in bees]
        ranked_idx = sorted(range(len(bees)),
                            key=lambda i: scores[i],
                            reverse=True)

        recruiters = []
        for idx in ranked_idx:
            prob = self.loyalty_probability(bees[idx].fitness,
                                            scores[ranked_idx[0]])
            if random.random() < prob:
                recruiters.append(idx)

        if not recruiters:  # đảm bảo có ít nhất 1 recruiter
            recruiters.append(ranked_idx[0])
        return recruiters

    def roulette_choose_recruiter(self, recruiters, bees):
        """Followers chọn recruiter theo roulette wheel."""
        scores = [bees[i].fitness for i in recruiters]
        total = sum(scores)
        probs = [s / total for s in scores]
        return random.choices(recruiters, weights=probs)[0]

    # Thuật toán chính

    def run(self, verbose=True):
        """Chạy thuật toán BCO."""
        self.initialize()

        for it in range(self.max_iterations):
            # 1. Forward pass
            new_bees = [self.forward_pass(bee) for bee in self.bees]

            # 2. Backward pass + chọn recruiters
            recruiters = self.select_recruiters(new_bees)

            # 3. Followers chọn recruiter
            updated_bees = []
            for i in range(self.B):
                if i in recruiters:
                    updated_bees.append(new_bees[i])
                else:
                    chosen = self.roulette_choose_recruiter(recruiters, new_bees)
                    updated_bees.append(new_bees[chosen])
            self.bees = updated_bees

            # 4. Cập nhật nghiệm tốt nhất
            for bee in self.bees:
                if bee.fitness > self.best_fitness:
                    self.best_solution = bee.solution
                    self.best_fitness = bee.fitness

            if verbose:
                print(f"Iter {it+1:3d} | "
                      f"Best fitness = {self.best_fitness:.6f}, "
                      f"Best solution = {self.best_solution}")

        return self.best_solution, self.best_fitness
