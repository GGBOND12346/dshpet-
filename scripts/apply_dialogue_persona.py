# -*- coding: utf-8 -*-
"""把自动化/联动弹窗文案换成「七分娇、三分傲」的傲娇风格。

落点：主配置 ``config.json`` 的 ``dialogue_mode`` + ``dialogue_phrases``
（全局层）。设置页「自动化与联动 → 台词模板」里看到的就是这些。

文案纪律（与程序契约一致，改错会静默失效）：
* 每行一条，同一事件可写多条，程序按顺序轮换、不连着重样；
* 只能用该事件**真实注入**的参数占位符（见 ``persona_template.PARAMETERS``）；
* 条件参数（sessionName/projectName/toolName/errorCode 等）缺失时占位符
  整段自动隐藏，所以不要把它写成句子的必要成分；
* 花括号里只写参数名，写错名字会原样露出 ``{xxx}``。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# 事件键 → 台词列表（按程序内真实触发时机撰写）
PHRASES: dict[str, list[str]] = {
    # ---- 开局与思考 ----
    "start": [
        "哼，又开始了？这次我勉强陪你看看。",
        "开工就开工，别指望我会夸你。",
    ],
    "thinking": [
        "在想什么呢……别误会，我只是刚好有空盯着你。",
        "慢慢想，我又不催你。反正闲着也是闲着。",
    ],
    # ---- 干活过程 ----
    "activity.default": [
        "哼，{name}又在忙？我在旁边看着呢，别出错哦。",
        "动作挺熟练嘛……才、才没有在夸你。",
    ],
    "activity.read": [
        "又是读{label}……看得懂吗你？不懂可以问我。",
        "哼，翻来翻去的样子还挺认真，勉强算你过关。",
    ],
    "activity.search": [
        "找东西这种事，我早就想告诉你在哪了。",
        "哼，{name}又在翻找，找到了记得说一声。",
    ],
    "activity.edit": [
        "改来改去的，看着就累。不过……你自己决定吧。",
        "哼，别把好好的东西改坏了。",
    ],
    "activity.run": [
        "跑起来了就跑起来了，别一副要表扬的样子。",
        "哼，{name}干活的样子……还、还行吧。",
    ],
    # ---- 需要人介入 ----
    "agent.attention": [
        "喂，{name}那边要你拍板了，快去。",
        "别光顾着发呆，{name}等着你呢。",
    ],
    "agent.error": [
        "出错了……不、不是你的问题吧？快看看。",
        "哼，{name}这次真出岔子了，别装看不见。",
    ],
    "agent.missing": [
        "本机好像没装{name}，我不是催你，随便说一句。",
        "没找到{name}……装不装随你，我又不缺人陪。",
    ],
    "approval.tool": [
        "{name}要动{toolName}了，批不批你自己看着办。",
        "哼，{name}在等你点头呢，别磨蹭。",
    ],
    "approval.generic": [
        "{name}在等你确认，我可不想替你拿主意。",
        "有东西要批，快点，别让我等太久。",
    ],
    "question.empty": [
        "{name}在问你话呢，随便答一句也行。",
        "有话问你，别装作没看见。",
    ],
    "question.one": [
        "{name}问：{body}。……我说了只是转达而已。",
        "哼，{body}——你自己回答。",
    ],
    "question.many": [
        "{name}一口气问了{count}个问题，你慢慢来。",
        "有{count}个问题等着你，别嫌烦。",
    ],
    # ---- 完成 ----
    "done.success": [
        "哼，做完了？……勉强算你厉害。",
        "总算完事了。下次也别让我等这么久。",
    ],
    "done.attention": [
        "做完了，不过还有事要你看一眼。",
        "哼，完是完了，你自己确认一下。",
    ],
    # ---- 失败 ----
    "failure.retry": [
        "失败了在重试……还行，没直接放弃。",
        "哼，一次没成而已，再来就是了。",
    ],
    "failure.tool": [
        "工具报错了，别慌，看看日志。",
        "哼，出错了……又不全是你的错。",
    ],
    "failure.generic": [
        "出问题了。……我、我在这里看着呢，别急。",
        "又失败了？先停一下，深呼吸。",
    ],
    "model_access.one": [
        "模型那边连不上，已经试了{count}次。等会儿再试吧。",
        "哼，接口那边有点问题，不是你的错。",
    ],
    "model_access.many": [
        "连着{count}次都没连上，先歇会儿吧。",
        "模型那边一直不通……你别硬撑。",
    ],
    "llm_error.api": [
        "接口报错了，检查一下配置。我不会笑你的。",
        "哼，接口又出问题，真会挑时候。",
    ],
    # ---- 桥接安装（联动）----
    "bridge.install.pending": [
        "正在装{name}的桥接组件……别催，我也在等。",
        "哼，先把{name}的东西装好再说。",
    ],
    "bridge.install.success": [
        "装好了。……我、我只是顺便确认一下。",
        "哼，{name}的桥接装好了，这下能看见我干活了。",
    ],
    "bridge.install.failed": [
        "没装成……你看看{detail}那边。",
        "哼，装失败了。不怪你，检查下环境吧。",
    ],
    "bridge.uninstall.failed": [
        "卸不干净了，可能得你手动看看。",
        "哼，{name}的桥接没卸掉，别赖我。",
    ],
    "bridge.unknown": [
        "收到个没见过的信号{event}，先记着。",
        "哼，这是什么事件{event}……我看看。",
    ],
    # ---- 余额 ----
    "balance.loading": [
        "查着呢，急什么。",
        "哼，正在问余额，别催。",
    ],
    "balance.result": [
        "余额{text}……省着点花。",
        "哼，{text}，你自己心里有数。",
    ],
}


def main() -> int:
    from pet.config import Config

    cfg = Config()
    cfg.reload()
    before_mode = cfg.get("dialogue_mode")
    before = cfg.get("dialogue_phrases") or {}

    cfg.set("dialogue_mode", "custom")
    cfg.set("dialogue_phrases", {"global": PHRASES})
    if not cfg.save():
        raise SystemExit("写入配置失败")
    cfg.reload()

    print(f"模式：{before_mode!r} → {cfg.get('dialogue_mode')!r}")
    print(f"写前事件数：{len(before)}  写后事件数：{len(PHRASES)}")
    print(f"配置：{cfg.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
