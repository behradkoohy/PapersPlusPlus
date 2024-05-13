import sqlite3


def create_database():
    # Connect to the database (if it doesn't exist, a new database will be created)
    conn = sqlite3.connect("papers.db")
    cursor = conn.cursor()
    cursor.execute('DROP TABLE Papers;')
    cursor.execute('DROP TABLE Authors;')
    cursor.execute('DROP TABLE PaperAuthors;')
    cursor.execute('DROP TABLE Categories;')
    cursor.execute('DROP TABLE PaperCategories;')

    # Create the Papers table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Papers (
                        PaperID TEXT PRIMARY KEY,
                        DateUpdated DATE,
                        DatePublished DATE,
                        Title TEXT,
                        Abstract TEXT,
                        PaperComment TEXT,
                        PaperLink TEXT
                    )"""
    )

    # Create the Authors table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Authors (
                        AuthorID INTEGER PRIMARY KEY,
                        AuthorName TEXT
                    )"""
    )

    # Create the PaperAuthors table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS PaperAuthors (
                        PaperID TEXT,
                        AuthorID INTEGER,
                        FOREIGN KEY(PaperID) REFERENCES Papers(PaperID),
                        FOREIGN KEY(AuthorID) REFERENCES Authors(AuthorID),
                        PRIMARY KEY (PaperID, AuthorID)
                    )"""
    )

    # Create the Categories table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Categories (
                        CategoryID INTEGER PRIMARY KEY,
                        CategoryName TEXT
                    )"""
    )

    # Create the PaperCategories table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS PaperCategories (
                        PaperID TEXT,
                        CategoryID INTEGER,
                        FOREIGN KEY(PaperID) REFERENCES Papers(PaperID),
                        FOREIGN KEY(CategoryID) REFERENCES Categories(CategoryID),
                        PRIMARY KEY (PaperID, CategoryID)
                    )"""
    )


    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("SQLite database and tables created successfully.")


def add_paper(paper_id, date_updated, date_published, title, abstract, authors, paper_comment, paper_link, categories):
    # Connect to the database
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()

    # Check if the paper already exists
    cursor.execute('''SELECT COUNT(*) FROM Papers WHERE PaperID = ?''', (paper_id,))
    paper_count = cursor.fetchone()[0]
    if paper_count > 0:
        # print("Paper with ID", paper_id, "already exists. Skipping...")
        conn.close()
        return

    # Insert data into Authors table and PaperAuthors table
    for author in authors:
        cursor.execute('''SELECT AuthorID FROM Authors WHERE AuthorName = ?''', (author,))
        author_row = cursor.fetchone()
        if author_row:
            author_id = author_row[0]
        else:
            cursor.execute('''INSERT INTO Authors (AuthorName) VALUES (?)''', (author,))
            author_id = cursor.lastrowid
        cursor.execute('''INSERT INTO PaperAuthors (PaperID, AuthorID) VALUES (?, ?)''', (paper_id, author_id))

    # Insert data into Categories table and PaperCategories table
    for category in categories:
        cursor.execute('''SELECT CategoryID FROM Categories WHERE CategoryName = ?''', (category,))
        category_row = cursor.fetchone()
        if category_row:
            category_id = category_row[0]
        else:
            cursor.execute('''INSERT INTO Categories (CategoryName) VALUES (?)''', (category,))
            category_id = cursor.lastrowid
        try:
            cursor.execute('''INSERT INTO PaperCategories (PaperID, CategoryID) VALUES (?, ?)''', (paper_id, category_id))
        except sqlite3.IntegrityError:
            print(paper_id, category_id)
    # Insert data into Papers table
    cursor.execute('''INSERT INTO Papers (PaperID, DateUpdated, DatePublished, Title, Abstract, PaperComment, PaperLink)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (paper_id, date_updated, date_published, title, abstract, paper_comment, paper_link))

    # Commit changes and close connection
    conn.commit()
    conn.close()



# add_paper('https://arxiv.org/abs/2105.12345', '2024-05-08', '2024-05-01', 'Sample Paper', 'This is a sample abstract.', ['John Doe', 'Jane Smith'], 'Good paper!', 'http://example.com/sample_paper', ['Computer Science', 'Artificial Intelligence'])
