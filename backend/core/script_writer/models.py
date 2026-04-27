from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ScriptSection:
    type: str    # intro | main | outro
    content: str
    duration_sec: int = 0


@dataclass
class Script:
    id: str
    title: str
    source_title: str
    source_url: str
    tone: str
    sections: list[ScriptSection]
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def full_text(self) -> str:
        return "\n\n".join(s.content for s in self.sections)

    @property
    def total_duration_sec(self) -> int:
        return sum(s.duration_sec for s in self.sections)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "source_title": self.source_title,
            "source_url": self.source_url,
            "tone": self.tone,
            "sections": [{"type": s.type, "content": s.content, "duration_sec": s.duration_sec} for s in self.sections],
            "full_text": self.full_text,
            "total_duration_sec": self.total_duration_sec,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ScriptRequest:
    source_title: str
    source_body: str
    source_url: str = ""
    tone: str = "informative"       # informative | storytelling | humor | dramatic
    language: str = "ko"            # ko | en
    target_duration_min: int = 10   # 목표 영상 길이(분)
    channel_intro: str = ""         # 채널 고정 인트로 문구
    channel_outro: str = ""         # 채널 고정 아웃트로 문구
