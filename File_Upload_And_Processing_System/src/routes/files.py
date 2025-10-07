from fastapi import  APIRouter


router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/")
def read_root():
    return {"message": "File Upload And Processing System"}