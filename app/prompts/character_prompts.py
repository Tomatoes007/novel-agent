CHARACTER_TEMPLATE = """
请基于以下项目信息生成 {character_count} 个核心角色，并直接输出 JSON 数组。

作品名：{title}
题材：{genre}
平台：{platform_style}
基调：{tone}
简介：{summary}

每个角色包含字段：
- name
- role
- identity
- personality_traits
- core_motivation
- weakness
- secret
- speaking_style
- growth_arc
- taboo
- first_appearance_chapter
- current_state
"""
