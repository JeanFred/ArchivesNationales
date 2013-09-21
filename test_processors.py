import unittest
from processors import look_for_sizes_unwrapped


class TestProcessors(unittest.TestCase):

    def test_CommandLineStdOut(self):
        values = [
            ('71,5 x 26 cm', ' {{Size|cm|71.5|26}}'),
            ('63 x 50 cm', ' {{Size|cm|63|50}}'),
            ('26, 4 x 16, 8 x 2 cm', ' {{Size|cm|26.4|16.8|2}}'),
            ('diametre 75 mm', 'diametre {{Size|mm|75}}')
        ]
        for value, expected in values:
            self.assertEqual(look_for_sizes_unwrapped(value), expected)