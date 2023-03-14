#该程序用于输出程序第一面
import fitz
def GetFirstPage(path):
    # 打开PDF文件
    pdf = fitz.open(path)
    # 创建一个空字符串来存储文本
    text = ''
    # 只读取第一页
    page = pdf[0]
    next_title = ['introduction','contents']
    # 获取摘要所在的页码
    abstract_page_number = 1
    # 如果当前页面是摘要页面，则读取文本
    if page.number == abstract_page_number - 1:
        text += page.get_text()

    end_index = [float('inf')] * len(next_title)
    if any(title.lower() in text.lower() for title in next_title):
        pix = 0
        for sub_title in next_title:
            if sub_title.lower() in text.lower():
                end_index[pix] = text.lower().index(sub_title.lower())
                pix = pix+1
        text = text[:min(end_index)]
    # 关闭PDF文件
    pdf.close()
    return text