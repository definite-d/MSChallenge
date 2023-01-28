"""
ContosoAPI

Project submission for the NACOSS GEPICT Conference task by Microsoft.
Developed by Afam-Ifediogor U. Divine (divineafam@gmail.com).'
"""

# Imports ______________________________________________________________________________________________________________
from fastapi import FastAPI
from db import con
from models import LibraryStaff, Books, Members, BorrowersRecords, BorrowersRecordDetails, BookReturnRecords, \
    BookReturnRecordDetails
from schema import LibraryStaff, Book, Member, BorrowersRecord, BorrowersRecordDetail, BookReturnRecord, \
    BookReturnRecordDetail
from datetime import date, timedelta, datetime


# Version ______________________________________________________________________________________________________________
__version__ = '1.0.2'


# API Setup ____________________________________________________________________________________________________________
api = FastAPI(
    title='ContosoAPI',
    description='Project submission for the NACOSS GEPICT Conference task by Microsoft. '
                'Developed by Afam-Ifediogor U. Divine (divineafam@gmail.com).',
    version=__version__,
    docs_url='/docs',
    debug=True,  # TODO: Change this to False before publishing.
)


# Internal Functions ___________________________________________________________________________________________________
def _borrowed_within_given_duration(record, number_of_days=30):
    """
    Internal function.

    Performs the actual datetime comparison.
    :param record: `record` is a single `BorrowersRecord.borrowers_dateborrowed`.
    :param number_of_days: `number_of_days` is the number of elapsed days to check for.
    :return: True if the book actually was borrowed within the given duration.
    """
    if (date.today() - record.date()).days <= number_of_days:
        return True
    return False


def _borrowed_between_given_dates(record, date_from: date, date_to: date):
    """
    Internal function.

    Checks if a record was borrowed between the start and end dates.
    :param record: `record` is a single `BorrowersRecord.borrowers_dateborrowed`.
    :param date_from: The first date bracket
    :param date_to: The second date bracket
    :return: True if the book actually was borrowed less than 30 days ago.
    """
    if date_from <= record.date() <= date_to:
        print(date_from, record.date(), date_to)
        return True
    return False


# API Endpoints ________________________________________________________________________________________________________
@api.get('/')
async def index():
    """
    "Homepage" of the API; gets basic information about the project.
    """
    return {
        'status': 200,
        'title': 'ContosoAPI',
        'description': 'Project submission for the NACOSS GEPICT Conference task by Microsoft. '
                       'Developed by Afam-Ifediogor U. Divine (divineafam@gamil.com).',
        'version': __version__,
        'developer': 'Afam-Ifediogor U. Divine',
        'developer_email': 'divineafam@gmail.com',
        'developer_github': 'https://github.com/definite-d/'
    }


@api.get('/books')
async def get_books():
    """
    Gets all books from the database.
    """
    return con.execute(Books.select()).fetchall()


@api.post('/books')
async def post_books(book: Book):
    """
    Posts (creates) a new book from scratch with supplied data.
    """
    data = con.execute(Books.insert().values(
        book_ID=book.book_ID,
        book_title=book.book_title,
        book_edition=book.book_edition,
        book_author=book.book_author,
        book_publisher=book.book_publisher,
        book_copies=book.book_copies,
        book_costs=book.book_costs,
        book_remarks=book.book_remarks,
    ))
    return data.is_insert


@api.get('/books/byauthor/{author}')
async def get_books_by_author(author: str):
    """
    Gets all books by a specific author.
    """
    return con.execute(Books.select().where(Books.c.book_author == author)).fetchall()


@api.get('/books/bypublisher/{publisher}')
async def get_books_by_author(publisher: str):
    """
    Gets all books published by a specific publisher.
    """
    return con.execute(Books.select().where(Books.c.book_publisher == publisher)).fetchall()


