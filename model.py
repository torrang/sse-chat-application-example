from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Message:
    sender: str
    message: str
    message_type: str
    timestamp: datetime

    def to_dict(self):
        return asdict(self)
