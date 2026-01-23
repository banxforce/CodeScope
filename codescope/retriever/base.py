from abc import ABC, abstractmethod
from typing import List

class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        queries: List["RetrievalQuery"]
    ) -> List["RetrievalResult"]:
        pass
