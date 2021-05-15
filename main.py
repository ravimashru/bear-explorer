from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


from bear import get_all_notes, get_note_by_id, get_backlinks, \
                    get_links, get_id_by_note_title

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_root(request: Request):
    all_notes = get_all_notes()
    backlinks = []
    note_contents = ''

    return templates.TemplateResponse(
        'index.html',
        {
            "request": request,
            "note_contents": note_contents,
            "all_notes": all_notes,
            "backlinks": backlinks
        }
    )

@app.get("/note/{note_id}")
def get_note(request: Request, note_id: str):

    note = get_note_by_id(note_id)
    note_contents = note["text"]

    links = get_links(note)
    for link in links:
        link_title = link[2:-2]
        link_note_id = get_id_by_note_title(link_title)
        html_link = f"<a href='{link_note_id}'>{link}</a>"
        note_contents = note_contents.replace(link, html_link)

    all_notes = get_all_notes()
    print(all_notes)

    backlinks = get_backlinks(note["title"])
    return templates.TemplateResponse(
        'index.html',
        {
            "request": request,
            "note_contents": note_contents,
            "all_notes": all_notes,
            "backlinks": backlinks
        }
    )

