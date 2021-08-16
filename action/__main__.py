"""
Deregister AMIs older than a custom age that matches a given name filter
"""
import os
from typing import List, Tuple

import boto3

from action.logger import logging
from action.models import Image

lg = logging.getLogger()


def handle_images(
    images: List[Image], max_age: int, set_deprecation_date: bool
) -> Tuple[List[Image], List[Image]]:
    """
    Remove (deregister) or deprecate AMIs based on `max_age` and `set_deprecation_date`
    :param set_deprecation_date: Whether to set a deprecation date based on `max_age` on AMIs
     that where found but are not yet eligible for removal
    :param max_age: Maximum number of days an AMI should exist. Images older than `max_age` days will be removed
    :param images: List of images filtered and eligible for removal/deprecation (if applicable)
    :return: a tuple with two lists: (images_to_remove, images_to_deprecate)
    """

    lg.info(f"{len(images)} images were found")
    images_to_remove = [image for image in images if image.age > max_age]
    remove_images(images_to_remove)

    images_to_deprecate = []
    if set_deprecation_date:
        images_to_deprecate = [
            image for image in images if image not in images_to_remove
        ]
        deprecate_images(images_to_deprecate, max_age)

    return images_to_remove, images_to_deprecate


def remove_images(images_to_remove: List[Image]):
    """
    Remove a list of Images
    :param images_to_remove:
    """
    if images_to_remove:
        lg.warning(f"{len(images_to_remove)} will be removed:")
        for image in images_to_remove:
            lg.warning(f"   {image.name} ({image.id})")
            remove_image(image)
        return
    lg.warning("No images will be removed")


def deprecate_images(images_to_deprecate: List[Image], max_age: int):
    """
    Set a deprecation date on a list of Images based on their `creation_date` + `max_age`
    :param images_to_deprecate:
    :param max_age:
    """
    if images_to_deprecate:
        lg.warning(f"{len(images_to_deprecate)} will be set as deprecated:")
        for image in images_to_deprecate:
            lg.warning(
                f"  {image.name} ({image.id}) will be deprecated at {image.deprecation_date(max_age).isoformat()}"
            )
            deprecate_image(image, max_age)
        return
    lg.warning("No images will be deprecated")


def deprecate_image(image: Image, max_age: int):
    """
    Deprecates an AMI using its `creation_date` + `max_age` as deprecation date
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.enable_image_deprecation
    :param image:
    :param max_age:
    """
    client = boto3.client("ec2")
    client.enable_image_deprecation(
        ImageId=image.id, DeprecateAt=image.deprecation_date(max_age)
    )


def remove_image(image: Image):
    """
    Remove a AMI based on image.id
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.deregister_image
    :param image:
    """
    client = boto3.client("ec2")
    client.deregister_image(ImageId=image.id)


def get_image_list(name_filter: str, owner: str) -> list[dict]:
    """
    Returns a list of AMIs based on a given name filter expression and ownership
    :param name_filter: an expression to match while searching AMIs, such as "*image*-dev"
    :param owner: the ID of the Owner Account of the desired images.
    :return: A list of found AMIs
    """
    ec2 = boto3.client("ec2")
    return ec2.describe_images(
        Owners=[owner],
        Filters=[
            {
                "Name": "name",
                "Values": [
                    name_filter,
                ],
            }
        ],
    )["Images"]


if __name__ == "__main__":
    image_info = get_image_list(
        os.environ["INPUT_NAME_FILTER"], os.environ["INPUT_OWNER"]
    )
    handle_images(
        Image.from_list(image_info),
        int(os.environ["INPUT_MAX_AGE"]),
        os.environ["INPUT_SET_DEPRECATION_DATE"] == "true",
    )
