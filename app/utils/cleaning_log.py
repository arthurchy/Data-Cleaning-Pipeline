# cleaning_log.py
class CleaningLog:
    def __init__(self):
        self._changes = []
    
    def log(self, column: str, change_type: str, detail: str, count: int) -> None:
        self._changes.append({
            "column": column,
            "change_type": change_type,
            "detail": detail,
            "count": count
        })

    def to_list(self) -> list:
        return list(self._changes)
    
    def is_empty(self) -> bool:
        return len(self._changes) == 0