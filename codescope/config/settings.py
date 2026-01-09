from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-large"

    class Config:
        env_file = ".env"

settings = Settings()


INSTRUCTION_TEMPLATES = {
    "java_backend": {
        "role": "你是一个资深的 Java 后端开发工程师",
        "constraints": [
            "Use Spring Boot 3.x",
            "使用 DDD 架构",
            "Use Lombok for boilerplate code",
            "Add proper logging"
        ],
        "output_requirements": [
            "Provide code only",
            "Do not include explanations",
            "Use Markdown format"
        ]
    },
    "python_script": {
        "role": "你是一个资深 Python 开发工程师",
        "constraints": [
            "遵循 PEP8 风格",
            "编写可复用函数",
            "添加必要注释"
        ],
        "output_requirements": [
            "Provide code only",
            "Do not include explanations",
            "Use Markdown format"
        ]
    }
}
