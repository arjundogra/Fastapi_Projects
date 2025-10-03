from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from database_connection import get_db
from models.members import Members, MemberCreateRequest, MemberResponse

memberRouter = APIRouter()

@memberRouter.post('/create',status_code=status.HTTP_201_CREATED)
def createMember(req: MemberCreateRequest, db : Session = Depends(get_db)):
    try:
        db_member = db.execute(text(f"Select * from members where email = '{req.email}'")).first()
        if db_member:
            raise HTTPException(status_code=400, detail="Email already registered")
        db.add(Members(**req.model_dump()))
        db.commit()
        return {"message":"Member Created Successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@memberRouter.get('/getAll', response_model= list[MemberResponse])
def getAllMembers(db: Session = Depends(get_db)):
    try:
        members = db.query(Members).all()
        return members
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@memberRouter.delete('/delete/{id}',status_code=status.HTTP_200_OK)
def deleteMember(id: int, db: Session = Depends(get_db)):
    try:
        member = db.query(Members).filter(Members.id == id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member Not Found")
        db.delete(member)
        db.commit()
        return {"message": "Deleted successfully", "id": id}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))