import os
import rarfile
def un_rar(file_name):
    """unrar zip file"""
    rar = rarfile.RarFile(file_name)  # 待解压文件
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    os.chdir(file_name + "_files")
    rar.extractall()  # 解压指定目录
    rar.close()

# un_rar(r'C:\cc\share\temp\760_eY28x7J.rar')
rf = rarfile.RarFile(r'C:\cc\share\temp\760_eY28x7J.rar')
rf.extractall(r'C:\cc\share\temp')