@api.get('/books/borrowed/approvedby/{staff_id}')
async def approved_by(staff_id: int):
    """
    Gets all book objects approved for borrowing by a LibraryStaff.
    """
    relevant_borrowers = [
        entry['borrowers_ID'] for entry in con.execute(BorrowersRecords.select()).fetchall()
        if entry['staff_ID'] == staff_id
    ]
    borrowers_details = []
    for borrowers_id in relevant_borrowers:
        try:
            borrowers_details.append(
                con.execute(
                    BorrowersRecordDetails.select().where(BorrowersRecordDetails.c.borrowers_ID == borrowers_id))
                .fetchone()['book_ID']
            )
        except TypeError:
            continue
    result = []
    for book_ID in borrowers_details:
        result.append(
            con.execute(Books.select().where(Books.c.book_ID == book_ID)).fetchone()
        )
    return result


@api.get('/books/borrowed/last30days')
async def get_books_borrowed_within_30_days():
    """
    Gets all book objects that have been borrowed within the last 30 days.
    """
    relevant_borrowers = [
        entry['borrowers_ID'] for entry in con.execute(BorrowersRecords.select()).fetchall()
        if _borrowed_within_given_duration(entry['borrowers_dateborrowed'])
    ]
    borrowers_details = []
    for borrowers_id in relevant_borrowers:
        try:
            borrowers_details.append(
                con.execute(
                    BorrowersRecordDetails.select().where(BorrowersRecordDetails.c.borrowers_ID == borrowers_id))
                .fetchone()['book_ID']
            )
        except TypeError:
            continue
    result = []
    for book_ID in borrowers_details:
        result.append(
            con.execute(Books.select().where(Books.c.book_ID == book_ID)).fetchone()
        )
    return result


@api.get('/books/borrowed/{member_id}')
async def get_books_borrowed_by_user_id(member_id: int):
    """
    Gets all the books borrowed by a specific `member_ID`.
    """
    relevant_borrowers = [
        entry['borrowers_ID'] for entry in con.execute(
            BorrowersRecords.select().where(BorrowersRecords.c.member_ID == member_id)
        ).fetchall()
    ]
    borrowers_details = []
    for borrowers_id in relevant_borrowers:
        try:
            borrowers_details.append(
                con.execute(
                    BorrowersRecordDetails.select().where(BorrowersRecordDetails.c.borrowers_ID == borrowers_id))
                .fetchone()['book_ID']
            )
        except TypeError:
            continue
    result = []
    for book_ID in borrowers_details:
        result.append(
            con.execute(Books.select().where(Books.c.book_ID == book_ID)).fetchone()
        )
    return result


@api.get('/books/borrowed/{date_from}/{date_to}')
async def get_books_borrowed_between_given_dates(date_from: date, date_to: date):
    """
    Gets any books borrowed between a given date bracket.
    """
    relevant_borrowers = [
        entry['borrowers_ID'] for entry in con.execute(BorrowersRecords.select()).fetchall()
        if _borrowed_between_given_dates(entry['borrowers_dateborrowed'], date_from, date_to)
    ]
    borrowers_details = []
    for borrowers_id in relevant_borrowers:
        try:
            borrowers_details.append(
                con.execute(BorrowersRecordDetails.select().where(BorrowersRecordDetails.c.borrowers_ID == borrowers_id))
                .fetchone()['book_ID']
            )
        except TypeError:
            continue
    result = []
    for book_ID in borrowers_details:
        result.append(
            con.execute(Books.select().where(Books.c.book_ID == book_ID)).fetchone()
        )
    return result


@api.get('/books/{book_id}')
async def get_book_by_id(book_id: int):
    """
    Gets a specific book by the `book_ID` property of that book.
    """
    return con.execute(Books.select().where(Books.c.book_ID == book_id)).fetchone()


@api.put('/books/{book_id}')
async def put_book_by_id(book_id: int, book: Book):
    """
    Puts (updates) the data of a specific book, except for the `book_ID`.
    """
    return con.execute(Books.update(
        book_title=book.book_title,
        book_edition=book.book_edition,
        book_author=book.book_author,
        book_publisher=book.book_publisher,
        book_copies=book.book_copies,
        book_costs=book.book_costs,
        book_remarks=book.book_remarks,
    ).where(Books.c.book_ID == book_id))


