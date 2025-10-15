from fastapi import  APIRouter, UploadFile, File, Depends, HTTPException, status


router = APIRouter(prefix="/files", tags=["Files"])

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        content = file.file.read()
        with open(file.filename,'wb') as fw:
            fw.write(content)
        return {"filename": file.filename, "content_type": file.content_type}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))