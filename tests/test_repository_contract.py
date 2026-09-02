import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_manifest_bootstrap_files_exist(self):
        manifest = json.loads((ROOT / "PROCESS_MANIFEST.json").read_text())
        self.assertEqual(manifest["name"], "hermes-zernio")
        for relpath in manifest["bootstrap_order"]:
            self.assertTrue((ROOT / relpath).exists(), relpath)

    def test_skill_has_safety_and_idempotency_guards(self):
        skill = (ROOT / "skills/integrations/zernio-operations/SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\n"))
        for term in ["aprovação explícita", "x-request-id", "409", "releia", "Nunca"]:
            self.assertIn(term, skill)

    def test_inventory_is_read_only_and_sanitizes_webhooks(self):
        script = (ROOT / "skills/integrations/zernio-operations/scripts/inventory_zernio.py").read_text()
        self.assertNotIn("POST", script)
        self.assertNotIn("PATCH", script)
        self.assertNotIn("DELETE", script)
        self.assertNotIn('"url": x.get', script)
        self.assertIn('"Authorization": f"Bearer {key}"', script)


if __name__ == "__main__":
    unittest.main()
