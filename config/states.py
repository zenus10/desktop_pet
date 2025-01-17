from enum import Enum, auto

class PetState(Enum):
    IDLE = auto()       # 静止(显示bear_idle.png)
    RUN = auto()        # 跑动(随机移动, 撞边后弹回)
    DRAGGED = auto()    # 被鼠标拖拽
    WORKING = auto()    # 工作(可显示某打字/思考gif)
    RANDOM_ACTION = auto()  # 随机动作(吃喝等)
    FALLING = auto()       # 新增：掉落
    BOUNCE = auto()         #新增：反弹
    EDGE_CLING = auto()    # 新增：趴在边缘

class MoodState(Enum):
    NORMAL = auto()
    ANGRY = auto()
    CRY = auto()
    LAUGH = auto()

class RandomActionType(Enum):
    EAT = auto()
    DRINK = auto()
    DANCE = auto()
    # 可扩展更多


