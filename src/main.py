from typing import List, Tuple
from graphics import GraphWin, Text, Point, GraphicsError, Rectangle
from utils import Status, get_status, get_yq_input, get_ranged_input


MSG_EXIT_OR_ENTER = (
    "Would you like to enter another set of data, or quit and view results?"
)


def main():
    CREDIT_RANGE = [0, 20, 40, 60, 80, 100, 120]
    statuses: List[Status] = []
    credits: List[Tuple[int, int, int]] = []

    while True:
        try:
            (status, credit) = round(CREDIT_RANGE)
            statuses.append(status)
            credits.append(credit)

            if not get_yq_input(MSG_EXIT_OR_ENTER):
                break
        except ValueError:
            continue
        except KeyboardInterrupt:
            # We have to account for keyboard interruptions like ctrl + c without throwing an exception.
            return exit(0)

    run_window(statuses)

    for i, credit in enumerate(credits):
        status = statuses[i]
        tuple_str = ", ".join(map(str, credit))
        print(f"{status.get_message()} - {tuple_str}")


def round(credit_range: List[int]) -> Tuple[Status, Tuple[int, int, int]]:
    """Initiates a round and returns a boolean describing whether to run another round or not."""

    inp_pass = get_ranged_input("Please enter the credits at pass", credit_range)
    inp_defer = get_ranged_input("Please enter the credits at defer", credit_range)
    inp_fail = get_ranged_input("Please enter the credits at fail", credit_range)
    total = inp_pass + inp_defer + inp_fail

    if total != 120:
        print(f"The total is incorrect. Expected 120, but got {total}!", end="\n\n")
        raise ValueError

    status = get_status(inp_pass, inp_defer, inp_fail)
    print(f"Status: {status.get_message()}", end="\n\n")

    return (status, (inp_pass, inp_defer, inp_fail))


def run_window(statuses: List[Status]):
    """
    Runs a window with graphics.py.
    NOTE: Blocks the main thread
    """

    WINDOW_X = 800
    WINDOW_Y = 600
    BAR_WIDTH = 100
    BAR_GAP = 25
    BAR_Y_START = 100
    BAR_Y_END = 450
    BAR_MAX_Y = BAR_Y_END - BAR_Y_START

    win = GraphWin("Histogram", WINDOW_X, WINDOW_Y)
    win.setBackground("White")

    title = Text(Point(150, 50), "Histogram Results")
    title.setTextColor("Black")
    title.setSize(18)
    title.setStyle("bold")
    title.draw(win)

    subtitle = Text(Point(125, WINDOW_Y - 50), f"{len(statuses)} outcomes in total")
    subtitle.setTextColor("Black")
    subtitle.setSize(14)
    subtitle.draw(win)

    # Calculation:
    # max_window - max_bar_width returns the remaining x width,
    # which could resolve the padding needed for a side to center the bars
    status_list = list(Status)
    max_bar_width = (BAR_WIDTH + BAR_GAP) * len(status_list)
    side_padding = (WINDOW_X - max_bar_width) / 2
    bar_item_size = BAR_MAX_Y / len(statuses)

    for i, status_type in enumerate(status_list):
        bar_x_start = side_padding + (BAR_WIDTH * i) + (BAR_GAP * i)
        bar_x_end = bar_x_start + BAR_WIDTH

        status_type_items = list(filter(lambda x: x == status_type, statuses))
        status_type_items_len = len(status_type_items)

        # We can find the start y of the bar_y by calculating the px from window top to graph bottom,
        # and then by calculating back from the bottom to top using bar_item_size
        bar_y_height = bar_item_size * status_type_items_len
        bar_y_start = BAR_Y_START + (BAR_MAX_Y - bar_y_height)

        bar = Rectangle(Point(bar_x_start, bar_y_start), Point(bar_x_end, BAR_Y_END))
        bar.setFill(status_type.get_color())
        bar.draw(win)

        label_x_start = bar_x_start + 50
        label = Text(Point(label_x_start, 475), status_type.get_label())
        label.setTextColor("Grey")
        label.setStyle("bold")
        label.draw(win)

        amount_y_start = bar_y_start - 15
        amount = Text(Point(label_x_start, amount_y_start), status_type_items_len)
        amount.setTextColor("Grey")
        amount.draw(win)

    # We need to keep the script active, else the window would close along with the script.
    while True:
        try:
            win.getMouse()
        # The graphic error here is referring to the window close button
        except GraphicsError:
            break


if __name__ == "__main__":
    main()
