#!/usr/bin/env python3
"""Turn a Twine 2 (Harlowe) story file into the 3D iPad version.

    python3 ingrid3d/build.py path/to/Ingrid.html

Reads the passages out of the published Twine HTML, injects them into
template.html and writes index.html next to it. Re-run it whenever you
edit the story in Twine. Also prints broken links and passages that can't
be reached, since those are easy to miss in Twine.
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_story(path):
    src = Path(path).read_text(encoding="utf-8")
    data = re.search(r"<tw-storydata([^>]*)>", src)
    if not data:
        sys.exit("No <tw-storydata> found - is this a published Twine 2 HTML file?")
    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', data.group(1)))
    if attrs.get("format", "").lower() != "harlowe":
        print(f"Warning: story format is {attrs.get('format')!r}; the player only understands Harlowe.")
    passages, start = {}, None
    for a, body in re.findall(r"<tw-passagedata([^>]*)>(.*?)</tw-passagedata>", src, re.S):
        pa = dict(re.findall(r'([\w-]+)="([^"]*)"', a))
        name = html.unescape(pa["name"])
        passages[name] = html.unescape(body)
        if pa.get("pid") == attrs.get("startnode"):
            start = name
    return {"name": html.unescape(attrs.get("name", "Story")), "start": start, "passages": passages}


LINK = re.compile(r"\[\[(.*?)\]\]", re.S)


def link_target(inner):
    if "->" in inner:
        return inner.rsplit("->", 1)[1]
    if "<-" in inner:
        return inner.split("<-", 1)[0]
    if "|" in inner:
        return inner.rsplit("|", 1)[1]
    return inner


def check(story):
    names = story["passages"]
    resolve = lambda t: t if t in names else next((n for n in names if n.strip() == t.strip()), None)
    graph, problems = {}, []
    for name, text in names.items():
        graph[name] = []
        for inner in LINK.findall(text):
            t = resolve(link_target(inner))
            if t is None:
                problems.append(f'Broken link in "{name}": [[{inner}]]')
            else:
                graph[name].append(t)
    seen, todo = set(), [story["start"]]
    while todo:
        n = todo.pop()
        if n in seen:
            continue
        seen.add(n)
        todo.extend(graph.get(n, []))
    for n in names:
        if n not in seen:
            problems.append(f'Unreachable from the start: "{n}"')
    return problems


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    story = read_story(sys.argv[1])
    template = (HERE / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(story, ensure_ascii=False).replace("</", "<\\/")
    out, n = re.subn(r"/\*STORY\*/.*?/\*END\*/", lambda _: f"/*STORY*/{payload}/*END*/", template, flags=re.S)
    if n != 1:
        sys.exit("Couldn't find the /*STORY*/ marker in template.html")
    (HERE / "index.html").write_text(out, encoding="utf-8")
    print(f'Built ingrid3d/index.html: "{story["name"]}", {len(story["passages"])} passages, starts at "{story["start"]}"')
    for p in check(story):
        print("  " + p)


if __name__ == "__main__":
    main()
