#!/usr/bin/python3
import abc
import typing


class DataProcessor(abc.ABC):
    rank: int
    list_data: list[str]

    def __init__(self) -> None:
        self.list_data = []
        self.rank = -1

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.list_data:
            raise ValueError("No data available")
        self.rank += 1
        return (self.rank, self.list_data.pop(0))


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)):
            return (True)
        if isinstance(data, list):
            for nodo in data:
                if not isinstance(nodo, (int, float)):
                    return (False)
            return (True)
        return (False)

    def ingest(self, data: int | float | list[int]
               | list[float] | list[int | float]) -> None:
        if self.validate(data):
            if isinstance(data, list):
                for nodo in data:
                    self.list_data.append(str(nodo))
            else:
                self.list_data.append(str(data))
        else:
            raise ValueError("Improper numeric data")


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return (True)
        if isinstance(data, list):
            for nodo in data:
                if not isinstance(nodo, str):
                    return (False)
            return (True)
        return (False)

    def ingest(self, data: str | list[str]) -> None:
        if self.validate(data):
            if isinstance(data, list):
                for nodo in data:
                    self.list_data.append(str(nodo))
            else:
                self.list_data.append(str(data))
        else:
            raise ValueError("Improper text data")


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, dict):
            return (True)
        if isinstance(data, list):
            for nodo in data:
                if not isinstance(nodo, dict):
                    return (False)
            return (True)
        return (False)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if self.validate(data):
            try:
                if isinstance(data, list):
                    for nodo in data:
                        self.list_data.append(f"{str(nodo['log_level'])}: "
                                              f"{str(nodo['log_message'])}")
                else:
                    self.list_data.append(f"{str(nodo['log_level'])}: "
                                          f"{str(nodo['log_message'])}")
            except KeyError:
                raise ValueError("Improper log data")
        else:
            raise ValueError("Improper log data")


def main() -> None:
    numeric = NumericProcessor()
    list_numeric = [1, 2, 3, 4, 5]
    text = TextProcessor()
    list_text = ["Hello", "Nexus", "'World"]
    log = LogProcessor()
    list_log = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]

    print("=== Code Nexus - Data Processor ===")
    print()
    print("Testing Numeric Processor...")
    print(f" Trying to validate input '42': {numeric.validate(42)}")
    print(f" Trying to validate input 'Hello': {numeric.validate('hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation: ")
    try:
        numeric.ingest(42)
    except Exception as e:
        print(f"Got exception: {e}")
    print(f"Processing data: {list_numeric}")
    try:
        numeric.ingest(list_numeric)
        print(" Extracting 3 values...")
        for i in range(3):
            response = numeric.output()
            print(f"Numeric value {response[0]}: {response[1]}")
    except ValueError as e:
        print(f"{e}")
    print()
    print("Testing Text Processor...")
    print(f" Trying to validate input'42': {text.validate(42)}")
    print(f" Processing data: {list_text}")
    try:
        text.ingest(list_text)
        print(" Extracting 1 value...")
        for i in range(1):
            response = text.output()
            print(f" Text value {response[0]}: {response[1]}")
    except ValueError as e:
        print(f"{e}")
    print()
    print("Testing Log Processor...")
    try:
        print(f" Trying to validate input 'Hello': {log.validate('Hello')}")
        print(f" Processing data: {list_log}")
        log.ingest(list_log)
        print(" Extracting 2 values...")
        for i in range(2):
            response = log.output()
            print(f"Log entry {response[0]}: {response[1]}")
    except ValueError as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
