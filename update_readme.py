import pathlib
import re
import sys

import jinja2
import sqlite_utils

root = pathlib.Path(__file__).parent.resolve()

index_re = re.compile(r"<!-- index starts -->")


def get_start_from_idx(findre, lines):
    """ Return the index of the first line matching findre. """
    for i, line in enumerate(lines):
        if findre.search(line):
            return i


def group_by_topic(db):
    """ Group rows by topic. """
    by_topic = {}
    for row in db["til"].rows_where(order_by="created_utc"):
        by_topic.setdefault(row["topic"], []).append(row)
    return by_topic


def render_readme(topics=None, count=0, template="readme-tempate.j2"):
    readme_template = jinja2.Template((root / template).read_text())
    rendered_contents = readme_template.render(topics=topics, count=count)
    return rendered_contents.splitlines()


if __name__ == "__main__":
    db = sqlite_utils.Database(root / "tils.db")
    grouped_topics = group_by_topic(db)

    if "--rewrite" in sys.argv:
        readme = root / "README.md"
        rendered_contents = render_readme(topics=grouped_topics, count=db["til"].count)
        readme_lines = readme.open().readlines()

        stating_linenum = get_start_from_idx(index_re, readme_lines)
        updated_lines = (
            "".join(readme_lines[:stating_linenum])
            + "\n".join(rendered_contents).strip()
        )
        readme.write_text(updated_lines)
