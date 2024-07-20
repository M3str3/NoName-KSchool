import json
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from snort import generate_snort_rule
import requests
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  
)

SERVER = "http://192.168.100.10:8000" # IP DE LA MAQUINA QUE EXTRAE LOS OBJETIVOS


@app.get("/ddosia/regs")
async def ddosia_regs(host_id: Optional[str] = Query(None), request_id: Optional[str] = Query(None), host: Optional[str] = Query(None)):
    req = f"{SERVER}/ddosia/regs"
    if host_id or request_id or host:
        req +="?"
    
    params = []

    if host_id:
        params.append(f"host_id={host_id}")
    if request_id:
        params.append(f"request_id={request_id}") 
    if host:
        params.append(f"host={host}")
    req += "&".join(params)
    print(f"{req}")
    response = requests.get(f"{req}")
    try:
        r = response.json()
        return r
    except Exception as e:
        r = response.text
        return {"r":{r},"e":e}

@app.get("/ddosia/domains/uniques")
async def ddosia_regs():
    req = f"{SERVER}/ddosia/domains/uniques"
    response = requests.get( req )

    try:
        return response.json()
    except Exception as error:
        return {"error": error}


@app.get("/ddosia/actual")
async def ddosia_regs():
    req = f"{SERVER}/ddosia/actual/uniques"
    response = requests.get( req )
    try: 
        print(response.json())
        return response.json()
    except Exception as error:
        return {"error":error}



@app.get("/ddosia/actual/uniques")
async def ddosia_regs():

    req = f"{SERVER}/ddosia/actual/uniques"

    response = requests.get( req )
    try: 
        print(response.json())
        return response.json()
    except Exception as error:
        return {"error":error}


@app.get("/ddosia/yara", response_class=PlainTextResponse)
async def ddosia_regs(request_id: str = None, host_id:str = None):
    if request_id:
        req = f"{SERVER}/ddosia/regs?request_id={request_id}"
    elif host_id:
        req = f"{SERVER}/ddosia/regs?host_id={host_id}"
    else:
        raise HTTPException(status_code=404, detail="Request ID or Host ID not found")

    response = requests.get(req)
    try:
        regs = response.json()["domains"]
    except Exception as error:
        return {"error": error}

    if not regs:
        raise HTTPException(status_code=404, detail="No records found for the given request ID")

    result = []
    print(regs)
    for reg in regs:
        sch = json.loads(reg['schema'])
        result.append(generate_snort_rule(sch))
    
    if len(result)==1:
        return result[0]

    return "\n".join(result)