#!/usr/bin/python3
import abc
import typing


class ExportPlugin(typing.Protocol):
    @abc.abstractmethod
    def process_output(self,data:list[tuple[int,str]]) -> None:
        pass


class ExportCSV(ExportPlugin):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        result = ""
        for nodo in data:
            result += nodo[1] + ","
        print("CSV Output:")
        print(result)


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


class DataStream():
    list_proc: list[DataProcessor]

    def __init__(self) -> None:
        self.list_proc = []

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self.list_proc.append(proc)
        else:
            print("Improper processor data ")

    def process_stream(self, stream: list[typing.Any]) -> None:
        for nodo in stream:
            fail_proc = True
            for proc in self.list_proc:
                if proc.validate(nodo):
                    proc.ingest(nodo)
                    fail_proc = False
                    break
            if fail_proc:
                print(f"DataStream error - Can't process element in stream: "
                      f"{nodo}")

    def print_processors_stats(self) -> None:
        i: int

        print("== DataStream statistics ==")
        if self.list_proc:
            for proc in self.list_proc:
                i = 0
                for data in proc.list_data:
                    i += 1
                name_proces = f"{proc.__class__.__name__}"
                name_proces = name_proces.replace("Processor", " Processor")
                print(f"{name_proces}: total {i + proc.rank + 1}"
                      f" items processed, remaining {i} on processor")
        else:
            print("No processor found, no data")


    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        list_output: list[tuple[int,str]] = list()
        for proc in self.list_proc:
            list_output: list[tuple[int,str]] = list()
            for i in range(nb):
                try:
                    list_output.append(proc.output())
                except ValueError:
                    continue
            plugin.process_output(list_output)


def main() -> None:
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    list_numeric = [3.14, -1, 2.71]
    uni_numeric = 42
    uni_text = ["Hello world"]
    list_text = ['Hi', 'five']
    list_log = [
        {'log_level': 'WARNING',
         'log_message': 'Telnet access! Use ssh instead'},
        {'log_level': 'INFO', 'log_message': 'User wil is connected'}
    ]
    list_data = uni_text, list_numeric, list_log, uni_numeric, list_text
    data: list[typing.Any] = []
    for nodo in list_data:
        data.append(nodo)
    exportCSV = ExportCSV()
    print("=== Code Nexus - Data Pipeline ===")
    print()
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()
    print()
    print("Registering Processors")
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(log)
    print()
    print(f"Send first batch of data on stream: {data}")
    stream.process_stream(data)
    print()
    stream.print_processors_stats()
    print()
    print("Send 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, exportCSV)












"""
    name_proces = f"{numeric.__class__.__name__}"
    name_proces = name_proces.replace("Processor", " Processor")
    print(f"Registering {name_proces}")
    stream.register_processor(numeric)
    print()
    print(f"Send first batch of data on stream: {data}")
    stream.process_stream(data)
    stream.print_processors_stats()
    print()
    print("Registering other data processors")
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(data)
    stream.print_processors_stats()
    print()
    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    stream.list_proc[0].output()
    stream.list_proc[0].output()
    stream.list_proc[0].output()
    stream.list_proc[1].output()
    stream.list_proc[1].output()
    stream.list_proc[2].output()
    stream.print_processors_stats()
"""


if __name__ == "__main__":
    main()
