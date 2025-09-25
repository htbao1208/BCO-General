import math, random
from BCO_gen import BCO

def build_distance_matrix(coords):
    n = len(coords)
    d = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dij = math.hypot(coords[i][0] - coords[j][0],
                             coords[i][1] - coords[j][1])
            d[i][j] = d[j][i] = dij
    return d

def route_length(route, dist):
    n = len(route)
    total = 0.0
    for i in range(n):
        a, b = route[i], route[(i+1) % n]
        total += dist[a][b]
    return total

def two_opt(route, dist, tries=60):
    """Thử cải thiện route bằng 2-opt."""
    best_route = route
    best_delta = 0.0
    for _ in range(tries):
        i, k = sorted(random.sample(range(1, len(route)), 2))
        if i >= k: 
            continue
        # tính delta
        a, b = route[i-1], route[i]
        c, d = route[k], route[(k+1) % len(route)]
        before = dist[a][b] + dist[c][d]
        after = dist[a][c] + dist[b][d]
        delta = after - before
        if delta < best_delta:
            best_delta = delta
            best_route = route[:i] + list(reversed(route[i:k+1])) + route[k+1:]
    return best_route if best_delta < 0 else route

class BCO_TSP(BCO):
    def __init__(self, coords, alpha=1.2, beta=2.0, stagnation_limit=80, **kwargs):
        self.coords = coords
        self.n = len(coords)
        self.dist = build_distance_matrix(coords)
        self.alpha = alpha
        self.beta = beta
        self.stagnation_limit = stagnation_limit

        super().__init__(
            fitness_function=self.evaluate,
            B=kwargs.get("B", 30),
            NC=kwargs.get("NC", 3),
            max_iterations=kwargs.get("max_iterations", 500),
            domain=(0, self.n-1),
            dim=self.n,
        )

    # ==== override các hàm ====
    def evaluate(self, route):
        return -route_length(route, self.dist)  # maximize

    def random_solution(self):
        sol = list(range(self.n))
        random.shuffle(sol)
        return sol

    def constructive_move(self, solution):
        return two_opt(solution, self.dist, tries=30)

    def loyalty_probability(self, fitness, best_fitness):
        gap = (best_fitness - fitness) / (abs(best_fitness) + 1e-9)
        p = math.exp(-self.alpha * gap)
        return max(0.05, min(0.9, p))

    def roulette_choose_recruiter(self, recruiters, bees):
        # recruiter score theo (1/cost^beta)
        scores = [(1.0 / (-bees[i].fitness)) ** self.beta for i in recruiters]
        total = sum(scores)
        pick = random.random() * total
        cum = 0.0
        for idx, w in zip(recruiters, scores):
            cum += w
            if cum >= pick:
                return idx
        return recruiters[-1]

    # ==== run với stagnation limit ====
    def run(self, verbose=True):
        self.initialize()
        best_iter = 0
        best_fit = self.best_fitness

        it = 0
        while it < self.max_iterations and (it - best_iter) < self.stagnation_limit:
            it += 1

            # forward pass
            new_bees = [self.forward_pass(bee) for bee in self.bees]

            # backward pass
            recruiters = self.select_recruiters(new_bees)

            updated_bees = []
            for i in range(self.B):
                if i in recruiters:
                    updated_bees.append(new_bees[i])
                else:
                    chosen = self.roulette_choose_recruiter(recruiters, new_bees)
                    updated_bees.append(new_bees[chosen])
            self.bees = updated_bees

            # update best
            for bee in self.bees:
                if bee.fitness > self.best_fitness:
                    self.best_solution = bee.solution
                    self.best_fitness = bee.fitness
                    best_iter = it

            if verbose and it % 10 == 0:
                print(f"Iter {it:4d} | best = {-self.best_fitness:.3f}")

        if verbose:
            print(f"Kết thúc ở iter {it}, best = {-self.best_fitness:.3f}")
        return self.best_solution, self.best_fitness