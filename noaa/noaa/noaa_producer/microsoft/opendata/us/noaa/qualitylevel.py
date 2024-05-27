""" QualityLevel """

# pylint: disable=invalid-name,line-too-long,too-many-instance-attributes


from enum import Enum

class QualityLevel(Enum):
    """
    Quality Assurance/Quality Control level"""

    Preliminary = 0
    Verified = 1
