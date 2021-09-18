from typing import List
from pydantic import BaseModel


class ElectionResult(BaseModel):
    party: str = "Party"
    votes: int = 100


class ElectionInfo(BaseModel):
    name: str = "Election"
    seats: int = 100
    results: List[ElectionResult] = []
