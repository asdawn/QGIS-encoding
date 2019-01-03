# QGIS-encoding

This converter can read all vector files in a folder and its sub-folders, and save them into another folder using specified character set.

![UI](/img/ui.jpg)

# Input
+ Input folder: select the folder which contains all the vector files to convert

+ Data format: now this tool supports only *ESRI shape* and *MapInfo mif*, all files of this format in the input folder will be processes (**will not be modified, just save a converted copy into the output folder**)

+ Character set: yes, you can specify the input character set. The default value is *System*, it depends on your OS.

# Output










--------------
Change log
+ ver 0.1 it works, except the two options(*keep* and *overwrite*). UI will be freezed, it should be fixed after functions implemented.

+ ver 0.2 the function is fully implemented. UI will be fixed in the next version using a worker thread. 


