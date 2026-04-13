def extract_main_content(text: str) -> str:
    if "### 正文" not in text:
        return text.strip()
    part = text.split("### 正文", 1)[1]
    if "### 结构化总结" in part:
        part = part.split("### 结构化总结", 1)[0]
    return part.strip()
