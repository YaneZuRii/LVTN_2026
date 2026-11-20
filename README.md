# LVTN 2026

Repo: https://github.com/YaneZuRii/LVTN_2026

| Thư mục | Nội dung |
|---------|----------|
| `video-ngonngukyhieu/` | Nhãn video VSL (`label.csv`) + hướng dẫn tải clip |
| *(gốc repo)* `database/` | CSDL mẫu (SQL) và API PHP (LTDD) — xem lịch sử commit trên GitHub |

## Trang chủ NNKH — nhận diện landmark (MediaPipe)

Giao diện **Dịch / Tra cứu / Luyện**: webcam + vẽ **2 tay**, **vai & khuỷu tay**, **4 điểm miệng**.

### Chạy desktop

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Chạy web

```bash
pip install -r requirements.txt
python web_app.py
```

Mở **http://127.0.0.1:8080** và cho phép camera.

### File chính

- `app.py`, `web_app.py`, `static/` — UI
- `vision.py`, `models.py` — MediaPipe Tasks (Python)
- `logo.py`, `assets/`

Lần đầu chạy desktop tự tải file `.task` vào `models/`. Web tải WASM/model qua CDN.