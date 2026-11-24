import json
import os
import unittest
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class SafetyDemo(unittest.TestCase):
    def test_review_cases(self):
        with sync_playwright() as engine:
            browser = engine.chromium.launch(executable_path=os.getenv("CHROMIUM_PATH"))
            page = browser.new_page()
            page.set_content((ROOT / "demo/safety-checker.html").read_text(encoding="utf-8"))
            cases = json.loads((ROOT / "evals/cases.json").read_text())
            lookups = [case["demo"] for case in cases if "demo" in case]
            lookups.extend([
                {"species": "", "substance": "garlic", "level": "unknown", "text": "select a species"},
                {"species": "horse", "substance": "grapefruit", "level": "unknown", "text": "Substance Not Found"},
                {"species": "horse", "substance": "Onions / Garlic", "level": "caution", "text": "Toxic to horses"},
            ])
            for case in lookups:
                with self.subTest(case=case):
                    page.select_option("#species", case["species"])
                    page.fill("#substance", case["substance"])
                    page.click("button")
                    expect(page.locator("#result")).to_have_class("result " + case["level"])
                    expect(page.locator("#result")).to_contain_text(case["text"])
            browser.close()
