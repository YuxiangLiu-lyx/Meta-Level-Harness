import json
from pathlib import Path
import tempfile
import unittest
from harness_lab.backend import digest, summarize, retryable_infrastructure
from harness_lab.protocol import generation_input, create_freeze, check_freeze, paired_counts, validate_harness
from harness_lab.verifier import semantic_outcome


class Invariants(unittest.TestCase):
    def test_retry_is_limited_to_missing_response_transport_failures(self):
        self.assertTrue(retryable_infrastructure({"status":"TIMEOUT","final_response":None}))
        for value in [{"status":"TIMEOUT","final_response":"answer"}, {"status":"USAGE_LIMIT"}, {"status":"COMPLETED"}, {"status":"PROTOCOL_VIOLATION"}, {"status":"INFRA_FAILURE","errors":["401 authentication connection failure"]}]:
            self.assertFalse(retryable_infrastructure(value))

    def test_input_integrity_and_answer_isolation(self):
        h = json.loads(Path("configs/manual.json").read_text())
        scenario = {"requirements": "Complete requirement\nsecond line", "schema": "entity User;\n", "reference": "SECRET", "verification_plan": "SECRET"}
        value = json.loads(generation_input(scenario, h, "PUBLIC"))
        self.assertEqual(value["requirements"], scenario["requirements"])
        self.assertEqual(value["schema"], scenario["schema"])
        self.assertNotIn("SECRET", json.dumps(value))
        h["input_order"] = ["schema", "schema", "requirements"]
        with self.assertRaises(ValueError): validate_harness(h)

    def test_unknown_never_becomes_liveness_success(self):
        for run in [{"returncode": 0, "timeout": False, "stdout": "unknown"},
                    {"returncode": 1, "timeout": False, "stdout": ": DOES NOT HOLD\nCounterexample found:"},
                    {"returncode": -9, "timeout": True, "stdout": ""}]:
            self.assertEqual(semantic_outcome(run, inverse=True), "UNRESOLVED")

    def test_proved_counterexample_and_inversion(self):
        run = {"returncode": 0, "timeout": False, "stdout": "Property: DOES NOT HOLD\nCounterexample found:"}
        self.assertEqual(semantic_outcome(run), "FAIL")
        self.assertEqual(semantic_outcome(run, True), "PASS")

    def test_cache_identity(self):
        a = {"task": "one", "protocol": "v1", "model": "fixed", "harness": "a", "input": "b"}
        for key in a:
            self.assertNotEqual(digest(a), digest({**a, key: "changed"}))

    def test_freeze_detects_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, frozen = Path(tmp)/"input", Path(tmp)/"freeze.json"
            source.write_text("original")
            create_freeze(frozen, [source], {})
            check_freeze(frozen)
            source.write_text("changed")
            with self.assertRaises(RuntimeError): check_freeze(frozen)

    def test_pair_statistics(self):
        got = paired_counts(dict(a="PASS", b="PASS", c="FAIL", d="FAIL"), dict(a="PASS", b="FAIL", c="PASS", d="FAIL"))
        self.assertEqual(got, dict(both_pass=1, meta_only=1, refine_only=1, both_fail=1, difference_percentage_points=0))

    def test_warning_is_not_tool_use(self):
        events = [{"type":"item.completed", "item":{"type":"error", "message":"warning"}}, {"type":"turn.completed", "usage":{}}]
        self.assertEqual(summarize(events,0)["tool_events"],0)
        events.append({"type":"item.completed", "item":{"type":"command_execution"}})
        self.assertEqual(summarize(events,0)["status"],"PROTOCOL_VIOLATION")


if __name__ == "__main__": unittest.main()
