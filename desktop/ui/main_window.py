import sys
import threading
import tkinter as tk
from pathlib import Path

import customtkinter as ctk
from desktop.ui.fonts import F

# 프로젝트 루트를 sys.path에 추가
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from desktop.client import APIClient
from desktop.ui.tab_sourcing import SourcingTab
from desktop.ui.tab_script import ScriptTab
from desktop.ui.tab_uploader import UploaderTab
from desktop.ui.tab_trend import TrendTab

# ── 컬러 팔레트 (디자인 시안 기준) ──────────────────────────────────
C = {
    "bg":        "#0E1014",
    "panel":     "#15181F",
    "panel2":    "#1B1F27",
    "panel3":    "#22262F",
    "border":    "#262A33",
    "text":      "#E7E9EE",
    "dim":       "#9097A3",
    "mute":      "#5C6370",
    "accent":    "#FF4655",
    "green":     "#3DD68C",
    "amber":     "#F5B544",
    "blue":      "#5B9CFF",
}

NAV_ITEMS = [
    ("collect",  "소재 수집"),
    ("script",   "대본 작성"),
    ("upload",   "업로드 예약"),
    ("trend",    "트렌드 분석"),
]

LOCAL_URL = "http://127.0.0.1:8421"
TEAM_URL  = ""   # 팀 서버 URL (.env TEAM_SERVER_URL 참조)


class NavButton(ctk.CTkButton):
    def __init__(self, master, label: str, tab_id: str, on_click, **kwargs):
        super().__init__(
            master,
            text=label,
            command=lambda: on_click(tab_id),
            anchor="w",
            corner_radius=7,
            height=36,
            font=F(size=13, weight="normal"),
            fg_color="transparent",
            text_color=C["dim"],
            hover_color=C["panel2"],
            **kwargs,
        )
        self.tab_id = tab_id

    def set_active(self, active: bool) -> None:
        if active:
            self.configure(
                fg_color=C["panel3"],
                text_color=C["text"],
                font=F(size=13, weight="bold"),
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=C["dim"],
                font=F(size=13, weight="normal"),
            )


class TubeFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TubeFlow")
        self.geometry("1280x800")
        self.minsize(900, 600)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color=C["bg"])

        self._server_mode = "local"
        self.client = APIClient(LOCAL_URL)
        self._nav_buttons: dict[str, NavButton] = {}
        self._current_tab = "collect"

        self._build_layout()
        self._switch_tab("collect")
        self._check_server_status()

    # ── 레이아웃 빌드 ─────────────────────────────────────────────

    def _build_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._sidebar = self._build_sidebar()
        self._sidebar.grid(row=0, column=0, sticky="nsew")

        self._content_frame = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        self._content_frame.grid(row=0, column=1, sticky="nsew")
        self._content_frame.grid_columnconfigure(0, weight=1)
        self._content_frame.grid_rowconfigure(0, weight=1)

        self._tabs: dict[str, ctk.CTkFrame] = {}

    def _build_sidebar(self) -> ctk.CTkFrame:
        sb = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=C["panel"])
        sb.grid_propagate(False)
        sb.grid_rowconfigure(5, weight=1)

        # 로고 행
        logo_frame = ctk.CTkFrame(sb, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 4))

        logo_box = ctk.CTkLabel(
            logo_frame,
            text="TF",
            width=28, height=28,
            corner_radius=7,
            fg_color=C["accent"],
            text_color="#ffffff",
            font=F(size=12, weight="bold"),
        )
        logo_box.grid(row=0, column=0, padx=(0, 10))

        logo_text = ctk.CTkFrame(logo_frame, fg_color="transparent")
        logo_text.grid(row=0, column=1)
        ctk.CTkLabel(logo_text, text="TubeFlow", text_color=C["text"],
                     font=F(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(logo_text, text="v0.1.0 · local", text_color=C["mute"],
                     font=F(size=10)).grid(row=1, column=0, sticky="w")
        self._version_label = logo_text.winfo_children()[1]

        # 섹션 레이블
        ctk.CTkLabel(sb, text="WORKSPACE", text_color=C["mute"],
                     font=F(size=10, weight="bold")).grid(
            row=1, column=0, sticky="w", padx=26, pady=(16, 4))

        # 네비게이션 버튼
        nav_frame = ctk.CTkFrame(sb, fg_color="transparent")
        nav_frame.grid(row=2, column=0, sticky="ew", padx=10)

        for i, (tab_id, label) in enumerate(NAV_ITEMS):
            btn = NavButton(nav_frame, label=label, tab_id=tab_id, on_click=self._switch_tab)
            btn.grid(row=i, column=0, sticky="ew", pady=1)
            nav_frame.grid_columnconfigure(0, weight=1)
            self._nav_buttons[tab_id] = btn

        # 스페이서
        ctk.CTkFrame(sb, fg_color="transparent", height=1).grid(row=5, column=0, sticky="nsew")

        # 서버 토글 섹션
        server_frame = ctk.CTkFrame(sb, fg_color=C["panel2"], corner_radius=8)
        server_frame.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 8))

        ctk.CTkLabel(server_frame, text="SERVER", text_color=C["mute"],
                     font=F(size=10, weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 4))

        self._server_seg = ctk.CTkSegmentedButton(
            server_frame,
            values=["로컬", "팀"],
            command=self._on_server_change,
            fg_color=C["panel3"],
            selected_color=C["accent"],
            selected_hover_color="#FF6B78",
            unselected_color=C["panel3"],
            font=F(size=12, weight="bold"),
        )
        self._server_seg.set("로컬")
        self._server_seg.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 6))

        self._status_dot = ctk.CTkLabel(server_frame, text="●", text_color=C["green"],
                                         font=F(size=8))
        self._status_dot.grid(row=2, column=0, sticky="w", padx=(12, 2), pady=(0, 10))
        self._status_label = ctk.CTkLabel(server_frame, text="127.0.0.1:8421",
                                           text_color=C["dim"], font=F(size=11))
        self._status_label.grid(row=2, column=1, sticky="w", pady=(0, 10))
        server_frame.grid_columnconfigure(1, weight=1)

        sb.grid_columnconfigure(0, weight=1)
        return sb

    # ── 탭 전환 ──────────────────────────────────────────────────

    def _switch_tab(self, tab_id: str) -> None:
        for tid, btn in self._nav_buttons.items():
            btn.set_active(tid == tab_id)

        for frame in self._tabs.values():
            frame.grid_remove()

        if tab_id not in self._tabs:
            self._tabs[tab_id] = self._create_tab(tab_id)

        self._tabs[tab_id].grid(row=0, column=0, sticky="nsew")
        self._current_tab = tab_id

    def _create_tab(self, tab_id: str) -> ctk.CTkFrame:
        constructors = {
            "collect": SourcingTab,
            "script":  ScriptTab,
            "upload":  UploaderTab,
            "trend":   TrendTab,
        }
        cls = constructors[tab_id]
        return cls(self._content_frame, client=self.client, colors=C)

    # ── 서버 모드 전환 ────────────────────────────────────────────

    def _on_server_change(self, value: str) -> None:
        self._server_mode = "local" if value == "로컬" else "team"
        if self._server_mode == "local":
            self.client.set_base_url(LOCAL_URL)
            self._status_label.configure(text="127.0.0.1:8421")
        else:
            from shared.config import get_settings
            url = get_settings().team_server_url or TEAM_URL or "팀 서버 미설정"
            self.client.set_base_url(url)
            self._status_label.configure(text=url[:24])
        self._check_server_status()

    def _check_server_status(self) -> None:
        def _ping():
            try:
                self.client.health()
                self.after(0, lambda: self._status_dot.configure(text_color=C["green"]))
            except Exception:
                self.after(0, lambda: self._status_dot.configure(text_color=C["accent"]))

        threading.Thread(target=_ping, daemon=True).start()
        self.after(30_000, self._check_server_status)


def main() -> None:
    app = TubeFlowApp()
    app.mainloop()


if __name__ == "__main__":
    main()
