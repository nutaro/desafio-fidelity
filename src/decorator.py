from datetime import datetime
from typing import Callable, Any
from zoneinfo import ZoneInfo


from log import CustomLogger


logger = CustomLogger().get_logger()


def time_it(function: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = datetime.now(tz=ZoneInfo('America/Sao_Paulo'))
        logger.info(f'Executando {function.__name__} na {start_time}')
        values = function(*args, **kwargs)
        stop_time = datetime.now(tz=ZoneInfo('America/Sao_Paulo'))
        logger.info(f'Finalizada {function.__name__} na {stop_time}')
        tempo_total = stop_time - start_time
        logger.info(f'A função {function.__name__} levou {tempo_total.total_seconds()} segundos')
        return values
    return wrapper
