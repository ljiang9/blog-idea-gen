"""blog-idea-gen 命令行入口。

用法示例：
    python3 cli.py --topic "Python 异步编程"
    python3 cli.py --topic "Rust 入门" --keyword "所有权" --keyword "生命周期"
    python3 cli.py --topic "Python 异步编程" --markdown
"""

from __future__ import annotations

import argparse
import sys

from blog_idea_gen import ideas, render_markdown


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="blog-idea-gen",
        description="按主题/关键词模板组合博客选题与角度清单（可选 LLM）",
    )
    p.add_argument("--topic", required=True, help="博客主题，如 Python 异步编程")
    p.add_argument("--keyword", action="append", default=[], help="关键词，可重复传入")
    p.add_argument("--markdown", action="store_true", help="以 Markdown 形式输出")
    p.add_argument("--llm", action="store_true", help="追加 LLM 灵感（需 OPENAI_API_KEY）")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = ideas(args.topic, args.keyword, use_llm=args.llm)

    if args.markdown:
        print(render_markdown(args.topic, result))
        return 0

    for i, idea in enumerate(result, 1):
        print(f"{i}. [{idea['angle']}] {idea['title']}")
        print(f"   角度：{idea['angle_desc']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
