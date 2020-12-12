# QGIS-encoding

![UI](/img/icon.png)

This converter can read all vector files in a folder and its sub-folders, and save them into another folder using specified character set.

----------------

## Installation

1. Download the latest converter_plugin_{version}.zip

    Please use the latest version. Though old versions may work, new versions work better.

2. Install it in QGIS's plugin manager 

    Start QGIS, open menu `Plugins` -> `Manage and install plubins` -> `Install from ZIP`, then select the zip file and install it.

    *The plugin manager will cost some time to get the list of available plugins on startup, just be patient.*

3. Check the installation
    
    It should be install in the menu `Vector` -> `Batch Encoding Converter` -> `Convert character encoding`. Besides, a shortcut will be added to the *plugins toolbar* which uses the icon show above. 

    *The plugins toolbar might be invisible, you can right click on the toolbar region and check it in the popup list.*

----------------

## Usage

![UI](/img/ui.jpg)

### Input
+ Input folder: select the folder which contains all the vector files to convert

+ Data format: now this tool supports only *ESRI shape* and *MapInfo mif*, all files of this format in the input folder will be processes (**will not be modified, just save a converted copy into the output folder**)

+ Character set: yes, you can specify the input character set. The default value is *System*, it depends on your OS.

### Output

+ Output folder: select the folder which to create the `copies` of input files (and folders)

+ Character set: output files will use this encoding

+ keep file names and file structures: if checked, folders will be created recursively according to the input folder, and file names will keep the same as the input files. If not checked, only files names will keep the same, all files will be saved in the output folder. 

### Processing

+ Max thread: number of background threads to use. If it go wrong frequently, please try safe mode (use 1 thread).

+ overwrite existing files without notification: if checked, existing files will be overwritten. If not checked, existing files will not be overwritten and a warning message will be pushed to the message bar.

    *This is a batch processing tool, so it won't stop if there are problems with some file. Please check the warning messages after finished.*

### OK and Cancel

+ OK: start the work, a message box will be shown after finished. 

    *In earlier versions tbe GUI of QGIS will be freezed because the work is running in a foreground thread. If you want to kill the process, you have to use the task manager to kill the QGIS instance.*

+ Cancel: just close the window and return to QGIS.

---------------

## Why not ogr2ogr?

ogr2ogr is a good tool,  with the `PGCLIENTENCODING` variable you can specify the encoding of input files, characters will be properly processed while importing into Postgres. However it can not correctly convert some GB18030 characters into UTF-8 while QGIS is okay, there exists some very special names of places in China. There are plenty of errors so I can not trace and correct them manually, I have to convert them with QGIS before importing them into database.

---------------

## Change log

+ ver 0.1 

    it works, except the two options(*keep* and *overwrite*). UI will be freezed, it should be fixed after functions implemented.

+ ver 0.2 

    the function is fully implemented. UI will be fixed in the next version using a worker thread. 

+ ver 0.2a

    fixed the folder creation bug, now `keep file names and file structures` works.

    updated the version in metadata to 0.2a.

    completed the readme file.

+ ver 0.3

    now multi-thread processing is available, though it still freeze the UI of QGIS.

+ ver 0.4

    add .E00 input format.

    add export format options.

## On develepment

If you want to modify it, please refer to the [PyQGis cookbook](https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins/plugins.html)

*Though I'm using Windows 10, I compile it under Linux (Windows Subsystem for Linux), or the dependencies is a headache.*


