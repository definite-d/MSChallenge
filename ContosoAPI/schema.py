from pydantic import BaseModel
from datetime import date


class LibraryStaff(BaseModel):
    staff_ID: int
    staff_firstname: str
    staff_lastname: str
    staff_mobilenumber: int
    staff_email: str
    staff_password: str
    staff_authsalt: str
    staff_category: str

    class Config:
        orm_mode = True


class Book(BaseModel):
    book_ID: int
    book_title: str
    book_edition: str
    book_author: str
    book_publisher: str
    book_copies: int
    book_costs: float
    book_remarks: str

    class Config:
        orm_mode = True


class Member(BaseModel):
    member_ID: int
    member_firstname: str
    member_lastname: str
    member_dateofbirth: date
    member_gender: str
    member_mobile: int
    member_email: str

    class Config:
        orm_mode = True


class BorrowersRecord(BaseModel):
    borrowers_ID: int
    member_ID: int
    staff_ID: int
    borrowers_dateborrowed: date
    borrowers_duereturndate: date

    class Config:
        orm_mode = True


class BorrowersRecordDetail(BaseModel):
    detail_ID: int
    borrowers_ID: int
    book_ID: int
    details_numberofcopies: int

    class Config:
        orm_mode = True


class BookReturnRecord(BaseModel):
    return_ID: int
    borrowers_ID: int
    return_datereturned: date

    class Config:
        orm_mode = True


class BookReturnRecordDetail(BaseModel):
    detail_ID: int
    return_ID: int
    book_ID: int
    details_numberofcopies: str

    class Config:
        orm_mode = True
