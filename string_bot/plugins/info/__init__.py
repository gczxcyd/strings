from nonebot import CommandGroup, CommandSession
from .data_source import *

__plugin_name__ = '信息'
__plugin_usage__ = r"""信息服务

指令: 历史上的今天 / 每日一句 / 新闻 / etc."""


cg = CommandGroup('info', only_to_me=False)


@cg.command('today_in_history', aliases=['历史上的今天'])
async def info_today_in_history(session: CommandSession):
    msg = await get_today_in_history()
    await session.send(msg)


@cg.command('one_sentence_a_day', aliases=['每日一句'])
async def info_one_sentence_a_day(session: CommandSession):
    msg = await get_one_sentence_a_day()
    await session.send(msg)


@cg.command('five_sayings', aliases=['five语录', '废物语录'])
async def info_five_sayings(session: CommandSession):
    msg = await get_five_sayings()
    await session.send(msg)


# **是什么垃圾
@cg.command('garbage_classification', aliases=['垃圾分类', '分类'])
async def info_garbage_classification(session: CommandSession):
    garbage = session.get('garbage', prompt='分类什么垃圾?')
    msg = await get_garbage_classification(garbage)
    await session.send(msg)


@cg.command('joke', aliases=['joke', '段子', '笑话'])
async def info_joke(session: CommandSession):
    msg = await get_a_joke()
    await session.send(msg)


@cg.command('news', aliases=['news', '新闻', '近闻'])
async def info_news(session: CommandSession):
    msg = await get_news()
    await session.send(msg)


@cg.command('weather', aliases=['天气', '查天气', '最近什么天气', '最近天气怎么样'])
async def info_weather(session: CommandSession):
    city = session.get('city', prompt='你想查哪个城市?')
    date = session.get('date', prompt='你想查哪一天?')
    msg = await get_weather_of_city(city, date)
    await session.send(msg)


@cg.command('daily_zhihu', aliases=['daily_zhihu', 'daily', '知乎日报'])
async def info_daily_zhihu(session: CommandSession):
    msg = await get_daily_zhihu()
    await session.send(msg)


@cg.command('gank', aliases=['gank', '干货', '整活'])
async def info_gank(session: CommandSession):
    msg = await get_gank()
    await session.send(msg)


@cg.command('steam', aliases=['steam sale', 'steam促销', 'steam优惠'])
async def info_steam(session: CommandSession):
    msg = await get_steam_sale()
    await session.send(msg)


@cg.command('steam_list', aliases=['steam sale list', 'steam促销列表', 'steam优惠列表'])
async def info_steam(session: CommandSession):
    msg = await get_steam_sale_list()
    await session.send(msg)


# 垃圾分类的参数处理器
@info_garbage_classification.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['garbage'] = stripped_arg.split()[0]
        return

    if not stripped_arg:
        session.pause('你倒是说啊')

    session.state[session.current_key] = stripped_arg


# 天气的参数处理器
@info_weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['city'] = stripped_arg.split()[0]
            try:
                session.state['date'] = stripped_arg.split()[1]
            except IndexError:
                session.state['date'] = None
        return

    if not stripped_arg:
        if session.state.get('date'):
            session.pause('要查询的城市名称不能为空呢，请重新输入')

        session.pause('要查询的日期不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg
