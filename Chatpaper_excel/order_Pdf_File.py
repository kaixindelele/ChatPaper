#将endnote中的pdf文件输出到一个文件夹中
import os
import shutil
# 设置源文件夹和目标文件夹路径
source_folder = "My EndNote Library.Data\\PDF"
target_folder = "paper"
# 遍历源文件夹中的所有子文件夹及其包含的文件
for root, dirs, files in os.walk(source_folder):
    for filename in files:
        # 如果找到PDF文件，则将其复制到目标文件夹中
        if filename.endswith(".pdf"):
            source_file_path = os.path.join(root, filename)
            target_file_path = os.path.join(target_folder, filename)
            shutil.copy2(source_file_path, target_file_path)
