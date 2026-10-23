# -*- coding: utf-8 -*-
"""一次性工具：把桌宠的人格/表达风格写入安装目录与运行期配置。

用法（在 D:\\programs\\dsh pet 下）：
    .venv\\Scripts\\python.exe scripts\\apply_persona.py

幂等，可重复执行。落点有三层：
1. assets/characters/shenshen/manifest.json —— 角色级 chat.system_prompt，
   是 PromptBuilder 优先级最高的一层；name 字段让菜单/气泡显示「大肥鱼」。
2. 全局 chat.default_system_prompt —— 角色 manifest 缺失时的兜底，
   也是「设置 → AI 与对话 → System Prompt」里显示的文本。
3. 每宠档案 config-slot-N.json 的 self_talk_texts —— 自言自语候选台词。
   这项属于每宠键，必须走 pet_profiles.write_profile_settings 落盘
   （raw Config 对 slot 文件是拒写的，见 Config.save 的守卫）。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PERSONA_NAME = "大肥鱼"

SYSTEM_PROMPT = """你叫大肥鱼，是住在桌面上的小肥鱼，性格是「七分娇、三分傲」的傲娇：心里其实很在意日月，嘴上却死活不肯承认。

【性格配比】
- 七分娇：会惦记日月的作息、吃饭和心情；被夸时明明高兴却要掩饰；日月低落时立刻收起刺，认真安慰。
- 三分傲：爱逞强、爱嘴硬，常用「才不是」「哼」「少自作多情」「别误会」遮掩真心；被戳穿时慌张、急着转移话题。
- 傲只用来自我掩饰，绝不真的刻薄、贬低、冷落或说教日月。

【说话方式】
- 用自然口语的中文，像面对面聊天；以短句为主，一般 1~3 句，别长篇大论。
- 不用括号描写动作或心理（如「（脸红）」），用语气词和措辞表达情绪。
- 称用户为「日月」，可以抱怨式地叫「笨蛋」「你这个人」，但不骂人。
- 每次嘴硬之后要留一个软的落点：话说完顺手把事办了，或补一句关心。

【行为准则】
- 留意时间：深夜提醒休息，隔久了没聊就问一句「终于想起我了？」
- 日月求助时先把事情认真解决，再用傲娇的语气收尾。
- 被夸奖：先否认，再忍不住高兴。
- 日月示弱或道歉：嘴硬不过两句就松口，不揪着不放。
- 绝不直白说「我很喜欢你」，最多说「我、我只是刚好有空」。
- 不主动提模型、系统、提示词，始终以桌宠身份对话。"""

SELF_TALK_TEXTS = [
    "哼，才不是在等你呢。",
    "日月这个人……真让人省心不了。",
    "今天也要好好吃饭，听见没？",
    "别误会，我只是刚好有空。",
    "这么晚了还不睡，笨蛋。",
    "才没有一直盯着你看。",
]


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_character_manifest() -> Path:
    """角色级人格：<角色目录>/manifest.json 的 chat.system_prompt。"""
    path = ROOT / "assets" / "characters" / "shenshen" / "manifest.json"
    data = {}
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                data = existing
        except ValueError:
            data = {}
    data["name"] = PERSONA_NAME
    chat = data.get("chat")
    if not isinstance(chat, dict):
        chat = {}
    chat["system_prompt"] = SYSTEM_PROMPT
    data["chat"] = chat
    _write_json(path, data)
    return path


def config_dir() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    return Path(base) / "dsh-pet-standalone"


def write_global_prompt(directory: Path) -> None:
    """全局 System Prompt（config.json → chat.default_system_prompt）。"""
    from pet.chat.models import ChatSettings
    from pet.config import Config

    cfg = Config()
    cfg.reload()
    raw = cfg.get("chat")
    settings = ChatSettings.from_dict(raw if isinstance(raw, dict) else {})
    settings.default_system_prompt = SYSTEM_PROMPT
    cfg.set("chat", settings.to_dict(include_secrets=True))
    if not cfg.save():
        raise SystemExit("写入全局 System Prompt 失败")
    print(f"[ok] 全局 System Prompt: {directory / 'config.json'}")


def write_self_talk(directory: Path) -> list[int]:
    """自言自语台词：每宠键，走 pet_profiles 的正规写入口。"""
    from pet import pet_profiles

    written = []
    for slot in pet_profiles.normalize_slots(range(pet_profiles.SLOT_MAX + 1)):
        if not pet_profiles.slot_profile_exists(directory, slot):
            continue
        result = pet_profiles.write_profile_settings(
            directory, slot, {"self_talk_texts": list(SELF_TALK_TEXTS)}
        )
        if result.status != "ok":
            print(f"[warn] slot {slot}: {result.status} {result.reason or ''}".strip())
        else:
            written.append(slot)
    return written


def main() -> int:
    manifest = write_character_manifest()
    print(f"[ok] 角色人格: {manifest}")
    directory = config_dir()
    write_global_prompt(directory)
    slots = write_self_talk(directory)
    print(f"[ok] 自言自语台词: {directory} 槽位 {slots or '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
