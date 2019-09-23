"""
Generate an ePub for Ward by J.C. McCrae
"""
import epub
from chapter import WildbowChapter


def generate_epub(path=None):
    first_chapter = WildbowChapter(
        url="https://twigserial.wordpress.com/2014/12/24/taking-root-1-1/"
    )
    book = epub.Book(first_chapter=first_chapter)
    book.title = "Twig"
    volume = epub.EPub(path=path)
    volume.books.append(book)
    creator = epub.meta.Creator(
        value="J.C. McCrae", file_as="McCrae, J.C.", scheme="marc:relators", role="aut"
    )
    description = epub.meta.Description(
        value="The year is 1921, and a little over a century has passed since a great "
        "mind unraveled the underpinnings of life itself.  Every week, it seems, "
        "the papers announce great advances, solving the riddle of immortality, "
        "successfully reviving the dead, the cloning of living beings, or blending "
        "of two animals into one.  For those on the ground, every week brings new "
        "mutterings of work taken by ‘stitched’ men of patchwork flesh that do not "
        "need to sleep, or more fearful glances as they have to step off the "
        "sidewalks to make room for great laboratory-grown beasts.  Often felt but "
        "rarely voiced is the notion that events are already spiraling out of the "
        "control of the academies that teach these things."
        "\n\n"
        "It is only this generation, they say, that the youth and children are "
        "able to take the mad changes in stride, accepting it all as a part of day "
        "to day life.  Of those children, a small group of strange youths from the "
        "Lambsbridge Orphanage stand out, taking a more direct hand in events."
    )
    book.package_document.meta_data.creators.append(creator)
    book.package_document.meta_data.descriptions.append(description)
    volume.generate()
    return volume


if __name__ == "__main__":
    generate_epub()
