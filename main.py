from model.Library import Library

def main():
    LIBRARY = Library()

    author1 = LIBRARY.create_author('Author 1', 'nacionality', 'education', 'description')
    author2 = LIBRARY.create_author('Author 2', 'nacionality', 'education', 'description')


    book = LIBRARY.create_book('code', 'Book 1', 'language', 'publication date', 'edition date', 'pages', 'size', 'publisher', 'isbn', 'edition number', author2, author1)
    
    if book:
        print(book.title)
        for author in book.authors:
            print(author.name)
    else:
        print('Falha ao adicionar Livro')

    # book1 = Book('Booo', 'Book 1', 'la', 'la', 'la', 'la', 'la', 'la', 'la')
    # book2 = Book('Baaaaa', 'Book 2', 'la', 'la', 'la', 'la', 'la', 'la', 'la')

    # author = Author('name', 'nacionality', 'education', 'description')
    # author.add_book_to_author(book1)
    # author.add_book_to_author(book2)

    # for book in author.books:
    #     print(book.title)
    # print()

    # author.remove_book_from_author(book1)
    # for book in author.books:
    #     print(book.title)
    ...

if __name__ == '__main__':
    main()
