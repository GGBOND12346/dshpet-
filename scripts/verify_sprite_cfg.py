# -*- coding: utf-8 -*-
"""按真实 overlay 拓扑复算：一只 sprite 的 cfg 读到的朗读开关到底是什么。

不创建 GUI，只复刻 _SpriteConfig 的取值路径（快照 → 清洗 → 回退主配置）。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pet import pet_profiles  # noqa: E402
from pet.config import Config, normalize_pet_profile_snapshot  # noqa: E402


class FakeShell:
    """只提供 _SpriteConfig 需要的两个属性。"""

    def __init__(self, config: Config, config_dir: Path):
        self._config = config
        self.sprite = object()
        self._spawned_slots: dict = {}
        self._spawn_config_dir = lambda: str(config_dir)


def main() -> int:
    cfg = Config()
    cfg.reload()
    cfgdir = cfg.dir
    shell = FakeShell(cfg, cfgdir)

    snapshot = pet_profiles.read_slot_snapshot(cfgdir, 0)
    data = dict(snapshot.profile.data) if snapshot.profile else {}
    values = normalize_pet_profile_snapshot(data)

    print(f"快照状态            : {snapshot.status}")
    print(f"清洗后 speak 开关   : {values.get('self_talk_speak_enabled')}")
    print(f"清洗后 speak 开关   : {values.get('self_talk_speak_enabled')}")
    print(f"主配置 speak 开关   : {cfg.get('self_talk_speak_enabled')}")
    print(f"主配置是否含该键    : {'self_talk_speak_enabled' in cfg.data}")
    print()
    print(f"清洗后 click 开关   : {values.get('click_show_self_talk')}")
    print(f"主配置 click 开关   : {cfg.get('click_show_self_talk')}")
    print()
    print(f"清洗后 self_talk 总开关: {values.get('self_talk_enabled')}")
    print(f"清洗后台词条数      : {len(values.get('self_talk_texts') or [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
