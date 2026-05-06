import tkinter as tk
import webbrowser
from datetime import datetime

import customtkinter as ctk
from desktop.ui.fonts import F

from desktop.client import APIClient


# ── 소스 정의 (카테고리, ID, 표시명, 설명) ──────────────────────────
SOURCE_GROUPS = [
    ("중국 이슈", [
        ("scmp",     "South China Morning Post", "홍콩 기반 · 중국 정치/경제 전문"),
        ("rfa",      "Radio Free Asia",          "중국 · 북한 · 동남아 공산국가 특화"),
    ]),
    ("일본 이슈", [
        ("nhk",      "NHK World",                "일본 국영방송 · 정치/사회 국제판"),
        ("nikkei",   "Nikkei Asia",              "일본 경제 · 기업 · 정세 분석"),
    ]),
    ("동남아 이슈", [
        ("cna",      "Channel NewsAsia",         "싱가포르 기반 · 동남아 전반"),
        ("diplomat", "The Diplomat",             "아시아 지정학 · 외교 심층 분석"),
    ]),
    ("국제 / 한국 시각", [
        ("koreaherald",  "Korea Herald",         "한국 주요 이슈 영문 보도"),
        ("reuters_asia", "Reuters Asia",         "로이터 아시아 속보"),
        ("bbc_asia",     "BBC News Asia",        "BBC 아시아 심층 보도"),
    ]),
    ("통합 검색", [
        ("guardian", "The Guardian",             "세계 정치 · 여행 심층 기사 (API 키 필요)"),
        ("newsapi",  "NewsAPI",                  "키워드 기반 전세계 뉴스 검색 (API 키 필요)"),
        ("youtube",  "YouTube 트렌드",            "아시아 인기 영상 트렌드 (국가 코드 기반)"),
    ]),
]

# 기본 체크 소스: 중국 + 동남아만 ON
DEFAULT_CHECKED = {"scmp", "rfa", "cna", "diplomat"}

# 초기 폴백 키워드 (트렌드 로드 전 표시)
DEFAULT_KEYWORDS = (
    "Taiwan strait, South China Sea, Xi Jinping, China economy, "
    "Myanmar coup, Cambodia China, Vietnam politics, North Korea missile, "
    "Indo-Pacific, US China rivalry, ASEAN summit, Japan military, "
    "Asia geopolitics, China sanctions, Korea China relations, Korea Japan"
)


