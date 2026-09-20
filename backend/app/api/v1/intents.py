from fastapi import APIRouter

from backend.app.intents.models import IntentRequest, IntentResult
from backend.app.intents.service import IntentService

router = APIRouter(prefix="/intents", tags=["intents"])
_service = IntentService()


@router.post("", response_model=IntentResult)
def classify_intent(request: IntentRequest) -> IntentResult:
    return _service.classify(request.text)
