# -*- coding: utf-8 -*-
"""一次性验证：周期气泡与点击两条路径是否都会朗读（不需要真实 GUI）。

用 window_alerts 的 host 形函数直接驱动，宿主是极简替身：
只提供这两条路径真正读到的属性，朗读通道用一个记录器接住。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pet import window_alerts  # noqa: E402


class _FakeBubble:
    """气泡控件替身：只记录被要求显示的文本。"""

    def __init__(self) -> None:
        self.shown: list[str] = []

    def set_interactive(self, *_args, **_kwargs) -> None:
        pass

    def show_text(self, text, *_args, **_kwargs) -> None:
        self.shown.append(str(text))

    def show_image(self, *_args, **_kwargs) -> None:
        pass


class _FakeCfg(dict):
    """配置替身：dict 语义 + 点击台词绑定查询。"""

    def click_talk_texts_for(self, character_id: str, action_id: str) -> list[str]:
        return []


class FakeHost:
    """自言自语两条路径所需的最小宿主面。"""

    def __init__(self, *, enabled: bool = True, speak: bool = True, image_chance: int = 0):
        self.cfg = _FakeCfg(
            self_talk_speak_enabled=speak,
            self_talk_image_chance=image_chance,
            character="shenshen",
        )
        self._self_talk_enabled = enabled
        self._self_talk_texts = ["哼，才不是在等你呢。", "这么晚了还不睡，笨蛋。"]
        self._self_talk_images = []
        self._self_talk_image_scale = 1.0
        self._self_talk_duration_seconds = 3.2
        self._self_talk_min_interval = 20.0
        self._self_talk_max_interval = 60.0
        self._last_self_talk_text = None
        self._bubble_busy_until = 0.0
        self.spoken: list[str] = []
        self.rescheduled: list[bool] = []
        self._speech_bubble = _FakeBubble()

    # —— 语音通道（app 接线到 AppShell.speak_self_talk 的那一个）——
    def on_self_talk_speak(self, text: str) -> None:
        self.spoken.append(text)

    # —— 气泡落地面 ——
    def _show_self_talk_text(self, text: str) -> bool:
        return True

    def _show_random_self_talk(self) -> bool:
        return window_alerts.show_random_self_talk(self)

    def _schedule_self_talk(self, *, after_display: bool = False) -> None:
        self.rescheduled.append(after_display)

    def isVisible(self) -> bool:  # noqa: N802 —— Qt 名
        return True

    def visible_content_rect(self):
        """气泡锚点（window_placement 读这个）。"""
        from PySide6.QtCore import QRect

        return QRect(0, 0, 160, 194)


class FrozenClock:
    """把 window.time.monotonic 固定在 1.0，让 busy 判定稳定为"不占用"。"""


def run_case(label: str, fake: FakeHost, action) -> None:
    fake.spoken.clear()
    action(fake)
    status = "会朗读" if fake.spoken else "不朗读"
    print(f"{label:<28} {status:<6} {fake.spoken}")


def main() -> int:
    import pet.window as window_mod

    original = window_mod.time.monotonic
    window_mod.time.monotonic = lambda: 1.0
    try:
        print("=" * 68)
        print("周期气泡路径（on_self_talk_timeout）")
        print("=" * 68)
        run_case("开关开着", FakeHost(), window_alerts.on_self_talk_timeout)
        run_case("朗读开关关闭", FakeHost(speak=False), window_alerts.on_self_talk_timeout)
        run_case("周期气泡总开关关闭", FakeHost(enabled=False), window_alerts.on_self_talk_timeout)

        print()
        print("=" * 68)
        print("点击路径（show_click_self_talk，未绑定专属台词时走随机）")
        print("=" * 68)

        def click(fake):
            window_alerts.show_click_self_talk(fake, "点击回应-元气挥手")

        run_case("开关开着", FakeHost(), click)
        run_case("朗读开关关闭", FakeHost(speak=False), click)

        print()
        print("=" * 68)
        print("重复朗读检查：点击回退分支是否只读一遍")
        print("=" * 68)
        f = FakeHost()
        window_alerts.show_click_self_talk(f, "点击回应-元气挥手")
        print(f"点击一次实际朗读 {len(f.spoken)} 次 -> {'正常' if len(f.spoken) == 1 else '重复！'}")
        f.spoken.clear()
        window_alerts.on_self_talk_timeout(f)
        print(f"定时一次实际朗读 {len(f.spoken)} 次 -> {'正常' if len(f.spoken) == 1 else '重复！'}")
    finally:
        window_mod.time.monotonic = original
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
