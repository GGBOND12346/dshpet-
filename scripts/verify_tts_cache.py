# -*- coding: utf-8 -*-
"""核对：自言自语台词是否已按当前音色合成进音频缓存。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pet import voice_chime  # noqa: E402
from pet.config import Config  # noqa: E402
from pet import pet_profiles  # noqa: E402

TEXTS = [
    "哼，才不是在等你呢。",
    "日月这个人……真让人省心不了。",
    "今天也要好好吃饭，听见没？",
    "别误会，我只是刚好有空。",
    "这么晚了还不睡，笨蛋。",
    "才没有一直盯着你看。",
]


def main() -> int:
    cfg_obj = Config()
    cfg_obj.reload()
    cfg = voice_chime.normalize_chime_config(cfg_obj)
    cache_dir = Path(cfg_obj.dir) / "voice_chime_cache"
    print(f"音色: {cfg.get('voice')}  语速: {cfg.get('rate')}  后端: {cfg.get('backend')}")
    print(f"缓存目录: {cache_dir}")
    print()
    have = 0
    for text in TEXTS:
        key = voice_chime.cache_key(text, cfg)
        path = cache_dir / f"{key}.mp3"
        ok = path.is_file() and path.stat().st_size > 0
        have += ok
        print(f"{'✓ 已合成' if ok else '· 尚未'}  {key}  {text}")
    print()
    print(f"覆盖率: {have}/{len(TEXTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
