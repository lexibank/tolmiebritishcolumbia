from pathlib import Path
import pylexibank
import attr
from clldutils.misc import slug


@attr.s
class CustomLanguage(pylexibank.Language):
    Tribe_or_Dialect = attr.ib(default=None)
    Modern_Designation = attr.ib(default=None)
    Comment = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "tolmiebritishcolumbia"
    language_class = CustomLanguage

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"}, separators=",", missing_data=("",), strip_inside_brackets=True
    )

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("wordlists.csv", dicts=True)

        args.writer.add_sources()
        languages = args.writer.add_languages()
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )

        for row in pylexibank.progressbar(data):
            for language in languages:
                args.writer.add_form(
                    Language_ID=language,
                    Parameter_ID=concepts[row["English"]],
                    Value=row[language],
                    Form=row[language],
                    Source=["Tolmie1884"],
                )
