def format_currency(value: float) -> str:
    formatted_value: str = f"R$ {value:,.2f}"
    return formatted_value


def format_number(value: int) -> str:
    formatted_number: str = f"{value:,}"
    return formatted_number


def format_percentage(value: float) -> str:
    formatted_percentage: str = f"{value:.2f}%"
    return formatted_percentage


def shorten_id(identifier: str, length: int = 8) -> str:
    if len(identifier) > length:
        short_id: str = f"{identifier[:length]}..."
        return short_id
    return identifier
