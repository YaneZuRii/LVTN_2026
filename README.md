# NNKH — Giao diện phiên dịch (demo MediaPipe)

Ứng dụng desktop Python, layout gần mock Figma (~90%): camera trực tiếp, nhận landmark MediaPipe.

## Tính năng

- **Dịch:** webcam (lật gương), vẽ landmark
  - Tối đa **2 tay** (MediaPipe Hands)
  - **Vai & khuỷu tay** (Pose: 11–14)
  - **4 điểm miệng** (Face Mesh)
- **Tra cứu / Luyện:** placeholder giao diện (nút pill trái)

MediaPipe **1.x** dùng API `tasks` (không còn `mp.solutions`). Lần chạy đầu sẽ tự tải các file `.task` vào thư mục `models/`.

## Cài đặt

```bash
cd D:\codeNNKH
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Mở trên web (trình duyệt)

Camera chạy **trên máy bạn** trong trình duyệt (MediaPipe JS). Cần **internet** lần đầu để tải model/WASM.

```bash
cd D:\codeNNKH
.\.venv\Scripts\activate
pip install fastapi uvicorn
python web_app.py
```

Mở trình duyệt: **http://127.0.0.1:8080** → bấm **Cho phép** khi được hỏi quyền camera.

- Máy khác trong mạng LAN: sửa `web_app.py` → `host="0.0.0.0"` rồi vào `http://<IP-máy-bạn>:8080` (vẫn cần HTTPS/camera policy tùy trình duyệt).
- Bản desktop (`app.py`) dùng Python + OpenCV; bản web (`web_app.py`) dùng JavaScript MediaPipe — giao diện giống nhau.

## Cấu trúc

- `app.py` — giao diện desktop (Tkinter)
- `web_app.py` + `static/` — giao diện web
- `vision.py` — MediaPipe (tay, pose, miệng)
- `logo.py` — logo tròn; `static/logo.png` cho web
- `models.py` — tải file `.task`

## Ghi chú luận văn

Vùng **Phiên dịch** hiện là mẫu (`ABC`, `cdscv`). Có thể nối model sklearn / API từ dự án `E:\ont7\backend` sau.