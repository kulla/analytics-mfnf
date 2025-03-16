from dataclasses import dataclass, field
from typing import List, Literal


@dataclass
class BookLine:
    name: str
    href: str


@dataclass
class SectionLine:
    name: str


@dataclass
class PageLine:
    name: str
    href: str


@dataclass
class Page:
    name: str
    href: str
    kind: Literal["page"] = "page"


@dataclass
class Section:
    name: str
    kind: Literal["section"] = "section"
    pages: List[Page] = field(default_factory=list)


@dataclass
class Book:
    name: str
    href: str
    kind: Literal["book"] = "book"
    sections: List[Section] = field(default_factory=list)


@dataclass
class Project:
    kind: Literal["project"] = "project"
    name: Literal["Mathe für Nicht-Freaks"] = "Mathe für Nicht-Freaks"
    href: Literal["Mathe für Nicht-Freaks"] = "Mathe für Nicht-Freaks"
    books: List[Book] = field(default_factory=list)


def parse_sitemap(sitemap_text):
    project: Project = Project()
    book: None | Book = None
    section: None | Section = None

    for line in sitemap_text.split("\n"):
        parsed_line = parse_sitemap_line(line)

        if parsed_line is None:
            continue

        if isinstance(parsed_line, BookLine):
            book = Book(name=parsed_line.name, href=parsed_line.href)
            section = None

            project.books.append(book)
        elif isinstance(parsed_line, SectionLine):
            section = Section(name=parsed_line.name)

            if book is None:
                raise ValueError(f"Section {section.name} is defined without a book")

            book.sections.append(section)
        elif isinstance(parsed_line, PageLine):
            page = Page(name=parsed_line.name, href=parsed_line.href)

            if book is None:
                raise ValueError(f"Page {page.name} is defined without a book")

            if section is None:
                for book_without_sections in ["Buchanfänge", "Über das Projekt"]:
                    if book.name == book_without_sections:
                        section = Section(name="Buchanfänge")

                        book.sections.append(section)

            if section is None:
                raise ValueError(f"Page {page.name} is defined without a section")

            section.pages.append(page)

    return project


def parse_sitemap_line(sitemap_line):
    if sitemap_line.startswith("===") and sitemap_line.endswith("==="):
        name = sitemap_line.strip("===").strip()

        if name:
            return SectionLine(name)
    elif sitemap_line.startswith("==") and sitemap_line.endswith("=="):
        href, name = parse_link(sitemap_line.strip("==").strip())

        if href and name:
            return BookLine(name, href)
    elif sitemap_line.startswith("* "):
        href, name = parse_link(sitemap_line.lstrip("* "))

        if href and name:
            return PageLine(name, href)

    return None


def parse_link(line):
    end_index = line.find("]]")

    if line.startswith("[[") and end_index > 2:
        link_content = line[2:end_index]
        link_parts = link_content.split("|")

        if len(link_parts) == 2:
            return link_parts

    return (None, None)
