from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class PMState:
    user_id: str = "demo-user"
    project_id: Optional[str] = None

    idea_text: str = ""
    profile: Dict[str, Any] = field(default_factory=lambda: {
        "writing_style": "concise-bullets",
        "prd_template": "standard",
    })

    context_snippets: List[str] = field(default_factory=list)
    context_sources: List[Dict[str, str]] = field(default_factory=list)

    prd_markdown: str = ""
    agent_log: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        self.agent_log.append(message)
