class PromptService:
    @staticmethod
    def render(template: str, **kwargs) -> str:
        return template.format(**kwargs)
