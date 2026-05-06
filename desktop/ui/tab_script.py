import tkinter as tk

import customtkinter as ctk
from desktop.ui.fonts import F

from desktop.client import APIClient


TONES = [
    ("informative",  "정보형",   "사실 중심 해설"),
    ("storytelling", "스토리형", "서사 중심 구성"),
    ("humor",        "유머형",   "캐주얼한 농담"),
    ("dramatic",     "드라마형", "강한 감성 훅"),
]

DURATIONS = [
    ("30",  "30초"),
    ("50",  "50초"),
    ("90",  "1분30초"),
    ("120", "2분"),
]


class ScriptTab(ctk.CTkFrame):
    """대본 작성 탭 — OpenAI gpt-4o 기반 AI 대본 생성."""

    def __init__(self, master, client: APIClient, colors: dict, **kwargs):
        super().__init__(master, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.client = client
        self.C = colors
        self._tone = "informative"
        self._duration = "50"
        self._pending_title: str = ""  # 업로드 탭으로 전달할 제목 임시 저장

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

        ctk.CTkLabel(hdr, text="대본 작성",
                     text_color=self.C["text"],
                     font=F(size=16, weight="bold")).grid(
            row=0, column=0, padx=24, pady=16, sticky="w")

        ctk.CTkLabel(hdr, text="수집된 소재를 AI로 영상 대본으로 변환합니다",
                     text_color=self.C["dim"],
                     font=F(size=12)).grid(
            row=0, column=1, padx=8, pady=16, sticky="w")

        self._save_btn = ctk.CTkButton(
            hdr, text="저장", width=80, height=32,
            fg_color=self.C["panel2"], hover_color=self.C["panel3"],
            text_color=self.C["text"], font=F(size=12),
            command=self._save_script,
        )
        self._save_btn.grid(row=0, column=2, padx=12, pady=12)

    # ── 바디 ─────────────────────────────────────────────────────

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

        # 소재 제목
        ctk.CTkLabel(left, text="소재 제목", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(20, 2))
        self._title_entry = ctk.CTkEntry(
            left, placeholder_text="소재 제목을 입력하세요",
            fg_color=self.C["panel2"], text_color=self.C["text"],
            border_color=self.C["border"], font=F(size=12),
        )
        self._title_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=4)

        # 소재 내용
        ctk.CTkLabel(left, text="소재 내용", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=2, column=0, sticky="w", padx=20, pady=(12, 2))
        self._body_entry = ctk.CTkTextbox(
            left, height=100, fg_color=self.C["panel2"],
            text_color=self.C["text"], font=F(size=12),
            border_width=1, border_color=self.C["border"],
        )
        self._body_entry.insert("1.0", "")
        self._body_entry.grid(row=3, column=0, sticky="ew", padx=20, pady=4)

        # URL
        ctk.CTkLabel(left, text="소재 URL (선택)", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=4, column=0, sticky="w", padx=20, pady=(8, 2))
        self._url_entry = ctk.CTkEntry(
            left, placeholder_text="https://...",
            fg_color=self.C["panel2"], text_color=self.C["text"],
            border_color=self.C["border"], font=F(size=11),
        )
        self._url_entry.grid(row=5, column=0, sticky="ew", padx=20, pady=4)

        # 구분선
        ctk.CTkFrame(left, fg_color=self.C["border"], height=1).grid(
            row=6, column=0, sticky="ew", padx=20, pady=12)

        # 어조 선택
        ctk.CTkLabel(left, text="어조 / 스타일", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=7, column=0, sticky="w", padx=20, pady=(0, 6))

        tone_frame = ctk.CTkFrame(left, fg_color="transparent")
        tone_frame.grid(row=8, column=0, sticky="ew", padx=20)
        tone_frame.grid_columnconfigure((0, 1), weight=1)

        self._tone_btns: dict[str, ctk.CTkButton] = {}
        for i, (tid, label, desc) in enumerate(TONES):
            btn = ctk.CTkButton(
                tone_frame, text=f"{label}\n{desc}",
                command=lambda t=tid: self._set_tone(t),
                height=50, corner_radius=7,
                fg_color=self.C["panel2"] if tid != self._tone else self.C["panel3"],
                border_color=self.C["accent"] if tid == self._tone else self.C["border"],
                border_width=1,
                text_color=self.C["text"], font=F(size=11),
                hover_color=self.C["panel3"],
            )
            btn.grid(row=i // 2, column=i % 2, padx=3, pady=3, sticky="ew")
            self._tone_btns[tid] = btn

        # 영상 길이
        ctk.CTkLabel(left, text="목표 길이", text_color=self.C["dim"],
                     font=F(size=11, weight="bold")).grid(
            row=9, column=0, sticky="w", padx=20, pady=(12, 6))

        dur_frame = ctk.CTkFrame(left, fg_color="transparent")
        dur_frame.grid(row=10, column=0, sticky="ew", padx=20)
        dur_frame.grid_columnconfigure(tuple(range(len(DURATIONS))), weight=1)

        self._dur_btns: dict[str, ctk.CTkButton] = {}
        for i, (dur_id, label) in enumerate(DURATIONS):
            btn = ctk.CTkButton(
                dur_frame, text=label,
                command=lambda d=dur_id: self._set_duration(d),
                height=30, corner_radius=6, width=60,
                fg_color=self.C["panel2"] if dur_id != self._duration else self.C["panel3"],
                border_color=self.C["accent"] if dur_id == self._duration else self.C["border"],
                border_width=1,
                text_color=self.C["text"], font=F(size=11),
                hover_color=self.C["panel3"],
            )
            btn.grid(row=0, column=i, padx=2)
            self._dur_btns[dur_id] = btn

        # 스페이서
        left.grid_rowconfigure(11, weight=1)

        # 생성 버튼
        self._gen_btn = ctk.CTkButton(
            left, text="대본 생성",
            command=self._generate,
            height=40,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            font=F(size=14, weight="bold"),
        )
        self._gen_btn.grid(row=12, column=0, sticky="ew", padx=20, pady=(8, 4))

        self._progress = ctk.CTkProgressBar(left, fg_color=self.C["panel2"],
                                              progress_color=self.C["accent"])
        self._progress.set(0)
        self._progress.grid(row=13, column=0, sticky="ew", padx=20, pady=(0, 8))

        self._status = ctk.CTkLabel(left, text="", text_color=self.C["dim"],
                                     font=F(size=11))
        self._status.grid(row=14, column=0, padx=20, pady=(0, 16))

    def _build_right_panel(self, parent) -> None:
        right = ctk.CTkFrame(parent, fg_color=self.C["bg"], corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        # 툴바
        toolbar = ctk.CTkFrame(right, fg_color=self.C["panel"], corner_radius=0, height=44)
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.grid_propagate(False)
        toolbar.grid_columnconfigure(1, weight=1)

        self._script_info = ctk.CTkLabel(toolbar, text="대본 미생성",
                                          text_color=self.C["dim"],
                                          font=F(size=12))
        self._script_info.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self._send_upload_btn = ctk.CTkButton(
            toolbar, text="업로드 탭으로",
            command=self._send_to_upload,
            height=30, width=120, state="disabled",
            fg_color=self.C["panel2"], hover_color=self.C["panel3"],
            text_color=self.C["text"], font=F(size=12),
        )
        self._send_upload_btn.grid(row=0, column=2, padx=12, pady=6)

        # 에디터
        self._editor = ctk.CTkTextbox(
            right,
            fg_color=self.C["panel"],
            text_color=self.C["text"],
            font=F(size=13),
            wrap="word",
            border_width=0,
        )
        self._editor.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # 하단 상태바
        status_bar = ctk.CTkFrame(right, fg_color=self.C["panel2"], corner_radius=0, height=28)
        status_bar.grid(row=2, column=0, sticky="ew")
        status_bar.grid_propagate(False)

        self._char_label = ctk.CTkLabel(status_bar, text="0자 · 약 0분",
                                         text_color=self.C["mute"],
                                         font=F(size=10))
        self._char_label.grid(row=0, column=0, padx=16, pady=4, sticky="w")

        self._editor.bind("<KeyRelease>", self._update_char_count)

    # ── 동작 ─────────────────────────────────────────────────────

    def _set_tone(self, tone_id: str) -> None:
        self._tone = tone_id
        for tid, btn in self._tone_btns.items():
            btn.configure(
                fg_color=self.C["panel3"] if tid == tone_id else self.C["panel2"],
                border_color=self.C["accent"] if tid == tone_id else self.C["border"],
            )

    def _set_duration(self, dur_id: str) -> None:
        self._duration = dur_id
        for did, btn in self._dur_btns.items():
            btn.configure(
                fg_color=self.C["panel3"] if did == dur_id else self.C["panel2"],
                border_color=self.C["accent"] if did == dur_id else self.C["border"],
            )

    def _generate(self) -> None:
        title = self._title_entry.get().strip()
        body = self._body_entry.get("1.0", "end").strip()
        url = self._url_entry.get().strip()

        if not title:
            self._set_status("소재 제목을 입력하세요.", error=True)
            return

        self._gen_btn.configure(state="disabled", text="생성 중...")
        self._progress.configure(mode="indeterminate")
        self._progress.start()
        self._set_status("OpenAI API 요청 중...")

        self.client.async_call(
            self.client.generate_script,
            source_title=title,
            source_body=body,
            source_url=url,
            tone=self._tone,
            language="ko",
            target_duration_sec=int(self._duration),
            on_success=self._on_gen_success,
            on_error=self._on_gen_error,
        )

    def _on_gen_success(self, result: dict) -> None:
        self.after(0, lambda: self._render_script(result))

    def _on_gen_error(self, msg: str) -> None:
        self.after(0, lambda: self._set_status(f"오류: {msg}", error=True))
        self.after(0, lambda: self._gen_btn.configure(state="normal", text="대본 생성"))
        self.after(0, lambda: (self._progress.stop(),
                               self._progress.configure(mode="determinate"),
                               self._progress.set(0)))

    def _render_script(self, result: dict) -> None:
        self._progress.stop()
        self._progress.configure(mode="determinate")
        self._progress.set(1)
        self._gen_btn.configure(state="normal", text="대본 생성")

        sections = result.get("sections", [])
        full_text = "\n\n".join(
            f"[{s.get('title', '')}]\n{s.get('content', '')}" for s in sections
        ) if sections else result.get("title", "") + "\n\n(대본 내용 없음)"

        self._editor.delete("1.0", "end")
        self._editor.insert("1.0", full_text)

        char_count = len(full_text)
        est_sec = result.get("total_duration_sec", int(char_count / (250 / 60)))
        self._script_info.configure(
            text=f"{result.get('title', '')[:40]} · {char_count}자 · 약 {est_sec}초",
            text_color=self.C["text"],
        )
        self._char_label.configure(text=f"{char_count}자 · 약 {est_sec}초")
        self._send_upload_btn.configure(state="normal")
        self._set_status("대본 생성 완료.")

    def _update_char_count(self, event=None) -> None:
        text = self._editor.get("1.0", "end").strip()
        chars = len(text)
        est_sec = int(chars / (250 / 60))
        self._char_label.configure(text=f"{chars}자 · 약 {est_sec}초")

    def _save_script(self) -> None:
        text = self._editor.get("1.0", "end").strip()
        if not text:
            return
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("Markdown", "*.md")],
            title="대본 저장",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self._set_status(f"저장 완료: {path}")

    def _send_to_upload(self) -> None:
        # _pending_title에 저장 후 이벤트 발생 (Windows data= 전달 불가 우회)
        self._pending_title = self._title_entry.get().strip()
        self.event_generate("<<SendToUpload>>")
        self._set_status("업로드 탭으로 전달했습니다.")

    def _set_status(self, msg: str, error: bool = False) -> None:
        color = self.C["accent"] if error else self.C["dim"]
        self._status.configure(text=msg, text_color=color)

    def load_source(self, title: str, body: str, url: str = "") -> None:
        """소재 수집 탭에서 소재를 전달받아 자동 입력합니다."""
        self._title_entry.delete(0, "end")
        self._title_entry.insert(0, title)
        self._body_entry.delete("1.0", "end")
        self._body_entry.insert("1.0", body)
        self._url_entry.delete(0, "end")
        self._url_entry.insert(0, url)
