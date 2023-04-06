from enum import Enum

class InputMode(Enum):
    """

    Input Mode

    Enum class defining all the 3 types of input modes
    used by the Neural Network.

    """

    BOTH = 1
    ONLY_FRAMES = 2
    ONLY_DIFFERENCES = 3