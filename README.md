[README.md](https://github.com/user-attachments/files/22453299/README.md)
#  Bee Colony Optimization (BCO) – General Version

##  Giới thiệu
Thuật toán **Bee Colony Optimization (BCO)** mô phỏng hành vi tìm kiếm thức ăn của ong mật.  
BCO gồm 2 pha lặp lại:  
- **Forward pass**: ong tự mở rộng nghiệm trong vài bước.  
- **Backward pass**: ong quay về tổ, chia sẻ nghiệm, rồi quyết định làm recruiter hay follower.  

Ong tốt hơn dễ trở thành recruiter, ong còn lại chọn recruiter theo roulette wheel.  
Thuật toán lặp đến khi đạt điều kiện dừng và trả về nghiệm tốt nhất.

---

##  Cấu trúc chính
- `Bee`: lưu `solution` và `fitness`.  
- `BCO`: lớp chính với các hàm:  
  - `initialize`: khởi tạo ong ngẫu nhiên.  
  - `constructive_move`: sinh bước đi mới quanh nghiệm.  
  - `forward_pass`: mỗi ong khám phá NC bước.  
  - `backward_pass`: đánh giá và xếp hạng ong.  
  - `loyalty_probability`: xác suất ong giữ nghiệm riêng.  
  - `select_recruiters`: chọn recruiter.  
  - `roulette_choose_recruiter`: follower chọn recruiter.  
  - `run`: vòng lặp chính.  

---

##  Ví dụ chạy thử

### Ví dụ 1: Hàm 1 biến
```python
# Hàm: f(x) = -(x-3)^2 + 9
# Cực đại tại x=3, giá trị f(3)=9
from bco_general import BCO

def f1(sol):
    x = sol[0]
    return -(x - 3)**2 + 9

bco = BCO(fitness_function=f1, B=10, NC=3, max_iterations=15, domain=(-10, 10), dim=1)
best_sol, best_fit = bco.run()
print("Best solution:", best_sol, "Best fitness:", best_fit)
```

 Kết quả:  
```
Best solution ≈ 3.00145
Best fitness ≈ 8.9999979
```

 Thuật toán tìm được nghiệm gần **x=3** với fitness gần **9**, rất sát cực đại lý thuyết.

---

### Ví dụ 2: Hàm nhiều biến (Sphere)
```python
def sphere(sol):
    return -sum(x**2 for x in sol)

bco2 = BCO(fitness_function=sphere, B=20, NC=3, max_iterations=30, domain=(-5, 5), dim=2)
best_sol, best_fit = bco2.run()
print("Best solution:", best_sol, "Best fitness:", best_fit)
```

 Kết quả: nghiệm gần `[0,0]` với fitness ≈ 0 (đúng cực đại toàn cục).  

---

##  Giải thích kết quả
- **Ban đầu**: ong phân tán ngẫu nhiên.  
- **Trong quá trình lặp**: ong tốt hơn có cơ hội làm recruiter, ong khác theo recruiter → dần hội tụ.  
- **Kết thúc**: nghiệm gần cực đại toàn cục.  

Ví dụ với hàm `f(x) = -(x-3)^2 + 9`:  
- Iter 1: ong tìm nghiệm quanh `x≈3.1`, fitness ≈ 8.99.  
- Iter 2–7: fitness tăng dần lên 8.9999, nghiệm dao động quanh [2.99–3.01].  
- Iter 8–15: nghiệm hội tụ về ~3.001, fitness ~8.999998 ≈ 9.  

 Điều này cho thấy BCO tìm kiếm đúng hướng và hội tụ về nghiệm tối ưu.  

---

##  Tham số
- `B`: số ong (10–50).  
- `NC`: số bước xây dựng (3–5).  
- `max_iterations`: số vòng lặp.  
- `domain`: miền tìm kiếm.  
- `dim`: số chiều nghiệm.  
