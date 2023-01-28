"""
Models Script

Responsible for the concept of Object Relational Mapping within this project.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Table
from sqlalchemy.orm import relationship
from db import meta

CASCADE = 'CASCADE'


LibraryStaff = Table(
    'librarystaff', meta, 
    Column('staff_ID', Integer, primary_key=True, autoincrement=True, index=True),
    Column('staff_firstname', String(64)),
    Column('staff_lastname', String(64)),
    Column('staff_mobilenumber', Integer),
    Column('staff_email', String(128), unique=True),
    Column('staff_password', String(256)),
    Column('staff_authsalt', String(128)),
    Column('staff_category', String(128)),
    # relationship('staff', 'BorrowersRecords', back_populates='staff')
)
    

Books = Table(
    'books', meta,
     Column('book_ID', Integer, primary_key=True, autoincrement=True, index=True),
     Column('book_title', String(64)),
     Column('book_edition', String(64)),
     Column('book_author', String(64)),
     Column('book_publisher', String(64)),
     Column('book_copies', Integer),
     Column('book_costs', Float(2)),
     Column('book_remarks', String(256)),
    # borrow_record_details = relationship('BorrowersRecordDetails', back_populates='book')
)

Members = Table(
    'members', meta,
    Column('member_ID', Integer, primary_key=True, autoincrement=True, index=True),
    Column('member_firstname', String(64)),
    Column('member_lastname', String(64)),
    Column('member_dateofbirth', Date),
    Column('member_gender', String(16)),
    Column('member_mobile', Integer),
    Column('member_email', String(128)),
    # borrower_record = relationship('BorrowersRecords', back_populates='member')
)

BorrowersRecords = Table(
    'borrowersrecords', meta,
    Column('borrowers_ID', Integer, primary_key=True, autoincrement=True, index=True),
    Column('member_ID', Integer, ForeignKey('members.member_ID', ondelete=CASCADE)),
    Column('staff_ID', Integer, ForeignKey('librarystaff.staff_ID', ondelete=CASCADE)),
    Column('borrowers_dateborrowed', Date),
    Column('borrowers_duereturndate', Date),
    # member = relationship('Members', back_populates='borrower_record')
    # relationship('staff', 'LibraryStaff', back_populates='borrower_record')
    # details = relationship('BorrowersRecordDetails', back_populates='record')
)

BorrowersRecordDetails = Table(
    'borrowersrecorddetails', meta,
    Column('details_ID', Integer, primary_key=True, autoincrement=True, index=True),
    Column('borrowers_ID', Integer, ForeignKey('BorrowersRecords.borrowers_ID')),
    Column('book_ID', Integer, ForeignKey('Books.book_ID')),
    Column('detail_numberofcopies', Integer),
    # record = relationship('BorrowersRecords', back_populates='details')
    # book = relationship('Books', back_populates='borrow_record_details')
)

BookReturnRecords = Table(
    'bookreturnrecords', meta,
    Column('return_ID', Integer, primary_key=True, autoincrement=True, index=True),
    Column('borrowers_ID', ForeignKey('BorrowersRecords.borrowers_ID')),
    Column('return_datereturned', Date),
    # borrower = relationship('BorrowersRecords')
)


BookReturnRecordDetails = Table(
    'BookReturnRecordDetails', meta,
    Column('detail_ID', Integer, primary_key=True, autoincrement=True, index=True),
    Column('return_ID', ForeignKey('BookReturnRecords.return_ID')),
    Column('book_ID', ForeignKey('Books.book_ID')),
    Column('details_numberofcopies', String(64)),
)

