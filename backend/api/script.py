from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.core.script_writer import ScriptRequest, ScriptWriterService

router = APIRouter(prefix="/script", tags=["대본 작성"])
_service = ScriptWriterService()


class GenerateRequest(BaseModel):
    source_title: str = Field(..., examples=["발리 여행이 위험해진 이유 - 현지인도 모르는 충격 사실"])
    source_body: str = Field(..., examples=["최근 발리에서..."])
    source_url: str = Field(default="")
    tone: str = Field(default="storytelling")
    language: str = Field(default="ko")
    target_duration_min: int = Field(default=10, ge=3, le=30)
    channel_intro: str = Field(default="")
    channel_outro: str = Field(default="")


class GenerateResponse(BaseModel):
    id: str
    title: str
    source_title: str
    tone: str
    full_text: str
    sections: list[dict]
    total_duration_sec: int
    saved_path: str
    created_at: str


@router.post("/generate", response_model=GenerateResponse)
async def generate_script(req: GenerateRequest):
    script_req = ScriptRequest(
        source_title=req.source_title,
        source_body=req.source_body,
        source_url=req.source_url,
        tone=req.tone,
        language=req.language,
        target_duration_min=req.target_duration_min,
        channel_intro=req.channel_intro,
        channel_outro=req.channel_outro,
    )
    result = _service.generate_and_save(script_req)
    return GenerateResponse(**result)


@router.get("/tones")
async def get_tones():
    return {
        "tones": [
            {"id": "informative",  "label": "정보 전달형", "desc": "명확하고 신뢰감 있는 어조"},
            {"id": "storytelling", "label": "스토리텔링형", "desc": "감성적이고 몰입감 있는 서술"},
            {"id": "humor",        "label": "유머형",      "desc": "유머와 위트를 곁들인 친근한 어조"},
            {"id": "dramatic",     "label": "드라마틱형",  "desc": "긴장감과 감동을 극대화하는 어조"},
        ]
    }
