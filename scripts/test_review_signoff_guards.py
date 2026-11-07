#!/usr/bin/env python3
"""Local, non-writing regression tests for independent figure sign-off safeguards."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from write_figure_review_register import validate_review_decisions, build_rows


def verify_rejection(label, row):
    try:
        validate_review_decisions(row)
    except ValueError:
        return
    raise AssertionError(f'Sign-off guard failed to reject: {label}')


def main():
    base = {'diagram_id': 'u1-origin-deuterostome-relationships',
            'scientific_reviewer': '', 'scientific_decision': 'PENDING', 'scientific_notes': '',
            'tamil_reviewer': '', 'tamil_decision': 'PENDING', 'tamil_notes': ''}
    validate_review_decisions(base)
    s1 = dict(base, scientific_decision='ACCEPTED')
    verify_rejection('unattributed acceptance', s1)
    s2 = dict(s1, scientific_reviewer='Biology Reviewer')
    verify_rejection('acceptance without evidence notes', s2)
    s3 = dict(s2, scientific_notes='Compared dorsal anatomical proportions with reference text')
    validate_review_decisions(s3)
    s4 = dict(s3, tamil_decision='ACCEPTED', tamil_reviewer='Biology Reviewer',
              tamil_notes='Checked Tamil terminology against textbook conventions')
    verify_rejection('same reviewer in both disciplines', s4)
    s5 = dict(s4, tamil_reviewer='Tamil Zoology Reviewer')
    validate_review_decisions(s5)
    verify_rejection('unrecognised decision', dict(base, tamil_decision='SIGNED'))
    # Changing the underlying image must revoke BOTH decisions, keeping notes.
    previously_signed = dict(s5, image_sha256='stale-figure-sha256')
    rows = build_rows({base['diagram_id']: previously_signed})
    first = next(row for row in rows if row['diagram_id'] == base['diagram_id'])
    assert first['scientific_decision'] == 'PENDING'
    assert first['tamil_decision'] == 'PENDING'
    assert 're-review required' in first['scientific_notes']
    print('PASS: independent reviewer sign-off rejects false acceptance, missing notes and duplicate reviewers')
    print('PASS: modified illustration revokes prior sign-off while preserving review notes')


if __name__ == '__main__':
    main()
