echo y|rmdir /s "compiled"
mkdir "compiled"
cd "compiled"
start pyinstaller -F "C:\Python\Projects\WindowsSensorsMqtt\src\main.py"