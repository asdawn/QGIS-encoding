# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EncodingConverter
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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5 import QtWidgets
from qgis.core import QgsVectorLayer
from qgis.core import QgsVectorFileWriter
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .encoding_converter_dialog import EncodingConverterDialog
import os.path
import os
import pathlib
import concurrent
from concurrent.futures import ThreadPoolExecutor


class EncodingConverter:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'EncodingConverter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Batch Encoding Converter')

        # Check if plugin was started the first time in current QGIS session
        # Will be set False once it was started
        self.first_start = True
        self.dlg = None


        # setup file format

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EncodingConverter', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/encoding_converter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Convert character encoding'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Batch Encoding Converter'),
                action)
            self.iface.removeToolBarIcon(action)

    def check(self, dlg):
        #check char set
        if dlg.encodingIn.text().strip()=="" or  dlg.encodingOut.text().strip()=="":
            QtWidgets.QMessageBox.information( None, "Invalid parameter", "Please specify the input/output character set." )
            return 0
        #check path
        if dlg.folderIn.filePath().strip()=="" or dlg.folderOut.filePath().strip()=="":
            QtWidgets.QMessageBox.information( None, "Invalid parameter", "Please choose the input/output folder." )
            return 0
        #check the same folder
        if os.path.samefile(dlg.folderIn.filePath().strip(), dlg.folderOut.filePath().strip()):
            QtWidgets.QMessageBox.information( None, "Invalid parameter", "Please choose another folder for output." )
            return 0
        #if everything is okay, now it is a simple check
        return 1

    def convertFile(self, pathIn, pathOut, charsetIn, charsetOut, ogrFormat):
        # the name of layer is not the identifier of layer (tested in python console, QGIS version 3.10 )
        # so we do not have to get a unique name, just use "temp"
        layer = QgsVectorLayer(pathIn, "temp", "ogr")
        crs = layer.sourceCrs()
        layer.setProviderEncoding(charsetIn)
        QgsVectorFileWriter.writeAsVectorFormat(layer,pathOut , charsetOut, crs, ogrFormat)
        return 0

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = EncodingConverterDialog()
            
        # show the dialog
        self.dlg.show()
        
        ready = 0
        result = 0
        # until cancel or params passed validation
        # do
        result = self.dlg.exec_()
        if result:
            ready = self.check(self.dlg)
        # while
        while ((not ready) and result):
            #do
            result = self.dlg.exec_()
            if result:
                ready = self.check(self.dlg)
        
        # finally do the work
        if ready and result:
            QtWidgets.QMessageBox.information( None, "Do the work", "Yes we can. But it will just run in the background." )
            
            ### char set
            charsetIn = self.dlg.encodingIn.text().strip()
            charsetOut = self.dlg.encodingOut.text().strip()
            
            ### path
            pathIn = self.dlg.folderIn.filePath().strip()
            pathOut = self.dlg.folderOut.filePath().strip()
            
            ### format = shp/mif
            formatOption = self.dlg.format.currentText()
            ogrFormat = "Mapinfo File"
            ext = ".mif"
            if formatOption == "ESRI Shape file (*.shp)":
                ogrFormat = "ESRI Shapefile"
                ext = ".shp"
            
            ### param keep, keep file structure or just copy into one folder ###
            keep = 0
            if self.dlg.optionKeep.isChecked():
                keep = 1
            
            ### flag replace, overwrite or skip existing files  ###
            replace = 0
            if self.dlg.overwrite.isChecked():
                replace = 1
            
            ### param thread number
            threadN = 1
            threadChoice = self.dlg.threads.currentText()
            if threadChoice == "2 threads":
                threadN = 2
            elif threadChoice == "4 threads":
                threadN = 4
            elif threadChoice == "8 threads":
                threadN = 8
            elif threadChoice == "16 threads":
                threadN = 16
            elif threadChoice == "unlimited - OS may crash!":
            # 0 means unlimited
                threadN = 0
            else:
                threadN = 1
           
            ### create a thread pool
            executor = ThreadPoolExecutor(max_workers=threadN)
            tasklist = []

            # scan files
            for dirpath,dirnames,filenames in os.walk(pathIn):
                for file in filenames:
                    # only process files of specified format
                    if file.lower().endswith(ext):
                        # flag skip, skip current file
                        skip = 0
                        # get the path
                        fullpathIn=os.path.join(dirpath,file)
                        self.iface.messageBar().pushInfo("Processing", fullpathIn)
                        fullPathOut = ""
                        # assure the directory
                        #### flag keep=1, mkdirs
                        if keep==1:
                            ##############################################
                            # simply replace to get the full path! 
                            ##############################################
                            fullPathOut = fullpathIn.replace(pathIn, pathOut, 1)
                            parentDir = os.path.dirname(fullPathOut)
                            # validate the output folder name
                            if os.path.exists(parentDir) and os.path.isdir(parentDir):
                                pass
                            elif os.path.exists(parentDir) and os.path.isfile(parentDir):
                                skip = 1
                                # though this file failed, the whole process will continue
                                self.iface.messageBar().pushWarning("Failed: invalid output path, skip", "Name of output path conflicts with existing file "+parentDir)
                            else:
                                os.makedirs(parentDir)
                                
                        # keep=0, just use the file name
                        else:
                            fullPathOut = os.path.join(pathOut,file)
                        
                        if skip:
                            pass
                        else:
                            #>>> check output path and write out
                            #### flag replace ####
                            if os.path.exists(fullPathOut):
                                ##### warning: invalid output path
                                if os.path.isdir(fullPathOut):
                                    self.iface.messageBar().pushWarning("Failed: invalid outputpath, skip.", fullpathIn+"-->"+fullPathOut)                            
                                ##### success: overwrited existing file
                                elif replace:
                                    task =  executor.submit(self.convertFile, fullpathIn, fullPathOut, charsetIn, charsetOut, ogrFormat)
                                    tasklist.append(task)
                                    self.iface.messageBar().pushSuccess("Overwrited", fullpathIn+"-->"+fullPathOut)
                                ##### warning: skipped existing file
                                else:
                                    self.iface.messageBar().pushWarning("Skipped", fullpathIn+"-->"+fullPathOut)    
                            else:
                                task =  executor.submit(self.convertFile, fullpathIn, fullPathOut, charsetIn, charsetOut, ogrFormat)
                                tasklist.append(task)
                                self.iface.messageBar().pushSuccess("Finished", fullpathIn+"-->"+fullPathOut)
                            #>>> output end
                        #end if skip
            ###  wait utill all tasks are finished
            for future in concurrent.futures.as_completed(tasklist):
                data = future.result()
            
            self.iface.messageBar().pushSuccess("Done", "Files are saved into "+pathOut+" using character set "+charsetOut)
            QtWidgets.QMessageBox.information( None, "Do the work", "Done." )
        # done

