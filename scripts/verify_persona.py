# -*- coding: utf-8 -*-
"""校验：模拟桌宠的真实取用链路，确认人格与台词已被读到。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pet.chat.models import ChatSettings  # noqa: E402
from pet.chat.prompt import PromptBuilder  # noqa: E402
from pet.config import Config  # noqa: E402
from pet import pet_profiles  # noqa: E402
from pet.catalog import character_display_name  # noqa: E402

chars_root = ROOT / "assets" / "characters"
builder = PromptBuilder(chars_root)

cfg = Config()
cfg.reload()
settings = ChatSettings.from_dict(cfg.get("chat") or {})

prompt = builder.effective_system_prompt(settings, "shenshen")
print("角色显示名 :", character_display_name("shenshen"))
print("生效人格来源:", "角色 manifest（覆盖全局）" if prompt.startswith("你叫大肥鱼") else "全局 System Prompt")
print("生效人格首行:", prompt.splitlines()[0])
print("人格长度    :", len(prompt), "字")

for slot in pet_profiles.normalize_slots(range(pet_profiles.SLOT_MAX + 1)):
    if pet_profiles.slot_profile_exists(ROOT.parent / "" / "__none__", slot):
        pass
print()
cfgdir = Config().dir
for slot in pet_profiles.normalize_slots(range(pet_profiles.SLOT_MAX + 1)):
    if not pet_profiles.slot_profile_exists(cfgdir, slot):
        continue
    profile = pet_profiles.read_slot_profile(cfgdir, slot)
    texts = profile.value("self_talk_texts") or []
    print(f"slot {slot} 自言自语（{len(texts)} 条）:")
    for line in texts:
        print("   ", line)
