from datetime import datetime

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
ref_date = datetime(2021, 8, 1, 15, 0, 0)


def test_from_list():
    images = Image.from_list(image_info=dummy_images)
    assert len(images) == len(dummy_images)
    assert "image-666" in [image.name for image in images]


def test_age_ok():
    image = Image(dummy_images[0], ref_date=ref_date)  # image-123 from 01/03/2021
    assert image.age == 153


def test_deprecation_date():
    image = Image(dummy_images[0], ref_date=ref_date)  # image-123 from 01/03/2021
    assert image.deprecation_date(30) == datetime(2021, 3, 31, 1, 30)
