# -*- coding: utf-8 -*-
"""校验自定义台词的占位符：只允许该事件真实注入的参数名。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_dialogue_persona import PHRASES  # noqa: E402

from pet.persona_template import (  # noqa: E402
    CONDITIONAL_PARAMETERS,
    LEGACY_HIDDEN_PARAMETERS,
    PARAMETERS,
)

PLACEHOLDER = re.compile(r"\{([^{}\s]+)\}")


def main() -> int:
    problems = []
    for key, lines in PHRASES.items():
        allowed = set(PARAMETERS.get(key, ())) | set(
            CONDITIONAL_PARAMETERS.get(key, ()))
        for line in lines:
            for name in PLACEHOLDER.findall(line):
                if name in LEGACY_HIDDEN_PARAMETERS:
                    problems.append(
                        f"{key}: 占位符 {{{name}}} 是退役字段，永不注入，会原样露出")
                elif name not in allowed:
                    problems.append(
                        f"{key}: 占位符 {{{name}}} 不在可用清单 {sorted(allowed)}")
    if problems:
        print("发现 %d 处问题：" % len(problems))
        for p in problems:
            print("  -", p)
        return 1
    total = sum(len(v) for v in PHRASES.values())
    print(f"OK：{len(PHRASES)} 个事件、{total} 条台词，占位符全部合法")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
