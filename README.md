# Bee Colony Optimization (BCO) – General & TSP

## Giới thiệu
Thuật toán **Bee Colony Optimization (BCO)** mô phỏng hành vi tìm kiếm thức ăn của ong mật.  
Mỗi vòng lặp gồm 2 pha chính:

- **Forward pass**: mỗi ong mở rộng nghiệm của mình trong vài bước để tìm nghiệm tốt hơn.  
- **Backward pass**: ong quay về tổ, chia sẻ nghiệm. Ong có nghiệm tốt trở thành **recruiter**, ong khác trở thành **followers** và chọn recruiter theo roulette wheel.  

Quá trình này giúp cả đàn ong vừa khai phá (exploration) vừa khai thác (exploitation), dần dần tiến tới nghiệm tốt nhất.

---

## Cấu trúc repo
- `BCO_gen.py`  
  - `Bee`: lưu nghiệm (`solution`) và giá trị (`fitness`).  
  - `BCO`: cài đặt tổng quát gồm các bước khởi tạo, forward, backward, chọn recruiter, cập nhật nghiệm tốt nhất.  

- `main.py`  
  Ví dụ chạy BCO trên hàm đơn giản \( f(x) = -(x-3)^2 + 9 \).  

- `tsp.py`  
  Ví dụ áp dụng BCO cho bài toán **Travelling Salesman Problem (TSP)**.  

---

## Hoạt động của BCO tổng quát
1. **Khởi tạo**: sinh quần thể ong ngẫu nhiên trong miền giá trị.  
2. **Forward pass**: mỗi ong thực hiện `NC` lần constructive move để cải thiện nghiệm.  
3. **Backward pass**: chọn recruiters theo fitness. Followers chọn recruiter theo roulette wheel.  
4. **Cập nhật nghiệm tốt nhất**.  
5. **Lặp** đến khi đạt số vòng lặp tối đa.  

---

## Ví dụ 1: General benchmark
```python
from BCO_gen import BCO

def f1(sol):
    x = sol[0]
    return -(x - 3)**2 + 9

bco = BCO(fitness_function=f1, B=10, NC=3, max_iterations=15, domain=(-10, 10), dim=1)
best_sol, best_fit = bco.run()
print("Best solution:", best_sol, "Best fitness:", best_fit)
Kết quả: nghiệm hội tụ gần 
𝑥
=
3
x=3, fitness ~9 (đúng cực đại lý thuyết).

Ví dụ 2: BCO cho TSP
Trong tsp.py, BCO được tùy biến cho bài toán TSP với các điểm khác biệt:

Biểu diễn nghiệm
Nghiệm là hoán vị (permutation) của các thành phố, ví dụ [0, 2, 1, 3] là thứ tự đi qua 4 thành phố.

Hàm đánh giá (fitness)
Mục tiêu: minimize độ dài tour.

Vì BCO tổng quát là maximize, ta định nghĩa:

\text{fitness(route)} = -\text{tour_length(route)}
Constructive move (khai thác nghiệm)
Sử dụng 2-opt local search: chọn ngẫu nhiên 2 cạnh trong tour, đảo ngược đoạn giữa → có thể giảm chiều dài tour.

Loyalty & Recruiters
Loyalty probability được tính theo công thức hàm mũ:

𝑝
=
exp
⁡
(
−
𝛼
⋅
cost
−
best_cost
best_cost
)
p=exp(−α⋅ 
best_cost
cost−best_cost
​
 )
→ route càng tệ thì ong càng dễ bỏ nghiệm riêng và theo recruiter.

Recruiters: ong có route tốt sẽ được chọn làm recruiter.

Followers: chọn recruiter theo roulette wheel với trọng số 
(
1
/
𝑐
𝑜
𝑠
𝑡
)
𝛽
(1/cost) 
β
 .

Điều kiện dừng
Ngoài số vòng lặp tối đa, tsp.py có thêm stagnation_limit: nếu sau X vòng không cải thiện nghiệm tốt nhất, thuật toán dừng sớm.

Quy trình chạy
Khởi tạo ngẫu nhiên một số tour.

Mỗi vòng:

Ong recruiter áp dụng 2-opt mạnh để cải thiện.

Ong follower: hoặc tiếp tục cải thiện nghiệm riêng, hoặc copy route recruiter và cải thiện.

Cập nhật tour ngắn nhất tìm được.

Dừng khi đạt max_iterations hoặc vượt quá stagnation_limit.

Kết quả mẫu
yaml
Copy code
Iter   10 | best = 4369.956
Iter   20 | best = 4356.673
...
Iter  100 | best = 4235.482
Kết thúc ở iter 111, best = 4235.482

Best tour length: 4235.482
Best route (index): [27, 7, 24, 12, 3, 9, ...]
Tour thu được được ghi vào file tour.csv để trực quan hóa hoặc vẽ.

Tham số chính
B: số ong.

NC: số bước xây dựng trong forward pass.

max_iterations: số vòng lặp tối đa.

domain, dim: dùng cho biến thực trong bản general.

alpha, beta: điều khiển loyalty và xác suất follower chọn recruiter trong TSP.

stagnation_limit: số vòng không cải thiện → dừng sớm (chỉ trong tsp.py).
