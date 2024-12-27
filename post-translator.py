import os
import glob
import time

import google.generativeai as genai

# 创建生成模型
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        }
    ]
)

# 支持的语言映射，按优先顺序排序
LANGUAGE_CODES = ["en", "zh-cn", "zh-tw", "ja", "de", "es", "fr", "hi", "it", "ko", "pt", "ru", "tr", "vi"]
LANGUAGE_FULL_NAMES = {
    "en": "English",
    "zh-cn": "Simplified Chinese",
    "zh-tw": "Traditional Chinese",
    "ja": "Japanese",
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "it": "Italian",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
    "tr": "Turkish",
    "vi": "Vietnamese"
}


# 翻译函数
def translate_with_gemini(input_text, target_language):
    time.sleep(2)
    prompt = f"""
Translate the following file content to natural {target_language}. Retain formatting, code blocks, and styles. Remove links to domains that contain acwing.com and luogu.com. Here's the file content:  
{input_text}"""
    retries = 0
    max_retries = 5
    while retries < max_retries:
        try:
            time.sleep(2)
            chat_session = model.start_chat(history=[])
            chat_response = chat_session.send_message(prompt)
            response = chat_response.text.strip()
            if response.startswith("```") and response.endswith("```"):
                response = response[3:-3]
            return response.strip()
        except Exception as e:
            retries += 1
            print(f"Error during translation to {target_language}: {e}")
            if retries < max_retries:
                print(f"Retrying... ({retries}/{max_retries})")
                time.sleep(retries * 30)
            else:
                print("Maximum retries reached. Exiting program.")
                raise


# 加载已有内容作为翻译基础
def load_existing_content(md_files, priority_languages):
    """
    按照优先级顺序 (priority_languages) 寻找已存在的文件。若找到，则返回其内容，用于翻译基准。
    """
    for lang_code in priority_languages:
        for file_path in md_files:
            filename = os.path.basename(file_path)
            if filename == "index.md" and lang_code == "en":
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            elif f"index.{lang_code}.md" in filename:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
    return None


def check_and_regenerate_if_needed(dirpath, md_files):
    """
    检查语言文件的修改时间，若简体中文(zh-cn)或英语(en)是所有文件中单独最新，
    则删除其他语言文件，并统一从该最新文件进行重新翻译。

    返回值:
        True  - 表示触发了重新翻译，并且已经完成了所有语言的生成，不需要再执行后续 'missing' 补翻译逻辑
        False - 表示未触发重新翻译，需要继续执行后续逻辑(检查是否有 missing 的文件再补翻译)
    """

    # 收集当前目录下已有语言文件的 {lang_code: (file_path, mtime)}
    lang_files_mtime = {}
    for file_path in md_files:
        filename = os.path.basename(file_path)
        stat = os.stat(file_path)
        mtime = stat.st_mtime  # 修改时间
        if filename == "index.md":
            lang_code = "en"
        else:
            parts = filename.split(".")
            # 形如：["index", "de", "md"] -> lang_code = "de"
            lang_code = parts[-2]
        lang_files_mtime[lang_code] = (file_path, mtime)

    # 如果目录下根本没有 zh-cn 或 en 文件，就无需检查此逻辑
    if "zh-cn" not in lang_files_mtime and "en" not in lang_files_mtime:
        return False

    # 找出修改时间最大的语言和对应的时间
    # 先提取一个 {lang_code: mtime}，方便比较
    mtime_dict = {lang: lang_files_mtime[lang][1] for lang in lang_files_mtime}
    newest_lang = max(mtime_dict, key=lambda l: mtime_dict[l])
    newest_time = mtime_dict[newest_lang]

    # 判断 newest_lang 是否是单独最大的（没有其他语言与它并列）
    # 若有并列或任何其他语言更新，不执行重翻译
    all_max_langs = [l for l, t in mtime_dict.items() if t == newest_time]
    if len(all_max_langs) > 1:
        # 有并列，不执行重翻译
        return False

    # 若这个 newest_lang 不是 zh-cn 或 en，则不执行重翻译
    if newest_lang not in ["zh-cn", "en"]:
        return False

    # newest_lang 确定是所有语言中的单独最新，并且是 zh-cn 或 en
    # 触发删除并重新翻译
    print(f"*** {newest_lang} is the single newest. Generating translations from this file. ***")

    # 先读取该最新文件内容
    base_file_path = lang_files_mtime[newest_lang][0]
    with open(base_file_path, "r", encoding="utf-8") as f:
        base_content = f.read()

    # 删除其他语言文件（不删除自己）
    for lang, (path, _) in lang_files_mtime.items():
        if lang != newest_lang:
            os.remove(path)
            print(f"Removed older file: {path}")

    # 获取需要翻译的目标语言
    # 如果 newest_lang == en，则还要翻译 zh-cn, zh-tw, ja, ...
    # 如果 newest_lang == zh-cn，则还要翻译 en, zh-tw, ja, ...
    # 当然，这里你也可以直接翻译成除 newest_lang 以外的所有语言
    target_langs = [l for l in LANGUAGE_CODES if l != newest_lang]

    # 执行翻译
    for lang_code in target_langs:
        # 在这里做一次保护，如果 base_content 为空，直接跳过
        if not base_content.strip():
            continue

        translated_content = translate_with_gemini(base_content, LANGUAGE_FULL_NAMES[lang_code])
        new_file_name = "index.md" if lang_code == "en" else f"index.{lang_code}.md"
        new_file_path = os.path.join(dirpath, new_file_name)
        with open(new_file_path, "w", encoding="utf-8") as translated_file:
            translated_file.write(translated_content)
        print(f"Generated translation for {lang_code}: {new_file_path}")

    # 返回 True，表示已经进行了重新翻译，不需要再执行后续缺失逻辑
    return True


