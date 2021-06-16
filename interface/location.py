from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    input: str

class LocationResponse():
    x: Optional[float] 
    y: Optional[float]
    address: Optional[str]
    distance: Optional[int]
    error: Optional[int]
    

