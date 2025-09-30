from typing import List
from typing import Tuple
from typing import Generic
from typing import TypeVar
from typing import Optional

from pydantic.generics import GenericModel


DataType = TypeVar("DataType")


class Pagination:
    default_offset = 0
    default_limit = 20

    def __init__(
            self,
            offset: int = default_offset,
            limit: int = default_limit,
    ):
        self.offset = offset
        self.limit = limit

    def get_offset_limit(self) -> Tuple[int, int]:
        return self.offset, self.limit


class ResponsePaginateSchema(GenericModel, Generic[DataType]):
    total: int
    items: Optional[List[DataType]] = None
