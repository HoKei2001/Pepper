import os


def wrap_text(input_file, output_file, max_line_length):
    with open(input_file, 'r', encoding='utf-8') as input_file, open(output_file, 'w') as output_file:
        for line in input_file:
            # 去除行末尾的换行符
            line = line.rstrip('\n')
            # 检查行长度是否大于最大行长度
            if len(line) > max_line_length:
                words = line.split()  # 将行拆分为单词
                current_line = ''
                for word in words:
                    if len(current_line) + len(word) + 1 <= max_line_length:
                        current_line += word + ' '
                    else:
                        output_file.write(current_line.strip() + '\n')
                        current_line = word + ' '
                if current_line:
                    output_file.write(current_line.strip() + '\n')
            else:
                output_file.write(line + '\n')


if __name__ == "__main__":
    nougat_status = os.system('')

    # 使用示例
    input_file = 'files/paper1.mmd'  # 输入文件名
    output_file = 'files/paper1.txt'  # 输出文件名
    reference_file = 'files/paper1_r.txt'
    max_line_length = 800  # 最大行长度

    wrap_text(input_file, output_file, max_line_length)

    with open(output_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 查找"## References"的位置
    references_index = None
    for i, line in enumerate(lines):
        if line.strip() == "## References":
            references_index = i
            break

    # 如果找到了"## References"，则剪切并保存其后的文本到新的文件中，并更新原始文件
    if references_index is not None:
        references_text = ''.join(lines[references_index + 1:])
        with open(reference_file, 'w', encoding='utf-8') as new_file:
            new_file.write(references_text)

        # 更新原始文件，删除"## References"之后的文本
        lines = lines[:references_index + 1]
        with open(output_file, 'w', encoding='utf-8') as original_file:
            original_file.writelines(lines)

        print("done")
    else:
        print("fail to find'## References'。")
