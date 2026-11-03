"""Automated static checks and linting for Antigravity Global Rules.

Run with:
    python -m unittest discover tests
    or
    python tests/test_rules.py
"""

from pathlib import Path
import re
import unittest

RULES_DIR = Path(__file__).resolve().parent.parent

# Core rules that must always be present in the repository
REQUIRED_RULES = [
    "executable_documentation.md",
    "modernization_rules.md",
    "python_decrufting.md",
    "security_and_standards.md",
]

# Hard ceilings for token economy and prompt efficiency
MAX_LINES_PER_RULE = 120
MAX_ESTIMATED_TOKENS_PER_RULE = 2000
MAX_TOTAL_ESTIMATED_TOKENS = 4000


class TestAntigravityRules(unittest.TestCase):
    """Test suite for validating Antigravity global rules consistency and hygiene."""

    @classmethod
    def setUpClass(cls):
        cls.rule_files = [
            f for f in RULES_DIR.glob("*.md")
            if f.is_file() and not f.name.startswith(".")
        ]
        cls.rule_map = {f.name: f.read_text(encoding="utf-8") for f in cls.rule_files}

    def test_required_rules_exist(self):
        """Verify that all foundational rule files exist in the rules directory."""
        found_names = set(self.rule_map.keys())
        for req in REQUIRED_RULES:
            self.assertIn(
                req,
                found_names,
                f"Missing required global rule file: {req}",
            )

    def test_no_unauthorized_markdown_in_rules_root(self):
        """Ensure no loose markdown files in rules root that Antigravity would inject into prompts."""
        root_md_files = {
            f.name for f in RULES_DIR.glob("*.md")
            if f.is_file() and not f.name.startswith(".")
        }
        self.assertEqual(
            root_md_files,
            set(REQUIRED_RULES),
            f"Unauthorized markdown files found in rules root: {root_md_files - set(REQUIRED_RULES)}",
        )

    def test_yaml_frontmatter(self):
        """Verify every rule has valid frontmatter with description and recognized trigger."""
        frontmatter_pattern = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
        valid_trigger_prefixes = ("always_on", "model_decision", "glob", "manual")
        for name, content in self.rule_map.items():
            match = frontmatter_pattern.match(content)
            self.assertIsNotNone(
                match,
                f"{name}: Missing or malformed YAML frontmatter (must start with '---')",
            )
            body = match.group(1)
            self.assertIn(
                "description:",
                body,
                f"{name}: Frontmatter missing 'description' field",
            )
            trigger_match = re.search(r"^trigger:\s*([^\r\n]+)", body, re.MULTILINE)
            self.assertIsNotNone(
                trigger_match,
                f"{name}: Frontmatter missing 'trigger' field",
            )
            trigger_val = trigger_match.group(1).strip()
            self.assertTrue(
                any(trigger_val.startswith(prefix) for prefix in valid_trigger_prefixes),
                f"{name}: Invalid trigger value '{trigger_val}' (must start with one of {valid_trigger_prefixes})",
            )

    def test_no_hardcoded_machine_paths(self):
        """Enforce zero hardcoded local machine paths or file:/// URIs in rules."""
        forbidden_patterns = [
            (re.compile(r"file:///[a-zA-Z]:", re.IGNORECASE), "Windows local file:/// URI"),
            (re.compile(r"file:///(?:Users|home)/", re.IGNORECASE), "POSIX local file:/// URI"),
            (re.compile(r"[a-zA-Z]:\\(?:Users|home)\\", re.IGNORECASE), "hardcoded Windows user path"),
            (re.compile(r"/(?:Users|home)/[a-zA-Z0-9_-]+/", re.IGNORECASE), "hardcoded POSIX home path"),
        ]
        for name, content in self.rule_map.items():
            for pattern, desc in forbidden_patterns:
                matches = pattern.findall(content)
                self.assertEqual(
                    len(matches),
                    0,
                    f"{name}: Contains forbidden {desc}: {matches}",
                )

    def test_token_and_line_budgets(self):
        """Enforce quantitative modularity and token ceilings on rule files."""
        total_tokens = 0
        for name, content in self.rule_map.items():
            lines = content.splitlines()
            line_count = len(lines)
            est_tokens = int(len(content) / 3.7)
            total_tokens += est_tokens

            self.assertLessEqual(
                line_count,
                MAX_LINES_PER_RULE,
                f"{name}: Exceeds line ceiling ({line_count} > {MAX_LINES_PER_RULE})",
            )
            self.assertLessEqual(
                est_tokens,
                MAX_ESTIMATED_TOKENS_PER_RULE,
                f"{name}: Exceeds estimated token ceiling ({est_tokens} > {MAX_ESTIMATED_TOKENS_PER_RULE})",
            )

        self.assertLessEqual(
            total_tokens,
            MAX_TOTAL_ESTIMATED_TOKENS,
            f"Total global rules overhead exceeds budget ({total_tokens} > {MAX_TOTAL_ESTIMATED_TOKENS})",
        )

    def test_executable_documentation_contract(self):
        """Validate core contractual clauses in executable_documentation.md."""
        content = self.rule_map.get("executable_documentation.md", "")
        self.assertIn("Scenario Combinations Matrix", content)
        self.assertIn("Pre-Run Verification One-Liners", content)
        self.assertRegex(content, r"\|\s*Scenario\s*/\s*Objective\s*\|")

    def test_modernization_rules_contract(self):
        """Validate core contractual clauses in modernization_rules.md."""
        content = self.rule_map.get("modernization_rules.md", "")
        self.assertIn("MIGRATION_LOG.md", content)
        self.assertIn("Pre-Commit Staging Audit Gate", content)
        self.assertIn("Comment & Reference Preservation", content)
        self.assertIn("POSIX Paths", content)

    def test_python_decrufting_contract(self):
        """Validate core contractual clauses in python_decrufting.md."""
        content = self.rule_map.get("python_decrufting.md", "")
        self.assertIn("__future__", content)
        self.assertIn("six", content)
        self.assertIn("past.builtins", content)
        self.assertIn("Preserve Domain Comments & Algorithms", content)

    def test_security_and_standards_contract(self):
        """Validate core contractual clauses in security_and_standards.md."""
        content = self.rule_map.get("security_and_standards.md", "")
        self.assertIn("Zero-Hardcoded Infrastructure", content)
        self.assertIn("SQL & Query Injection", content)
        self.assertIn("!important", content)
        self.assertIn("Quantitative Modularity Budgets", content)
        self.assertRegex(content, r"\|\s*\*\*Source File\*\*\s*\|")


if __name__ == "__main__":
    unittest.main()
