rpa-ide，一套seebot运行调试工具

#### 开发环境准备

```python
# 1. 通过Pycharm终端安装PySide6
    pip install PySide6
# 2. 配置Pycharm扩展工具
    settings -> Tools -> External Tools 
    1. QtDesigner
    Program: D:\AppData\rpa-ide\Lib\site-packages\PySide6\designer.exe
    Warking directory: $FileDir$
    2. PyUIC
    Program: D:\AppData\rpa-ide\Scripts\python.exe
    Arguments: $FileName$ -o $FileNameWithoutExtension$.py
    Warking directory: $FileDir$
    3. 打开UI
    Program: D:\AppData\rpa-ide\Lib\site-packages\PySide6\designer.exe
    Arguments: $FilePath$
    Warking directory: $ProjectFileDir$
# 3. 打开UI文件，右键.ui文件，执行External Tools -> 打开UI，
# 4. 使用QtDesigner，生成一个winform窗体的.ui文件，右键该文件，执行External Tools -> PyUIC，生成一个同名的.py文件
```


