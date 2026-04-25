#!/usr/bin/python3
import abc
import typing


class DataProcessor(abc.ABC):
    rank: int
    list_data: list[str]

    def __init__(self):
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
    def __init__(self):
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

    def ingest(self, data: typing.Any) -> None:
        if self.validate(data):
            if isinstance(data, list):
                for nodo in data:
                    self.list_data.append(str(nodo))
            else:
                self.list_data.append(str(data))
        else:
            raise ValueError("Improper numeric data")


class TextProcessor(DataProcessor):
    def __init__(self):
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

    def ingest(self, data: typing.Any) -> None:
        if self.validate(data):
            if isinstance(data, list):
                for nodo in data:
                    self.list_data.append(str(nodo))
            else:
                self.list_data.append(str(data))
        else:
            raise ValueError("Improper text data")


class LogProcessor(DataProcessor):
    def __init__(self):
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

    def ingest(self, data: typing.Any) -> None:
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


class DataStream():
    list_proc: list[DataProcessor]

    def __init__(self):
        self.list_proc = []


    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self.list_proc.append(proc)
        else:
            print("Improper processor data ")
    
    def process_stream(self, stream: list[typing.Any]) -> None:
        for nodo in stream:
            for proc in list_proc:
                if proc.validate(nodo):
                    


def main():
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    list_numeric = [3.14, -1, 2.71]
    uni_numeric = 42
    uni_text = ["Hello world"]
    list_text = ['Hi','five']
    list_log = [
        {'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'},
        {'log_level': 'INFO', 'log_message': 'User wil is connected'}
    ]
    data = uni_text, list_numeric, list_log, uni_numeric, list_text

    print("=== Code Nexus - Data Stream ===")
    print()
    print("Initialize Data Stream...")
    stream = DataStream()
    print()
    print("Registering Numeric Processor")
    stream.register_processor(numeric)
    print()
    print(f"Send first batch of data on stream: {data}")





if __name__ == "__main__":
    main()
