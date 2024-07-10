from typing import List
import math
import aiohttp
import asyncio
import numpy as np


async def get_matrix(url: str) -> List[int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            matrix = await response.text()
            list_number = [int(i) for i in matrix.split() if i.isdigit()]
            root = math.sqrt(len(list_number))
            list_matrix = np.array(list_number).reshape(int(root), int(root))

            list_zm = []
            len_number = len(list_number)









            # list_zm = []
            # index_1 = 0
            # index_2 = 0
            # while len_number != 0:




























asyncio.run(get_matrix(
    'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'))
