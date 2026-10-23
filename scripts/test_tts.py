# -*- coding: utf-8 -*-
"""验证 edge-tts 合成链是否可用（只合成，不播放）。"""
from __future__ import annotations

import asyncio
import sys

import edge_tts


async def main() -> int:
    text = "哼，才不是在等你呢。"
    voice = sys.argv[1] if len(sys.argv) > 1 else "zh-CN-XiaoyiNeural"
    communicate = edge_tts.Communicate(text, voice)
    audio = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    print(f"voice={voice} {len(audio)} bytes")
    return 0 if audio else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
