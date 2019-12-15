from nonebot import CommandGroup, CommandSession
import random
import shlex
from .data_source import get_random_things

__plugin_name__ = '随机'
__plugin_usage__ = r"""有关随机

指令: 随机数 / 打乱 / 抽签 / 找点乐子"""


cg = CommandGroup('random', only_to_me=False)


@cg.command('number', aliases=['随机数'])
async def random_number(session: CommandSession):
    argv = shlex.split(session.current_arg_text)
    start, end = 1, 100
    try:
        if len(argv) == 1:
            start, end = 1, int(argv[0])
        elif len(argv) > 1:
            start, end = int(argv[0]), int(argv[1])
    except ValueError:
        session.finish('格式错误，随机数范围需是数字')

    start = min(start, end)
    end = max(start, end)
    if end > 10000 or start < -10000:
        session.pause('范围过大，请重新输入')

    await session.send(str(random.randint(start, end)))


@cg.command('shuffle', aliases=['打乱'])
async def random_shuffle(session: CommandSession):
    argv = shlex.split(session.current_arg_text)
    if len(argv) == 3 and argv[0] == '-r':
        try:
            start = int(argv[1])
            end = int(argv[2]) + 1
            if end - start > 1000:
                session.finish('范围过大')
            t = list(range(start, end))
        except ValueError:
            session.finish('范围需是整数')
            return
    else:
        t = argv.copy()

    if not t:
        session.finish('格式错误，需要提供要打乱的内容')

    random.shuffle(t)
    await session.send(' '.join(map(str, t)))


@cg.command('choice', aliases=['抽签'])
async def random_choice(session: CommandSession):
    argv = shlex.split(session.current_arg_text)
    if not argv:
        session.finish('格式错误，需要提供要抽签的内容')
    await session.send(random.choice(argv))


@cg.command('random_things', aliases=['找点乐子', '找点事做', '没事找事'])
async def random_choice(session: CommandSession):
    msg = await get_random_things()
    await session.send(msg)
