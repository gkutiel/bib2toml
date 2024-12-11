from dataclasses import dataclass
from datetime import date, datetime

import toml
from cattrs import Converter, unstructure
from pybtex.database import parse_file


def parse_datetime_from_string(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")


bib_converter = Converter()

bib_converter.register_structure_hook(
    datetime,
    lambda d, _: parse_datetime_from_string(d))


@dataclass
class BibEntry:
    title: str
    year: int
    timestamp: datetime
    url: str
    booktitle: str | None = None
    journal: str | None = None
    school: str | None = None


@dataclass
class TomlEntry:
    name: str
    publisher: str
    releaseDate: date
    url: str
    summary: str


if __name__ == '__main__':
    bib = parse_file('resume.bib')

    for k, v in bib.entries.items():
        bib_entry = bib_converter.structure(v.fields, BibEntry)

        publisher = bib_entry.booktitle or bib_entry.journal or bib_entry.school

        assert publisher is not None, 'Publisher is None'

        toml_entry = TomlEntry(
            name=bib_entry.title,
            publisher=publisher,
            releaseDate=bib_entry.timestamp.date(),
            url=bib_entry.url,
            summary=''
        )

        print()
        print('[[publications]]')
        print(toml.dumps(unstructure(toml_entry)))
