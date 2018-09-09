# Assignment 7: The Book Browser application displays a list of books found in the Books database.
# The user can sort the list by Title or Author, search by a specified value across all columns,
# and view the details of a selected book from the list.

import tkinter
import sqlite3
import os

db = None  # initialize the global variable for the database connection


class BookBrowser:
    def __init__(self, rows):
        # GUI information
        font = "Arial 14 normal"
        padding = 10
        bg_color = "MediumTurquoise"
        btn_bg_color = "PaleTurquoise"
        btn_padding = 25
        btn_font="Arial 10 normal"

        self.main_window = tkinter.Tk()
        self.main_window.configure(background=bg_color)
        self.main_window.title("Award Winning Books")
        self.main_window.geometry('1000x780')  # (width x height)

        try:
            # Header
            tkinter.Label(self.main_window, text="Award Winning Books Browser", font=font, padx=padding, pady=padding, background=bg_color).grid(row=0, columnspan=4)

            # Title and Author sort Buttons.
            # When a button is clicked, the self.sort_books function is called to display the books in Title or Author order
            tkinter.Button(self.main_window, text='Title', background=btn_bg_color, padx=btn_padding, font=btn_font, command=lambda: self.sort_books('Title')).grid(row=1, column=0)
            tkinter.Button(self.main_window, text='Author', background=btn_bg_color, padx=btn_padding, font=btn_font, command=lambda: self.sort_books('Author')).grid(row=1, column=1)

            # Search Entry field and Button.
            # Entry field can be used by the user to specify a search value.
            # When the search Button is clicked, the self.search_books function is called to find all books that contain the search value in any of its columns
            self.searchvalue = tkinter.StringVar()
            self.searchterm_entry = tkinter.Entry(self.main_window, textvariable=self.searchvalue, width=20).grid(row=1, column=2)
            tkinter.Button(self.main_window, text='Search', command=self.search_books, background=btn_bg_color, padx=btn_padding, font=btn_font).grid(row=1, column=3)

            # When the window is initially displayed, all books in the database are displayed
            self.display_rows(rows)

            tkinter.mainloop()
        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred: ', err)


    # Display the Title and Author of the books found in the rows variable.
    # This function is called when the window is initially displayed, and by the sort and search functions.
    # It is a general purpose function that displays whatever rows are passed to it.
    def display_rows(self, rows):
        #GUI customization variables
        padding_side = 20
        padding_len = 5
        font = "Garamond 11 normal"
        bg_color = "MediumTurquoise"
        # Clear any previous rows of data before displaying the books found in the rows variable
        for label in self.main_window.grid_slaves():
            if int(label.grid_info()['row']) > 1:
                label.grid_forget()
        self.clear_book_details()    # clear book details (if present)

        # Book titles are displayed as labels with a Radiobutton.
        # Each Radiobutton has a variable with a unique value defined by the book ISBN (self.book_isbn)
        self.book_isbn = tkinter.StringVar()    # variable, with a unique value, that is associated with each book
        self.book_isbn.set("not selected yet")  # forces the radio buttons to initially display as not selected

        try:
            if rows==[]:
                tkinter.Label(self.main_window, text="No results found",padx=padding_side, font=font, background=bg_color).grid(row=2)
            else:
                # Loop through each tuple in the rows variable and create a Radiobutton with the book Title, followed by a Label with the Author
                r = 2
                for book in rows:
                    tkinter.Radiobutton(self.main_window, text=book[1], variable=self.book_isbn, value=book[0], command=self.get_book_details, padx=padding_side, font=font, background=bg_color).grid(row=r, column=0, sticky=tkinter.constants.W)
                    tkinter.Label(self.main_window, text=book[2], padx=padding_side, font=font, background=bg_color).grid(row=r, column=1, sticky=tkinter.constants.W)
                    r += 1
        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred: ', err)

    # Sort the books by the value in the column variable.
    def sort_books(self, column):
        # Clear the book details (if present) before displaying the sorted results
        self.clear_book_details()

        # Create the SQL statement, execute the query, fetch the results, and call self.display_rows(rows)
        try:
            cursor = db.cursor()
            sql = "SELECT * FROM book ORDER BY " + column
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.display_rows(rows)
        except sqlite3.IntegrityError as err:
            print('Integrity Error:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error:', err)
        except sqlite3.Error as err:
            print('Error:', err)

    # Search the books by the value specified in the search Entry field.
    # The list of books should contain all books where any column contains the search value
    def search_books(self):
        value = self.searchvalue.get()  # "user-specified search value"

        # Create the SQL statement, execute the query, fetch the results, and call self.display_rows(rows)
        try:
            cursor = db.cursor()
            sql = "SELECT * FROM book WHERE isbn LIKE '%" + value + "%' OR title LIKE '%" + value + "%' OR author LIKE '%" + value + "%' OR publisher LIKE '%" + value + "%' OR format LIKE '%" + value + "%' OR subject LIKE '%" + value + "%'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.display_rows(rows)
        except sqlite3.IntegrityError as err:
            print('Integrity Error:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error:', err)
        except sqlite3.Error as err:
            print('Error:', err)

    # When the user clicks a Radiobutton, use the associated ISBN to query the database for that specific book.
    def get_book_details(self):
        isbn = self.book_isbn.get() #"ISBN value associated with the book Title that was clicked"
        # Create the SQL statement, execute the query, fetch the results.
        # Call self.display_book_details(rows) to display the details for the book (ISBN, Title, Author, Publisher, Format, Subject)
        try:
            cursor = db.cursor()
            sql = "SELECT * FROM book WHERE isbn ='" + isbn + "'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.display_book_details(rows)
        except sqlite3.IntegrityError as err:
            print('Integrity Error:', err)
        except sqlite3.OperationalError as err:
            print('Operational Error:', err)
        except sqlite3.Error as err:
            print('Error:', err)

    # Display the details for a specific book
    def display_book_details(self, rows):
        # Clear the previous book details (if present)
        self.clear_book_details()

        # GUI customization variables
        bg_color = "White"
        bg_color_heading = "MediumSpringGreen"
        font = "Arial 12 normal"
        padding=5
        padding_header = 30

        # Create a frame inside of the grid to contain the book details
        self.details_frame = tkinter.Frame(self.main_window, background=bg_color)
        self.details_frame.grid(row=3, column=2, rowspan=20, columnspan=2)

        self.isbn_text=tkinter.StringVar()
        self.title_text = tkinter.StringVar()
        self.author_text = tkinter.StringVar()
        self.publisher_text = tkinter.StringVar()
        self.format_text = tkinter.StringVar()
        self.subject_text = tkinter.StringVar()
        isbn_result = "ISBN: " + rows[0][0]
        self.isbn_text.set(isbn_result)
        title_result = "Title: " + rows[0][1]
        self.title_text.set(title_result)
        author_result = "Author: " + rows[0][2]
        self.author_text.set(author_result)
        publisher_result = "Publisher: " + rows[0][3]
        self.publisher_text.set(publisher_result)
        format_result = "Format: " + rows[0][4]
        self.format_text.set(format_result)
        subject_result = "Subject: " + rows[0][5]
        self.subject_text.set(subject_result)

        try:
            # Each book detail (ISBN, Title, Author, Publisher, Format, Subject) is displayed as a Label.
            # Each Label is laid out in a single column grid inside the Frame.
            # For example, each Label would be defined as follows:
            tkinter.Label(self.details_frame, text="Details for selected award winning book", background=bg_color_heading, font=font, padx=padding_header).grid(row=1, column=0)
            tkinter.Label(self.details_frame, textvariable=self.isbn_text, background=bg_color, font=font, padx=padding).grid(row=2, column=0, sticky=tkinter.constants.W)
            tkinter.Label(self.details_frame, textvariable=self.title_text, background=bg_color, font=font, padx=padding).grid(row=3, column=0, sticky=tkinter.constants.W)
            tkinter.Label(self.details_frame, textvariable=self.author_text, background=bg_color, font=font, padx=padding).grid(row=4, column=0, sticky=tkinter.constants.W)
            tkinter.Label(self.details_frame, textvariable=self.publisher_text, background=bg_color, font=font, padx=padding).grid(row=5, column=0, sticky=tkinter.constants.W)
            tkinter.Label(self.details_frame, textvariable=self.format_text, background=bg_color, font=font, padx=padding).grid(row=6, column=0, sticky=tkinter.constants.W)
            tkinter.Label(self.details_frame, textvariable=self.subject_text, background=bg_color, font=font, padx=padding).grid(row=7, column=0, sticky=tkinter.constants.W)
        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred: ', err)

    # Remove the Frame with the book details from the window using the destroy function.
    # This is needed to remove the previous book details when sorting or displaying new book details
    def clear_book_details(self):
        try:
            self.details_frame.destroy()
        except Exception as err:
            print("No problem, there is no Frame to destroy")


# Connect to the BOOKS database, execute the query to retrieve all of the books.
# Create the BookBrowser GUI and pass it the rows variable that contains the list of books.
def main():
    global db
    try:
        dbname = 'books.db'
        if os.path.exists(dbname):
            db = sqlite3.connect(dbname)
            cursor = db.cursor()
            sql = 'SELECT * FROM BOOK'
            cursor.execute(sql)
            rows = cursor.fetchall()
            BookBrowser(rows)
            db.close()
        else:
            print('Error:', dbname, 'does not exist')
    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on connect:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)


main()
