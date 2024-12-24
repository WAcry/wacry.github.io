import os
import glob
import time

import google.generativeai as genai

# 创建生成模型
generation_config = {
    "temperature": 1,
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
LANGUAGE_FULL_NAMES = {"en": "English", "zh-cn": "Simplified Chinese", "zh-tw": "Traditional Chinese", "ja": "Japanese",
                       "de": "German", "es": "Spanish", "fr": "French", "hi": "Hindi", "it": "Italian", "ko": "Korean",
                       "pt": "Portuguese", "ru": "Russian", "tr": "Turkish", "vi": "Vietnamese"}


# 翻译函数
def translate_with_gemini(input_text, target_language):
    prompt = f"""
Translate the following file content to {target_language}. Retain formatting, code blocks, and styles. Do not use ``` to wrap the whole content. Here's the file content:  
{input_text}
    """
    retries = 0
    max_retries = 5
    while retries < max_retries:
        try:
            time.sleep(2)
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            return response.text.strip()
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
    api_key = input("Enter your Gemini API key: ")
    genai.configure(api_key=api_key)
    main()
