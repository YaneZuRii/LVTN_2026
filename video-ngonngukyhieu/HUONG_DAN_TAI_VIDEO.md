# Video ngôn ngữ ký hiệu Việt Nam — nguồn và cách tải

## Nguồn dữ liệu

| Mục | Chi tiết |
|-----|----------|
| Tên dataset | SignConnect (VSL) |
| Nguồn | [Hugging Face — Lakeserl/SignConnect](https://huggingface.co/datasets/Lakeserl/SignConnect) |
| Gốc | QIPEDC / Kaggle VSL |
| Số video | 4362 file `.mp4` (~2,7 GB) |
| Nhãn trên Git | `label.csv` — cột `VIDEO`, `LABEL` (tiếng Việt) |
| Bản local (máy bạn) | `D:\dulieungongukyhieu\vsl-signconnect` |

File video **không** lưu trên GitHub (quá lớn). Chỉ lưu file nhãn.

## Cách tải toàn bộ video về máy

### Cách 1 — Hugging Face (khuyên dùng)

```powershell
pip install huggingface_hub
```

```python
from pathlib import Path
from huggingface_hub import snapshot_download

dest = Path(r"D:\dulieungongukyhieu\vsl-signconnect")
dest.mkdir(parents=True, exist_ok=True)
snapshot_download(
    repo_id="Lakeserl/SignConnect",
    repo_type="dataset",
    local_dir=str(dest),
    allow_patterns=["Videos/*.mp4", "Text/label.csv"],
)
```

Video nằm tại: `...\vsl-signconnect\Videos\`

### Cách 2 — Trang web Hugging Face

1. Mở https://huggingface.co/datasets/Lakeserl/SignConnect/tree/main/Videos  
2. Tải từng file hoặc dùng CLI của Hugging Face.

## Ghép nhãn với video

Mỗi dòng trong `label.csv`:

```text
ID,VIDEO,LABEL
5,D0002.mp4,tỉnh
```

Mở `Videos\D0002.mp4` tương ứng với nhãn **tỉnh**.