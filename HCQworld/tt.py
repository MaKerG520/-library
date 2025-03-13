import re

def split_novel_to_md(file_path, chapters_per_file=50):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式匹配章节标题
    chapter_pattern = re.compile(r'##?\s*第(\d+)章\s*(.*)')
    matches = list(chapter_pattern.finditer(content))
    

    start_index = 0
    file_count = 1
    while start_index < len(matches):
        end_index = min(start_index + chapters_per_file, len(matches))

        # 获取当前部分的所有章节
        current_chapters = matches[start_index:end_index]
        
        # 获取当前部分的起始和结束位置
        if start_index == 0:
            start_pos = matches[start_index].start()
        else:
            start_pos = matches[start_index].start() - len(f'## 第{matches[start_index][0]}章')
        if end_index == len(matches):
            end_pos = len(content)
        else:
            end_pos = matches[end_index].start()

        current_text = content[start_pos:end_pos].strip()

        # 写入文件，并确保每个文件以“第*章 章节名”开头
        with open(f"{file_count}.md", 'w', encoding='utf-8') as output:
            for match in current_chapters:
                chapter_number = int(match.group(1))
                chapter_title = match.group(2).strip()
                file_count += 1
                output.write(f'## 第{chapter_number}章 {chapter_title}\n')
                # 找到并写入章节内容
                chapter_start = match.end()
                if current_chapters.index(match) < len(current_chapters) - 1:
                    chapter_end = current_chapters[current_chapters.index(match) + 1].start()
                else:
                    chapter_end = end_pos
                chapter_content = content[chapter_start:chapter_end].strip()
                output.write(chapter_content + '\n\n')

        start_index = end_index
        

# 使用函数
split_novel_to_md('input.txt')