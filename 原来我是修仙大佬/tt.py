import re
def chinese_to_arabic(ch_num):
    """ 基础中文数字转换（支持1-9999） """
    num_map = {
        '零':0, '一':1, '二':2, '三':3, '四':4,
        '五':5, '六':6, '七':7, '八':8, '九':9,
        '十':10, '百':100, '千':1000, '万':10000
    }
    
    result = 0
    temp = 0  # 临时存储单位前的数字
    for char in ch_num:
        value = num_map.get(char, 0)
        if value < 10:  # 普通数字
            temp = temp * 10 + value if temp else value
        elif value >= 10:  # 遇到单位
            result += (temp if temp > 0 else 1) * value
            temp = 0
    return result + temp  # 加上最后的余数
def convert_novel(input_path, chunk_size=50):
    """ 文件分章转换核心函数 """
    chapter_counter = 0
    current_start = None
    output_file = None
    buffer = []
    
    # 增强型正则表达式（兼容带空格的情况）
    pattern = re.compile(r'^第\s*([零一二三四五六七八九十百千万]+)\s*章\s*(.*)$')
    
    with open(input_path, 'r', encoding='gbk') as f:
        for line in f:
            line = line.rstrip()  # 保留行尾格式
            match = pattern.match(line)
            
            if match:
                chapter_counter += 1
                ch_num_str = match.group(1)
                title = match.group(2).strip()
                
                # 转换中文数字
                try:
                    ch_num = chinese_to_arabic(ch_num_str)
                except:
                    ch_num = chapter_counter  # 失败时使用计数器
                
                # 初始化第一个文件
                if not output_file:
                    current_start = ch_num
                    output_file = open(f"{current_start}.md", 'w', encoding='utf-8')
                
                # 分章逻辑
                if chapter_counter % chunk_size == 0:
                    output_file.write('\n'.join(buffer) + '\n')
                    output_file.close()
                    current_start = ch_num  # 新文件起始章
                    output_file = open(f"{current_start}.md", 'w', encoding='utf-8')
                    buffer = [f"# 第{ch_num}章 {title}"]
                else:
                    buffer.append(f"# 第{ch_num}章 {title}")
            else:
                buffer.append(line)
    
    # 写入最后剩余内容
    if output_file and buffer:
        output_file.write('\n'.join(buffer))
        output_file.close()
if __name__ == "__main__":
    convert_novel("原来我是修仙大佬.txt", chunk_size=50)

