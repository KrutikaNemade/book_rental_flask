from flask import Flask, render_template, request, redirect

app = Flask(__name__)

class Book:
    def __init__(self, book_id, title, author, status):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status

def load_books():
    books = []
    with open("books.txt", "r") as f:
        for line in f:
            book_id, title, author, status = line.strip().split(",")
            books.append(Book(book_id, title, author, status))
    return books

def save_books(books):
    with open("books.txt", "w") as f:
        for book in books:
            f.write(f"{book.book_id},{book.title},{book.author},{book.status}\n")

@app.route("/")
def index():
    books = load_books()
    return render_template("index.html", books=books)

@app.route("/rent", methods=["GET", "POST"])
def rent():
    if request.method == "POST":
        book_id = request.form["book_id"]
        books = load_books()
        for book in books:
            if book.book_id == book_id and book.status == "Available":
                book.status = "Rented"
        save_books(books)
        return redirect("/")
    return render_template("rent.html")

@app.route("/return", methods=["GET", "POST"])
def return_book():
    if request.method == "POST":
        book_id = request.form["book_id"]
        books = load_books()
        for book in books:
            if book.book_id == book_id and book.status == "Rented":
                book.status = "Available"
        save_books(books)
        return redirect("/")
    return render_template("return.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_id = request.form["book_id"]
        title = request.form["title"]
        author = request.form["author"]
        books = load_books()
        books.append(Book(book_id, title, author, "Available"))
        save_books(books)
        return redirect("/")
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
