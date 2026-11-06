# SPDX-License-Identifier: GPL-3.0
import json
from pathlib import Path
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = runpy.run_path(str(ROOT / 'product' / 'roboparty-product'))


class ProductTests(unittest.TestCase):
    def test_explicit_profile_validates_against_board(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'robots' / 'rpo').mkdir(parents=True)
            (root / 'robots' / 'rpo' / 'robot.yaml').write_text('robot:\n  type: rpo\n')
            data = {'schema': 1, 'product': 'rpo', 'profile': 'rpo', 'dof': 23}
            info = PRODUCT['validate'](data, root / 'robots', board='rdkx5')
            self.assertEqual(info['profile'], 'rpo')
            self.assertEqual(info['dof'], 23)

    def test_board_product_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'robots' / 'rp1').mkdir(parents=True)
            (root / 'robots' / 'rp1' / 'robot.yaml').write_text('robot:\n  type: rp1\n')
            data = {'schema': 1, 'product': 'rp1', 'profile': 'rp1', 'dof': 28}
            with self.assertRaises(ValueError):
                PRODUCT['validate'](data, root / 'robots', board='rdkx5')

    def test_auto_uses_board_mapping(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'robots' / 'rpo').mkdir(parents=True)
            (root / 'robots' / 'rpo' / 'robot.yaml').write_text('robot:\n  type: rpo\n')
            data = {'schema': 1, 'product': 'auto', 'profile': 'auto'}
            info = PRODUCT['validate'](data, root / 'robots', board='rdkx5')
            self.assertEqual(info['profile'], 'rpo')


if __name__ == '__main__':
    unittest.main()
