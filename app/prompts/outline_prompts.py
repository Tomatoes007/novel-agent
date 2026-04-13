OUTLINE_TEMPLATE = """
请为以下作品生成第 {volume_no} 卷大纲，并直接输出 JSON。

作品名：{title}
题材：{genre}
平台：{platform_style}
基调：{tone}
简介：{summary}

角色卡：
{character_cards}

世界观：
{world_rules}

请生成 {chapter_count} 章，格式如下：
{{
  "volume_title": "",
  "volume_goal": "",
  "major_conflict": "",
  "end_hook": "",
  "chapters": [
    {{
      "chapter_no": 1,
      "title": "",
      "chapter_goal": "",
      "conflict": "",
      "new_information": "",
      "foreshadowing": [],
      "cliffhanger": ""
    }}
  ]
}}
"""
