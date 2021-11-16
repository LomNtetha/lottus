from context import LottusContext
from entities import GeneratedWindow
from exceptions import InvalidSelectedOptionError, ProcessorNotFoundError, ProcessorInvalidReturnError


def default_processor(lottus_context: LottusContext, command: str) -> GeneratedWindow:
    current_window = lottus_context.current_window

    if current_window.options and len(current_window.options) > 1:
        for op in current_window.options:
            if op.identifier == command:
                processor = lottus_context.processors[op.window]
                break
        else:
            raise InvalidSelectedOptionError(None,
                                             f"Invalid select option {op.identifier} on window {current_window.name}")
    else:
        raise InvalidSelectedOptionError(None, f"Window has no list of options")

    if processor:
        window = processor(lottus_context, command)

        if not isinstance(window, GeneratedWindow):
            raise ProcessorInvalidReturnError(
                None,
                f"Processor {processor} for window {current_window.name} returned an invalid response")
        else:
            return window
    else:
        raise ProcessorNotFoundError(None, f"Processor for window {current_window.name} not found")
