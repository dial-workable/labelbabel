from labelbabel import __version__

import unittest

class DefaultTestCase(unittest.TestCase):
    def test_version(self) -> None:
        assert __version__ == '0.1.0'
