from typing import Any, List
import json
from codescope.llm.client import LLMClient
from codescope.pipeline.builders.retrieval_query_builder import RetrievalQueryBuilder
from codescope.pipeline.builders.semantic_task_builder import SemanticTaskBuilder
from codescope.pipeline.intent_analyzer import IntentAnalyzer
from codescope.pipeline.requirement_parser import RequirementParser
from codescope.pipeline.validators.semantic_task_validator import SemanticTaskValidator


class SemanticExecutionPipeline:

    def __init__(
            self,
            llm: "LLMClient",
            requirement_parser: RequirementParser,
            intent_analyzer: "IntentAnalyzer",
            task_builder: "SemanticTaskBuilder",
            task_validator: "SemanticTaskValidator",
            query_builder: "RetrievalQueryBuilder",
    ):
        self.llm = llm
        self.requirement_parser = requirement_parser
        self.intent_analyzer = intent_analyzer
        self.task_builder = task_builder
        self.task_validator = task_validator
        self.query_builder = query_builder

    def run(self, raw_text: str) -> None:
        print("\n================ Phase 6 Dry Run ================\n")
        print("【Raw text】")
        print(raw_text)

        # 1. Requirement
        requirement = self.requirement_parser.parse(raw_text)
        print("\n【Requirement】")
        print(self._pretty(requirement))

        # 2. IntentAnalysis
        intent = self.intent_analyzer.analyze(requirement)
        print("\n【IntentAnalysis】")
        print(self._pretty(intent))

        # 3. SemanticTask 构建
        tasks = self.task_builder.build(intent)
        print("\n【SemanticTasks（Before Validation）】")
        print(self._pretty(tasks))

        # 4. SemanticTask 校验
        self.task_validator.validate_all(tasks)
        print("\n【SemanticTasks Validation】✓ PASSED")

        # 5. RetrievalQuery 构建
        queries = self.query_builder.build(tasks)
        print("\n【RetrievalQueries】")
        print(self._pretty(queries))

        print("\n================ Dry Run Finished ================\n")

    def _pretty(self, obj) -> str:
        """
        将任意对象格式化为美观的JSON字符串用于控制台输出。

        这个方法递归地处理嵌套对象和列表，确保最终的输出具有良好的可读性。
        支持Pydantic模型、dataclass、普通Python对象等。

        参数：
        ----------
        obj : Any
            需要格式化的对象，可以是：
            - 普通Python对象（有__dict__属性）
            - 列表或数组
            - 字典或其他可序列化的类型

        返回：
        ----------
        str
            格式化后的JSON字符串，具有以下特点：
            - 2个空格缩进
            - 保留Unicode字符（如中文）
            - 递归处理嵌套结构

        示例：
        ----------
        >>> _pretty({"name": "张三", "age": 25})
        {
          "name": "张三",
          "age": 25
        }

        >>> _pretty([SemanticTask(...), SemanticTask(...)])
        [
          {
            "task_id": "...",
            "intent": "...",
            ...
          },
          ...
        ]
        """
        # 处理普通Python对象（如Pydantic模型、dataclass等）
        if hasattr(obj, "__dict__"):
            # 直接使用对象的__dict__属性，将其转换为字典后序列化
            return json.dumps(obj.__dict__, ensure_ascii=False, indent=2)

        # 处理列表类型
        if isinstance(obj, list):
            # 递归地将列表中的每个元素转换为字典形式
            return json.dumps(
                [self._to_dict(o) for o in obj],
                ensure_ascii=False,
                indent=2,
            )

        # 处理其他可以直接序列化的类型（字典、字符串、数字等）
        return json.dumps(obj, ensure_ascii=False, indent=2)

    def _to_dict(self, obj):
        """
        递归地将任意对象转换为字典形式。

        这是_pretty方法的辅助方法，专门处理对象的深度转换。
        它会递归地处理对象的属性，包括嵌套对象和列表。

        参数：
        ----------
        obj : Any
            需要转换的对象，通常是：
            - 普通Python对象
            - Pydantic模型实例
            - dataclass实例
            - 列表或字典

        返回：
        ----------
        dict | Any
            - 如果obj有__dict__属性，返回转换后的字典
            - 如果是列表，递归转换每个元素
            - 其他情况直接返回原对象

        递归转换规则：
        ----------
        1. 对象 → 遍历所有属性键值对
        2. 列表 → 递归转换每个元素
        3. 嵌套对象 → 递归调用_to_dict
        4. 基本类型 → 直接保留

        示例：
        ----------
        >>> obj = SemanticTask(
                task_id="test",
                intent="测试",
                entities=[EntityRef(...), EntityRef(...)]
            )
        >>> _to_dict(obj)
        {
            "task_id": "test",
            "intent": "测试",
            "entities": [
                {"entity_type": "...", "name": "...", ...},
                ...
            ]
        }
        """
        # 检查是否是普通Python对象（包含__dict__属性）
        if hasattr(obj, "__dict__"):
            result = {}
            # 遍历对象的所有属性
            for key, value in obj.__dict__.items():
                # 跳过内部使用的私有属性（以_开头）
                if key.startswith("_"):
                    continue

                # 处理列表类型的属性值
                if isinstance(value, list):
                    # 递归转换列表中的每个元素
                    result[key] = [self._to_dict(item) for item in value]
                # 处理嵌套对象类型的属性值
                elif hasattr(value, "__dict__"):
                    result[key] = self._to_dict(value)
                # 处理基本类型（字符串、数字、布尔值等）
                else:
                    result[key] = value
            return result

        # 如果对象没有__dict__属性，直接返回（如字符串、数字、None等）
        return obj
