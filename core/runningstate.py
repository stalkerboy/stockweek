from enum import Enum


class RunningState(Enum):
    STOP = '정지'
    READY = '준비중'
    RUNNING = '동작중'
    ERROR = '에러'
