from enum import Enum
from typing import List


def get_yq_input(label: str) -> bool:
    while True:
        text = input(label + " [Y/q]: ")
        text = text.lower()

        match text:
            case "y" | "yes":
                return True
            case "q" | "quit":
                return False
            case _:
                print('Input is invalid. Only "y", "yes", "q" and "quit" are allowed!')
                continue


def get_ranged_input(label: str, range: List[int]) -> int:
    input_range_str = ", ".join(map(str, range))

    while True:
        try:
            num = int(input(label + ": "))
            if num not in range:
                print(f"Expected the input to be in the {input_range_str} range!")
                continue

            return num
        except ValueError:
            print("An integer is required!")
            continue


class Status(Enum):
    PROGRESS = 0
    PROGRESS_TRAILER = 1
    NO_PROGRESS_RETRIEVER = 2
    EXCLUDE = 3

    def get_message(self) -> str:
        match self:
            case Status.PROGRESS:
                return "Progress"
            case Status.PROGRESS_TRAILER:
                return "Progress (module trailer)"
            case Status.NO_PROGRESS_RETRIEVER:
                return "Do not progress - module retriever"
            case Status.EXCLUDE:
                return "Exclude"

    def get_label(self) -> str:
        match self:
            case Status.PROGRESS:
                return "Progress"
            case Status.PROGRESS_TRAILER:
                return "Trailer"
            case Status.NO_PROGRESS_RETRIEVER:
                return "Retriever"
            case Status.EXCLUDE:
                return "Exclude"

    def get_color(self) -> str:
        match self:
            case Status.PROGRESS:
                return "Green"
            case Status.PROGRESS_TRAILER:
                return "Yellow"
            case Status.NO_PROGRESS_RETRIEVER:
                return "Red"
            case Status.EXCLUDE:
                return "Red"


def get_status(pass_mark: int, defer_mark: int, fail_mark: int) -> Status:
    if fail_mark >= 80:
        return Status.EXCLUDE

    if pass_mark == 120:
        return Status.PROGRESS
    elif pass_mark == 100:
        return Status.PROGRESS_TRAILER
    elif pass_mark >= 40 or (defer_mark >= 40 and pass_mark <= 20):
        return Status.NO_PROGRESS_RETRIEVER

    raise ValueError("FATAL: Invalid mark range")