class SourcingTab(ctk.CTkFrame):
    """소재 수집 탭 — 아시아/정치 특화 멀티소스 수집."""

    def __init__(self, master, client: APIClient, colors: dict, **kwargs):
        super().__init__(master, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.client = client
        self.C = colors
        self._articles: list[dict] = []
        self._selected: list[bool] = []
        self._source_vars: dict[str, tk.BooleanVar] = {}
        self._pending_transfer: dict = {}  # 대본 탭으로 전달할 소재 임시 저장

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        # 앱 시작 시 트렌딩 키워드 자동 로드
        self.after(500, self._load_keywords_on_start)

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
                     text="중국 · 일본 · 동남아 · 국제 정세 소재를 수집합니다",
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
        # 좌측 패널 전체를 스크롤 가능하게
        left_outer = ctk.CTkFrame(parent, width=300, fg_color=self.C["panel"], corner_radius=0)
        left_outer.grid(row=0, column=0, sticky="nsew")
        left_outer.grid_propagate(False)
        left_outer.grid_columnconfigure(0, weight=1)
        left_outer.grid_rowconfigure(1, weight=1)

        # 키워드 입력 (스크롤 밖 고정)
        kw_frame = ctk.CTkFrame(left_outer, fg_color=self.C["panel"], corner_radius=0)
        kw_frame.grid(row=0, column=0, sticky="ew")
        kw_frame.grid_columnconfigure(0, weight=1)

        # 키워드 라벨 + 갱신 버튼
        kw_label_row = ctk.CTkFrame(kw_frame, fg_color="transparent")
        kw_label_row.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 2))
        kw_label_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(kw_label_row, text="검색 키워드",
                     text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=0, column=0, sticky="w")

        self._kw_status_lbl = ctk.CTkLabel(
            kw_label_row, text="로딩 중...",
            text_color=self.C["mute"], font=F(size=9),
        )
        self._kw_status_lbl.grid(row=0, column=1, padx=(6, 8), sticky="e")

        self._kw_refresh_btn = ctk.CTkButton(
            kw_label_row, text="갱신",
            command=self._refresh_keywords,
            height=20, width=44,
            fg_color=self.C["panel2"], hover_color=self.C["panel3"],
            text_color=self.C["dim"], font=F(size=10),
            border_width=1, border_color=self.C["border"],
            corner_radius=4,
        )
        self._kw_refresh_btn.grid(row=0, column=2, sticky="e")

        self._kw_entry = ctk.CTkTextbox(
            kw_frame, height=72, fg_color=self.C["panel2"],
            text_color=self.C["text"], font=F(size=12),
            border_width=1, border_color=self.C["border"],
        )
        self._kw_entry.insert("1.0", DEFAULT_KEYWORDS)
        self._kw_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))

        # 소스 선택 (스크롤 영역)
        scroll = ctk.CTkScrollableFrame(
            left_outer, fg_color=self.C["panel"],
            scrollbar_button_color=self.C["panel3"],
        )
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        row_idx = 0
        for group_name, sources in SOURCE_GROUPS:
            # 그룹 헤더
            grp_hdr = ctk.CTkFrame(scroll, fg_color=self.C["panel2"], corner_radius=6)
            grp_hdr.grid(row=row_idx, column=0, sticky="ew", padx=12, pady=(10, 4))
            grp_hdr.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(grp_hdr, text=group_name,
                         text_color=self.C["accent"],
                         font=F(size=11, weight="bold")).grid(
                row=0, column=0, sticky="w", padx=10, pady=5)
            row_idx += 1

            for src_id, src_name, src_desc in sources:
                var = tk.BooleanVar(value=(src_id in DEFAULT_CHECKED))
                self._source_vars[src_id] = var

                # 소스 카드
                card = ctk.CTkFrame(scroll, fg_color="transparent", corner_radius=0)
                card.grid(row=row_idx, column=0, sticky="ew", padx=12, pady=1)
                card.grid_columnconfigure(1, weight=1)

                cb = ctk.CTkCheckBox(
                    card, text="", variable=var, width=20,
                    fg_color=self.C["accent"], hover_color="#FF6B78",
                    checkmark_color="#ffffff",
                )
                cb.grid(row=0, column=0, padx=(4, 6), pady=4, rowspan=2)

                ctk.CTkLabel(card, text=src_name,
                             text_color=self.C["text"],
                             font=F(size=12, weight="bold"),
                             anchor="w").grid(row=0, column=1, sticky="ew", pady=(4, 0))

                ctk.CTkLabel(card, text=src_desc,
                             text_color=self.C["mute"],
                             font=F(size=10),
                             anchor="w").grid(row=1, column=1, sticky="ew", pady=(0, 4))

                row_idx += 1

        # 수집 개수 슬라이더
        row_idx_outer = 2
        limit_frame = ctk.CTkFrame(left_outer, fg_color=self.C["panel"], corner_radius=0)
        limit_frame.grid(row=row_idx_outer, column=0, sticky="ew")
        limit_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(limit_frame, text="소스당 최대 수집",
                     text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(8, 2))

        sl_row = ctk.CTkFrame(limit_frame, fg_color="transparent")
        sl_row.grid(row=1, column=0, sticky="ew", padx=20)
        sl_row.grid_columnconfigure(0, weight=1)

        self._limit_var = tk.IntVar(value=20)
        self._limit_label = ctk.CTkLabel(sl_row, text="20개",
                                          text_color=self.C["text"],
                                          font=F(size=12))
        self._limit_label.grid(row=0, column=1, padx=(8, 0))

        ctk.CTkSlider(
            sl_row, from_=5, to=50, number_of_steps=9,
            variable=self._limit_var,
            command=lambda v: self._limit_label.configure(text=f"{int(v)}개"),
            button_color=self.C["accent"], progress_color=self.C["accent"],
        ).grid(row=0, column=0, sticky="ew")

        # 수집 버튼
        btn_frame = ctk.CTkFrame(left_outer, fg_color=self.C["panel"], corner_radius=0)
        btn_frame.grid(row=3, column=0, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)

        self._collect_btn = ctk.CTkButton(
            btn_frame, text="수집 실행",
            command=self._run_collect,
            height=40,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            font=F(size=14, weight="bold"),
        )
        self._collect_btn.grid(row=0, column=0, sticky="ew", padx=20, pady=(8, 4))

        self._progress_bar = ctk.CTkProgressBar(btn_frame, fg_color=self.C["panel2"],
                                                  progress_color=self.C["accent"])
        self._progress_bar.set(0)
        self._progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 4))

        self._status_lbl = ctk.CTkLabel(btn_frame, text="",
                                         text_color=self.C["dim"],
                                         font=F(size=11))
        self._status_lbl.grid(row=2, column=0, padx=20, pady=(0, 12))

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

        self._send_btn = ctk.CTkButton(
            toolbar, text="대본으로 보내기",
            command=self._send_to_script,
            height=30, width=130,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            font=F(size=12, weight="bold"),
            state="disabled",
        )
        self._send_btn.grid(row=0, column=2, padx=12, pady=6)

        # 결과 목록
        self._result_frame = ctk.CTkScrollableFrame(
            right, fg_color=self.C["bg"],
            scrollbar_button_color=self.C["panel3"],
        )
        self._result_frame.grid(row=1, column=0, sticky="nsew")
        self._result_frame.grid_columnconfigure(0, weight=1)

    # ── 동작 ─────────────────────────────────────────────────────

    def _run_collect(self) -> None:
        keywords_raw = self._kw_entry.get("1.0", "end").strip()
        keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
        sources = [sid for sid, var in self._source_vars.items() if var.get()]
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

        for w in self._result_frame.winfo_children():
            w.destroy()

        self._count_label.configure(text=f"수집된 소재 {len(articles)}개")
        self._set_status(f"{len(articles)}개 소재 수집 완료 · {datetime.now().strftime('%H:%M:%S')}")

        for i, art in enumerate(articles):
            self._add_article_row(i, art)

        self._update_send_btn()

    # 카테고리별 배지 색상
    _CATEGORY_COLORS = {
        "china":  "#FF6B6B",
        "japan":  "#F5B544",
        "sea":    "#3DD68C",
        "korea":  "#5B9CFF",
        "world":  "#A78BFA",
        "travel": "#FB923C",
        "video":  "#FF4655",
    }

    def _add_article_row(self, idx: int, art: dict) -> None:
        row = ctk.CTkFrame(
            self._result_frame,
            fg_color=self.C["panel"], corner_radius=8,
            border_width=1, border_color=self.C["border"],
        )
        row.grid(row=idx, column=0, sticky="ew", padx=12, pady=4)
        row.grid_columnconfigure(2, weight=1)

        # 체크박스
        var = tk.BooleanVar(value=False)
        cb = ctk.CTkCheckBox(
            row, text="", variable=var, width=20,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            checkmark_color="#ffffff",
            command=lambda i=idx, v=var: self._toggle(i, v.get()),
        )
        cb.grid(row=0, column=0, padx=(12, 4), pady=10, rowspan=3)

        # 카테고리 배지
        cat = art.get("category", "world")
        cat_color = self._CATEGORY_COLORS.get(cat, self.C["dim"])
        ctk.CTkLabel(row, text=cat.upper(), text_color=cat_color,
                     font=F(size=9, weight="bold"), width=50,
                     anchor="center").grid(
            row=0, column=1, padx=(4, 6), pady=(10, 0), sticky="n")

        # 소스명 + 날짜 (한 줄)
        source = art.get("source_name", "")
        pub = art.get("published_at", "")[:10]
        meta_frame = ctk.CTkFrame(row, fg_color="transparent")
        meta_frame.grid(row=0, column=2, sticky="ew", padx=4, pady=(10, 0))
        meta_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(meta_frame, text=source[:28], text_color=self.C["dim"],
                     font=F(size=10, weight="bold"), anchor="w").grid(
            row=0, column=0, sticky="w")
        ctk.CTkLabel(meta_frame, text=pub, text_color=self.C["mute"],
                     font=F(size=10)).grid(row=0, column=1, padx=(8, 0), sticky="e")

        # 제목 (번역본 우선, 없으면 원문)
        title = (art.get("title_ko") or art.get("title", "(제목 없음)"))[:120]
        ctk.CTkLabel(row, text=title, text_color=self.C["text"],
                     font=F(size=12, weight="bold"),
                     wraplength=500, anchor="w", justify="left").grid(
            row=1, column=1, columnspan=2, sticky="ew", padx=4, pady=(2, 0))

        # 요약 본문 (번역본 우선, 없으면 원문, 앞 120자)
        body = (art.get("body_ko") or art.get("body", "")).strip()
        if body:
            preview = body[:120] + ("..." if len(body) > 120 else "")
            ctk.CTkLabel(row, text=preview, text_color=self.C["mute"],
                         font=F(size=11),
                         wraplength=500, anchor="w", justify="left").grid(
                row=2, column=1, columnspan=2, sticky="ew", padx=4, pady=(2, 0))

        # 원문 보기 버튼
        url = art.get("url", "")
        btn_frame = ctk.CTkFrame(row, fg_color="transparent")
        btn_frame.grid(row=3, column=1, columnspan=2, sticky="w", padx=4, pady=(4, 8))

        if url:
            link_btn = ctk.CTkButton(
                btn_frame,
                text="원문 보기 ->",
                command=lambda u=url: webbrowser.open(u),
                height=22, width=90,
                fg_color="transparent",
                hover_color=self.C["panel2"],
                text_color=self.C["blue"],
                font=F(size=10, weight="bold"),
                border_width=1,
                border_color=self.C["blue"],
                corner_radius=4,
            )
            link_btn.grid(row=0, column=0)
        else:
            ctk.CTkLabel(btn_frame, text="링크 없음",
                         text_color=self.C["mute"],
                         font=F(size=10)).grid(row=0, column=0)

    def _toggle(self, idx: int, val: bool) -> None:
        self._selected[idx] = val
        self._update_send_btn()

    def _update_send_btn(self) -> None:
        cnt = sum(self._selected)
        state = "normal" if cnt > 0 else "disabled"
        self._send_btn.configure(
            state=state,
            text=f"대본으로 보내기 ({cnt})" if cnt else "대본으로 보내기",
        )

    def _send_to_script(self) -> None:
        selected = [a for a, s in zip(self._articles, self._selected) if s]
        if not selected:
            return
        art = selected[0]
        self._pending_transfer = {
            "source_title": art.get("title_ko") or art.get("title", ""),
            "source_body":  art.get("body_ko")  or art.get("body",  ""),
            "source_url":   art.get("url", ""),
        }
        self.event_generate("<<SendToScript>>")
        display_title = (art.get("title_ko") or art.get("title", ""))[:40]
        self._set_status(f"'{display_title}...' 를 대본 탭으로 전달했습니다.")

    # ── 키워드 자동 갱신 ─────────────────────────────────────────

    def _load_keywords_on_start(self) -> None:
        """앱 시작 시 캐시된 키워드를 우선 로드합니다."""
        self._kw_refresh_btn.configure(state="disabled", text="로딩...")
        self.client.async_call(
            self.client.get_trending_keywords,
            refresh=False,
            on_success=self._on_keywords_loaded,
            on_error=self._on_keywords_error,
        )

    def _refresh_keywords(self) -> None:
        """갱신 버튼 클릭 시 Google Trends에서 강제 새로고침합니다."""
        self._kw_refresh_btn.configure(state="disabled", text="갱신 중...")
        self._kw_status_lbl.configure(text="Google Trends 조회 중...")
        self.client.async_call(
            self.client.get_trending_keywords,
            refresh=True,
            on_success=self._on_keywords_loaded,
            on_error=self._on_keywords_error,
        )

    def _on_keywords_loaded(self, result: dict) -> None:
        self.after(0, lambda: self._apply_keywords(result))

    def _on_keywords_error(self, msg: str) -> None:
        self.after(0, lambda: self._kw_status_lbl.configure(
            text="기본값 사용 중", text_color=self.C["mute"]))
        self.after(0, lambda: self._kw_refresh_btn.configure(
            state="normal", text="갱신"))

    def _apply_keywords(self, result: dict) -> None:
        keywords = result.get("keywords", [])
        if not keywords:
            return

        # 키워드 입력창 업데이트
        self._kw_entry.delete("1.0", "end")
        self._kw_entry.insert("1.0", ", ".join(keywords))

        # 상태 레이블: 소스 + 업데이트 시각
        source = result.get("source", "")
        updated_at = result.get("updated_at", "")
        source_label = {
            "google_trends": "Google Trends",
            "cache": "캐시",
            "fallback": "기본값",
        }.get(source, source)

        self._kw_status_lbl.configure(
            text=f"{source_label} · {updated_at}",
            text_color=self.C["green"] if source == "google_trends" else self.C["mute"],
        )
        self._kw_refresh_btn.configure(state="normal", text="갱신")

    def _set_status(self, msg: str, error: bool = False) -> None:
        color = self.C["accent"] if error else self.C["dim"]
        self._status_lbl.configure(text=msg, text_color=color)
