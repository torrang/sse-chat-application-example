from typing import List
from dataclasses import dataclass


@dataclass
class User:
    """ User class """
    pass


@dataclass
class Room:
    """ Room class """
    room_id: int
    users: List[User]
