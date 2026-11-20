
from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
import cv2
from PIL import Image, ImageTk

from logo import render_circular
from vision import LandmarkProcessor

COLOR_BG = "#FFFFFF"
COLOR_BLACK = "#0A0A0A"
COLOR_WHITE = "#FFFFFF"
COLOR_PANEL = "#111111"

VIDEO_SIZE = 504
WIN_W = 1440
WIN_H = 1024


def make_logo(size: int = 56) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(render_circular(size, bg=COLOR_BLACK))


class PillButton(tk.Canvas):
    def __init__(
        self,
        master,
        text: str,
        *,
        active: bool = False,
        command=None,
        width=240,
        height=52,
        **kwargs,
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            bg=COLOR_BG,
            highlightthickness=0,
            **kwargs,
        )
        self._text = text
        self._active = active
        self._command = command
        self.bind("<Configure>", self._redraw)
        self.bind("<Button-1>", self._on_click)
        self._redraw()

    def set_active(self, active: bool) -> None:
        self._active = active
        self._redraw()

    def _on_click(self, _event) -> None:
        if self._command:
            self._command()

    def _redraw(self, _event=None) -> None:
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        if self._active:
            fill, outline, fg = COLOR_BLACK, COLOR_BLACK, COLOR_WHITE
        else:
            fill, outline, fg = COLOR_WHITE, COLOR_BLACK, COLOR_BLACK
        self.create_oval(0, 0, h, h, fill=fill, outline=outline, width=2)
        self.create_oval(w - h, 0, w, h, fill=fill, outline=outline, width=2)
        self.create_rectangle(h // 2, 0, w - h // 2, h, fill=fill, outline="")
        self.create_line(h // 2, 0, w - h // 2, 0, fill=outline, width=2)
        self.create_line(h // 2, h, w - h // 2, h, fill=outline, width=2)
        self.create_text(
            w // 2,
            h // 2,
            text=self._text,
            fill=fg,
            font=("Segoe UI", 13, "bold"),
        )


class MainPanel(tk.Canvas):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, bg=COLOR_BG, highlightthickness=0, **kwargs)
        self._photo: ImageTk.PhotoImage | None = None
        self.bind("<Configure>", self._redraw)

    def set_frame(self, photo: ImageTk.PhotoImage) -> None:
        self._photo = photo
        self._redraw()

    def layout_metrics(self) -> dict[str, int]:
        w = max(self.winfo_width(), 1080)
        h = max(self.winfo_height(), 780)
        pad = 6
        inner_w = w - 2 * pad
        inner_h = h - 2 * pad
        gap_div = 32
        mx = 28
        video_size = int(min(inner_h * 0.86, inner_w * 0.43, VIDEO_SIZE))
        vx = pad + mx
        vy = pad + (inner_h - video_size) // 2
        div_x = vx + video_size + gap_div
        line_inset = int(video_size * 0.1)
        return {
            "w": w,
            "h": h,
            "pad": pad,
            "video_size": video_size,
            "vx": vx,
            "vy": vy,
            "div_x": div_x,
            "line_y1": vy + line_inset,
            "line_y2": vy + video_size - line_inset,
            "tx": div_x + 28,
            "ty": vy + 12,
        }

    def _redraw(self, _event=None) -> None:
        self.delete("all")
        m = self.layout_metrics()
        w, h, pad = m["w"], m["h"], m["pad"]
        vs = m["video_size"]
        vx, vy, div_x = m["vx"], m["vy"], m["div_x"]

        self.create_rounded_rect(
            pad, pad, w - pad, h - pad, r=32, fill=COLOR_PANEL, outline=""
        )

        self.create_rectangle(
            vx - 4,
            vy - 4,
            vx + vs + 4,
            vy + vs + 4,
            fill=COLOR_WHITE,
            outline="",
        )

        if self._photo:
            self.create_image(vx + vs // 2, vy + vs // 2, image=self._photo)
        else:
            self.create_text(
                vx + vs // 2,
                vy + vs // 2,
                text="Đang mở camera…",
                fill="#666",
                font=("Segoe UI", 12),
            )

        self.create_line(
            div_x, m["line_y1"], div_x, m["line_y2"], fill=COLOR_WHITE, width=2
        )

        self.create_text(
            m["tx"],
            m["ty"],
            text="Phiên dịch:",
            anchor="nw",
            fill=COLOR_WHITE,
            font=("Segoe UI", 22, "bold"),
        )

    def create_rounded_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [
            x1 + r,
            y1,
            x2 - r,
            y1,
            x2,
            y1,
            x2,
            y1 + r,
            x2,
            y2 - r,
            x2,
            y2,
            x2 - r,
            y2,
            x1 + r,
            y2,
            x1,
            y2,
            x1,
            y2 - r,
            x1,
            y1 + r,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("NNKH — Không âm thanh - không khoảng cách")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.configure(bg=COLOR_BG)
        self.minsize(960, 680)

        self._processor = LandmarkProcessor()
        self._cap: cv2.VideoCapture | None = None
        self._running = True
        self._current_tab = "dich"
        self._translation_lines = ["ABC", "cdscv"]

        title_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")

        # Header
        header = tk.Frame(self, bg=COLOR_BG)
        header.pack(fill=tk.X, padx=52, pady=(36, 22))
        self._logo = make_logo(56)
        tk.Label(header, image=self._logo, bg=COLOR_BG).pack(side=tk.LEFT)
        tk.Label(
            header,
            text="Không âm thanh - không khoảng cách",
            font=title_font,
            bg=COLOR_BG,
            fg=COLOR_BLACK,
        ).pack(side=tk.LEFT, padx=16)

        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill=tk.BOTH, expand=True, padx=52, pady=(0, 40))

        sidebar = tk.Frame(body, bg=COLOR_BG, width=240)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 28))
        sidebar.pack_propagate(False)

        self._btn_dich = PillButton(
            sidebar, "Dịch", active=True, command=lambda: self._switch_tab("dich")
        )
        self._btn_dich.pack(pady=(12, 10))
        self._btn_tra = PillButton(
            sidebar, "Tra cứu", active=False, command=lambda: self._switch_tab("tra")
        )
        self._btn_tra.pack(pady=10)
        self._btn_luyen = PillButton(
            sidebar, "Luyện", active=False, command=lambda: self._switch_tab("luyen")
        )
        self._btn_luyen.pack(pady=10)

        right = tk.Frame(body, bg=COLOR_BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._panel = MainPanel(right)
        self._panel.pack(fill=tk.BOTH, expand=True)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._open_camera()
        self.after(50, self._loop)

    def _switch_tab(self, tab: str) -> None:
        self._current_tab = tab
        self._btn_dich.set_active(tab == "dich")
        self._btn_tra.set_active(tab == "tra")
        self._btn_luyen.set_active(tab == "luyen")

    def _open_camera(self) -> None:
        self._cap = cv2.VideoCapture(0)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def _loop(self) -> None:
        if not self._running or self._cap is None:
            return

        if self._current_tab == "dich":
            ok, frame = self._cap.read()
            if ok:
                frame = cv2.flip(frame, 1)
                annotated = self._processor.process(frame)

                rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                vs = self._panel.layout_metrics()["video_size"]
                img = img.resize((vs, vs), Image.Resampling.LANCZOS)
                self._photo = ImageTk.PhotoImage(img)
                self._panel.set_frame(self._photo)
                self._draw_translation_on_panel()
        else:
            self._draw_translation_on_panel()

        self.after(33, self._loop)

    def _draw_translation_on_panel(self) -> None:

        canvas = self._panel
        canvas.delete("trans")

        m = canvas.layout_metrics()
        tx, ty = m["tx"], m["ty"]

        lines = self._translation_lines
        if self._current_tab == "tra":
            lines = ["(Tra cứu từ / câu)", "— module sau"]
        elif self._current_tab == "luyen":
            lines = ["(Luyện chuỗi ký tự)", "— module sau"]

        for i, line in enumerate(lines):
            canvas.create_text(
                tx,
                ty + i * 40,
                text=line,
                anchor="nw",
                fill=COLOR_WHITE,
                font=("Segoe UI", 16),
                tags="trans",
            )

    def _on_close(self) -> None:
        self._running = False
        if self._cap:
            self._cap.release()
        self._processor.close()
        self.destroy()


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()