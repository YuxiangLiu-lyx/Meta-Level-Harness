"""Portable evidence audit; incomplete evidence never implies success.

The pre-export implementation is preserved in the P1 provenance directory and Git.
"""
import argparse
import json
from pathlib import Path
import sys
from review_offline import audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parents[1] /
                        'artifacts/posthoc/P1-20261111-midreport/review_bundle')
    args = parser.parse_args()
    try:
        result = audit(args.package)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        result = {'level2_status': 'INCOMPLETE', 'tool_audit_status': 'UNKNOWN',
                  'observed_tool_events': None, 'error': str(exc)}
    print(json.dumps(result, indent=2))
    return 0 if result['level2_status'] == 'COMPLETE' else 2


if __name__ == '__main__':
    sys.exit(main())
