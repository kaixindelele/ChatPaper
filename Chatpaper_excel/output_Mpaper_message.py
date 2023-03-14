# 该脚本用于处理文献N篇，使用3.5模型输出到txt文件中
import os
import glob
import re       #用于删除多余换行
from readAbstract import GetFirstPage
from OpenAI_readPaper import ReadPaper_c
from OpenAI_readPaper import ReadPaper_e

def Mpaper(openaikey):
        # 要查找PDF文件的文件夹路径
        folder_path = "paper"
        # 获取该文件夹下所有的PDF文件的路径
        pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
        pix=1
        for pdf_file in pdf_files:
                # 打印每个PDF文件的路径
                text = GetFirstPage(pdf_file)
                try:
                        resultc = ReadPaper_c(text, openaikey)
                except Exception as e:
                        print("There is a wrong. Retry for "+str(e)+"s")
                try:
                        resulte = ReadPaper_e(text,openaikey)
                except Exception as e:
                        print("There is a wrong. Retry for "+str(e)+"s")
                print('Paper-' + str(pix) + ' have already been read')
                #将返回内容按标准格式输出
                # 去除多余空行
                #resulte = re.sub(r'\n+', '\n', resulte)
                #resultc = re.sub(r'\n+', '\n', resultc)
                #resulte = resulte.strip('\n')
                #resultc = resultc.strip('\n')
                # 中文输出到从c.txt
                txtfilec = 'paper_information/' + str(pix) + 'c.txt'
                with open(txtfilec, 'w', encoding="utf-8") as f:
                        f.write(resultc)
                # 英文输出到从e.txt
                txtfilee = 'paper_information/' + str(pix) + 'e.txt'
                with open(txtfilee, 'w', encoding="utf-8") as f:
                        f.write(resulte)
                #写入其他信息
                txtfile = 'paper_information/' + str(pix) + '.txt'
                with open(txtfile, 'w', encoding="utf-8") as f:
                        f.write(pdf_file)
                pix = pix + 1


