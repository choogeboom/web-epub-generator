"""
Generate an ePub from Pact, by J.C. McCrae
"""
import epub

from chapter import WildbowChapter


def generate_epub(path=None):
    first_chapter = WildbowChapter(
        url='https://pactwebserial.wordpress.com/2013/12/17/bonds-1-1/')
    book = epub.Book(first_chapter=first_chapter)
    book.title = 'Pact'
    volume = epub.EPub(path=path)
    volume.books.append(book)
    creator = epub.meta.Creator(value='J.C. McCrae',
                                file_as='McCrae, J.C.',
                                scheme='marc:relators',
                                role='aut')
    description = epub.meta.Description(
        value='Blake Thorburn was driven away from home and family by a '
              'vicious fight over inheritance, returning only for a deathbed '
              'visit with the grandmother who set it in motion.   '
              'Blake soon finds himself '
              'next in line to inherit the property, a trove of dark '
              'supernatural knowledge, and the many enemies his grandmother '
              'left behind her in the small town of Jacob’s Bell.\n\n'
              'Pact is the second undertaking of Wildbow (J.C. McCrae in real '
              'life) following the completion of the popular superhero web '
              'serial Worm.  Pact is a web serial in the modern supernatural '
              'genre, and was updated one chapter at a time on Tuesdays and '
              'Saturdays, 12:01am, eastern standard time.  Chapters are '
              'grouped into arcs, five to ten chapters that cover a single '
              'theme or '
              'substory, with side content appearing between arcs.  It now '
              'joins Worm as a finished work, having run for a little over a '
              'year and three months.\n\n'
              'Any resemblance to real people, things or places is '
              'coincidental.  Pact is liable to be dark, given the author’s '
              'tendencies & style.  With that in mind, trigger warnings abound.'
              '  Though efforts are made to treat all mature subjects with the '
              'gravitas it deserves, young and emotionally vulnerable readers '
              'are advised to skip over this story.  Expect violence and foul '
              'language, and know that sex may well happen, though it will '
              'occur ‘offscreen’.\n\n'
              'Pact is generally aimed at readers aged eighteen or older, '
              'acknowledging that some younger people are more than capable of '
              'handling the aforementioned material and topics, while some '
              'older people can’t.  Use your own judgement, because you know '
              'yourself best.')
    book.package_document.meta_data.creators.append(creator)
    book.package_document.meta_data.contributors.append(transcriber)
    book.package_document.meta_data.descriptions.append(description)
    volume.generate()
    return volume


if __name__ == '__main__':
    generate_epub()
