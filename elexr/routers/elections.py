from fastapi import APIRouter, HTTPException, Depends
from voting import apportionment
from ..types import election, message
from ..security import oauth2_scheme

router = APIRouter(
    prefix="/elections",
    tags=["elections"],
    responses={404: {"description": "Not found"}},
)


@router.post("/method/{method_name}", responses={405: {"model": message.Message}})
def election(method_name: str, election_info: election.ElectionInfo, token: str = Depends(oauth2_scheme)):
    valid_methods = {"dhondt": apportionment.dhondt, "sainte_lague": apportionment.sainte_lague}
    if method_name not in valid_methods:
        raise HTTPException(status_code=405, detail={"message": "Invalid apportionment method"})
    votes = list(map((lambda x: x.votes), election_info.results))
    seats = election_info.seats
    assignments = valid_methods[method_name](votes, seats)
    return {
        "seats": [{"party": result.party, "seats": assignments[i]} for i, result in enumerate(election_info.results)],
        "token": token
    }
