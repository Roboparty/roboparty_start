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
            self.assertFalse(info['capabilities']['bms'])
            self.assertFalse(info['capabilities']['camera'])

    def test_board_product_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'robots' / 'rp1').mkdir(parents=True)
            (root / 'robots' / 'rp1' / 'robot.yaml').write_text('robot:\n  type: rp1\n')
            data = {'schema': 1, 'product': 'rp1', 'profile': 'rp1', 'dof': 28}
            with self.assertRaises(ValueError):
                PRODUCT['validate'](data, root / 'robots', board='rdkx5')

    def test_explicit_capabilities_override_defaults(self):
        data = {'schema': 1, 'product': 'rpo', 'profile': 'rpo',
                'capabilities': {'bms': True, 'camera': False}}
        info = PRODUCT['resolve'](data, board='rdkx5')
        self.assertTrue(info['capabilities']['bms'])
        self.assertFalse(info['capabilities']['camera'])
        with self.assertRaisesRegex(ValueError, 'unknown capabilities'):
            PRODUCT['resolve']({**data, 'capabilities': {'typo': True}}, board='rdkx5')
        with self.assertRaisesRegex(ValueError, 'booleans'):
            PRODUCT['resolve']({**data, 'capabilities': {'bms': 'yes'}}, board='rdkx5')

    def test_packages_follow_capabilities(self):
        packages = PRODUCT['CAPABILITY_PACKAGES']
        rpo = PRODUCT['resolve']({'schema': 1, 'product': 'rpo', 'profile': 'rpo'},
                                 board='rdkx5')
        self.assertEqual([packages[name] for name, enabled
                          in rpo['capabilities'].items() if enabled and name in packages], [])
        rp1 = PRODUCT['resolve']({'schema': 1, 'product': 'rp1', 'profile': 'rp1'},
                                 board='robopi2')
        enabled = {packages[name] for name, value in rp1['capabilities'].items()
                   if value and name in packages}
        self.assertTrue({'roboparty-bms', 'roboparty-camera', 'robopi-addon',
                         'roboparty-imu', 'roboparty-analyze', 'roboparty-motors',
                         'adbd'} <= enabled)
        self.assertNotIn('roboparty-rp-head', enabled)
        self.assertNotIn('roboparty-dexhand', enabled)
        self.assertNotIn('roboparty-lidar', enabled)

    def test_auto_uses_board_mapping(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'robots' / 'rpo').mkdir(parents=True)
            (root / 'robots' / 'rpo' / 'robot.yaml').write_text('robot:\n  type: rpo\n')
            data = {'schema': 1, 'product': 'auto', 'profile': 'auto'}
            info = PRODUCT['validate'](data, root / 'robots', board='rdkx5')
            self.assertEqual(info['profile'], 'rpo')
            self.assertFalse(info['capabilities']['bms'])

    def test_auto_x86_64_uses_sim(self):
        info = PRODUCT['resolve']({'schema': 1, 'product': 'auto', 'profile': 'auto'},
                                  board='x86_64')
        self.assertEqual(info['product'], 'rpo-sim')
        self.assertEqual(info['profile'], 'rpo-sim')

    def test_sim_profile_validates_without_robot_yaml(self):
        info = PRODUCT['validate'](
            {'schema': 1, 'product': 'rpo-sim', 'profile': 'rpo-sim'},
            robots_dir='/nonexistent', board='x86_64')
        self.assertEqual(info['profile'], 'rpo-sim')


if __name__ == '__main__':
    unittest.main()
