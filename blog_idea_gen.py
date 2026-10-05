"""blog-idea-gen：按主题 / 关键词模板组合出博客选题与角度清单。

无 LLM 时用角度模板（教程 / 清单 / 案例 / 对比 / 避坑 / 观点等）与主题拼接，
生成一组可直接使用的博客标题与写作角度。可选 LLM 生成更多灵感。
"""

from __future__ import annotations

import json
import os
import urllib.request

ANGLES: list[dict[str, str]] = [
    {"key": "tutorial", "label": "入门教程",
     "title": "{topic} 上手指南：从零开始的完整教程",
     "angle": "面向新手，按步骤讲清核心概念与第一个可运行示例。"},
    {"key": "listicle", "label": "清单干货",
     "title": "关于 {topic}，你必须知道的 10 件事",
     "angle": "用编号清单快速罗列要点，适合收藏与转发。"},
    {"key": "beginner", "label": "新手避坑",
     "title": "学习 {topic} 常见的 7 个坑，我替你踩过了",
     "angle": "从亲身经验出发，盘点新手高频错误与规避方法。"},
    {"key": "case", "label": "实战案例",
     "title": "我是如何用 {topic} 解决真实问题的（完整复盘）",
     "angle": "以一个真实项目为主线，讲背景、做法、结果与反思。"},
    {"key": "comparison", "label": "横向对比",
     "title": "{topic} 方案横评：主流做法到底怎么选？",
     "angle": "列出 2-4 个主流方案，从成本、性能、易用性做对比。"},
    {"key": "opinion", "label": "观点输出",
     "title": "关于 {topic}，我有一些不同看法",
     "angle": "抛出反共识观点，给出论据与边界，引发讨论。"},
    {"key": "deepdive", "label": "深度原理",
     "title": "{topic} 背后的原理，一篇讲透",
     "angle": "下沉到机制与原理，配图示，写给有基础的读者。"},
    {"key": "faq", "label": "问答合集",
     "title": "{topic} 高频问题 FAQ：一次性答全",
     "angle": "收集读者最常问的问题，逐条给出简明答案。"},
]


def generate_ideas(topic: str, keywords: list[str] | None = None) -> list[dict]:
    """根据主题生成选题清单。每个选题含 title / angle / 建议关键词。"""
    topic = topic.strip()
    if not topic:
        raise ValueError("主题不能为空")
    kws = [k.strip() for k in (keywords or []) if k.strip()]

    ideas = []
    for a in ANGLES:
        title = a["title"].format(topic=topic)
        ideas.append({
            "angle_key": a["key"],
            "angle": a["label"],
            "title": title,
            "angle_desc": a["angle"],
            "suggested_keywords": [topic] + kws,
        })
    return ideas


def render_markdown(topic: str, ideas: list[dict]) -> str:
    """把选题清单渲染成 Markdown。"""
    lines = [f"# 博客选题清单：{topic}", ""]
    for i, idea in enumerate(ideas, 1):
        lines.append(f"## {i}. {idea['title']}")
        lines.append("")
        lines.append(f"- 写作角度：{idea['angle']} —— {idea['angle_desc']}")
        kws = "、".join(idea["suggested_keywords"])
        lines.append(f"- 建议关键词：{kws}")
        lines.append("")
    return "\n".join(lines)


def generate_ideas_llm(topic: str, keywords: list[str] | None = None,
                       api_key: str | None = None,
                       base_url: str | None = None,
                       model: str | None = None) -> list[dict]:
    """调用 LLM 生成额外选题，返回与本地模板相同结构的列表。无 key 抛错。"""
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                or "https://api.openai.com/v1").rstrip("/")
    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        raise RuntimeError("未设置 OPENAI_API_KEY")
    kw = "、".join(keywords or [])
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是资深内容策划，输出严格的 JSON 数组，不要解释。"},
            {"role": "user", "content": (
                f"围绕主题「{topic}」，关键词「{kw}」，给出 5 个博客选题。"
                f"输出 JSON 数组，每个元素含 title(字符串)、angle(字符串)、angle_desc(字符串)。")},
        ],
        "temperature": 0.8,
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"].strip().strip("`")
    if content.startswith("json"):
        content = content[4:].strip()
    parsed = json.loads(content)
    out = []
    for item in parsed:
        out.append({
            "angle_key": "llm",
            "angle": item.get("angle", "LLM 灵感"),
            "title": item.get("title", ""),
            "angle_desc": item.get("angle_desc", ""),
            "suggested_keywords": [topic] + (keywords or []),
        })
    return out


def ideas(topic: str, keywords: list[str] | None = None,
          use_llm: bool = False) -> list[dict]:
    """统一入口：本地模板 +（可选）LLM 追加。"""
    base = generate_ideas(topic, keywords)
    if use_llm and os.environ.get("OPENAI_API_KEY"):
        try:
            return base + generate_ideas_llm(topic, keywords)
        except Exception as exc:
            print(f"[warn] LLM 选题失败，仅使用本地模板：{exc}")
    return base
