import os
import unittest
from types import SimpleNamespace

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent.gtm_agent import send_prospect_email
from gtm_agent.gtm_records import PROSPECTS


class SendProspectEmailTest(unittest.TestCase):
    def setUp(self):
        self.runtime = SimpleNamespace(config={})
        self.from_rep = {"email": "rep@example.com", "name": "Test Rep"}

    def test_disqualified_prospects_are_blocked_without_message_id(self):
        for prospect_id in ("LEAD-50001", "LEAD-50002", "LEAD-50003", "LEAD-50004", "LEAD-50005"):
            result = send_prospect_email.func(
                prospect={"prospect_id": prospect_id, "email": PROSPECTS[prospect_id]["email"]},
                subject="Follow-up",
                body="Hello",
                runtime=self.runtime,
                from_rep=self.from_rep,
            )

            self.assertEqual(
                result,
                {
                    "status": "blocked",
                    "reason": "prospect is disqualified",
                    "prospect_id": prospect_id,
                },
            )
            self.assertNotIn("message_id", result)

    def test_qualified_prospects_are_sent(self):
        for prospect_id, prospect in PROSPECTS.items():
            if prospect["disqualified"]:
                continue

            result = send_prospect_email.func(
                prospect={"prospect_id": prospect_id, "email": prospect["email"]},
                subject="Follow-up",
                body="Hello",
                runtime=self.runtime,
                from_rep=self.from_rep,
            )

            self.assertEqual(result["status"], "sent")
            self.assertIn("message_id", result)


if __name__ == "__main__":
    unittest.main()
