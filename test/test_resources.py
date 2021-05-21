# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'danylaksono@ugm.ac.id'
__date__ = '2020-12-24'
__copyright__ = 'Copyright 2020, Dany Laksono'

import unittest
from modules.utils import icon

from qgis.PyQt.QtGui import QIcon



class GeoKKPDialogTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        geokkp_icon = icon("icon.png")
        self.assertFalse(geokkp_icon.isNull())

if __name__ == "__main__":
    suite = unittest.makeSuite(GeoKKPResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
