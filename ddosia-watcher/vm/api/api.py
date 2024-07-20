import json
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

from datetime import datetime, timedelta

def string_to_datetime(date_string):
    f = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    f -= timedelta(minutes=5)
    return f
def datetime_to_string(date_datetime):
    return date_datetime.strftime('%Y-%m-%d %H:%M:%S')

extensiones_a_paises = {
    "ac": "Ascension Island",
    "ad": "Andorra",
    "ae": "United Arab Emirates",
    "al": "Albania",
    "am": "Armenia",
    "at": "Austria",
    "az": "Azerbaijan",
    "ba": "Bosnia and Herzegovina",
    "be": "Belgium",
    "bg": "Bulgaria",
    "by": "Belarus",
    "ch": "Switzerland",
    "cy": "Cyprus",
    "cz": "Czech Republic",
    "de": "Germany",
    "dk": "Denmark",
    "ee": "Estonia",
    "es": "Spain",
    "fi": "Finland",
    "fr": "France",
    "gb": "United Kingdom",
    "ge": "Georgia",
    "gr": "Greece",
    "hr": "Croatia",
    "hu": "Hungary",
    "ie": "Ireland",
    "is": "Iceland",
    "it": "Italy",
    "li": "Liechtenstein",
    "lt": "Lithuania",
    "lu": "Luxembourg",
    "lv": "Latvia",
    "mc": "Monaco",
    "md": "Moldova",
    "me": "Montenegro",
    "mk": "North Macedonia",
    "mt": "Malta",
    "nl": "Netherlands",
    "no": "Norway",
    "pl": "Poland",
    "pt": "Portugal",
    "ro": "Romania",
    "rs": "Serbia",
    "ru": "Russia",
    "se": "Sweden",
    "si": "Slovenia",
    "sk": "Slovakia",
    "sm": "San Marino",
    "tr": "Turkey",
    "ua": "Ukraine",
    "uk": "United Kingdom",
    "va": "Vatican City"
}


def get_db_connection():
    conn = sqlite3.connect('../database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/ddosia/regs")
async def ddosia_regs(host_id: Optional[str] = Query(None), request_id: Optional[str] = Query(None), host: Optional[str] = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM regs"
    conditions = []
    parameters = []

    if host_id:
        conditions.append("host_id = ?")
        parameters.append(host_id)
    if request_id:
        conditions.append("request_id = ?")
        parameters.append(request_id)
    if host:
        conditions.append("host = ?")
        parameters.append(host)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(parameters))
    domains = cursor.fetchall()
    conn.close()

    return {"domains": [dict(domain) for domain in domains]}


@app.get("/ddosia/domains/uniques")
async def ddosia_regs():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT DISTINCT host FROM regs;"
    cursor.execute(query)
    domains = cursor.fetchall()
    conn.close()

    return {"domains": [dict(domain) for domain in domains]}


@app.get("/ddosia/actual")
async def ddosia_regs():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT last_time_seen FROM regs ORDER BY last_time_seen DESC LIMIT 1;"
    cursor.execute(query)
    out = cursor.fetchall()
    last_time = datetime_to_string(string_to_datetime([dict(domain) for domain in out][0]['last_time_seen']))
    query = "SELECT * FROM regs where last_time_seen>?;"
    cursor.execute(query, (last_time,))
    domains = cursor.fetchall()
    conn.close()
    return {"domains": [dict(domain) for domain in domains]}


@app.get("/ddosia/actual/uniques")
async def ddosia_regs():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT last_time_seen FROM regs ORDER BY last_time_seen DESC LIMIT 1;"
    cursor.execute(query)
    out = cursor.fetchall()
    dat = [dict(domain) for domain in out][0]['last_time_seen']
    dat2 = datetime_to_string(string_to_datetime(dat))
    print(dat)
    print(dat2)
    query = "SELECT * FROM regs where last_time_seen BETWEEN ? AND ?;"
    print(query)
    cursor.execute(query, (dat2,dat,))
    domains = cursor.fetchall()
    #print(domains)
    conn.close()
    out = {"domains": [dict(domain) for domain in domains]}

    result = {"domains": [], 'date': dat, 'countries': []}
    for t in out['domains']:
        ext = t['host'].split('.')[-1]
        if ext in extensiones_a_paises and extensiones_a_paises[ext] not in result['countries']:
            result["countries"].append(extensiones_a_paises[ext])
        if t['host'] not in result["domains"]:
            result["domains"].append(t["host"])
    return result


