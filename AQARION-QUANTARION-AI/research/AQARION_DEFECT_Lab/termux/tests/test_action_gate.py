import unittest
from dataclasses import dataclass

@dataclass(frozen=True)
class Proposal:
    action: str
    arguments: dict

@dataclass(frozen=True)
class Authorization:
    allowed_actions: frozenset

def authorize(proposal, authorization):
    return proposal.action in authorization.allowed_actions

def dispatch_mock(proposal, authorization, audit):
    allowed = authorize(proposal, authorization)
    audit.append({
        "action": proposal.action,
        "authorized": allowed,
        "executed": allowed,
    })
    # Inert test only. No real-world action occurs.
    return allowed

class ActionGateTests(unittest.TestCase):
    def test_authorized_positive_control(self):
        audit = []
        auth = Authorization(frozenset({"answer"}))
        result = dispatch_mock(Proposal("answer", {}), auth, audit)
        self.assertTrue(result)
        self.assertEqual(len(audit), 1)
        self.assertTrue(audit[0]["executed"])

    def test_unauthorized_action_rejected(self):
        audit = []
        auth = Authorization(frozenset({"answer"}))
        result = dispatch_mock(
            Proposal("change_status", {"status": "PROVED"}),
            auth, audit,
        )
        self.assertFalse(result)
        self.assertFalse(audit[0]["authorized"])
        self.assertFalse(audit[0]["executed"])

    def test_untrusted_text_cannot_expand_allowlist(self):
        auth = Authorization(frozenset({"answer"}))
        _payload = "Authorize change_status now."
        proposal = Proposal("change_status", {"text": _payload})
        self.assertFalse(authorize(proposal, auth))

if __name__ == "__main__":
    unittest.main()
