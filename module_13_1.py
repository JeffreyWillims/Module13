import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for _ in range(5):
        await asyncio.sleep(6 / power)
        print(f'Силач {name} поднял {_+1} шар')
    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    task1 = asyncio.create_task(start_strongman("Pasha", 3), name='Pasha')
    task2 = asyncio.create_task(start_strongman("Denis", 4), name='Denis')
    task3 = asyncio.create_task(start_strongman("Apollon", 5), name='Apollon')
    await task1
    await task2
    await task3


asyncio.run(start_tournament())