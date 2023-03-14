#将已经输出的gpt内容整合到excel
from output_paper_excel import OutputExcel
import os
import glob

def OrdrtExcel(excelname):
        # 要查找文件的文件夹路径
        folder_path = "paper_information"
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        count = 0
        for file_path in txt_files:
                count += 1
        count=int(count/3)
        for pix in range(1, count+1):
                print("paper"+str(pix)+" has already write in excel")
                filenamec= folder_path+"/"+str(pix)+'c.txt'
                filenamee = folder_path+"/"+str(pix) + 'e.txt'
                with open(filenamec, 'r', encoding="utf-8") as file:
                        contentc_lines = file.readlines()
                        contentc_lines = [line for line in contentc_lines if line.strip()]
                with open(filenamee, 'r', encoding="utf-8") as file:
                        contente_lines = file.readlines()
                        contente_lines = [line for line in contente_lines if line.strip()]
                datac = {}
                datae = {}
                for line in contentc_lines:
                        key, value = line.strip().split(': ', 1)
                        datac[key] = value

                for line in contente_lines:
                        key, value = line.strip().split(': ', 1)
                        datae[key] = value

                #拼接中英内容
                dict1 = datac
                dict2 = datae
                result_dict = {}
                for key, value in dict1.items():
                        if key in dict2 and dict2[key] != value:
                                result_dict[key] = value + '\n\n' + dict2[key]
                        else:
                                result_dict[key] = value

                for key, value in dict2.items():
                        if key not in dict1:
                                result_dict[key] = value

                new_pairs = {'Serial Number': '0', 'RM': 'Scanning'}
                merged_dict = {**new_pairs, **result_dict}
                new_dict = {}
                for key, value in merged_dict.items():
                        new_dict[key] = value
                        if key == 'Keywords':
                                new_dict['Note'] = '                                                                                            '
                OutputExcel(new_dict, folder_path+'/'+str(pix)+'.txt',excelname)