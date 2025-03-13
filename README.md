# -library

详见下文

```python
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
    input_file = "input.txt"  # 输入文件路径
    convert_novel(input_file)



## [大一实习，你跑去749收容怪物 ](https://github.com/MaKerG520/-library/blob/main/749SRS/part1.md#%E7%AC%AC1%E7%AB%A0-%E7%AD%89%E4%BA%86%E4%BA%8C%E5%8D%81%E5%B9%B4%E7%9A%84%E9%87%91%E6%89%8B%E6%8C%87%E7%BB%88%E4%BA%8E%E6%9C%89%E8%83%BD%E7%94%A8%E7%9A%84%E5%B8%8C%E6%9C%9B%E4%BA%86)

## [全民求生，获得D级人员模拟器](https://github.com/MaKerG520/-library/blob/main/D%E7%BA%A7/part1.md#%E7%AC%AC1%E7%AB%A0-%E5%BC%80%E5%B1%80%E6%88%90%E4%B8%BAd%E7%BA%A7%E4%BA%BA%E5%91%98)

## [我合成了全世界](https://github.com/MaKerG520/-library/blob/main/HCQworld/1.md#%E7%AC%AC1%E7%AB%A0-%E5%9C%B0%E7%90%83%E5%9E%83%E5%9C%BE%E5%9C%BA)

## [放开那个魔法师](https://github.com/MaKerG520/-library/blob/main/MFS/1.md#%E7%AC%AC1%E7%AB%A0-%E5%BC%80%E7%AB%AF)

## [末世直播召唤黑粉后，惊动了国家](https://github.com/MaKerG520/-library/blob/main/MSZB/part1.md#%E7%AC%AC1%E7%AB%A0-%E4%BA%BA%E5%9C%A8%E6%9C%AB%E4%B8%96%E6%90%9E%E7%9B%B4%E6%92%AD)

## [直播：上什么北大，跟爹上A大！](https://github.com/MaKerG520/-library/blob/main/SAD/part1.md#%E7%AC%AC1%E7%AB%A0-%E4%B8%8A%E4%BB%80%E4%B9%88%E5%8C%97%E5%A4%A7%E8%B7%9F%E7%88%B9%E4%B8%8Aa%E5%A4%A7)

## [原来我是修仙大佬](https://github.com/MaKerG520/-library/blob/main/XXDL/1.md#%E7%AC%AC1%E7%AB%A0-%E5%BC%80%E5%B1%80%E5%B0%B1%E5%92%8C%E7%B3%BB%E7%BB%9F%E6%95%A3%E4%BC%99)
