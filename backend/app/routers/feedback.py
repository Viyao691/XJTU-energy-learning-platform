"""Same-origin feedback submission for visitors and signed-in website users."""
from fastapi import Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.feedback import save_feedback


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    message: str = Field(min_length=1, max_length=1000)
    contact: str | None = Field(default=None, max_length=200)


class FeedbackResponse(BaseModel):
    message: str


def register_feedback_routes(app, get_db) -> None:
    @app.post("/api/v1/feedback", response_model=FeedbackResponse)
    def submit_feedback(payload: FeedbackRequest, request: Request, response: Response, db: Session = Depends(get_db)):
        sent = save_feedback(db, request, payload.message, payload.contact or None)
        response.headers["Cache-Control"] = "private, no-store"
        return FeedbackResponse(message="反馈已保存，管理员通知已提交" if sent else "反馈已保存，管理员通知暂时延迟")
