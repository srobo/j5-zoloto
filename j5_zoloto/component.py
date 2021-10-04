"""Classes for Fiducial Marker Camera."""

from abc import abstractmethod
from pathlib import Path
from typing import Generator, List, Type, Union

from j5.components.component import Component, Interface
from zoloto.marker import BaseMarker, EagerMarker, Marker, UncalibratedMarker


class MarkerCameraInterface(Interface):
    """An interface containing the methods required for a marker camera."""

    def process_frame(
        self,
        identifier: int,
    ) -> Generator[Union[UncalibratedMarker, Marker], None, None]:
        """
        Get markers that the camera can see.

        :param identifier: Camera identifier, ignored.
        """
        raise NotImplementedError  # pragma: nocover

    def process_frame_eager(self, identifier: int) -> Generator[EagerMarker, None, None]:
        """
        Get markers that the camera can see.

        :param identifier: Camera identifier, ignored.
        """
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def save_annotated_image(self, identifier: int, file: Path) -> None:
        """Save an annotated image to a file."""
        raise NotImplementedError  # pragma: nocover


class MarkerCamera(Component):
    """
    Camera that can identify fiducial markers.

    Additionally, it will do pose estimation, along with some calibration
    in order to determine the spatial positon and orientation of the markers
    that it has detected.
    """

    def __init__(
            self,
            identifier: int,
            backend: MarkerCameraInterface,
    ) -> None:
        self._backend = backend
        self._identifier = identifier

    @staticmethod
    def interface_class() -> Type[MarkerCameraInterface]:
        """Get the interface class that is required to use this component."""
        return MarkerCameraInterface

    @property
    def identifier(self) -> int:
        """An integer to identify the component on a board."""
        return self._identifier

    def see(self, *, eager: bool = True) -> List[BaseMarker]:
        """
        Capture an image and identify fiducial markers.

        :param eager: Process the pose estimations of markers immediately.
        :returns: list of markers that the camera could see.
        """
        if eager:
            return list(self._backend.process_frame_eager(self._identifier))
        else:
            return list(self._backend.process_frame(self._identifier))

    def save(self, path: Union[Path, str]) -> None:
        """Save an annotated image to a path."""
        if isinstance(path, str):
            path = Path(path)
        self._backend.save_annotated_image(self._identifier, path)
