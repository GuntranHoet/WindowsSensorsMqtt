@echo off
echo y|rmdir /s "compiled"
mkdir "compiled"
cd "compiled"
call pyinstaller -w -F "%cd%\..\..\src\main.py"
ren dist\main.exe WindowsSensorsMQTT.exe
%SystemRoot%\explorer.exe "%cd%\dist"