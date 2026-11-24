import csv
import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_references as client


class ReferenceChecker(unittest.TestCase):
    def test_batch_with_failure_and_rate_limit(self):
        payload = {"results": [
            {"id": "123", "effective_tier": "C", "source": {"title": "=Test title"},
             "verifiability": "verified",
             "dimension_signals": [{"name": "Species applicability", "detail": "Study in dogs"}]},
            {"id": "PMC456", "error": "rate limited"},
        ], "notes": ["Limit reached"]}
        out, err = io.StringIO(), io.StringIO()
        with patch.object(client, "urlopen", return_value=io.BytesIO(json.dumps(payload).encode())) as post:
            with redirect_stdout(out), redirect_stderr(err):
                status = client.main(["123", "PMC456", "10.1234/a+b"])
        request = post.call_args.args[0]
        self.assertEqual(request.full_url, "https://vetevidence.com/vecs/batch")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(json.loads(request.data), {"ids": ["123", "PMC456", "10.1234/a+b"]})
        rows = list(csv.DictReader(io.StringIO(out.getvalue()), delimiter="\t"))
        self.assertEqual(rows[0]["VECS tier"], "III")
        self.assertEqual(rows[0]["Title"], "'=Test title")
        self.assertEqual(rows[0]["Species applicability"], "Study in dogs")
        self.assertEqual(rows[1]["Status"], "rate limited")
        self.assertEqual(rows[2]["Status"], "No result returned")
        self.assertEqual(rows[2]["VetEvidence"], "https://vetevidence.com/?doi=10.1234%2Fa%2Bb")
        self.assertIn("Limit reached", err.getvalue())
        self.assertEqual(status, 1)

    def test_retracted_source_has_no_usable_tier(self):
        out = io.StringIO()
        result = client.summarize(["123"], {"results": [{"id": "123", "effective_tier": None,
                                   "verifiability": "retracted"}]})
        status = client.report(result, out, io.StringIO())
        self.assertIn("—\tretracted", out.getvalue())
        self.assertIn("No usable tier", out.getvalue())
        self.assertEqual(status, 0)

    def test_invalid_input_never_posts(self):
        for args in [["text about a patient"], ["123"] * 16]:
            with self.subTest(args=args), patch.object(client, "assess") as post:
                with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
                    client.main(args)
                post.assert_not_called()


    def test_existing_tool_names_still_resolve(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "integrations/hermes"))
        import vetclaw_hermes as hermes
        for current, previous, args in [
            ("list_veterinary_skills", "list_vetclaw_skills", {"category": "literature"}),
            ("get_veterinary_skill", "get_vetclaw_skill", {"name": "evidence-grading"}),
        ]:
            result = hermes.dispatch(current, args)
            self.assertTrue(result)
            self.assertNotIn("error", result)
            self.assertEqual(result, hermes.dispatch(previous, args))

    def test_hermes_discovery_and_dispatch(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "integrations/hermes"))
        import vetclaw_hermes as hermes
        name = "check_veterinary_references"
        self.assertIn(name, [t["function"]["name"] for t in hermes.tool_schemas()])
        with patch.object(client, "assess", return_value={"results": [{"id": "123", "effective_tier": "D"}]}):
            result = hermes.dispatch(name, {"identifiers": ["123"]})
        self.assertEqual(result["results"][0]["tier"], "IV")
        self.assertIn("error", hermes.dispatch(name, {"identifiers": ["patient details"]}))
