import unittest

from blog_idea_gen import (ANGLES, generate_ideas, ideas, render_markdown)


class TestGenerate(unittest.TestCase):
    def test_count_matches_angles(self):
        result = generate_ideas("Python 异步编程")
        self.assertEqual(len(result), len(ANGLES))

    def test_title_contains_topic(self):
        result = generate_ideas("Rust")
        for idea in result:
            self.assertIn("Rust", idea["title"])

    def test_keywords_included(self):
        result = generate_ideas("Rust", ["所有权", "生命周期"])
        kws = result[0]["suggested_keywords"]
        self.assertIn("所有权", kws)
        self.assertIn("生命周期", kws)

    def test_empty_topic_raises(self):
        with self.assertRaises(ValueError):
            generate_ideas("   ")

    def test_each_idea_has_fields(self):
        result = generate_ideas("Go")
        for idea in result:
            for f in ("angle_key", "angle", "title", "angle_desc", "suggested_keywords"):
                self.assertIn(f, idea)


class TestRender(unittest.TestCase):
    def test_markdown(self):
        ideas_list = generate_ideas("K8s")
        md = render_markdown("K8s", ideas_list)
        self.assertIn("# 博客选题清单：K8s", md)
        self.assertIn("## 1.", md)

    def test_ideas_no_llm_returns_template(self):
        result = ideas("Go", use_llm=False)
        self.assertEqual(len(result), len(ANGLES))


if __name__ == "__main__":
    unittest.main()
