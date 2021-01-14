# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoKKP
                                 A QGIS plugin
 This plugin ports GeoKKP for National Land Agency of Indonesia
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-12-24
        copyright            : (C) 2020 by Dany Laksono
        email                : danylaksono@ugm.ac.id
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GeoKKP class from file GeoKKP.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geokkp import GeoKKP
    return GeoKKP(iface)