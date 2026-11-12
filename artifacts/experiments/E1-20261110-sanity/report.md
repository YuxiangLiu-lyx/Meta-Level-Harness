# E1: Verifier sanity check

## Research Question
Does the evaluator accept reference policies and reject clear semantic, syntax, and schema faults?

## Hypothesis
All five reference policies pass; ten semantic mutants and three grammar/schema controls fail at their intended gate.

## Setup and Controlled Variables
First five fixed design20 scenarios. Cedar CLI 4.14.1 experimental build and CVC5 1.4.2, official ARM binaries. Published RAISE verification plans and references are used unchanged. The strict adapter preserves unresolved outcomes instead of treating solver failure as success after liveness inversion. Unsupported check types and empty plans are unresolved. No model calls.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. Completed 18/18 controls.

## Results
References: 5/5 pass. Semantic faults: 10/10 detected, comprising five removed security conditions and five universal-denial mutants. Syntax controls: 2/2 syntax failures. Undeclared-attribute control: 1/1 schema failure. Expectations met: 18/18. Undetected known semantic mutants: 0/10. Unresolved evaluations: 0/18.

## Error Analysis
Removing the document version-lock condition violates ceilings. Removing the wire-approval authority threshold permits an underqualified requester. Denying all requests violates permission floors or liveness. See results.json for each change, expected outcome, actual result, and check-level evidence. An upstream hazard was identified before formal runs: liveness wrappers invert false values even when the underlying solver failed. The local adapter distinguishes VERIFIED, counterexample-backed DOES NOT HOLD, and unresolved process/solver outcomes. It still invokes actual Cedar symbolic analysis; it does not score policy strings by similarity.

## Interpretation
The evaluator detects these ten deliberately clear semantic faults and separates parse/schema errors. It is ready for a small model baseline.

## Limitations
Five scenarios cannot establish soundness or completeness of all benchmark checks. Some published requirements omit relationships required by verification plans; for example the patent scenario's plan restricts examination to the assigned examiner although the natural-language text does not explicitly state assignment. Scores measure published-plan compliance, with possible requirement/reference mismatch. We do not alter data or select easier replacements. Full test remains closed.

## Next Action
Freeze Manual and run five design scenarios, then reuse those outputs when extending to design20.

## Reproduction
`PYTHONPATH=src python3 scripts/sanity.py`. Existing score caches require matching verifier code, binary hashes, policy, and evaluation-material hashes. Raw Cedar command outputs are external and indexed by score.json; mutation policies and expected outcomes are in this experiment directory.
