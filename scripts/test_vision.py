# -*- coding: utf-8 -*-
"""实测桌宠的视觉链路：截屏 → 编码 → 视觉模型请求 → 是否拿到文本回答。

只读取本机已配置的 provider / keyring，不修改任何配置。
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
    p = settings.active_config
    p.api_key = cfg.resolve_api_key(p)

    print("=== provider ===")
    print(f"聊天模型      : {p.model}")
    print(f"视觉模型推导  : {vision.resolve_vision_model(p)}")
    print(f"vision_same_as_chat: {p.vision_same_as_chat}")
    print(f"base_url      : {p.base_url}")
    print(f"API Key       : {'已配置 (len=%d)' % len(str(p.api_key)) if p.api_key else '缺失'}")
    print()

    print("=== 截屏能力 ===")
    info = vision.foreground_window_info()
    print(f"前台窗口      : {(info or {}).get('title', '<不可用>')}")
    try:
        data = vision.capture_screen_bytes()
        print(f"全屏截图      : OK, {len(data)} bytes JPEG")
    except Exception as exc:
        print(f"全屏截图      : 失败 {type(exc).__name__}: {exc}")
        return 1
    if info:
        try:
            img = vision.capture_window_rect(info["rect"])
            print(f"窗口截图      : OK, image={img.size if hasattr(img, 'size') else '?'}")
        except Exception as exc:
            print(f"窗口截图      : 失败 {type(exc).__name__}: {exc}")
    print()

    print("=== 视觉请求（真实调用）===")
    system_prompt = "你叫大肥鱼，是桌面宠物。用一句话说出你看到的内容。"
    try:
        reply = vision._post_vision_request(
            data, "测试窗口", system_prompt, p, pet_name="大肥鱼")
        text = str(reply)
        print(f"模型回答（{len(text)} 字）:")
        print(text[:500])
    except Exception as exc:
        print(f"请求失败: {type(exc).__name__}: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
