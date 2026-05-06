# -*- coding: utf-8 -*-
"""바탕화면에 TubeFlow 바로가기를 생성합니다."""
import os
import sys
import win32com.client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DESKTOP  = os.path.join(os.path.dirname(BASE_DIR), "바탕 화면") if "바탕 화면" not in BASE_DIR else os.path.dirname(BASE_DIR)
PYTHON   = sys.executable
PWY      = os.path.join(BASE_DIR, "launch_gui.pyw")
LNK      = os.path.join(DESKTOP, "TubeFlow.lnk")

if os.path.exists(LNK):
    os.remove(LNK)

sh = win32com.client.Dispatch("WScript.Shell")
s  = sh.CreateShortcut(LNK)
s.TargetPath       = PYTHON
s.Arguments        = f'"{PWY}"'
s.WorkingDirectory = BASE_DIR
s.WindowStyle      = 1
s.IconLocation     = PYTHON + ",0"
s.Description      = "TubeFlow - 유튜브 채널 운영 자동화"
s.Save()

v = sh.CreateShortcut(LNK)
print(f"바로가기 생성 완료: {LNK}")
print(f"타겟: {v.TargetPath}")
print(f"인수: {v.Arguments}")
print(f"작업폴더: {v.WorkingDirectory}")
