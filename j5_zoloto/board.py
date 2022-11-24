"""Virtual Camera Board for detecting Fiducial Markers."""

from pathlib import Path
from typing import List, Optional, Set, Type, Union, cast

from j5.backends import Backend
from j5.boards import Board
from j5.components import Component
from numpy import ndarray
from zoloto.marker import BaseMarker

from .component import MarkerCamera, MarkerCameraInterface


class ZolotoCameraBoard(Board):
    """Virtual Camera Board for detecting fiducial markers."""

    name: str = "Zoloto Camera Board"

    def __init__(self, serial: str, backend: Backend):
        self._serial = serial
        self._backend = backend

        self._camera = MarkerCamera(0, cast(MarkerCameraInterface, backend))

    @property
    def serial_number(self) -> str:
        """Get the serial number."""
        return self._serial

    @property
    def firmware_version(self) -> Optional[str]:
        """Get the firmware version of the board."""
        return self._backend.firmware_version

    def make_safe(self) -> None:
        """Make this board safe."""
        self._camera.close()

    @staticmethod
    def supported_components() -> Set[Type[Component]]:
        """List the types of components supported by this board."""
        return {
            MarkerCamera,
        }

    # Proxy methods from MarkerCamera object
    def see(
        self,
        *,
        eager: bool = True,
        frame: Optional[ndarray] = None,
    ) -> List[BaseMarker]:
        """
        Capture an image and identify fiducial markers.

        :param eager: Process the pose estimations of markers immediately.
        :param frame: Optional frame to process instead of capturing one.
        :returns: list of markers that the camera could see.
        """
        return self._camera.see(eager=eager, frame=frame)

    def see_ids(self, *, frame: Optional[ndarray] = None) -> List[int]:
        """
        Capture an image and identify fiducial markers.

        This method does not perform pose estimation, so is faster than ``see``.

        :param frame: Optional frame to process instead of capturing one.
        :returns: A list of IDs for the markers that were visible.
        """
        return self._camera.see_ids(frame=frame)

    def capture(self) -> ndarray:
        """
        Get the raw image data from the camera.

        :returns: Camera pixel data
        """
        return self._camera.capture()

    def save(self, path: Union[Path, str], *, frame: Optional[ndarray] = None) -> None:
        """
        Save an annotated image to a path.

        :param path: Path to save file to.
        :param frame: Optional frame to process instead of capturing one.
        """
        self._camera.save(path, frame=frame)