@api.delete('/books/{book_id}')
async def get_book_by_id(book_id: int):
    """
    Deletes an entry for a book from the database.
    """
    con.execute(Books.delete().where(Books.c.book_ID == book_id))
    return get_books()


@api.get('/borrowed')
async def get_borrowed():
    """
    Gets all borrower events.
    """
    return con.execute(BorrowersRecords.select()).fetchall()


@api.post('/borrowed')
async def post_borrowed(borrowersrecord: BorrowersRecord):
    """
    Posts (creates) a new borrower record from scratch with supplied data.
    """
    data = con.execute(BorrowersRecords.insert().values(
        borrowers_ID=borrowersrecord.borrowers_ID,
        member_ID=borrowersrecord.member_ID,
        staff_ID=borrowersrecord.staff_ID,
        borrowers_dateborrowed=borrowersrecord.borrowers_dateborrowed,
        borrowers_duereturndate=borrowersrecord.borrowers_duereturndate,
    ))
    return data.is_insert


@api.get('/borrowed/{borrowers_id}')
async def get_borrowed_by_id(borrowers_id: int):
    """
    Gets a specific borrower by the `borrowers_ID` property of that book.
    """
    return con.execute(BorrowersRecords.select().where(BorrowersRecords.c.borrowers_ID == borrowers_id)).fetchall()


@api.put('/borrowed/{borrowers_id}')
async def put_borrowed_by_id(borrowers_id: int, borrowersrecord: BorrowersRecord):
    """
    Puts (updates) the data of a specific borrower, except for the `borrowers_ID`.
    """
    data = con.execute(BorrowersRecords.update(
        borrowers_ID=borrowersrecord.borrowers_ID,
        member_ID=borrowersrecord.member_ID,
        staff_ID=borrowersrecord.staff_ID,
        borrowers_dateborrowed=borrowersrecord.borrowers_dateborrowed,
        borrowers_duereturndate=borrowersrecord.borrowers_duereturndate,
    ).where(BorrowersRecords.c.borrowers_ID == borrowers_id))
    return data.is_insert


@api.delete('/borrowed/{borrowers_id}')
async def delete_borrowed_by_id(borrowers_id: int):
    """
    Deletes an entry for a borrower from the database.
    """
    con.execute(BorrowersRecords.delete().where(BorrowersRecords.c.borrowers_ID == borrowers_id))
    return get_borrowed()
        

@api.get('/returned')
async def get_returned():
    """
    Gets all borrower events.
    """
    return con.execute(BookReturnRecords.select()).fetchall()


@api.post('/returned')
async def post_returned(returnrecord: BookReturnRecord):
    """
    Posts (creates) a new borrower record from scratch with supplied data.
    """
    data = con.execute(BookReturnRecords.insert().values(
        return_ID=returnrecord.return_ID,
        borrowers_ID=returnrecord.borrowers_ID,
        return_datereturned=returnrecord.return_datereturned,
    ))
    return data.is_insert


@api.get('/returned/{return_id}')
async def get_returned_by_id(return_id: int):
    """
    Gets a specific borrower by the `return_ID` property of that book.
    """
    return con.execute(BookReturnRecords.select().where(BookReturnRecords.c.return_ID == return_id)).fetchall()


@api.put('/returned/{return_id}')
async def put_returned_by_id(return_id: int, returnrecord: BookReturnRecord):
    """
    Puts (updates) the data of a specific borrower, except for the `return_ID`.
    """
    data = con.execute(BookReturnRecords.update(
        borrowers_ID=returnrecord.borrowers_ID,
        return_datereturned=returnrecord.return_datereturned,
    ).where(BookReturnRecords.c.return_ID == return_id))
    return data.is_insert


@api.delete('/returned/{return_id}')
async def delete_returned_by_id(return_id: int):
    """
    Deletes an entry for a borrower from the database.
    """
    con.execute(BookReturnRecords.delete().where(BookReturnRecords.c.return_ID == return_id))
    return get_returned()
