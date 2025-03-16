from mfnf.sitemap import parse_link, parse_sitemap, Project, Book, Section, Page


def test_parse_sitemap_success():
    sitemap_text = unindent("""
        == [[Mathe für Nicht-Freaks: Analysis 1|Analysis 1]] ==
        === Section 1 ===
        * [[Mathe für Nicht-Freaks: Grundlagen der Analysis 1|Grundlagen]]
        * [[Mathe für Nicht-Freaks: Definitionen der Analysis 1|Definitionen]]
        == [[Mathe für Nicht-Freaks: Buchanfänge|Buchanfänge]] ==
        * [[Mathe für Nicht-Freaks: Funktionalanalysis|Funktionalanalysis]]

    """)
    expected_project = Project(
        books=[
            Book(
                name="Analysis 1",
                href="Mathe für Nicht-Freaks: Analysis 1",
                sections=[
                    Section(
                        name="Section 1",
                        pages=[
                            Page(
                                name="Grundlagen",
                                href="Mathe für Nicht-Freaks: Grundlagen der Analysis 1",
                            ),
                            Page(
                                name="Definitionen",
                                href="Mathe für Nicht-Freaks: Definitionen der Analysis 1",
                            ),
                        ],
                    ),
                ],
            ),
            Book(
                name="Buchanfänge",
                href="Mathe für Nicht-Freaks: Buchanfänge",
                sections=[
                    Section(
                        name="Buchanfänge",
                        pages=[
                            Page(
                                name="Funktionalanalysis",
                                href="Mathe für Nicht-Freaks: Funktionalanalysis",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    project = parse_sitemap(sitemap_text)

    assert project == expected_project


def test_parse_link_success():
    for link in [
        "[[Mathe für Nicht-Freaks: Analysis 1|Analysis 1]]",
        "[[Mathe für Nicht-Freaks: Analysis 1|Analysis 1]] {{Status|fertig}}",
    ]:
        href, name = parse_link(link)

        assert name == "Analysis 1"
        assert href == "Mathe für Nicht-Freaks: Analysis 1"


def test_parse_link_failure():
    for link in [
        "Analysis 1",
        "[[Analysis 1]]",
        "[[Analysis 1|Analysis 1",
        "[[Analysis 1|Analysis 1]",
    ]:
        assert parse_link(link) == (None, None)


def unindent(text: str) -> str:
    lines = text.strip().split("\n")
    return "\n".join(line.lstrip() for line in lines)
