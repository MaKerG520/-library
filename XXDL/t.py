import re
from cn2an import cn2an
def convert_novel(input_path, chunk_size=50):
    """ 智能分章转换核心函数 """
    chapter_counter = 0  # 章节计数器
    file_counter = 1     # 文件计数器
    current_file = None  # 当前写入文件
    buffer = []          # 内容缓冲区
    
    # 章节标题正则（兼容中英文数字混合）
    pattern = re.compile(r'^第\s*([零一二三四五六七八九十百千万0-9]+)\s*章\s+(.*)$')
    
    with open(input_path, 'r', encoding='gbk') as f:
        for line in f:
            line = line.rstrip()  # 保留行尾空白
            match = pattern.match(line)
            
            if match:  # 检测到章节标题
                chapter_counter += 1
                ch_num_str = match.group(1)
                title = match.group(2)
                
                # 转换中文数字为阿拉伯数字
                try:
                    ch_num = int(cn2an(ch_num_str, "smart"))
                except:
                    ch_num = chapter_counter
                
                # 生成Markdown标题
                md_title = f"# 第{ch_num}章 {title}\n"
                
                # 初始化第一个文件
                if not current_file:
                    start_num = ch_num
                    current_file = open(f"{start_num}.md", 'w', encoding='utf-8')
                
                # 达到分章阈值时创建新文件
                if chapter_counter % chunk_size == 0:
                    # 写入缓冲区内容
                    current_file.write('\n'.join(buffer))
                    current_file.close()
                    
                    # 重置状态
                    start_num = ch_num + 1  # 下一文件起始章号
                    file_counter += 1
                    buffer = [md_title]
                    current_file = open(f"{start_num}.md", 'w', encoding='utf-8')
                else:
                    buffer.append(md_title)
            else:  # 普通内容行
                buffer.append(line)
    
    # 写入最后剩余内容
    if current_file and buffer:
        current_file.write('\n'.join(buffer))
        current_file.close()
if __name__ == "__main__":
    input_file = "原来我是修仙大佬.txt"  # 输入文件路径
    convert_novel(input_file)

