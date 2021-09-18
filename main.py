from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from voting import apportionment


class Message(BaseModel):
    message: str = "Server error"


class ElectionResult(BaseModel):
    party: str = "Party"
    votes: int = 100


class ElectionInfo(BaseModel):
    name: str = "Election"
    seats: int = 100
    results: List[ElectionResult] = []


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
        <html>
            <head>
                <title>Elexr</title>
            </head>
            <body>
                <h1>Elexr</h1>
            </body>
        </html>
        """


@app.post("/election/method/{method_name}", responses={405: {"model": Message}})
def election(method_name: str, election_info: ElectionInfo):
    valid_methods = {"dhondt": apportionment.dhondt, "sainte_lague": apportionment.sainte_lague}
    if method_name not in valid_methods:
        raise HTTPException(status_code=405, detail={"message": "Invalid apportionment method"})
    votes = list(map((lambda x: x.votes), election_info.results))
    seats = election_info.seats
    assignments = valid_methods[method_name](votes, seats)
    return {
        "seats": [{"party": result.party, "seats": assignments[i]} for i, result in enumerate(election_info.results)]
    }
