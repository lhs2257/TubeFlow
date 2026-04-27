import customtkinter as ctk

# 한국어 UI 폰트 우선순위: 맑은 고딕 > 나눔고딕 > 돋움 > 기본
_KOREAN_FONT = "맑은 고딕"
_MONO_FONT   = "Cascadia Code"


def F(size: int = 13, weight: str = "normal", mono: bool = False) -> ctk.CTkFont:
    """UI 전역 폰트 팩토리. 한국어 최적화."""
    family = _MONO_FONT if mono else _KOREAN_FONT
    return ctk.CTkFont(family=family, size=size, weight=weight)
