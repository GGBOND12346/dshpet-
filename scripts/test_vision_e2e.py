# -*- coding: utf-8 -*-
"""端到端：用与菜单相同的入口（AskAboutScreen）跑一次真实视觉问答。

不启动 GUI，只复用 widget 的调用面：截屏 → vision.ask_about_screen → 文本。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    from pet import vision
    from pet.chat.models import ChatSettings
    from pet.config import Config

    cfg = Config()
    cfg.reload()
    settings = ChatSettings.from_dict(cfg.get("chat") or {})
    provider = settings.active_config
    provider.api_key = cfg.resolve_api_key(provider)

    system_prompt = settings.default_system_prompt
    pet_name = cfg.character_display_name(
        str(cfg.get("character", "shenshen")))

    print("=== 与「看看屏幕」菜单相同的调用面 ===")
    print(f"角色显示名 : {pet_name}")
    print(f"system 首行: {system_prompt.splitlines()[0][:40]}...")
    print()

    shot = vision.capture_screen_bytes()
    app_info = vision.foreground_app_info()
    print(f"截图 {len(shot)} bytes，前台应用: {app_info}")
    print("请求中…")

    reply = vision.ask_about_screen(
        shot, app_info, system_prompt, provider, pet_name=pet_name)
    print()
    print(f"=== 桌宠回答（{len(reply)} 字）===")
    print(reply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
