import re

def parse_chapters(content):
    chapters = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # 匹配章节标题
        match = re.match(r'^第(\d+)章\s*(.*)', line)
        if match:
            chapter_number = int(match.group(1))
            chapter_title = match.group(2).strip()
            chapter_content = []

            # 提取章节内容直到下一个章节标题或文件结束
            j = i + 1
            while j < len(lines) and not re.match(r'^第\d+章', lines[j].strip()):
                chapter_content.append(lines[j].strip())
                j += 1

            chapters.append((chapter_number, chapter_title, '\n'.join(chapter_content).strip()))
            i = j - 1  # 跳到下一个章节标题的前一行

        i += 1

    return chapters

def split_novel_to_md(file_path, chapters_per_file=50):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    chapters = parse_chapters(content)

    start_index = 0
    file_count = 1
    while start_index < len(chapters):
        end_index = min(start_index + chapters_per_file, len(chapters))
        output_filename = f"part{file_count}.md"

        with open(output_filename, 'w', encoding='utf-8') as output:
            for chapter_number, chapter_title, chapter_content in chapters[start_index:end_index]:
                output.write(f'## 第{chapter_number}章 {chapter_title}\n\n')
                output.write(f'{chapter_content}\n\n')

        start_index = end_index
        file_count += 1

# 使用函数
split_novel_to_md('input.txt')