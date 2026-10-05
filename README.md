# blog-idea-gen

零依赖的**博客选题生成器**：给定一个主题和若干关键词，用一套写作角度模板（入门教程、清单干货、新手避坑、实战复盘、横向对比、观点输出、深度原理、FAQ）自动组合出一批可直接动笔的博客标题与写作角度。可选接入 LLM 追加更多灵感；没有 key 时本地模板已能产出完整清单。

## 功能简介

- 8 种写作角度模板，一键套用到任意主题。
- 每个选题给出：标题、写作角度说明、建议关键词。
- 支持纯文本 / Markdown 两种输出。
- 可选 LLM 追加灵感（OpenAI 兼容接口，仅标准库）。

## 快速开始

```bash
python3 cli.py --topic "Python 异步编程"

python3 cli.py --topic "Rust 入门" --keyword "所有权" --keyword "生命周期" --markdown
```

## 无 API key 如何运行

本项目**默认纯模板运行**，无需任何 key，本地立即生成完整选题清单。
仅当你想让 LLM 额外补充几个非常规角度时，才需要：

```bash
export OPENAI_API_KEY=sk-xxx
python3 cli.py --topic "Python 异步编程" --llm
```

## 目录说明

```
blog-idea-gen/
├── blog_idea_gen.py   # 角度模板 + 选题组合 + 可选 LLM
├── cli.py            # 命令行入口
├── tests/
│   └── test_blog_idea.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
