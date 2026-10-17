#!/usr/bin/env python3
"""Behavior and negative tests for the delivered bound_check.py."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).with_name('bound_check.py')
spec = importlib.util.spec_from_file_location('bound_check', SOURCE)
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

class BoundTests(unittest.TestCase):
    def test_partition_enumeration(self):
        for n, bell in enumerate((1, 2, 5, 15), 1):
            parts = list(bc.partitions(n))
            self.assertEqual(len(parts), bell)
            self.assertEqual(len(set(parts)), bell)

    def test_integer_bound(self):
        self.assertEqual([bc.state_bound(n) for n in range(1, 9)],
                         [0,0,0,1,1,2,3,4])
        with self.assertRaises(ValueError):
            bc.state_bound(0)

    def test_wrong_cycles_rejected(self):
        for n, labels, expected in (
            (5, (0,0,1,1,1), 1),
            (7, (0,0,0,0,1,1,1), 3),
            (8, (0,0,0,0,1,1,1,1), 4),
        ):
            T = tuple((i+1) % n for i in range(n))
            with self.assertRaises(RuntimeError):
                bc.check_witness(T, labels, expected)

    def test_full_partition_not_single_marker(self):
        T = (0,0,0,1,1)
        full = bc.evaluate(T, (0,1,0,0,2))
        collapsed = bc.evaluate(T, (0,1,0,0,1))
        self.assertEqual((full['m'],full['r'],full['gap']), (4,4,0))
        self.assertEqual((collapsed['m'],collapsed['r'],collapsed['gap']), (4,3,1))

    def test_incomplete_enumeration_rejected(self):
        for n in range(1, 5):
            with self.assertRaises(RuntimeError):
                bc.require_count(n, bc.EXPECTED_COUNTS[n]-1)

    def test_malformed_system_rejected(self):
        for T, labels in (((),()), ((2,0),(0,1)), ((0,),(0,1)),
                          ((0,1),(0,2)), ((0,1),(0,-1))):
            with self.assertRaises(ValueError):
                bc.evaluate(T, labels)

    def test_corrupted_rank_rejected(self):
        with patch.object(bc, 'rank_q', return_value=1):
            with self.assertRaises(RuntimeError):
                bc.evaluate((0,1), (0,1))

    def test_corrupted_stable_size_rejected(self):
        with patch.object(bc, 'stable_size', return_value=99):
            with self.assertRaises(RuntimeError):
                bc.evaluate((0,), (0,))

    def test_missing_required_argument(self):
        p = subprocess.run([sys.executable,str(SOURCE)], capture_output=True)
        self.assertNotEqual(p.returncode,0)

    def test_existing_receipt_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'receipt.json'
            path.write_text('do not overwrite')
            p = subprocess.run([sys.executable,str(SOURCE),'--receipt',str(path)],
                               capture_output=True)
            self.assertNotEqual(p.returncode,0)
            self.assertEqual(path.read_text(),'do not overwrite')

    def test_full_cli_and_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'receipt.json'
            p = subprocess.run([sys.executable,str(SOURCE),'--receipt',str(path)],
                               capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr)
            data = json.loads(path.read_text())
            self.assertEqual(data['status'],'PASS')
            self.assertEqual(data['total_exhaustive_pairs'],3984)
            self.assertEqual([x['pairs'] for x in data['exhaustive']],[1,8,135,3840])
            self.assertEqual([x['gap'] for x in data['witnesses']],[1,2,3,4])
            self.assertEqual(data['source_sha256'],hashlib.sha256(SOURCE.read_bytes()).hexdigest())

if __name__ == '__main__':
    unittest.main(verbosity=2)
