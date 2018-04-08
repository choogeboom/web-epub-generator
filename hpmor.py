import epub
from chapter import HPMoRChapter


def generate_epub(path=None):
    first_chapter = HPMoRChapter(url='http://hpmor.com/chapter/1')
    book = epub.Book(first_chapter=first_chapter)
    book.title = 'Harry Potter and the Methods of Rationality'
    volume = epub.EPub(path=path)
    volume.books.append(book)
    creator = epub.meta.Creator(value='Eliezer Yudkowsky',
                                file_as='Yudkowsky, Eliezer',
                                scheme='marc:relators',
                                role='aut')
    description = epub.meta.Description(value='Petunia married a biochemist, and Harry '
                                              'grew up reading science and science '
                                              'fiction. Then came the Hogwarts letter, '
                                              'and a world of intriguing new '
                                              'possibilities to exploit. And new '
                                              'friends, like Hermione Granger, '
                                              'and Professor McGonagall, and Professor '
                                              'Quirrell... ')
    book.package_document.meta_data.creators.append(creator)
    book.package_document.meta_data.contributors.append(transcriber)
    book.package_document.meta_data.descriptions.append(description)
    volume.generate()
    return volume


if __name__ == "__main__":
    generate_epub()


