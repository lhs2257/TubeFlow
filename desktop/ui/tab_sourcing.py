import tkinter as tk
from datetime import datetime

import customtkinter as ctk
from desktop.ui.fonts import F

from desktop.client import APIClient


class SourcingTab(ctk.CTkFrame):
    """소재 수집 탭 — Guardian / NewsAPI / RSS / YouTube 통합 수집."""

    SOURCES = [
        ("guardian",  "The Guardian"),
        ("newsapi",   "NewsAPI"),
        ("rss",       "RSS 피드"),
        ("youtube",   "YouTube 트렌드"),
    ]

    def __init__(self, master, client: APIClient, colors: dict, **kwargs):
        super().__init__(master, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.client = client
        self.C = colors
        self._articles: list[dict] = []
        self._selected: list[bool] = []
        self._source_vars: dict[str, tk.BooleanVar] = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()

    # ── 헤더 ─────────────────────────────────────────────────────

    def _build_header(self) -> None:
        hdr = ctk.CTkFrame(self, fg_color=self.C["panel"], corner_radius=0, height=56)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(hdr, text="소재 수집",
                     text_color=self.C["text"],
                     font=F(size=16, weight="bold")).grid(
            row=0, column=0, padx=24, pady=16, sticky="w")

        ctk.CTkLabel(hdr,
                     text="Guardian · NewsAPI · RSS · YouTube 에서 여행 콘텐츠 소재를 수집합니다",
                     text_color=self.C["dim"],
                     font=F(size=12)).grid(
            row=0, column=1, padx=8, pady=16, sticky="w")

    # ── 바디 (좌: 설정 / 우: 결과) ──────────────────────────────

    def _build_body(self) -> None:
        body = ctk.CTkFrame(self, fg_color=self.C["bg"], corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self._build_left_panel(body)
        self._build_right_panel(body)

    def _build_left_panel(self, parent) -> None:
        left = ctk.CTkFrame(parent, width=300, fg_color=self.C["panel"], corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew")
        left.grid_propagate(False)
        left.grid_columnconfigure(0, weight=1)

        pad = {"padx": 20, "pady": 6}

        # 키워드
        ctk.CTkLabel(left, text="키워드", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(20, 2))
        self._kw_entry = ctk.CTkTextbox(
            left, height=72, fg_color=self.C["panel2"],
            text_color=self.C["text"], font=F(size=12),
            border_width=1, border_color=self.C["border"],
        )
        self._kw_entry.insert("1.0", "travel, tourism, vacation")
        self._kw_entry.grid(row=1, column=0, sticky="ew", **pad)

        # 소스 선택
        ctk.CTkLabel(left, text="수집 소스", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=2, column=0, sticky="w", padx=20, pady=(12, 2))

        src_frame = ctk.CTkFrame(left, fg_color="transparent")
        src_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=4)
        src_frame.grid_columnconfigure((0, 1), weight=1)

        for i, (src_id, label) in enumerate(self.SOURCES):
            var = tk.BooleanVar(value=True)
            self._source_vars[src_id] = var
            cb = ctk.CTkCheckBox(
                src_frame, text=label, variable=var,
                text_color=self.C["text"], font=F(size=12),
                fg_color=self.C["accent"], hover_color="#FF6B78",
                checkmark_color="#ffffff",
            )
            cb.grid(row=i // 2, column=i % 2, sticky="w", pady=3)

        # 수집 개수
        ctk.CTkLabel(left, text="소스당 최대 수집", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=4, column=0, sticky="w", padx=20, pady=(12, 2))

        limit_frame = ctk.CTkFrame(left, fg_color="transparent")
        limit_frame.grid(row=5, column=0, sticky="ew", padx=20)
        limit_frame.grid_columnconfigure(0, weight=1)

        self._limit_var = tk.IntVar(value=20)
        self._limit_label = ctk.CTkLabel(limit_frame, text="20개",
                                          text_color=self.C["text"],
                                          font=F(size=12))
        self._limit_label.grid(row=0, column=1, padx=(8, 0))

        slider = ctk.CTkSlider(
            limit_frame, from_=5, to=50, number_of_steps=9,
            variable=self._limit_var,
            command=lambda v: self._limit_label.configure(text=f"{int(v)}개"),
            button_color=self.C["accent"], progress_color=self.C["accent"],
        )
        slider.grid(row=0, column=0, sticky="ew")

        # 스페이서
        ctk.CTkFrame(left, fg_color="transparent").grid(row=6, column=0, sticky="nsew")
        left.grid_rowconfigure(6, weight=1)

        # 수집 버튼
        self._collect_btn = ctk.CTkButton(
            left, text="수집 실행",
            command=self._run_collect,
            height=40,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            font=F(size=14, weight="bold"),
        )
        self._collect_btn.grid(row=7, column=0, sticky="ew", padx=20, pady=(8, 4))

        self._progress_bar = ctk.CTkProgressBar(left, fg_color=self.C["panel2"],
                                                  progress_color=self.C["accent"])
        self._progress_bar.set(0)
        self._progress_bar.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 16))

        self._status_lbl = ctk.CTkLabel(left, text="", text_color=self.C["dim"],
                                         font=F(size=11))
        self._status_lbl.grid(row=9, column=0, padx=20, pady=(0, 16))

    def _build_right_panel(self, parent) -> None:
        right = ctk.CTkFrame(parent, fg_color=self.C["bg"], corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        # 결과 툴바
        toolbar = ctk.CTkFrame(right, fg_color=self.C["panel"], corner_radius=0, height=44)
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.grid_propagate(False)
        toolbar.grid_columnconfigure(1, weight=1)

        self._count_label = ctk.CTkLabel(toolbar, text="수집된 소재 0개",
                                          text_color=self.C["text"],
                                          font=F(size=13, weight="bold"))
        self._count_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=12, pady=6)

        self._send_btn = ctk.CTkButton(
            btn_frame, text="대본으로 보내기",
            command=self._send_to_script,
            height=30, width=130,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            font=F(size=12, weight="bold"),
            state="disabled",
        )
        self._send_btn.grid(row=0, column=0, padx=(0, 4))

        # 결과 목록
        self._result_frame = ctk.CTkScrollableFrame(
            right, fg_color=self.C["bg"],
            scrollbar_button_color=self.C["panel3"],
        )
        self._result_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self._result_frame.grid_columnconfigure(0, weight=1)

    # ── 동작 ─────────────────────────────────────────────────────

    def _run_collect(self) -> None:
        keywords_raw = self._kw_entry.get("1.0", "end").strip()
        keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
        sources = [sid for sid, _ in self.SOURCES if self._source_vars[sid].get()]
        limit = int(self._limit_var.get())

        if not sources:
            self._set_status("소스를 하나 이상 선택하세요.", error=True)
            return

        self._collect_btn.configure(state="disabled", text="수집 중...")
        self._progress_bar.set(0)
        self._set_status("수집 요청 전송 중...")

        self._start_progress_animation()

        self.client.async_call(
            self.client.collect_sources,
            keywords=keywords or None,
            sources=sources,
            limit=limit,
            on_success=self._on_collect_success,
            on_error=self._on_collect_error,
        )

    def _start_progress_animation(self) -> None:
        self._progress_bar.configure(mode="indeterminate")
        self._progress_bar.start()

    def _stop_progress_animation(self) -> None:
        self._progress_bar.stop()
        self._progress_bar.configure(mode="determinate")
        self._progress_bar.set(1)

    def _on_collect_success(self, result: dict) -> None:
        self.after(0, lambda: self._render_results(result))

    def _on_collect_error(self, msg: str) -> None:
        self.after(0, lambda: self._set_status(f"오류: {msg}", error=True))
        self.after(0, lambda: self._collect_btn.configure(state="normal", text="수집 실행"))
        self.after(0, self._stop_progress_animation)

    def _render_results(self, result: dict) -> None:
        self._stop_progress_animation()
        self._collect_btn.configure(state="normal", text="수집 실행")

        articles = result.get("articles", [])
        self._articles = articles
        self._selected = [False] * len(articles)

        # 기존 위젯 제거
        for w in self._result_frame.winfo_children():
            w.destroy()

        self._count_label.configure(text=f"수집된 소재 {len(articles)}개")
        self._set_status(f"{len(articles)}개 소재 수집 완료 · {datetime.now().strftime('%H:%M:%S')}")

        for i, art in enumerate(articles):
            self._add_article_row(i, art)

        self._update_send_btn()

    def _add_article_row(self, idx: int, art: dict) -> None:
        row = ctk.CTkFrame(
            self._result_frame,
            fg_color=self.C["panel"], corner_radius=8,
            border_width=1, border_color=self.C["border"],
        )
        row.grid(row=idx, column=0, sticky="ew", padx=12, pady=4)
        row.grid_columnconfigure(1, weight=1)

        # 체크박스
        var = tk.BooleanVar(value=False)
        cb = ctk.CTkCheckBox(
            row, text="", variable=var, width=20,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            checkmark_color="#ffffff",
            command=lambda i=idx, v=var: self._toggle(i, v.get()),
        )
        cb.grid(row=0, column=0, padx=(12, 4), pady=12, rowspan=2)

        # 소스 배지
        source = art.get("source_name", art.get("source", ""))
        src_colors = {
            "Guardian": self.C["blue"],
            "NewsAPI": self.C["green"],
            "RSS": self.C["amber"],
            "YouTube Trends": self.C["accent"],
        }
        src_color = next((v for k, v in src_colors.items() if k.lower() in source.lower()), self.C["dim"])

        ctk.CTkLabel(row, text=source[:18], text_color=src_color,
                     font=F(size=10, weight="bold")).grid(
            row=0, column=1, sticky="w", padx=4, pady=(10, 0))

        # 제목
        title = art.get("title", "(제목 없음)")[:120]
        ctk.CTkLabel(row, text=title, text_color=self.C["text"],
                     font=F(size=12),
                     wraplength=500, anchor="w", justify="left").grid(
            row=1, column=1, sticky="ew", padx=4, pady=(0, 8))

        # 날짜
        pub = art.get("published_at", "")[:10]
        ctk.CTkLabel(row, text=pub, text_color=self.C["mute"],
                     font=F(size=10)).grid(
            row=0, column=2, padx=12, pady=(10, 0), sticky="e")

    def _toggle(self, idx: int, val: bool) -> None:
        self._selected[idx] = val
        self._update_send_btn()

    def _update_send_btn(self) -> None:
        cnt = sum(self._selected)
        state = "normal" if cnt > 0 else "disabled"
        self._send_btn.configure(state=state,
                                   text=f"대본으로 보내기 ({cnt})" if cnt else "대본으로 보내기")

    def _send_to_script(self) -> None:
        selected = [a for a, s in zip(self._articles, self._selected) if s]
        if not selected:
            return
        # 첫 번째 선택 항목을 스크립트 탭으로 전달 (향후 이벤트 버스로 확장 가능)
        art = selected[0]
        event_data = {
            "source_title": art.get("title", ""),
            "source_body": art.get("body", ""),
            "source_url": art.get("url", ""),
        }
        self.event_generate("<<SendToScript>>", data=str(event_data))
        self._set_status(f"'{art['title'][:40]}...' 를 대본 탭으로 전달했습니다.")

    def _set_status(self, msg: str, error: bool = False) -> None:
        color = self.C["accent"] if error else self.C["dim"]
        self._status_lbl.configure(text=msg, text_color=color)
