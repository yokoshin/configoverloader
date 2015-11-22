import unittest
import os
import configoverload as cfgol


class TestConfigOverload(unittest.TestCase):
    example_base_dir = os.path.join('.', 'data')
    example_a_path = os.path.join(example_base_dir, 'example_a.ini')
    example_a_fp = open(example_a_path, 'r')
    example_b_path = os.path.join(example_base_dir, 'example_b.ini')

    def setUp(self):
        cfgol.register_default_context({"env": None, "role": None, "node": None})

    def make_example_a_path(self, env=None, role=None, node=None):
        if env:
            return os.path.join(self.example_base_dir, 'env', env, 'example_a.ini')
        if role:
            return os.path.join(self.example_base_dir, 'role', role, 'example_a.ini')
        if node:
            return os.path.join(self.example_base_dir, 'node', node, 'example_a.ini')

    def test_no_context_globfp(self):
        cfgol.register_default_context({"env": None, "role": None, "node": None})
        ls = cfgol.globfp(self.example_a_fp)
        self.assertEqual(0, len(ls))

    def test_no_context_glob(self):
        cfgol.register_default_context({"env": None, "role": None, "node": None})
        ls = cfgol.glob(self.example_a_path)
        self.assertEqual(1, len(ls))

    def test_with_env_globfp(self):
        cfgol.register_default_context({"env": env_detector, "role": None, "node": None})
        ls = cfgol.globfp(self.example_a_fp)
        self.assertListEqual([self.make_example_a_path(env='env_a')], ls)

        ls = cfgol.globfp(self.example_a_fp, env='env_b')
        self.assertListEqual([], ls)

    def test_with_env_glob(self):
        cfgol.register_default_context({"env": env_detector, "role": None, "node": None})
        ls = cfgol.glob(self.example_a_path)
        self.assertListEqual([self.example_a_path, self.make_example_a_path(env='env_a')], ls)

        ls = cfgol.glob(self.example_a_path, env='env_b')
        self.assertEqual([self.example_a_path], ls)

    def test_with_role_globfp(self):

        cfgol.register_default_context({"env": None, "role": role_detector, "node": None})
        ls = cfgol.globfp(self.example_a_fp)
        self.assertListEqual([self.make_example_a_path(role='role_a')], ls)

        ls = cfgol.globfp(self.example_a_fp, role='role_b')
        self.assertListEqual([], ls)

    def test_with_role_glob(self):
        cfgol.register_default_context({"env": None, "role": role_detector, "node": None})
        ls = cfgol.glob(self.example_a_path)
        self.assertListEqual([self.example_a_path, self.make_example_a_path(role='role_a')], ls)

        ls = cfgol.glob(self.example_a_path, role='role_b')
        self.assertListEqual([self.example_a_path], ls)

    def test_with_node_globfp(self):
        cfgol.register_default_context({"env": None, "role": None, "node": node_detector})

        ls = cfgol.globfp(self.example_a_fp)
        self.assertListEqual([self.make_example_a_path(node='node_a')], ls)

        ls = cfgol.globfp(self.example_a_fp, node='node_b')
        self.assertEqual(0, len(ls))

    def test_with_node_glob(self):

        cfgol.register_default_context({"env": None, "role": None, "node": node_detector})
        ls = cfgol.glob(self.example_a_path)
        self.assertListEqual([self.example_a_path, self.make_example_a_path(node='node_a')], ls)

        ls = cfgol.glob(self.example_a_path, node='node_b')
        self.assertListEqual([self.example_a_path], ls)

    def test_combination_of_node_env_role(self):
        cfgol.register_default_context({"env": env_detector, "role": role_detector, "node": node_detector})

        ls = cfgol.glob(self.example_a_path)

        self.assertListEqual([self.example_a_path,
                              self.make_example_a_path(env='env_a'),
                              self.make_example_a_path(role='role_a'),
                              self.make_example_a_path(node='node_a'),
                              ],
                             ls)

    def test_multi_roles(self):
        cfgol.register_default_context({"env": env_detector, "role": multi_role_detector, "node": node_detector})

        ls = cfgol.glob(self.example_a_path)

        self.assertListEqual([self.example_a_path,
                              self.make_example_a_path(env='env_a'),
                              self.make_example_a_path(role='role_a'),
                              self.make_example_a_path(role='role_c'),
                              self.make_example_a_path(node='node_a'),
                              ],
                             ls)

    def test_multiple_files(self):
        cfgol.register_default_context({"env": env_detector, "role": role_detector, "node": node_detector})

        ls = cfgol.glob([self.example_a_path, self.example_b_path])

        self.assertListEqual([self.example_a_path,
                              self.make_example_a_path(env='env_a'),
                              self.make_example_a_path(role='role_a'),
                              self.make_example_a_path(node='node_a'),
                              self.example_b_path,
                              ],
                             ls)


def env_detector():
    return 'env_a'


def node_detector():
    return 'node_a'


def role_detector():
    return 'role_a'


def multi_role_detector():
    return ['role_a', 'role_c']
