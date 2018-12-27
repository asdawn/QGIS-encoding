# QGIS-encoding

本工具用于对指定目录（含子目录）中的矢量文件的编码进行转换，结果将按照原始的目录结构与名称进行另存。

## 1. 动机
在使用**ogr2ogr**进行**GB18030->UTF-8**字符编码转换或者直接导入**PostGIS**时，部分字符转换失败。使用QGIS转换则不报错。之前是使用**groovy**写了生成**py-QGIS**脚本的脚本，运行稍麻烦不易共享，现在直接封装为QGIS插件。

## 2. 插件开发方法
插件开发参考了[https://blog.csdn.net/deirjie/article/details/77043954](https://blog.csdn.net/deirjie/article/details/77043954)。
我使用的是QGIS 3，所以安装的插件是QGIS Plugin Builder 3。

创建时基本按照提示一路向前，设置为实验性项目，项目主页为当前项目[QGIS-encoding](https://github.com/asdawn/QGIS-encoding)。Windows下出现各种问题，包括缺失pyrcc5、pip3失灵等，于是直接在Mac下折腾...



