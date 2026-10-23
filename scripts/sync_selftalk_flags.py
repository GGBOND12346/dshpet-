# -*- coding: utf-8 -*-
"""把自言自语族开关同步到**主配置**（AppShell.config 的读源）。

为什么要单独一支：这些键存在两份真值——
* `config-slot-0.json`（每宠档案，桌面气泡/点击行为读它）
* `config.json`（主配置，`AppShell._self_talk_speak_wanted` 决定音频通道生死）

只改档案时，气泡照常冒、开关看着是开的，但音频通道始终不创建，
表现就是"有气泡没声音"。这里把两边对齐，并保留原有值不动其它键。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

WANTED = {
    "self_talk_speak_enabled": True,
    "click_show_self_talk": True,
    "self_talk_enabled": True,
    "self_talk_voice_precache_enabled": False,  # 本机无 CosyVoice，预缓存只会超时
}


def main() -> int:
    from pet.config import Config

    cfg = Config()
    cfg.reload()
    before = {key: cfg.data.get(key) for key in WANTED}
    for key, value in WANTED.items():
        cfg.set(key, value)
    if not cfg.save():
        raise SystemExit("写入主配置失败")
    cfg.reload()
    print("主配置写前：", before)
    print("主配置写后：", {key: cfg.data.get(key) for key in WANTED})
    print(f"文件：{cfg.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
