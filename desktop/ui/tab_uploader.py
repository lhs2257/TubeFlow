import tkinter as tk
from datetime import datetime, timedelta
from tkinter import filedialog

import customtkinter as ctk

from desktop.client import APIClient


PRIVACY_OPTIONS = [
    ("private",   "비공개"),
    ("unlisted",  "미등록"),
    ("public",    "공개"),
]

STATUS_COLORS = {
    "pending":    "#F5B544",
    "uploading":  "#5B9CFF",
    "processing": "#5B9CFF",
    "done":       "#3DD68C",
    "failed":     "#FF4655",
}
STATUS_LABELS = {
    "pending":    "예약됨",
    "uploading":  "업로드 중",
    "processing": "처리 중",
    "done":       "완료",
    "failed":     "실패",
}


class UploaderTab(ctk.CTkFrame):
    """업로드 예약 탭 — YouTube 업로드 큐 관리."""

    def __init__(self, master, client: APIClient, colors: dict, **kwargs):
        super().__init__(master, fg_color=colors["bg"], corner_radius=0, **kwargs)
        self.client = client
        self.C = colors
        self._privacy = "private"
        self._video_path = ""
        self._thumbnail_path = ""
        self._tags: list[str] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._refresh_queue()

    # ── 헤더 ─────────────────────────────────────────────────────

    def _build_header(self) -> None:
        hdr = ctk.CTkFrame(self, fg_color=self.C["panel"], corner_radius=0, height=56)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(hdr, text="업로드 예약",
                     text_color=self.C["text"],
                     font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, padx=24, pady=16, sticky="w")
        ctk.CTkLabel(hdr, text="영상을 업로드하고 게시 일정을 관리합니다",
                     text_color=self.C["dim"], font=ctk.CTkFont(size=12)).grid(
            row=0, column=1, padx=8, pady=16, sticky="w")

        ctk.CTkButton(
            hdr, text="큐 새로고침", command=self._refresh_queue,
            height=32, width=110,
            fg_color=self.C["panel2"], hover_color=self.C["panel3"],
            text_color=self.C["text"], font=ctk.CTkFont(size=12),
        ).grid(row=0, column=2, padx=12, pady=12)

    # ── 바디 ─────────────────────────────────────────────────────

    def _build_body(self) -> None:
        body = ctk.CTkFrame(self, fg_color=self.C["bg"], corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, minsize=360)
        body.grid_rowconfigure(0, weight=1)

        self._build_form(body)
        self._build_queue_panel(body)

    def _build_form(self, parent) -> None:
        form = ctk.CTkScrollableFrame(parent, fg_color=self.C["bg"],
                                       scrollbar_button_color=self.C["panel3"])
        form.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        form.grid_columnconfigure(0, weight=1)

        pad = {"padx": 24, "pady": 5}

        # 영상 파일 선택
        self._section_label(form, "영상 파일", row=0)
        video_row = ctk.CTkFrame(form, fg_color=self.C["panel2"],
                                  corner_radius=8, border_width=1,
                                  border_color=self.C["border"])
        video_row.grid(row=1, column=0, sticky="ew", **pad)
        video_row.grid_columnconfigure(0, weight=1)

        self._video_label = ctk.CTkLabel(video_row, text="파일을 선택하세요",
                                          text_color=self.C["dim"],
                                          font=ctk.CTkFont(size=12), anchor="w")
        self._video_label.grid(row=0, column=0, padx=12, pady=10, sticky="ew")

        ctk.CTkButton(video_row, text="찾아보기", width=90, height=28,
                      fg_color=self.C["panel3"], hover_color=self.C["border"],
                      text_color=self.C["text"], font=ctk.CTkFont(size=11),
                      command=self._pick_video).grid(row=0, column=1, padx=8, pady=8)

        # 제목
        self._section_label(form, "제목", row=2)
        self._title_entry = ctk.CTkEntry(form, placeholder_text="영상 제목 (최대 100자)",
                                          fg_color=self.C["panel2"],
                                          text_color=self.C["text"],
                                          border_color=self.C["border"],
                                          font=ctk.CTkFont(size=13))
        self._title_entry.grid(row=3, column=0, sticky="ew", **pad)

        # 설명
        self._section_label(form, "설명", row=4)
        self._desc_box = ctk.CTkTextbox(form, height=90, fg_color=self.C["panel2"],
                                         text_color=self.C["text"],
                                         border_width=1, border_color=self.C["border"],
                                         font=ctk.CTkFont(size=12))
        self._desc_box.grid(row=5, column=0, sticky="ew", **pad)

        # 태그
        self._section_label(form, "태그 (쉼표로 구분)", row=6)
        self._tag_entry = ctk.CTkEntry(form, placeholder_text="여행, 해외여행, 발리...",
                                        fg_color=self.C["panel2"],
                                        text_color=self.C["text"],
                                        border_color=self.C["border"],
                                        font=ctk.CTkFont(size=12))
        self._tag_entry.grid(row=7, column=0, sticky="ew", **pad)

        # 공개 범위
        self._section_label(form, "공개 범위", row=8)
        priv_frame = ctk.CTkFrame(form, fg_color="transparent")
        priv_frame.grid(row=9, column=0, sticky="ew", **pad)

        self._priv_var = tk.StringVar(value="private")
        for i, (val, label) in enumerate(PRIVACY_OPTIONS):
            rb = ctk.CTkRadioButton(
                priv_frame, text=label, value=val,
                variable=self._priv_var,
                fg_color=self.C["accent"], hover_color="#FF6B78",
                text_color=self.C["text"], font=ctk.CTkFont(size=12),
            )
            rb.grid(row=0, column=i, padx=(0, 16))

        # 예약 게시 섹션
        sched_card = ctk.CTkFrame(form, fg_color=self.C["panel2"],
                                   corner_radius=8, border_width=1,
                                   border_color=self.C["border"])
        sched_card.grid(row=10, column=0, sticky="ew", padx=24, pady=(12, 5))
        sched_card.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(sched_card, text="예약 게시 (비워두면 즉시)",
                     text_color=self.C["text"],
                     font=ctk.CTkFont(size=12, weight="bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(10, 4))

        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self._date_entry = ctk.CTkEntry(sched_card, placeholder_text=tomorrow,
                                         fg_color=self.C["panel3"],
                                         text_color=self.C["text"],
                                         border_color=self.C["border"],
                                         font=ctk.CTkFont(size=12))
        self._date_entry.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 10))

        self._time_entry = ctk.CTkEntry(sched_card, placeholder_text="19:00",
                                         fg_color=self.C["panel3"],
                                         text_color=self.C["text"],
                                         border_color=self.C["border"],
                                         font=ctk.CTkFont(size=12))
        self._time_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=(0, 10))

        ctk.CTkLabel(sched_card, text="로컬 시간 기준",
                     text_color=self.C["mute"],
                     font=ctk.CTkFont(size=11)).grid(
            row=1, column=2, padx=8, pady=(0, 10))

        # 등록 버튼
        self._submit_btn = ctk.CTkButton(
            form, text="예약 등록",
            command=self._submit,
            height=40,
            fg_color=self.C["accent"], hover_color="#FF6B78",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self._submit_btn.grid(row=11, column=0, sticky="ew", padx=24, pady=(12, 4))

        self._form_status = ctk.CTkLabel(form, text="", text_color=self.C["dim"],
                                          font=ctk.CTkFont(size=11))
        self._form_status.grid(row=12, column=0, pady=(0, 16))

    def _build_queue_panel(self, parent) -> None:
        panel = ctk.CTkFrame(parent, fg_color=self.C["panel"], corner_radius=0)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        # 큐 헤더
        q_hdr = ctk.CTkFrame(panel, fg_color=self.C["panel2"],
                               corner_radius=0, height=44)
        q_hdr.grid(row=0, column=0, sticky="ew")
        q_hdr.grid_propagate(False)
        q_hdr.grid_columnconfigure(1, weight=1)

        self._queue_title = ctk.CTkLabel(q_hdr, text="예약 큐 (0개)",
                                          text_color=self.C["text"],
                                          font=ctk.CTkFont(size=13, weight="bold"))
        self._queue_title.grid(row=0, column=0, padx=16, pady=10, sticky="w")

        ctk.CTkButton(q_hdr, text="실행", command=self._run_pending,
                      height=28, width=60,
                      fg_color=self.C["accent"], hover_color="#FF6B78",
                      text_color="#fff", font=ctk.CTkFont(size=11, weight="bold")).grid(
            row=0, column=2, padx=10, pady=8)

        # 큐 목록
        self._queue_scroll = ctk.CTkScrollableFrame(
            panel, fg_color=self.C["panel"],
            scrollbar_button_color=self.C["panel3"],
        )
        self._queue_scroll.grid(row=1, column=0, sticky="nsew")
        self._queue_scroll.grid_columnconfigure(0, weight=1)

    # ── 헬퍼 ─────────────────────────────────────────────────────

    def _section_label(self, parent, text: str, row: int) -> None:
        ctk.CTkLabel(parent, text=text, text_color=self.C["dim"],
                     font=ctk.CTkFont(size=11, weight="bold")).grid(
            row=row, column=0, sticky="w", padx=24, pady=(12, 2))

    # ── 동작 ─────────────────────────────────────────────────────

    def _pick_video(self) -> None:
        path = filedialog.askopenfilename(
            title="영상 파일 선택",
            filetypes=[("영상 파일", "*.mp4 *.mov *.avi *.mkv"), ("모든 파일", "*.*")],
        )
        if path:
            self._video_path = path
            name = path.split("/")[-1].split("\\")[-1]
            self._video_label.configure(text=name, text_color=self.C["text"])

    def _submit(self) -> None:
        if not self._video_path:
            self._set_form_status("영상 파일을 선택하세요.", error=True)
            return
        title = self._title_entry.get().strip()
        if not title:
            self._set_form_status("제목을 입력하세요.", error=True)
            return

        desc = self._desc_box.get("1.0", "end").strip()
        tags_raw = self._tag_entry.get().strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        privacy = self._priv_var.get()

        scheduled_at = None
        date_str = self._date_entry.get().strip()
        time_str = self._time_entry.get().strip() or "19:00"
        if date_str:
            try:
                scheduled_at = f"{date_str}T{time_str}:00"
            except Exception:
                self._set_form_status("날짜 형식이 잘못되었습니다 (YYYY-MM-DD).", error=True)
                return

        self._submit_btn.configure(state="disabled", text="등록 중...")
        self.client.async_call(
            self.client.add_upload,
            video_path=self._video_path,
            title=title,
            description=desc,
            tags=tags,
            privacy=privacy,
            scheduled_at=scheduled_at,
            on_success=self._on_submit_success,
            on_error=self._on_submit_error,
        )

    def _on_submit_success(self, result: dict) -> None:
        self.after(0, lambda: self._set_form_status(
            f"예약 등록 완료: {result.get('title', '')[:40]}"))
        self.after(0, lambda: self._submit_btn.configure(state="normal", text="예약 등록"))
        self.after(0, self._refresh_queue)

    def _on_submit_error(self, msg: str) -> None:
        self.after(0, lambda: self._set_form_status(f"오류: {msg}", error=True))
        self.after(0, lambda: self._submit_btn.configure(state="normal", text="예약 등록"))

    def _run_pending(self) -> None:
        self.client.async_call(
            self.client.run_pending_uploads,
            on_success=lambda r: self.after(0, lambda: self._refresh_queue()),
            on_error=lambda e: None,
        )

    def _refresh_queue(self) -> None:
        self.client.async_call(
            self.client.get_upload_queue,
            on_success=self._on_queue_loaded,
            on_error=lambda e: None,
        )

    def _on_queue_loaded(self, result: dict) -> None:
        queue = result.get("queue", [])
        self.after(0, lambda: self._render_queue(queue))

    def _render_queue(self, queue: list[dict]) -> None:
        for w in self._queue_scroll.winfo_children():
            w.destroy()

        pending = [j for j in queue if j.get("status") == "pending"]
        self._queue_title.configure(text=f"예약 큐 ({len(pending)}개 대기)")

        if not queue:
            ctk.CTkLabel(self._queue_scroll, text="예약된 항목이 없습니다.",
                         text_color=self.C["mute"],
                         font=ctk.CTkFont(size=12)).grid(row=0, column=0, pady=24)
            return

        for i, job in enumerate(queue):
            self._add_queue_card(i, job)

    def _add_queue_card(self, idx: int, job: dict) -> None:
        status = job.get("status", "pending")
        color = STATUS_COLORS.get(status, self.C["dim"])
        label = STATUS_LABELS.get(status, status)

        card = ctk.CTkFrame(self._queue_scroll, fg_color=self.C["panel2"],
                             corner_radius=7, border_width=1,
                             border_color=self.C["border"])
        card.grid(row=idx, column=0, sticky="ew", padx=10, pady=4)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text=job.get("title", "")[:50],
                     text_color=self.C["text"],
                     font=ctk.CTkFont(size=12),
                     wraplength=280, anchor="w", justify="left").grid(
            row=0, column=0, sticky="ew", padx=10, pady=(8, 2))

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 8))

        ctk.CTkLabel(info_frame, text=label, text_color=color,
                     font=ctk.CTkFont(size=10, weight="bold")).grid(
            row=0, column=0, sticky="w")

        sched = job.get("scheduled_at") or "즉시"
        if sched and sched != "즉시":
            sched = sched[:16].replace("T", " ")
        ctk.CTkLabel(info_frame, text=sched, text_color=self.C["mute"],
                     font=ctk.CTkFont(size=10)).grid(row=0, column=1, padx=8, sticky="w")

        if status == "pending":
            ctk.CTkButton(
                card, text="취소", width=48, height=22,
                fg_color="transparent", hover_color=self.C["panel3"],
                text_color=self.C["accent"], font=ctk.CTkFont(size=10),
                border_width=1, border_color=self.C["accent"],
                command=lambda jid=job.get("id", ""): self._cancel_job(jid),
            ).grid(row=0, column=1, padx=8, pady=(8, 2))

    def _cancel_job(self, job_id: str) -> None:
        self.client.async_call(
            self.client.cancel_upload,
            job_id,
            on_success=lambda r: self.after(0, self._refresh_queue),
            on_error=lambda e: None,
        )

    def _set_form_status(self, msg: str, error: bool = False) -> None:
        color = self.C["accent"] if error else self.C["dim"]
        self._form_status.configure(text=msg, text_color=color)
