"""
Context specific entities to represent AWS resources
"""

from datetime import datetime, timedelta
from typing import List


class Image:
    """
    Entity that represents the AWS AMI resource with the relevant info on this context
    """

    def __init__(self, info: dict, ref_date: datetime = None):
        self.creation_date = datetime.strptime(
            info.get("CreationDate", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.id = info.get("ImageId")
        self.name = info.get("Name")
        self.state = info.get("State")
        if ref_date:
            self.ref_date = ref_date
        else:
            self.ref_date = self.default_ref_date()

    @classmethod
    def from_list(cls, image_info: list) -> List["Image"]:
        return [Image(info) for info in image_info]

    @property
    def age(self) -> int:
        return int((self.ref_date - self.creation_date).days)

    def deprecation_date(self, max_age: int):
        return self.creation_date + timedelta(days=max_age)

    @classmethod
    def default_ref_date(cls):
        return datetime.now()
