"""Example usage of j5-zoloto."""

from j5 import BaseRobot, BoardGroup

from j5_zoloto import ZolotoCameraBoard, ZolotoSingleHardwareBackend


class Robot(BaseRobot):
    """A robot with a single CV camera."""

    def __init__(self) -> None:
        self._cameras = BoardGroup.get_board_group(
            ZolotoCameraBoard,
            ZolotoSingleHardwareBackend,
        )

    @property
    def camera(self) -> ZolotoCameraBoard:
        """Camera board."""
        return self._cameras.singular()


if __name__ == "__main__":
    robot = Robot()

    while True:
        print(robot.camera.see(eager=False))  # noqa: T001
