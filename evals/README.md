# Community review cases

Each synthetic prompt in [cases.json](cases.json) tests one behavior that a clinician or developer can observe. To evaluate an assistant, run each prompt in a fresh session. Record the model, skill revision, date, answer, and a pass or fail for each expected behavior. Review clinical responses with a veterinarian. These examples cover a few failure modes and cannot establish clinical performance.

To contribute a case, add an entry with a stable ID, a fictional prompt, observable expectations, and a supporting source. Link a primary reference or applicable label for a clinical claim. The optional `demo` field runs the specified lookup against the browser demo in CI. For reviewed demo warnings, edit the cited Markdown matrix and run `python3 scripts/sync_safety_warnings.py`.

Run the citation client tests with `python3 -m unittest discover -s evals -p test_references.py`. To exercise the demo, install Python Playwright, run `python3 -m playwright install chromium`, then `python3 -m unittest discover -s evals -p test_demo.py`.
