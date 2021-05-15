import sqlite3
import re

path = "/Users/<username>/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/"

def get_note_by_id(id):
    conn = sqlite3.connect(path + 'database.sqlite')
    c = conn.cursor()
    result = c.execute(
        'SELECT ZTITLE, ZTEXT FROM ZSFNOTE WHERE ZUNIQUEIDENTIFIER=:zuid',
        {"zuid":id}
    ).fetchall()
    c.close()

    if len(result) == 0:
        return None

    title = result[0][0]
    text = result[0][1]
    return {"title": title, "text": text}

def get_all_notes():
    conn = sqlite3.connect(path + 'database.sqlite')
    c = conn.cursor()
    result = c.execute(
        'SELECT ZTITLE, ZTEXT, ZUNIQUEIDENTIFIER FROM ZSFNOTE',
    ).fetchall()
    c.close()
    notes = []
    for r in result:
        notes.append({
            "title": r[0],
            "text": r[1],
            "id": r[2]
        })

    return notes

def get_backlinks(note_title):
    link = f'[[{note_title}]]'
    notes = get_all_notes()
    backlinks = []
    for note in notes:
        links = get_links(note)
        if link in links:
            backlinks.append(note)
    return backlinks

def get_links(note):
    links = re.findall("\[\[.*\]\]", note["text"])
    return links

def get_id_by_note_title(note_title):
    conn = sqlite3.connect(path + 'database.sqlite')
    c = conn.cursor()
    result = c.execute(
        'SELECT ZUNIQUEIDENTIFIER FROM ZSFNOTE WHERE ZTITLE=:ztitle',
        {"ztitle":note_title}
    ).fetchall()
    c.close()

    if len(result) == 0:
        return None

    return result[0][0]


