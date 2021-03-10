from datetime import datetime, timedelta

from .ControllerProofPurpose import ControllerProofPurpose


class AssertionProofPurpose(ControllerProofPurpose):
    def __init__(self, date: datetime = None, max_timestamp_delta: timedelta = None):
        super().__init__("assertionMethod", date, max_timestamp_delta)
