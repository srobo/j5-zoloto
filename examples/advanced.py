"""Example usage of j5-zoloto with custom camera and backend."""

from j5 import BaseRobot, BoardGroup
from zoloto.cameras import Camera
from zoloto.marker_type import MarkerType

from j5_zoloto import ZolotoCameraBoard, ZolotoSingleHardwareBackend


class MyCamera(Camera):
    """Camera with custom marker size LUT."""

    def get_marker_size(self, marker_id: int) -> int:
        """Get the size of a given marker."""
        if marker_id in range(0, 100):
            return 250
        else:
            return 100


class MyZolotoSingleHardwareBackend(ZolotoSingleHardwareBackend):
    """Backend with customisations."""

    camera_class = MyCamera
    marker_type = MarkerType.APRILTAG_16H5


class Robot(BaseRobot):
    """A robot with a single CV camera."""

    def __init__(self) -> None:
        self._cameras = BoardGroup.get_board_group(
            ZolotoCameraBoard,
            MyZolotoSingleHardwareBackend,
        )

    @property
    def camera(self) -> ZolotoCameraBoard:
        """Camera board."""
        return self._cameras.singular()


if __name__ == "__main__":
    robot = Robot()

    while True:
        print(robot.camera.see())  # noqa: T001
