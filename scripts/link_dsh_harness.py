# -*- coding: utf-8 -*-
"""把桌宠与 DeepSeek Harness 联动起来。

做两件事，都可重复执行（幂等）：
1. 指定 pnpm 入口——本机没有全局 pnpm，用 DSH 桌面端自带的那份
   （pnpm 11.28.5）。桥接插件经 pnpm 安装，找不到 pnpm 就装不上。
2. 打开 DSH 联动开关（agent_link.dsh）。

装桥接插件本身由桌宠在开启联动时自己做（见 agent_link 的安装辅助），
本脚本不代劳——那条路径要处理 profile 的 bundles 层与 pnpm 版本差异。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# DSH 桌面端自带的 pnpm（桌面端进程命令行里用的就是这一份）
DSH_PNPM = Path(
    r"D:\programs\deepseek\resources\runtime\primary-runtime\dependencies\pnpm\bin\pnpm.mjs"
)


def main() -> int:
    from pet.config import Config

    if not DSH_PNPM.is_file():
        raise SystemExit(f"找不到 DSH 自带的 pnpm：{DSH_PNPM}")

    cfg = Config()
    cfg.reload()

    before = {
        "pnpm_bin": cfg.get("pnpm_bin"),
        "agent_link.dsh": (cfg.get("agent_link") or {}).get("dsh"),
    }

    cfg.set("pnpm_bin", str(DSH_PNPM))
    link = dict(cfg.get("agent_link") or {})
    link["dsh"] = True
    cfg.set("agent_link", link)

    if not cfg.save():
        raise SystemExit("写入配置失败")
    cfg.reload()

    after = {
        "pnpm_bin": cfg.get("pnpm_bin"),
        "agent_link.dsh": (cfg.get("agent_link") or {}).get("dsh"),
    }
    print("写前:", before)
    print("写后:", after)
    print(f"配置文件: {cfg.path}")
    print(f"pnpm 入口: {DSH_PNPM}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
