import tkinter as tk

import customtkinter as ctk

from desktop.client import APIClient


REGIONS = [
    ("US", "미국"),
    ("GB", "영국"),
    ("JP", "일본"),
    ("AU", "호주"),
    ("KR", "한국"),
    ("CA", "캐나다"),
    ("FR", "프랑스"),
    ("DE", "독일"),
]

TIMEFRAMES = [
    ("now 1-d",   "24시간"),
    ("now 7-d",   "7일"),
    ("today 1-m", "30일"),
    ("today 3-m", "3개월"),
]


class TrendTab(ctk.CTkFrame):
    """트렌드 분석 탭 — YouTube + Google Trends 통합 리포트."""

    def __init__(self, master, client: APIClient, colors: dict, **kwargs):
        super().__init__(master, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.client = client
        self.C = colors
        self._region_vars: dict[str, tk.BooleanVar] = {}
        self._timeframe = "now 7-d"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._load_latest()

    # ── 헤더 ─────────────────────────────────────────────────────

    def _build_header(self) -> None:
        hdr = ctk.CTkFrame(self, fg_color=self.C["panel"], corner_radius=0, height=56)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(hdr, text="트렌드 분석",
                     text_color=self.C["text"],
                     font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, padx=24, pady=16, sticky="w")
        ctk.CTkLabel(hdr, text="YouTube · Google Trends 데이터로 콘텐츠 기회를 발굴합니다",
                     text_color=self.C["dim"], font=ctk.CTkFont(size=12)).grid(
            row=0, column=1, padx=8, pady=16, sticky="w")

    # ── 바디 ─────────────────────────────────────────────────────

    def _build_body(self) -> None:
        body = ctk.CTkFrame(self, fg_color=self.C["bg"], corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self._build_left_panel(body)
        self._build_right_panel(body)

    def _build_left_panel(self, parent) -> None:
        left = ctk.CTkFrame(parent, width=280, fg_color=self.C["panel"], corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew")
        left.grid_propagate(False)
        left.grid_columnconfigure(0, weight=1)

        # 분석 국가
        ctk.CTkLabel(left, text="분석 국가", text_color=self.C["dim"],
                     font=ctk.CTkFont(size=11, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(20, 6))

        region_frame = ctk.CTkFrame(left, fg_color="transparent")
        region_frame.grid(row=1, column=0, sticky="ew", padx=20)
        region_frame.grid_columnconfigure((0, 1), weight=1)

        for i, (code, name) in enumerate(REGIONS):
            var = tk.BooleanVar(value=(code in ("US", "GB", "JP", "KR")))
            self._region_vars[code] = var
            cb = ctk.CTkCheckBox(
                region_frame, text=f"{code} {name}", variable=var,
                text_color=self.C["text"], font=ctk.CTkFont(size=11),
                fg_color=self.C["accent"], hover_color="#FF6B78",
                checkmark_color="#ffffff",
            )
            cb.grid(row=i // 2, column=i % 2, sticky="w", pady=3)

        # 기간
        ctk.CTkLabel(left, text="분석 기간", text_color=self.C["dim"],
                     font=ctk.CTkFont(size=11, weight="bold")).grid(
            row=2, column=0, sticky="w", padx=20, pady=(16, 6))

        tf_frame = ctk.CTkFrame(left, fg_color="transparent")
        tf_frame.grid(row=3, column=0, sticky="ew", padx=20)
        tf_frame.grid_columnconfigure((0, 1), weight=1)

        self._tf_btns: dict[str, ctk.CTkButton] = {}
        for i, (tf_id, label) in enumerate(TIMEFRAMES):
            btn = ctk.CTkButton(
                tf_frame, text=label, height=30,
                command=lambda t=tf_id: self._set_timeframe(t),
                fg_color=self.C["panel3"] if tf_id == self._timeframe else self.C["panel2"],
                border_color=self.C["accent"] if tf_id == self._timeframe else self.C["border"],
                border_width=1,
                text_color=self.C["text"], font=ctk.CTkFont(size=11),
                hover_color=self.C["panel3"],
            )
            btn.grid(row=i // 2, column=i % 2, padx=2, pady=2, sticky="ew")
            self._tf_btns[tf_id] = btn

        # 소스당 수집 수
        ctk.CTkLabel(left, text="국가당 수집 수", text_color=self.C["dim"],
                     font=ctk.CTkFont(size=11, weight="bold")).grid(
            row=4, column=0, sticky="w", padx=20, pady=(16, 4))

        limit_row = ctk.CTkFrame(left, fg_color="transparent")
        limit_row.grid(row=5, column=0, sticky="ew", padx=20)
        limit_row.grid_columnconfigure(0, weight=1)

        self._yt_limit = tk.IntVar(value=10)
        self._yt_limit_lbl = ctk.CTkLabel(limit_row, text="10개",
                                            text_color=self.C["text"],
                                            font=ctk.CTkFont(size=12))
        self._yt_limit_lbl.grid(row=0, column=1, padx=(6, 0))

        ctk.CTkSlider(
            limit_row, from_=5, to=30, number_of_steps=5,
            variable=self._yt_limit,
            command=lambda v: self._yt_limit_lbl.configure(text=f"{int(v)}개"),
            button_color=self.C["accent"], progress_color=self.C["accent"],
        ).grid(row=0, column=0, sticky="ew")

        # 스페이서
        left.grid_rowconfigure(6, weight=1)

        # 분석 버튼
        self._analyze_btn = ctk.CTkButton(
            left, text="트렌드 분석 실행",
            command=self._run_analyze,
            height=40,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self._analyze_btn.grid(row=7, column=0, sticky="ew", padx=20, pady=(8, 4))

        self._progress = ctk.CTkProgressBar(left, fg_color=self.C["panel2"],
                                              progress_color=self.C["accent"])
        self._progress.set(0)
        self._progress.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 8))

        self._status = ctk.CTkLabel(left, text="", text_color=self.C["dim"],
                                     font=ctk.CTkFont(size=11))
        self._status.grid(row=9, column=0, padx=20, pady=(0, 16))

    def _build_right_panel(self, parent) -> None:
        right = ctk.CTkFrame(parent, fg_color=self.C["bg"], corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        # 요약 카드 행
        self._stat_frame = ctk.CTkFrame(right, fg_color=self.C["bg"], corner_radius=0, height=90)
        self._stat_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 0))
        self._stat_frame.grid_propagate(False)
        self._stat_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._stat_cards: list[dict] = []
        stat_defs = [
            ("상위 키워드", "-", self.C["accent"]),
            ("분석 국가 수", "-", self.C["blue"]),
            ("YouTube 영상", "-", self.C["green"]),
            ("Google 키워드", "-", self.C["amber"]),
        ]
        for i, (label, val, color) in enumerate(stat_defs):
            card = ctk.CTkFrame(self._stat_frame, fg_color=self.C["panel2"],
                                 corner_radius=8, border_width=1,
                                 border_color=self.C["border"])
            card.grid(row=0, column=i, sticky="ew", padx=4, pady=4)
            ctk.CTkLabel(card, text=label, text_color=self.C["mute"],
                         font=ctk.CTkFont(size=10, weight="bold")).grid(
                row=0, column=0, sticky="w", padx=10, pady=(8, 0))
            val_lbl = ctk.CTkLabel(card, text=val, text_color=color,
                                    font=ctk.CTkFont(size=18, weight="bold"))
            val_lbl.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))
            self._stat_cards.append({"label": label, "widget": val_lbl})

        # 키워드 테이블
        table_frame = ctk.CTkFrame(right, fg_color=self.C["panel"], corner_radius=0)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(8, 0))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)

        # 테이블 헤더
        t_hdr = ctk.CTkFrame(table_frame, fg_color=self.C["panel2"],
                               corner_radius=0, height=36)
        t_hdr.grid(row=0, column=0, sticky="ew")
        t_hdr.grid_propagate(False)
        t_hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(t_hdr, text="인기 키워드 순위",
                     text_color=self.C["text"],
                     font=ctk.CTkFont(size=12, weight="bold")).grid(
            row=0, column=0, padx=16, pady=8, sticky="w")

        self._gen_time = ctk.CTkLabel(t_hdr, text="",
                                       text_color=self.C["mute"],
                                       font=ctk.CTkFont(size=10))
        self._gen_time.grid(row=0, column=1, padx=12, pady=8, sticky="e")

        # 키워드 목록
        self._kw_scroll = ctk.CTkScrollableFrame(
            table_frame, fg_color=self.C["panel"],
            scrollbar_button_color=self.C["panel3"],
        )
        self._kw_scroll.grid(row=1, column=0, sticky="nsew")
        self._kw_scroll.grid_columnconfigure(0, weight=1)

    # ── 동작 ─────────────────────────────────────────────────────

    def _set_timeframe(self, tf_id: str) -> None:
        self._timeframe = tf_id
        for tid, btn in self._tf_btns.items():
            btn.configure(
                fg_color=self.C["panel3"] if tid == tf_id else self.C["panel2"],
                border_color=self.C["accent"] if tid == tf_id else self.C["border"],
            )

    def _run_analyze(self) -> None:
        regions = [code for code, _ in REGIONS if self._region_vars[code].get()]
        if not regions:
            self._set_status("국가를 하나 이상 선택하세요.", error=True)
            return

        self._analyze_btn.configure(state="disabled", text="분석 중...")
        self._progress.configure(mode="indeterminate")
        self._progress.start()
        self._set_status("YouTube + Google Trends 분석 중... (수십 초 소요)")

        self.client.async_call(
            self.client.analyze_trends,
            regions=regions,
            timeframe=self._timeframe,
            yt_limit_per_region=int(self._yt_limit.get()),
            on_success=self._on_analyze_success,
            on_error=self._on_analyze_error,
        )

    def _on_analyze_success(self, result: dict) -> None:
        self.after(0, lambda: self._render_result(result))

    def _on_analyze_error(self, msg: str) -> None:
        self.after(0, lambda: self._set_status(f"오류: {msg}", error=True))
        self.after(0, lambda: self._analyze_btn.configure(state="normal", text="트렌드 분석 실행"))
        self.after(0, lambda: (self._progress.stop(),
                               self._progress.configure(mode="determinate"),
                               self._progress.set(0)))

    def _load_latest(self) -> None:
        self.client.async_call(
            self.client.get_trend_keywords,
            top=30,
            on_success=lambda r: self.after(0, lambda: self._render_keywords_only(r)),
            on_error=lambda e: None,
        )

    def _render_result(self, result: dict) -> None:
        self._progress.stop()
        self._progress.configure(mode="determinate")
        self._progress.set(1)
        self._analyze_btn.configure(state="normal", text="트렌드 분석 실행")

        top_kw = result.get("top_keywords", [])
        self._stat_cards[0]["widget"].configure(
            text=top_kw[0] if top_kw else "-")
        self._stat_cards[1]["widget"].configure(
            text=str(len(result.get("regions", []))))
        self._stat_cards[2]["widget"].configure(
            text=str(result.get("youtube_trend_count", 0)))
        self._stat_cards[3]["widget"].configure(
            text=str(result.get("google_trend_count", 0)))

        gen_at = result.get("generated_at", "")[:16].replace("T", " ")
        self._gen_time.configure(text=f"분석 시각: {gen_at}")
        self._set_status(result.get("summary", "분석 완료"))

        self._load_latest()

    def _render_keywords_only(self, data: dict) -> None:
        keywords = data.get("keywords", [])
        top_kw = data.get("top_keywords", [])

        for w in self._kw_scroll.winfo_children():
            w.destroy()

        if not keywords:
            ctk.CTkLabel(self._kw_scroll, text="분석된 키워드가 없습니다. 트렌드 분석을 실행하세요.",
                         text_color=self.C["mute"],
                         font=ctk.CTkFont(size=12)).grid(row=0, column=0, pady=24)
            return

        if top_kw:
            self._stat_cards[0]["widget"].configure(text=top_kw[0])

        gen_at = data.get("generated_at", "")[:16].replace("T", " ")
        if gen_at:
            self._gen_time.configure(text=f"분석 시각: {gen_at}")

        # 헤더 행
        hdr_row = ctk.CTkFrame(self._kw_scroll, fg_color=self.C["panel2"], corner_radius=0)
        hdr_row.grid(row=0, column=0, sticky="ew", pady=(0, 2))
        hdr_row.grid_columnconfigure(1, weight=1)

        for col, (text, w) in enumerate([("#", 40), ("키워드", 0), ("소스", 80), ("점수", 80)]):
            ctk.CTkLabel(hdr_row, text=text, text_color=self.C["mute"],
                         font=ctk.CTkFont(size=10, weight="bold"),
                         width=w if w else 0).grid(
                row=0, column=col, padx=(16 if col == 0 else 8), pady=6,
                sticky="w" if col < 2 else "e")

        # 데이터 행
        max_score = max((k.get("score", 0) for k in keywords), default=1) or 1
        source_colors = {
            "google":   self.C["blue"],
            "youtube":  self.C["accent"],
            "combined": self.C["green"],
        }

        for i, kw in enumerate(keywords[:30]):
            bg = self.C["panel"] if i % 2 == 0 else self.C["panel2"]
            row = ctk.CTkFrame(self._kw_scroll, fg_color=bg, corner_radius=0)
            row.grid(row=i + 1, column=0, sticky="ew")
            row.grid_columnconfigure(1, weight=1)

            # 순위
            ctk.CTkLabel(row, text=f"{i + 1:02d}",
                         text_color=self.C["mute"],
                         font=ctk.CTkFont(size=11), width=40).grid(
                row=0, column=0, padx=16, pady=8, sticky="w")

            # 키워드 + 바
            kw_frame = ctk.CTkFrame(row, fg_color="transparent")
            kw_frame.grid(row=0, column=1, sticky="ew", padx=8, pady=6)
            kw_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(kw_frame, text=kw.get("keyword", ""),
                         text_color=self.C["text"],
                         font=ctk.CTkFont(size=12, weight="bold" if i < 3 else "normal"),
                         anchor="w").grid(row=0, column=0, sticky="ew")

            score = kw.get("score", 0)
            bar_pct = score / max_score
            bar_bg = ctk.CTkFrame(kw_frame, fg_color=self.C["panel3"],
                                   corner_radius=2, height=4)
            bar_bg.grid(row=1, column=0, sticky="ew", pady=(2, 0))
            bar_fill = ctk.CTkFrame(bar_bg, fg_color=self.C["accent"],
                                     corner_radius=2, height=4,
                                     width=max(int(bar_pct * 200), 4))
            bar_fill.place(x=0, y=0)

            # 소스
            src = kw.get("source", "")
            src_color = source_colors.get(src, self.C["dim"])
            ctk.CTkLabel(row, text=src, text_color=src_color,
                         font=ctk.CTkFont(size=10), width=80).grid(
                row=0, column=2, padx=8, pady=8, sticky="e")

            # 점수
            ctk.CTkLabel(row, text=f"{score:.1f}",
                         text_color=self.C["dim"],
                         font=ctk.CTkFont(family="Courier New", size=11), width=80).grid(
                row=0, column=3, padx=16, pady=8, sticky="e")

    def _set_status(self, msg: str, error: bool = False) -> None:
        color = self.C["accent"] if error else self.C["dim"]
        self._status.configure(text=msg, text_color=color)
