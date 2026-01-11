"""
Template Index（Phase 2.5）。

职责：
- 管理 Template Profile
- 提供基于 Requirement 的候选模板集合
"""

import json
from pathlib import Path
from typing import List, Dict


class TemplateIndex:
    def __init__(self, profile_dir: str):
        self.profile_dir = Path(profile_dir)
        self.profiles: List[Dict] = []

    def load_profiles(self):
        """
        加载所有 Template Profile JSON 文件。
        """
        for file in self.profile_dir.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                self.profiles.append(json.load(f))

    def list_profiles(self) -> List[Dict]:
        """
        返回所有模板 Profile。
        """
        return self.profiles
