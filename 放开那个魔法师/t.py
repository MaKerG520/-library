import re
def chinese_to_arabic(ch_num_str):
    """ 中文数字转阿拉伯数字 (支持1-9999) """
    num_map = {
        '零':0, '一':1, '二':2, '三':3, '四':4, '五':5,
        '六':6, '七':7, '八':8, '九':9, '十':10,
        '百':100, '千':1000, '万':10000
    }
    
    result = 0
    temp_num = 0
    for char in ch_num_str:
        value = num_map.get(char, 0)
        if value < 10:
            temp_num = temp_num * 10 + value if temp_num else value
        elif value >= 10:
            result += (temp_num if temp_num > 0 else 1) * value
            temp_num = 0
    return result + temp_num
def format_spaces(text):
    """ 智能空格格式化 """
    # 把2个以上连续空格转换成换行+缩进
    return re.sub(r' {2,}', '\n\t', text.strip())
def convert_novel(input_file, chunk_size=50):
    """ 文件转换主函数 """
    chapter_counter = 0
    current_start = None
    output_file = None
    buffer = []
    
    chapter_pattern = re.compile(
        r'^第\s*([一二三四五六七八九十百千万]+)\s*章\s*(.*?)\s*$'
    )
    with open(input_file, 'r', encoding='gbk') as f:
        for line in f:
            # 预处理：保留行尾换行符，移除首尾空白
            raw_line = line.rstrip('\n').strip()
            match = chapter_pattern.match(line)
            
            if match:  # 处理章节行
                chapter_counter += 1
                ch_num_str, title = match.groups()
                
                try:
                    ch_num = chinese_to_arabic(ch_num_str)
                except:
                    ch_num = chapter_counter  # 转换失败时使用顺序编号
                
                # 初始化或创建新文件
                if not output_file or chapter_counter % chunk_size == 1:
                    if output_file:
                        output_file.close()
                    current_start = ch_num
                    output_file = open(f"{current_start}.md", 'w', encoding='utf-8')
                
                # 添加章节标题到缓冲区
                buffer.append(f"# 第{ch_num}章 {title}")
            else:  # 处理正文内容
                if raw_line:  # 忽略空行
                    buffer.append(format_spaces(raw_line))
            
            # 达到分章数量时写入文件
            if chapter_counter % chunk_size == 0 and chapter_counter != 0:
                output_file.write('\n\n'.join(buffer) + '\n')
                buffer = []
    
    # 写入最后剩余内容
    if output_file and buffer:
        output_file.write('\n\n'.join(buffer))
        output_file.close()
if __name__ == "__main__":
    # 使用示例（直接运行）
    convert_novel("input.txt")  # 自动生成 1.md, 51.md, 101.md...

