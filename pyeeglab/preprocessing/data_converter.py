import logging
from typing import List

from json import dumps
from numpy import ndarray, ones, triu
from pandas import DataFrame

from ..io import Raw
from .pipeline import Preprocessor


class ToDataframe(Preprocessor):

    def __init__(self) -> None:
        super().__init__()
        logging.debug('Create DataFrame converter preprocessor')

    def to_json(self) -> str:
        json = {self.__class__.__name__ : {}}
        json = dumps(json)
        return json

    def run(self, data: Raw, **kwargs) -> DataFrame:
        dataframe = data.open().to_data_frame()
        return dataframe


class ToNumpy(Preprocessor):

    def __init__(self, dtype: str = 'float32') -> None:
        super().__init__()
        logging.debug('Create Numpy (%s) converter preprocessor', dtype)
        self.dtype = dtype

    def to_json(self) -> str:
        json = {
            self.__class__.__name__ : {
                'dtype': self.dtype
            }
        }
        json = dumps(json)
        return json

    def run(self, data: List[DataFrame], **kwargs) -> List[ndarray]:
        data = [d.to_numpy(dtype=self.dtype) for d in data]
        return data


class CorrelationToAdjacency(Preprocessor):

    def __init__(self) -> None:
        super().__init__()
        logging.debug('Create adjacency converter preprocessor')

    def to_json(self) -> str:
        json = {self.__class__.__name__ : {}}
        json = dumps(json)
        return json

    def run(self, data: List[DataFrame], **kwargs) -> List[DataFrame]:
        mask = triu(ones(data[0].shape, dtype='bool'), k=1)
        data = [d.where(mask) for d in data]
        data = [d.stack().reset_index() for d in data]
        for d in data:
            d.columns = ['From', 'To', 'Weight']
        return data
