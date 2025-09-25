from typing import List

def parse_comma_separated_values(value: str) -> List[str]:
    return value.split(',') if value else []
