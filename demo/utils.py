import re
import yaml


# 1. 提供文件路径，返回文件内容（字符串）
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# 2. 提供字符串内容，返回文件头和主要内容两个字符串
def split_content(content):
    content = content.strip()  # 去掉首尾空白字符
    match = re.match(r"^(---\n.*?\n---\n)(.*)$", content, re.DOTALL)
    if match:
        front_matter = match.group(1)  # 文件头部分
        main_content = match.group(2)  # 主要内容部分
        return front_matter, main_content
    else:
        raise ValueError("文件格式不正确，没有找到 YAML 文件头。")


# 3. 提供字符串文件头，转换为字典
def parse_yaml_to_dict(yaml_string):
    yaml_string = yaml_string.lstrip()  # 去掉前面的空白字符
    yaml_content = yaml_string.strip("---\n")  # 去掉 YAML 文件头的分隔符
    return yaml.safe_load(yaml_content)  # 使用 PyYAML 转换为字典


# 4. 提供字典，转换回字符串文件头
from ruamel.yaml import YAML
from io import StringIO


def dict_to_yaml_string(yaml_dict):
    """
    使用 ruamel.yaml 将字典转换为带有 YAML 文件头的字符串，确保列表项前有适当的缩进。

    参数:
        yaml_dict (Dict): 需要转换的字典。

    返回:
        str: 转换后的 YAML 字符串。
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)  # 设置缩进参数
    stream = StringIO()
    yaml.dump(yaml_dict, stream)
    yaml_content = stream.getvalue()
    return f"---\n{yaml_content}---\n"


# 5 提供文件路径和文件内容，重写或者创建文件
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


# 6. 提供文件路径，格式化文件头，
def format_front_matter(file_path):
    # 读取文件内容
    content = read_file(file_path)

    # 分割文件内容为文件头和主要内容
    front_matter, main_content = split_content(content)

    # 将文件头字符串解析为字典
    front_matter_dict = parse_yaml_to_dict(front_matter)

    # 将字典转换回文件头字符串
    new_front_matter = dict_to_yaml_string(front_matter_dict)

    # 重写文件
    new_content = new_front_matter + main_content
    write_file(file_path, new_content)


# 7. 比较两个 YAML 字典
def compare_yaml_dicts(dict1, dict2):
    """
    检查两个 YAML 字典是否具有相同的键，并验证以下内容：
    - 列表值的长度是否一致。
    - 值的类型是否相同。

    参数:
        dict1 (dict): 第一个 YAML 字典。
        dict2 (dict): 第二个 YAML 字典。

    返回:
        bool: 如果两个字典的键、列表长度和值类型一致，则返回 True；否则返回 False。
        dict: 不同的地方，作为报告返回。
    """
    report = {"missing_keys": [], "type_mismatches": [], "list_length_mismatches": []}

    # 获取两个字典的键
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())

    # 找出缺失的键
    missing_in_dict1 = keys2 - keys1
    missing_in_dict2 = keys1 - keys2

    if missing_in_dict1:
        report["missing_keys"].append({"in_dict2_not_in_dict1": list(missing_in_dict1)})
    if missing_in_dict2:
        report["missing_keys"].append({"in_dict1_not_in_dict2": list(missing_in_dict2)})

    # 比较相同键的值
    common_keys = keys1 & keys2
    for key in common_keys:
        value1 = dict1[key]
        value2 = dict2[key]

        # 检查类型是否相同
        if type(value1) != type(value2):
            report["type_mismatches"].append({key: {"type_dict1": type(value1), "type_dict2": type(value2)}})
            continue

        # 如果是列表，检查长度是否一致
        if isinstance(value1, list) and isinstance(value2, list):
            if len(value1) != len(value2):
                report["list_length_mismatches"].append(
                    {key: {"length_dict1": len(value1), "length_dict2": len(value2)}})

    # 返回结果
    is_identical = not (report["missing_keys"] or report["type_mismatches"] or report["list_length_mismatches"])
    return is_identical, report


# 示例用法
if __name__ == "__main__":
    file_path = "index.md"

    # 1. 读取文件内容
    content = read_file(file_path)

    # 2. 分割文件内容为文件头和主要内容
    front_matter, main_content = split_content(content)

    # 3. 将文件头字符串解析为字典
    front_matter_dict = parse_yaml_to_dict(front_matter)

    # 4. 将字典转换回文件头字符串
    new_front_matter = dict_to_yaml_string(front_matter_dict)

    # 5. 重写文件
    format_front_matter(file_path)

    # 6. 比较两个 YAML 字典
    dict1 = {"title": "Hello, World!", "tags": ["python", "yaml"]}
    dict2 = {"title": "你好世界", "tags": ["python", "yaml"]}
    is_identical, report = compare_yaml_dicts(dict1, dict2)
