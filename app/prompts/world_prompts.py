WORLD_TEMPLATE = """
请为以下小说生成世界观设定，并直接输出 JSON 对象。

作品名：{title}
题材：{genre}
平台：{platform_style}
基调：{tone}
简介：{summary}

JSON 至少包含：
{{
  "world_background": "",
  "power_system": {{}},
  "factions": [],
  "locations": [],
  "world_rules": [],
  "taboos": [],
  "resources": []
}}
"""
