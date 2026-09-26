from fastapi import APIRouter

from backend.app.tools.system import OpenAppTool

router = APIRouter(prefix="/system", tags=["system"])
_tool = OpenAppTool()


@router.get("/apps")
def list_apps() -> dict:
    return {"apps": sorted(_tool.ALLOWED_APPS)}


@router.post("/apps/open")
def open_app(app: str) -> dict:
    result = _tool.execute(_tool.validate({"app": app}))
    return result.model_dump()
