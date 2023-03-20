import fitz, io, os
from PIL import Image


class Paper:
    def __init__(self, path, title='', url='', abs='', authers=[]):
        # 初始化函数，根据pdf路径初始化Paper对象                
        self.url =  url           # 文章链接
        self.path = path          # pdf路径
        self.section_names = []   # 段落标题
        self.section_texts = {}   # 段落内容    
        self.abs = abs
        self.title_page = 0
        if title == '':
            self.pdf = fitz.open(self.path) # pdf文档
            self.title = self.get_title()
            self.parse_pdf()            
        else:
            self.title = title
        self.authers = authers        
        self.roman_num = ["I", "II", 'III', "IV", "V", "VI", "VII", "VIII", "IIX", "IX", "X"]
        self.digit_num = [str(d+1) for d in range(10)]
        self.first_image = ''
        
    def parse_pdf(self):
        self.pdf = fitz.open(self.path) # pdf文档
        self.text_list = [page.get_text() for page in self.pdf]
        self.all_text = ' '.join(self.text_list)
        self.section_page_dict = self._get_all_page_index() # 段落与页码的对应字典
        print("section_page_dict", self.section_page_dict)
        self.section_text_dict = self._get_all_page() # 段落与内容的对应字典
        self.section_text_dict.update({"title": self.title})
        self.section_text_dict.update({"paper_info": self.get_paper_info()})
        self.pdf.close()         
        
    def get_paper_info(self):
        first_page_text = self.pdf[self.title_page].get_text()
        if "Abstract" in self.section_text_dict.keys():
            abstract_text = self.section_text_dict['Abstract']
        else:
            abstract_text = self.abs
        try:
            introduction_text = self.section_text_dict['Introduction']
            first_page_text = first_page_text.replace(abstract_text, "").replace(introduction_text, "")
        except KeyError:
            first_page_text = None
            
        return first_page_text
        
    def get_image_path(self, image_path=''):
        """
        将PDF中的第一张图保存到image.png里面，存到本地目录，返回文件名称，供gitee读取
        :param filename: 图片所在路径，"C:\\Users\\Administrator\\Desktop\\nwd.pdf"
        :param image_path: 图片提取后的保存路径
        :return:
        """
        # open file
        max_size = 0
        image_list = []
        with fitz.Document(self.path) as my_pdf_file:
            # 遍历所有页面
            for page_number in range(1, len(my_pdf_file) + 1):
                # 查看独立页面
                page = my_pdf_file[page_number - 1]
                # 查看当前页所有图片
                images = page.get_images()                
                # 遍历当前页面所有图片
                for image_number, image in enumerate(page.get_images(), start=1):           
                    # 访问图片xref
                    xref_value = image[0]
                    # 提取图片信息
                    base_image = my_pdf_file.extract_image(xref_value)
                    # 访问图片
                    image_bytes = base_image["image"]
                    # 获取图片扩展名
                    ext = base_image["ext"]
                    # 加载图片
                    image = Image.open(io.BytesIO(image_bytes))
                    image_size = image.size[0] * image.size[1]
                    if image_size > max_size:
                        max_size = image_size
                    image_list.append(image)
        for image in image_list:                            
            image_size = image.size[0] * image.size[1]
            if image_size == max_size:                
                image_name = f"image.{ext}"
                im_path = os.path.join(image_path, image_name)
                print("im_path:", im_path)
                
                max_pix = 480
                origin_min_pix = min(image.size[0], image.size[1])
                
                if image.size[0] > image.size[1]:
                    min_pix = int(image.size[1] * (max_pix/image.size[0]))
                    newsize = (max_pix, min_pix)
                else:
                    min_pix = int(image.size[0] * (max_pix/image.size[1]))
                    newsize = (min_pix, max_pix)
                image = image.resize(newsize)
                
                image.save(open(im_path, "wb"))
                return im_path, ext
        return None, None
    
    # 定义一个函数，根据字体的大小，识别每个章节名称，并返回一个列表
    def get_chapter_names(self,):
        # # 打开一个pdf文件
        doc = fitz.open(self.path) # pdf文档        
        text_list = [page.get_text() for page in doc]
        all_text = ''
        for text in text_list:
            all_text += text
        # # 创建一个空列表，用于存储章节名称
        chapter_names = []
        for line in all_text.split('\n'):
            line_list = line.split(' ')
            if '.' in line:
                point_split_list = line.split('.')
                space_split_list = line.split(' ')
                if 1 < len(space_split_list) < 5:
                    if 1 < len(point_split_list) < 5 and (point_split_list[0] in self.roman_num or point_split_list[0] in self.digit_num):
                        print("line:", line)
                        chapter_names.append(line)      
                    # 这段代码可能会有新的bug，本意是为了消除"Introduction"的问题的！
                    elif 1 < len(point_split_list) < 5:
                        print("line:", line)
                        chapter_names.append(line)     
        
        return chapter_names
        
    def get_title(self):
        doc = self.pdf # 打开pdf文件
        max_font_size = 0 # 初始化最大字体大小为0
        max_string = "" # 初始化最大字体大小对应的字符串为空
        max_font_sizes = [0]
        for page_index, page in enumerate(doc): # 遍历每一页
            text = page.get_text("dict") # 获取页面上的文本信息
            blocks = text["blocks"] # 获取文本块列表
            for block in blocks: # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']): # 如果是文字类型
                    if len(block["lines"][0]["spans"]):
                        font_size = block["lines"][0]["spans"][0]["size"] # 获取第一行第一段文字的字体大小            
                        max_font_sizes.append(font_size)
                        if font_size > max_font_size: # 如果字体大小大于当前最大值
                            max_font_size = font_size # 更新最大值
                            max_string = block["lines"][0]["spans"][0]["text"] # 更新最大值对应的字符串
        max_font_sizes.sort()                
        print("max_font_sizes", max_font_sizes[-10:])
        cur_title = ''
        for page_index, page in enumerate(doc): # 遍历每一页
            text = page.get_text("dict") # 获取页面上的文本信息
            blocks = text["blocks"] # 获取文本块列表
            for block in blocks: # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']): # 如果是文字类型
                    if len(block["lines"][0]["spans"]):
                        cur_string = block["lines"][0]["spans"][0]["text"] # 更新最大值对应的字符串
                        font_flags = block["lines"][0]["spans"][0]["flags"] # 获取第一行第一段文字的字体特征
                        font_size = block["lines"][0]["spans"][0]["size"] # 获取第一行第一段文字的字体大小                         
                        # print(font_size)
                        if abs(font_size - max_font_sizes[-1]) < 0.3 or abs(font_size - max_font_sizes[-2]) < 0.3:                        
                            # print("The string is bold.", max_string, "font_size:", font_size, "font_flags:", font_flags)                            
                            if len(cur_string) > 4 and "arXiv" not in cur_string:                            
                                # print("The string is bold.", max_string, "font_size:", font_size, "font_flags:", font_flags) 
                                if cur_title == ''    :
                                    cur_title += cur_string                       
                                else:
                                    cur_title += ' ' + cur_string     
                            self.title_page = page_index
                            # break
        title = cur_title.replace('\n', ' ')                        
        return title


    def _get_all_page_index(self):
        # 定义需要寻找的章节名称列表
        section_list = ["Abstract", 
                        'Introduction', 'Related Work', 'Background', 
                        "Preliminary", "Problem Formulation",
                        'Methods', 'Methodology', "Method", 'Approach', 'Approaches',
                        # exp
                        "Materials and Methods", "Experiment Settings",
                        'Experiment',  "Experimental Results", "Evaluation", "Experiments",                        
                        "Results", 'Findings', 'Data Analysis',                                                                        
                        "Discussion", "Results and Discussion", "Conclusion",
                        'References']
        # 初始化一个字典来存储找到的章节和它们在文档中出现的页码
        section_page_dict = {}
        # 遍历每一页文档
        for page_index, page in enumerate(self.pdf):
            # 获取当前页面的文本内容
            cur_text = page.get_text()
            # 遍历需要寻找的章节名称列表
            for section_name in section_list:
                # 将章节名称转换成大写形式
                section_name_upper = section_name.upper()
                # 如果当前页面包含"Abstract"这个关键词
                if "Abstract" == section_name and section_name in cur_text:
                    # 将"Abstract"和它所在的页码加入字典中
                    section_page_dict[section_name] = page_index
                # 如果当前页面包含章节名称，则将章节名称和它所在的页码加入字典中
                else:
                    if section_name + '\n' in cur_text:
                        section_page_dict[section_name] = page_index
                    elif section_name_upper + '\n' in cur_text:
                        section_page_dict[section_name] = page_index
        # 返回所有找到的章节名称及它们在文档中出现的页码
        return section_page_dict

    def _get_all_page(self):
        """
        获取PDF文件中每个页面的文本信息，并将文本信息按照章节组织成字典返回。

        Returns:
            section_dict (dict): 每个章节的文本信息字典，key为章节名，value为章节文本。
        """
        text = ''
        text_list = []
        section_dict = {}
        
        # 再处理其他章节：
        text_list = [page.get_text() for page in self.pdf]
        for sec_index, sec_name in enumerate(self.section_page_dict):
            print(sec_index, sec_name, self.section_page_dict[sec_name])
            if sec_index <= 0 and self.abs:
                continue
            else:
                # 直接考虑后面的内容：
                start_page = self.section_page_dict[sec_name]
                if sec_index < len(list(self.section_page_dict.keys()))-1:
                    end_page = self.section_page_dict[list(self.section_page_dict.keys())[sec_index+1]]
                else:
                    end_page = len(text_list)
                print("start_page, end_page:", start_page, end_page)
                cur_sec_text = ''
                if end_page - start_page == 0:
                    if sec_index < len(list(self.section_page_dict.keys()))-1:
                        next_sec = list(self.section_page_dict.keys())[sec_index+1]
                        if text_list[start_page].find(sec_name) == -1:
                            start_i = text_list[start_page].find(sec_name.upper())
                        else:
                            start_i = text_list[start_page].find(sec_name)
                        if text_list[start_page].find(next_sec) == -1:
                            end_i = text_list[start_page].find(next_sec.upper())
                        else:
                            end_i = text_list[start_page].find(next_sec)                        
                        cur_sec_text += text_list[start_page][start_i:end_i]
                else:
                    for page_i in range(start_page, end_page):                    
#                         print("page_i:", page_i)
                        if page_i == start_page:
                            if text_list[start_page].find(sec_name) == -1:
                                start_i = text_list[start_page].find(sec_name.upper())
                            else:
                                start_i = text_list[start_page].find(sec_name)
                            cur_sec_text += text_list[page_i][start_i:]
                        elif page_i < end_page:
                            cur_sec_text += text_list[page_i]
                        elif page_i == end_page:
                            if sec_index < len(list(self.section_page_dict.keys()))-1:
                                next_sec = list(self.section_page_dict.keys())[sec_index+1]
                                if text_list[start_page].find(next_sec) == -1:
                                    end_i = text_list[start_page].find(next_sec.upper())
                                else:
                                    end_i = text_list[start_page].find(next_sec)  
                                cur_sec_text += text_list[page_i][:end_i]
                section_dict[sec_name] = cur_sec_text.replace('-\n', '').replace('\n', ' ')
        return section_dict
                
def main():
    path = r'demo.pdf'
    paper = Paper(path=path)
    paper.parse_pdf()
    for key, value in paper.section_text_dict.items():
        print(key, value)
        print("*"*40)    
    

if __name__ == '__main__':
    main()
