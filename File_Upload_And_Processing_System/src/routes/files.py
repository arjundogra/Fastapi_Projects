from fastapi import  APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.files import FileResponseModel
from database_connection import get_db
from models.files import Files
from core.auth import verify_access_token

router = APIRouter(prefix="/files", tags=["Files"])

@router.post('/upload', response_model=FileResponseModel)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), user_id = Depends(verify_access_token)):
    try:
        import os
        content = file.file.read()
        current_dir = os.getcwd()
        if not os.path.exists(f'{current_dir}/files'):
            os.makedirs(f'{current_dir}/files')
        with open(f'{current_dir}/files/{file.filename}','wb') as fw:
            fw.write(content)
        newData = Files(
            filename = file.filename,
            filepath = f'{current_dir}\files\{file.filename}',
            status = 'pending',
            uploaded_by = user_id
        )
        db.add(newData)
        db.commit()
        db.refresh(newData)
        return newData
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get('/', response_model=list[FileResponseModel])
async def get_all_files(db: Session = Depends(get_db), user_id = Depends(verify_access_token)):
    try:
        files = db.query(Files).filter(Files.uploaded_by == user_id).all()
        return files
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/{file_id}', response_model=FileResponseModel)
async def get_file(file_id: int, db: Session = Depends(get_db), user_id = Depends(verify_access_token)):
    try:
        file_record = db.query(Files).filter(Files.id == file_id, Files.uploaded_by == user_id).first()
        if not file_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return file_record
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    

@router.delete('/{file_id}')
async def delete_file(file_id: int, db: Session = Depends(get_db), user_id = Depends(verify_access_token)):
    try:
        file_record = db.query(Files).filter(Files.id == file_id, Files.uploaded_by == user_id).first()
        if not file_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        db.delete(file_record)
        db.commit()
        return {"detail": "File deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))