# 主函数：递归查找文件并翻译
def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
    posts_dir = os.path.join(root_dir, "posts")

    for dirpath, _, filenames in os.walk(posts_dir):
        md_files = [
            os.path.join(dirpath, filename)
            for filename in filenames
            if filename.startswith("index.") and filename.endswith(".md")
        ]

        if not md_files:
            continue  # 当前文件夹没有 index.*.md，跳过

        # -------------------
        # 新增的重新翻译逻辑
        # -------------------
        # 如果 check_and_regenerate_if_needed 返回 True，表示已经触发了删除旧文件并重翻译
        # 则不再执行后续的“缺失才补翻译”逻辑
        if check_and_regenerate_if_needed(dirpath, md_files):
            # 重新获取一下当前目录下的 md_files（因为旧文件已删除，新文件已创建）
            md_files = [
                os.path.join(dirpath, filename)
                for filename in os.listdir(dirpath)
                if filename.startswith("index.") and filename.endswith(".md")
            ]
            continue

        # -----------------------
        # 原来的“缺失才补翻译”逻辑
        # -----------------------
        # 提取已存在的语言
        existing_languages = set()
        for file_path in md_files:
            filename = os.path.basename(file_path)
            if filename == "index.md":
                existing_languages.add("en")
            else:
                lang_code = filename.split(".")[-2]
                existing_languages.add(lang_code)

        # 检查缺少的语言
        missing_languages = set(LANGUAGE_CODES) - existing_languages
        if missing_languages:
            print(f"Missing translations in {dirpath}: {missing_languages}")

            # 加载内容作为翻译基础
            base_content = load_existing_content(md_files, LANGUAGE_CODES)
            if not base_content:
                print(f"Warning: No suitable content found in {dirpath}, skipping.")
                continue

            # 翻译缺少的语言
            for lang_code in missing_languages:
                translated_content = translate_with_gemini(base_content, LANGUAGE_FULL_NAMES[lang_code])
                new_file_name = "index.md" if lang_code == "en" else f"index.{lang_code}.md"
                new_file_path = os.path.join(dirpath, new_file_name)
                with open(new_file_path, "w", encoding="utf-8") as translated_file:
                    translated_file.write(translated_content)
                print(f"Generated translation for {lang_code}: {new_file_path}")

        time.sleep(2)


if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    genai.configure(api_key=api_key)
    main()
