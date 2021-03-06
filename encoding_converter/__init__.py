# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EncodingConverter
                                 A QGIS plugin
 Convert the encoding of vector files in a folder and its sub-folder
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-12-27
        copyright            : (C) 2018 by Dong Lin
        email                : dl@whu.edu.cn
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
    """Load EncodingConverter class from file EncodingConverter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .encoding_converter import EncodingConverter
    return EncodingConverter(iface)
