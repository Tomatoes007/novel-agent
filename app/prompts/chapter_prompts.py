CHAPTER_WRITE_TEMPLATE = """
请根据以下资料写出本章正文。

【项目定位】
{project_profile}

【当前卷目标】
{volume_goal}

【当前章节大纲】
{chapter_outline}

【相关角色卡】
{character_cards}

【世界观规则】
{world_rules}

【最近章节摘要】
{recent_summaries}

【当前未回收伏笔】
{open_foreshadowings}

【语义检索召回的历史记忆】
{retrieved_memories}

【额外要求】
{extra_requirements}

写作要求：
1. 本章必须围绕当前章节目标推进。
2. 不要重复前文已经交代清楚的信息。
3. 主角行为必须符合人设。
4. 本章至少包含一个有效冲突。
5. 结尾必须有明显钩子。
6. 字数控制在 {word_count} 左右。

请按以下格式输出：

### 正文
（这里写正文）

### 结构化总结
```json
{{
  "title": "",
  "chapter_summary": "",
  "new_characters": [],
  "new_locations": [],
  "new_items": [],
  "new_foreshadowing": [],
  "resolved_foreshadowing": [],
  "relationship_changes": [],
  "power_changes": [],
  "timeline_events": []
}}
```
"""
