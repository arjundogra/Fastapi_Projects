from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from database_connection import get_db
from models.books import Books, BooksRequest, BooksResponse

bookRouter = APIRouter(tags=['Books'])

@bookRouter.post('/add',status_code=status.HTTP_201_CREATED)
async def addBook(req: BooksRequest, db: Session = Depends(get_db)):
    try:
        db.add(Books(**req.model_dump()))
        db.commit()
        return "Added Successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@bookRouter.get('/get', response_model= list[BooksResponse])
async def getBooks(db: Session = Depends(get_db)):
    # books : list[Books] = db.execute(text('Select * from books')).all()
    books : list[Books] = db.query(Books).all()
    return books

@bookRouter.get('/get/{id}',response_model=BooksResponse)
async def getBookById(id, db: Session = Depends(get_db)):
    try:
        # book = db.query(Books).filter(Books.id == id).first()
        book = db.execute(text(f'Select * from Books where id = {id}')).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book Not Found")
        return book
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@bookRouter.patch('/update/{id}',status_code=status.HTTP_200_OK)
def updateBook(id: int, req: BooksRequest = Body(...), db: Session = Depends(get_db)):
    Book = db.query(Books).filter(Books.id == id).first()
    for key,val in req.model_dump(exclude_unset=True).items():
        setattr(Book,key,val)
    db.commit()
    return "Updated"


@bookRouter.delete('/delete/{id}',status_code=status.HTTP_200_OK)
async def deleteById(id: int ,db:Session = Depends(get_db)):
    try:
        book = db.query(Books).filter(Books.id == id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book Not found")
        db.delete(book)
        db.commit()
        return {"message": "Deleted successfully", "id": id}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))