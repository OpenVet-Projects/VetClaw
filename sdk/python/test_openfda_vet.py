"""
Unit tests for the OpenFDA Veterinary SDK query builder.

These tests inject a fake HTTP session and assert on the request parameters the
client constructs (and how they encode onto the wire). No real network calls are
made.

Run:  python3 -m unittest
"""
from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from urllib.parse import urlencode

from openfda_vet import OpenFDAVet


def _fake_session(payload=None, status=200):
    """Build a fake requests-like session whose .get() returns a canned response."""
    if payload is None:
        payload = {"meta": {"results": {"total": 0}}, "results": []}
    response = MagicMock()
    response.status_code = status
    response.json.return_value = payload
    response.text = ""
    session = MagicMock()
    session.get.return_value = response
    return session


def _captured_params(session):
    """Return the params dict passed to session.get()."""
    session.get.assert_called_once()
    _, kwargs = session.get.call_args
    return kwargs["params"]


def _wire_query(params):
    """Encode params exactly as requests/urllib would put them on the wire."""
    return urlencode(params)


class SearchQueryTests(unittest.TestCase):
    def test_single_filter_search(self):
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.search(species="Dog", limit=5)

        params = _captured_params(session)
        self.assertEqual(params["search"], 'animal.species:"DOG"')
        self.assertNotIn("AND", params["search"])
        self.assertEqual(params["limit"], 5)

    def test_two_filter_search_uses_spaced_and(self):
        # Regression lock for the "+AND+" double-encoding bug: two filters must be
        # joined with a spaced " AND ", never a literal "+AND+".
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.search(species="Dog", drug="Amoxicillin")

        params = _captured_params(session)
        search = params["search"]

        self.assertEqual(search, 'animal.species:"DOG" AND drug.name:"AMOXICILLIN"')
        self.assertIn(" AND ", search)
        self.assertNotIn("+AND+", search)
        self.assertNotIn("%2BAND%2B", search)

        # The wire-encoded form: the space becomes "+", yielding the correct
        # "...+AND+..." and never the broken "%2BAND%2B".
        wire = _wire_query(params)
        self.assertIn("+AND+", wire)
        self.assertNotIn("%2BAND%2B", wire)

    def test_three_filter_search_chains_and(self):
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.search(species="Dog", drug="Ivermectin", reaction="Seizure")

        search = _captured_params(session)["search"]
        self.assertEqual(
            search,
            'animal.species:"DOG" AND drug.name:"IVERMECTIN" '
            'AND reaction.veddra_term_name:"Seizure"',
        )
        self.assertNotIn("+AND+", search)
        self.assertNotIn("%2BAND%2B", _wire_query({"search": search}))

    def test_count_appends_exact(self):
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.count("drug.name", species="Dog")

        params = _captured_params(session)
        self.assertEqual(params["count"], "drug.name.exact")
        self.assertEqual(params["search"], 'animal.species:"DOG"')

    def test_count_exact_can_be_disabled(self):
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.count("drug.name", exact=False)

        self.assertEqual(_captured_params(session)["count"], "drug.name")

    def test_count_does_not_double_append_exact(self):
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.count("drug.name.exact")

        self.assertEqual(_captured_params(session)["count"], "drug.name.exact")

    def test_top_reactions_uses_exact_and_spaced_and(self):
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.top_reactions("Cat", drug="Ivermectin")

        params = _captured_params(session)
        self.assertEqual(params["count"], "reaction.veddra_term_name.exact")
        self.assertIn(" AND ", params["search"])
        self.assertNotIn("%2BAND%2B", params["search"])

    def test_top_breeds_uses_exact(self):
        session = _fake_session()
        client = OpenFDAVet(session=session)
        client.top_breeds("Dog")

        self.assertEqual(
            _captured_params(session)["count"], "animal.breed.breed_component.exact"
        )

    def test_request_does_not_mutate_caller_params(self):
        # _request must copy before injecting api_key, leaving the caller's dict intact.
        session = _fake_session()
        client = OpenFDAVet(api_key="SECRET", session=session)
        original = {"search": 'animal.species:"DOG"', "limit": 5}
        snapshot = dict(original)

        client._request(original)

        self.assertEqual(original, snapshot)
        self.assertNotIn("api_key", original)
        # The request actually sent still carries the api_key (on the copy).
        self.assertEqual(_captured_params(session).get("api_key"), "SECRET")


if __name__ == "__main__":
    unittest.main()
