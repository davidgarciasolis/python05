#!/usr/bin/python3
import abc
from typing import Any

class DataProcessor(abc.ABC):
    rank: int
    list_data: list[str]

    def __init__(self):
        self.list_data = []
        self.rank = -1

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        pass
    
    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.list_data:
            raise Exception("No data available")
        self.rank += 1
        return (self.rank, self.list_data.pop(0))


class NumericProcessor(DataProcessor):

    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(nodo, (int, float)) for nodo in data)
        return False
    
    def ingest(self, data: Any) -> None:
        if self.validate(data):
            if isinstance(data, list):
                for nodo in data:
                    self.list_data.append(str(nodo))
            else:
                self.list_data.append(str(data))
        else:
            raise Exception("Improper numeric data")
		


def main():
    numeric = NumericProcessor()


    print("=== Code Nexus - Data Processor ===")
    print()
    print("Testing Numeric Processor...")
    print(f" Trying to validate input '42': {numeric.validate(42)}")
    print(f" Trying to validate input 'Hello': {numeric.validate('hello')}")
    print(f"Test invalid ingestion of string 'foo' without prior validation: ")
    try:
        numeric.ingest("foo")
    except Exception as e:
        print(f"Got exception: {e}")
    for i in range(1, 6):
        numeric.ingest(i)
    print(f"Processing data: {numeric.list_data}")
    print(" Extracting 3 values...")
    for i in range(3):
        response = numeric.output()
        print(f"Numeric value {response[0]}:")
	


if __name__ == "__main__":
	main()