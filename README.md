# Bee Colony Optimization (BCO) – General & TSP

Thuật toán **Bee Colony Optimization (BCO)** mô phỏng hành vi tìm kiếm thức ăn của ong mật.  
Repo này gồm phần **cài đặt tổng quát** và ví dụ **ứng dụng cho Travelling Salesman Problem (TSP)**.

---

## Cấu trúc repo

BCO-General/
│
├── BCO_gen.py # Thuật toán BCO tổng quát (class Bee, class BCO)
├── main.py # Ví dụ: chạy BCO trên hàm f(x) = -(x-3)^2 + 9
└── tsp.py # Ứng dụng: giải Travelling Salesman Problem (TSP)
---

## Cách hoạt động của BCO

1. **Khởi tạo (Initialize)**  
   Sinh quần thể ong với nghiệm ngẫu nhiên, tính fitness và chọn nghiệm tốt nhất ban đầu.

2. **Forward pass**  
   Mỗi ong mở rộng nghiệm của mình trong `NC` bước bằng `constructive_move`.  
   Nếu nghiệm mới tốt hơn thì cập nhật.

3. **Backward pass**  
   - Chọn một số ong tốt làm recruiter.  
   - Các ong còn lại (followers) chọn recruiter bằng roulette wheel.

4. **Cập nhật nghiệm tốt nhất**  
   Sau mỗi vòng, kiểm tra để lưu nghiệm tốt nhất toàn cục.

5. **Lặp lại**  
   Tiếp tục cho đến khi đạt số vòng lặp tối đa (`max_iterations`)  
   hoặc dừng sớm nếu có stagnation limit (trong TSP).

---

## Ví dụ 1: BCO tổng quát

Trong `main.py`:

```python
from BCO_gen import BCO

# Hàm f(x) = -(x-3)^2 + 9, cực đại tại x = 3
def f1(sol):
    x = sol[0]
    return -(x - 3)**2 + 9

bco = BCO(fitness_function=f1, B=10, NC=3, max_iterations=15, domain=(-10, 10), dim=1)
best_sol, best_fit = bco.run()
print("Best solution:", best_sol, "Best fitness:", best_fit)
Kết quả: nghiệm hội tụ gần x=3, fitness ~9.

Ví dụ 2: BCO cho TSP
Trong tsp.py, BCO được tùy biến để giải Travelling Salesman Problem:

Biểu diễn nghiệm: hoán vị các thành phố (permutation).

Fitness:

Copy code
fitness(route) = -tour_length(route)
vì BCO maximize, còn TSP cần minimize.

Constructive move: áp dụng 2-opt để cải thiện tour.

Recruiters & Followers: ong tốt làm recruiter, followers chọn recruiter theo roulette wheel dựa trên (1/cost^β).

Stagnation limit: dừng khi không cải thiện thêm sau nhiều vòng.

Kết quả mẫu:

yaml
Copy code
Iter   10 | best = 4369.956
Iter   20 | best = 4356.673
...
Iter  100 | best = 4235.482
Kết thúc ở iter 111, best = 4235.482

Best tour length: 4235.482
Best route: [27, 7, 24, 12, 3, 9, 20, ...]
Tour tìm được cũng được lưu ra file tour.csv để trực quan hóa.

Tham số chính
B: số ong trong quần thể.

NC: số bước constructive move trong forward pass.

max_iterations: số vòng lặp tối đa.

domain, dim: miền và số chiều nghiệm (trong bản general).

alpha, beta: tham số điều khiển loyalty và cách followers chọn recruiter (TSP).

stagnation_limit: số vòng không cải thiện trước khi dừng (TSP).
