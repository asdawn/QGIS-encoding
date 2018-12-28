# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EncodingConverterDialog
                                 A QGIS plugin
 Convert the encoding of vector files in a folder and its sub-folder
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-12-27
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Dong Lin
        email                : dl@whu.edu.cn
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from qgis.gui import QgsFileWidget

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'encoding_converter_dialog_base.ui'))


class EncodingConverterDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(EncodingConverterDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.format.addItem("ESRI Shape file (*.shp)")
        self.format.addItem("MapInfo Mif file (*.mif)")
        self.folderIn.setStorageMode(QgsFileWidget.GetDirectory)
        self.folderOut.setStorageMode(QgsFileWidget.GetDirectory)
