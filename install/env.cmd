set PYROOT=E:\Python310
set PATH=%PYROOT%;%PYROOT%\Scripts;%PATH%;

set MYROOT=%~dp0..\
pushd %MYROOT%

set PYTHONPATH=%PYTHONPATH%;%MYROOT%\src\sc

::python.exe -m pip install --upgrade pip

::pip.exe install -U PyInstaller
::pip.exe install tk
::pip.exe install py7zr


