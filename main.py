from aiogram.utils import executor
from aiogram.bot import Bot
from aiogram.types import ParseMode, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from funcs.side_functions import hello_text as ht
from funcs.shop_analyzer import Analyze
import matplotlib.pyplot as plt
from aiogram.utils.exceptions import Throttled
import random
import os

bot = Bot(
    token='5820279492:AAE-4_0teoYCkfzJlZfJMMS9H23O2rye8pM',
    disable_web_page_preview=True,
    parse_mode=ParseMode.HTML
)
dp = Dispatcher(bot)


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Давайте договоримся не флудить.\n"
                   "Запрос можно делать раз в 5 секунд!")

@dp.message_handler(commands=['start'])
@dp.throttled(anti_flood, rate=5)
async def start_func(m: Message):

    await bot.send_message(
        m.from_user.id,
        str(ht()) + "\n\nДанный бот поможет вам найти самую дешевую технику в Беларуси!\n"
                    "Просто напишите название техники, например IPhone 13, "
                    "наш бот сам проанализирует крупные магазины и выдаст оптимальные варианты!"
    )


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=5)
async def main_func(m: Message):
    data = Analyze(m.text)
    output = await data.get_analysis_data()
    plt.title("Сравнение цен в магазинах")
    visual_data = [[], []]
    text = 'Вот, <b>минимальные</b> цены на ' + m.text + " в разных магазинах!\n\n"
    kb = InlineKeyboardMarkup()
    print(output)
    for i in output:
        print(output)
        if not output[i]:
            continue
        visual_data[0].append(i)
        visual_data[1].append(output[i][0])
        text += i + ' от ' + str(output[i][0]) + 'руб\n'
        kb.add(InlineKeyboardButton("Перейти в " + i + f" ({str(output[i][0])}руб)", url=str(output[i][1])))
    if visual_data[0]:
        photo = 'temp' + "/" + str(random.randint(1, 10000)) + '.png'
        plt.bar(visual_data[0], visual_data[1])
        plt.xlabel("Магазины")
        plt.ylabel("Цена (BYN)")
        plt.savefig(photo)
        await bot.send_photo(
            chat_id=m.from_user.id,
            photo=open(photo, 'rb'),
            caption=text,
            reply_markup=kb
        )
        os.remove(photo)
    else:
        await bot.send_message(
            m.from_user.id,
            'По вашему запросу ничего не найдено :('
        )

if __name__ == "__main__":
    executor.start_polling(dp)
