import unittest

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


def contains_key(value, key):
    if isinstance(value, dict):
        return key in value or any(contains_key(item, key) for item in value.values())
    if isinstance(value, list):
        return any(contains_key(item, key) for item in value)
    return False


class ProspectDataBoundaryTest(unittest.TestCase):
    def test_tools_exclude_billing_qualification_for_every_prospect(self):
        for prospect_id in data_service.PROSPECTS:
            get_result = get_prospect.invoke({"prospect_id": prospect_id})
            profile_result = build_prospect_profile.invoke({"prospect_id": prospect_id})

            self.assertFalse(contains_key(get_result, "billing_qualification"))
            self.assertFalse(contains_key(profile_result, "billing_qualification"))


if __name__ == "__main__":
    unittest.main()
