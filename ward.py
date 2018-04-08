"""
Generate an ePub for Ward by J.C. McCrae
"""
import epub
from chapter import WildbowChapter


def generate_epub(path=None):
    first_chapter = WildbowChapter(
        url='https://www.parahumans.net/2017/10/21/glow-worm-0-1/')
    book = epub.Book(first_chapter=first_chapter)
    book.title = 'Ward'
    volume = epub.EPub(path=path)
    volume.books.append(book)
    creator = epub.meta.Creator(value='J.C. McCrae',
                                file_as='McCrae, J.C.',
                                scheme='marc:relators',
                                role='aut')
    description = epub.meta.Description(
        value='The unwritten rules that govern the fights and outright wars between '
              '‘capes’ have been amended: everyone gets their second chance.  It’s an '
              'uneasy thing to come to terms with when notorious supervillains and even '
              'monsters are playing at being hero.  The world ended two years ago, and '
              'as humanity straddles the old world and the new, there aren’t records, '
              'witnesses, or facilities to answer the villains’ past actions in the '
              'present.  One of many compromises, uneasy truces and deceptions that are '
              'starting to splinter as humanity rebuilds.'
              '\n\n'
              'None feel the injustice of this new status quo or the lack of '
              'established footing more than the past residents of the parahuman '
              'asylums.  The facilities hosted parahumans and their victims, but the '
              'facilities are ruined or gone; one of many fragile ex-patients is left '
              'to find a place in a fractured world.  She’s perhaps the person least '
              'suited to have anything to do with this tenuous peace or to stand '
              'alongside these false heroes.  She’s put in a position to make the '
              'decision: will she compromise to help forge what they call, with dark '
              'sentiment, a second golden age?  Or will she stand tall as a gilded dark '
              'age dawns?')
    book.package_document.meta_data.creators.append(creator)
    book.package_document.meta_data.contributors.append(transcriber)
    book.package_document.meta_data.descriptions.append(description)
    volume.generate()
    return volume


if __name__ == '__main__':
    generate_epub()
