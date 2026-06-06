# AIDEOM-VN Dashboard

Hệ thống **AIDEOM-VN Dashboard** là một ứng dụng Web tương tác được xây dựng bằng **Streamlit** (Frontend) và các thư viện Tối ưu hóa/Phân tích Dữ liệu mạnh mẽ của Python (Backend: `scipy.optimize`, `pulp`, `gymnasium`, v.v.). Hệ thống này giúp trực quan hóa và giải quyết 12 bài toán mô hình ra quyết định khác nhau (từ Quy hoạch tuyến tính, TOPSIS, Tối ưu động liên thời gian đến Học tăng cường).

---

## 🚀 Hướng dẫn Chạy Hệ thống (Local)

Bạn có thể chạy dự án này bằng **Docker** (nhanh nhất) hoặc cài đặt trực tiếp **Python** trên máy tính (MacOS / Windows).

### Lựa chọn 1: Chạy trực tiếp bằng Python (Khuyên dùng)
Yêu cầu máy tính đã cài đặt sẵn Python (phiên bản 3.10 trở lên).

**Dành cho MacOS / Linux:**
```bash
# 1. Tạo môi trường ảo (Virtual Environment)
python3 -m venv venv

# 2. Kích hoạt môi trường
source venv/bin/activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 4. Khởi chạy Dashboard
streamlit run app.py
```

**Dành cho Windows:**
```powershell
# 1. Tạo môi trường ảo
python -m venv venv

# 2. Kích hoạt môi trường
.\venv\Scripts\activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 4. Khởi chạy Dashboard
streamlit run app.py
```

Sau khi chạy lệnh cuối cùng, trình duyệt sẽ tự động mở trang web tại địa chỉ: 👉 **http://localhost:8501**

---

### Lựa chọn 2: Chạy bằng Docker (Không cần cài đặt Python)
Yêu cầu máy tính đã cài đặt **Docker Desktop**.

```bash
# Khởi động hệ thống (Lần đầu tiên sẽ mất khoảng 2-3 phút để tải thư viện)
docker-compose up --build
```
Truy cập ứng dụng tại: 👉 **http://localhost:8501**

Để dừng hệ thống, bạn gõ `Ctrl + C` trên Terminal hoặc chạy lệnh:
```bash
docker-compose down
```

---

## 📁 Cấu trúc Dự án
- `app.py`: Tệp tin giao diện chính của Streamlit (Frontend Dashboard).
- `src/`: Chứa các thuật toán xử lý tối ưu (Backend).
  - `optimization.py`: Lõi giải thuật các bài toán (LP, NLP, NSGA-II, Scipy SLSQP, v.v.).
  - `rl_env.py`: Môi trường Học tăng cường (Reinforcement Learning) cho Bài 11.
  - `data_loader.py`: Xử lý nạp dữ liệu.
- `notebooks/`: Chứa các file Jupyter Notebook tương ứng cho 12 bài, được tự động sinh ra từ bộ mã nguồn `src/` bằng công cụ `generate_notebooks.py`.
- `data/`: Thư mục chứa các tệp tin CSV/Excel đầu vào.
- `outputs/`: Thư mục lưu trữ các hình ảnh đồ thị và bảng kết quả dạng tĩnh.
- `Dockerfile` & `docker-compose.yml`: Cấu hình môi trường Container chuẩn.
