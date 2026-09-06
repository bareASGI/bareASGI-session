"""Session Storage"""

from abc import ABCMeta, abstractmethod


class SessionStorage[T](metaclass=ABCMeta):
    """Session Storage"""

    @abstractmethod
    async def load(self, key: str) -> T:
        """Load session data

        Args:
            key (str): The session key.

        Returns:
            T: The session data.
        """

    @abstractmethod
    async def save(self, key: str, session: T) -> None:
        """Save session data

        Args:
            key (str): The session key.
            session (T): The session data.
        """
