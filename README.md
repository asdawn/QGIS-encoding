# QGIS-encoding

本工具用于对指定目录（含子目录）中的矢量文件的编码进行转换，结果将按照原始的目录结构与名称进行另存。

## 1. 动机

在使用**ogr2ogr**进行**GB18030->UTF-8**字符编码转换或者直接导入**PostGIS**时，部分字符转换失败。使用QGIS转换则不报错。之前是使用**groovy**写了生成**py-QGIS**脚本的脚本，运行稍麻烦不易共享，现在直接封装为QGIS插件。

## 2. 开发环境配置

插件开发参考了[https://blog.csdn.net/deirjie/article/details/77043954](https://blog.csdn.net/deirjie/article/details/77043954)，
[https://www.qgistutorials.com/en/docs/building_a_python_plugin.html](https://www.qgistutorials.com/en/docs/building_a_python_plugin.html)。

我使用的是QGIS 3，所以安装的插件是QGIS Plugin Builder 3。

创建时基本按照提示一路向前，设置为实验性项目，项目主页为当前项目[QGIS-encoding](https://github.com/asdawn/QGIS-encoding)。Windows下出现各种问题，包括缺失pyrcc5、pip3失灵等，于是直接使用Windows内置的**Ubuntu bash**，安装了以下包：

```bash
sudo apt-get install python3
sudo apt-get install python3-pip
#zip命令需要使用压缩软件
sudo apt-get install zip p7zip
pip3 install pyqt5
pip3 install pb_tool
```

**pb_tool**是一个半傻瓜式的QGIS插件生成工具，其用法为：
>**clean**       Remove compiled resource and ui files<br>
  **clean-docs**  Remove the built HTML help files from the build directory<br>
  **compile**    Compile the resource and ui files<br>
  **config**      Create a config file based on source files in the current...<br>
  **create**      Create a new plugin in the current directory using either the...<br>
  **dclean**      Remove the deployed plugin from the .qgis2/python/plugins...<br>
  **deploy**      Deploy the plugin to QGIS plugin directory using parameters in...<br>
  **doc**         Build HTML version of the help files using sphinx<br>
  **help**        Open the pb_tools web page in your default browser<br>
  **list**        List the contents of the configuration file<br>
  **translate**   Build translations using lrelease.<br>
  **update**      Check for update to pb_tool<br>
  **validate**    Check the pb_tool.cfg file for mandatory sections/files.<br>
  **version**     Return the version of pb_tool and exit<br>
  **zip**         Package the plugin into a zip file suitable for uploading to...<br>

**pb_tool**也适用于**QGIS 3**，不用担心。不喜欢仔细看说明的小伙伴知道这个就够了：
>**compile**命令可以编译<br>
**zip**命令可以将插件打包为可安装的压缩包

由于**bash**下实际上没有安装QGIS（安装也没办法使用，不支持图形界面），必须手工创建相应的目录（假设账户名为*d*）：
```bash
#make dir
sudo mkdir -p /home/d/.local/share/QGIS/QGIS3/profiles/default/python/plugins
#grant priviledge
sudo chown d /home/d/.local -R
```

**提示**：
>Mac OS X下，QGIS 3的插件目录在
`/Users/账户/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`下，和QGIS 2不同。

## 3. 界面设计

初始的UI大致如下：
![UI设计](/img/ui.jpg)

+ 输入设置
>选择文件夹<br>
选择输入字符集
选择数据类型

+ 输出设置
>输出文件夹<br>
选择输出字符集<br>
选择是保留原有的目录结构还是直接展开到输出文件夹

+ 数据类型支持：
> ESRI Shape file<br>
MapInfo MIF file<br>

## 4. 内部逻辑

### 4.1 init
读取可用的Character set，更新2个字符集列表（默认为System->UTF8）
加载数据格式列表，默认为shape

### 4.3 点击OK后
如果有选项未设置则提示重填。

然后便利输入文件夹（及其子目录）下指定类型的文件，以指定编码打开，然后另存至指定输出文件夹。信息在python控制台输出，进度条先不管。

## 5. 版权

采用和QGIS相同的GPL v2协议。









