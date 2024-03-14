from typing import List

from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM


async def orgainzed_kb(kb: List[IKB], rows: int = 2) -> List[List[IKB]]:
    organize = [kb[i: i + rows] for i in range(0, len(kb), rows)]
    return organize


async def get_yes_no_kb(data) -> IKM:
    kb = [
        [
            IKB("Yes", f"yes:{data}"),
            IKB("No", f"get.cancel")
        ]
    ]

    return IKM(kb)

async def get_yes_no_kb2(data) -> IKM:
    kb = [
        [
            IKB("Yes", f"yes:{data}"),
            IKB("No", f"get.cancel")
        ]
    ]

    return IKM(kb)
