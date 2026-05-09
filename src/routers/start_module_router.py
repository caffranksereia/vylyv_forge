from fastapi import APIRouter

router = APIRouter(prefix="/start_module", tags=["start_module"])


@router.get("/")
def list_start_module() -> list[dict]:
    return []


@router.get("/{item_id}")
def get_start_module(item_id: str) -> dict[str, str]:
    return {
        "id": item_id,
        "message": "Start_Module found.",
    }


@router.post("/")
def create_start_module() -> dict[str, str]:
    return {
        "message": "Start_Module created.",
    }


@router.put("/{item_id}")
def update_start_module(item_id: str) -> dict[str, str]:
    return {
        "id": item_id,
        "message": "Start_Module updated.",
    }


@router.delete("/{item_id}")
def delete_start_module(item_id: str) -> dict[str, str]:
    return {
        "id": item_id,
        "message": "Start_Module deleted.",
    }
