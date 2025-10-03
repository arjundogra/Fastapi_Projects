from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from database_connection import get_db
from models.borrowRecord import BorrowRecordRequest, BorrowRecord
from models.books import Books
from models.members import Members

borrowRecordRouter = APIRouter(tags=['BorrowRecords'])

@borrowRecordRouter.post('/add',status_code=status.HTTP_201_CREATED)
async def addBorrowRecord(req: BorrowRecordRequest,db: Session = Depends(get_db)):
    try:
        book_id = req.book_id
        member_id = req.member_id
        book = db.query(Books).filter(Books.id == book_id).first()
        member = db.query(Members).filter(Members.id == member_id).first()
        if book is None or member is None:
            raise HTTPException(status_code=404, detail="Book or Member Not Found")
        if not book.is_available:
            raise HTTPException(status_code=400, detail="Book is not available")
        db.add(BorrowRecord(**req.model_dump()))
        db.query(Books).filter(Books.id == book_id).update({"is_available": False})
        db.commit()
        return {"message": "Added Successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@borrowRecordRouter.post('/return/{id}',status_code=status.HTTP_200_OK)
def returnBook(id:int, db: Session = Depends(get_db)):
    try:
        record = db.query(BorrowRecord).filter(BorrowRecord.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Borrow Record Not Found")
        if record.return_date is not None:
            raise HTTPException(status_code=400, detail="Book already returned")
        book_id = record.book_id
        db.query(BorrowRecord).filter(BorrowRecord.id == id).update({"return_date": text('CURRENT_DATE')})
        db.query(Books).filter(Books.id == book_id).update({"is_available": True})
        db.commit()
        return {"message": "Book Returned Successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@borrowRecordRouter.get('/get')
async def getAllBorrowRecords(db: Session = Depends(get_db)):
    records = db.query(BorrowRecord).all()
    allRecords = []
    for record in records:
        allRecords.append({
            "id": record.id,
            "member_id": record.member_id,
            "member_name": record.member.name,
            "book_id": record.book_id,
            "book_name": record.book.name,
            "borrow_date": record.borrow_date,
            "return_date": record.return_date
        })
    return allRecords