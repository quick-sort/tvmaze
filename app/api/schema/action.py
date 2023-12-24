from typing import Optional
import enum

class EnumAction(enum.Enum):
    like = 'like'
    unlike = 'unlike'
    bookmark = 'bookmark'
    unbookmark = 'unbookmark'