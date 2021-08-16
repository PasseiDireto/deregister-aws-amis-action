from datetime import datetime

import mock

from action.__main__ import handle_images
from action.models import Image

dummy_images = [
    {
        "Name": "image-123",
        "CreationDate": "2021-03-01T01:30:00.000Z",
        "State": "available",
    },
    {
        "Name": "image-abc",
        "CreationDate": "2021-06-06T03:45:00.000Z",
        "State": "available",
    },
    {
        "Name": "image-666",
        "CreationDate": "2021-05-07T15:00:00.000Z",
        "State": "available",
    },
]


@mock.patch("action.__main__.remove_image")
@mock.patch("action.__main__.deprecate_image")
@mock.patch(
    "action.models.Image.default_ref_date", return_value=datetime(2021, 8, 1, 15, 0, 0)
)
def test_main(remover, deprecator, env):
    images = Image.from_list(dummy_images)
    images_to_remove, images_to_deprecate = handle_images(images, 60, True)

    assert len(images_to_remove) == 2
    assert len(images_to_deprecate) == 1
    assert images_to_deprecate[0].name == "image-abc"
