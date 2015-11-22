import unittest
from configoverload.configloverloader import default_node_detector


class TestDefaultNodeDetector(unittest.TestCase):
    def test_default_detector(self):
        a = default_node_detector()
        # the result depends on network
        # print(a)
