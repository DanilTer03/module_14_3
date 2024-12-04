from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Update
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = 'API_TOKEN'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button, button2)

kb = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
kb.add(button)
kb.add(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n '
                              'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161', reply_markup=kb)
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup=kb1)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст', reply_markup=None)
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост', reply_markup=None)
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес', reply_markup=None)
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша дневная норма калорий: {calories} ккал', reply_markup=kb)
    await state.finish()


def start(update: Update):
    keyboard = [[InlineKeyboardButton("Купить", callback_data='buy')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Добро пожаловать! Выберите опцию:", reply_markup=reply_markup)


def get_buying_list(update: Update):
    products = [
        {"name": "Витамины1", "description": "Витамины для всех", "price": 100, "image": "https://avatars.mds.yandex.net/get-mpic/5209485/2a0000018f19274b8857fddbd1b7ba9d3cbc/180x240"},
        {"name": "Витамины2", "description": "Витамины для мужчин", "price": 200, "image": "https://yabs.yandex.ru/count/WpmejI_zOoVX2Ldo0tKP04Dkhiqui9Sc27YN2EWWc534EQ3SQG9zFfSxUxRVkVE6Er-_u_M6EzmGjZrzEgVEQ0x5fVSjnMtdiog4PD_vKuhd-1DwGtbc7ELmEgEvdKUVqgVjnEze3irjdgeGDOTJEiMdKwaJ2kMf2id8CSrpfnI7sdRrnuW6q8yrI0Zfw0V9UhIKzBD48udenofKmmZ9g8hZvwZwWsIzNer-JaX1s4-eSohDfKzdBdr6RQTTOeb6aeax-iHps-cKsYIKPYJLpcajeuO-xNg8g7OwfJKGLQbMGZ8wIggJwY8hKKr5KXfQge6eGqSrwbefQAbgX7G4kGEcR1vmf4D200XG-WWY-4618Go3ZkCDFF4Fy-HZu9ZErflNVFoO4eG7eU83MIK5Q1_8yXMWVI2Rf03j0rcz0hGgbfZbV4s4PmXgWJ53pEacFOaBVmZx3ruwCibZbR0FMU-1soo3meHa0B67yaMGY9Uo8K2-1lYowF6fxQTTKuTgIANJf_IUFgLG_2cLIcidL0hDfL7erBRl-vRQ4U1WCpZCGaX5DnROTEFrYs3msn548r24tEnZSsKr4B2SppTC0MpWYkYg6fmwZ3FZQZNi8EpGTRr6tt0bYDdWObsIEXfkasQxo0mXfSHI0YMatFTzttS0NnXqdRk78QES3TbgfLZOEg3hJ3DacYo1A58KjaqT2sRIwaunOcQCNgKXmesa6n540DCrwY6ec7UD2MhgCPjSPdDd9ia2--4CJtb5FZY494p-bqxozhrqahVFNV8G_Fiox0lxjHH-yFqiXHzyJ7FJYebPRbenbKKzGj5fymN9g2PnTDialVLJMiXqDkhBVejCaj2JlP8wlZy_fZqO0IV59ct-UoVHwePrAUGqlzz9nE2okew6vRKU2PkVsn0oVQeEIqMGkvWhbKgb30jADB6PZig_PPBB1gI7dnCZ_7a4Cq2Z7Z4Sz0S-AquAGH9F83Yx84lQzms-ib0RY7LAH2AWQtiqcfyebgkmKwA6Xgf--5WCEcjmL5baLKRyBiO8HpzJKZN9TCiznMew49vza_B9sv7lTsXgx8GYI7e4RzDqY20A2BiuxhD0WiziAru0~2?clid=1648&src_pof=1648&baobab_event_id=m49t6rm81&wprid=1733311956785750-77724572937297789-balancer-l7leveler-kubr-yp-vla-121-BAL&icookie=Cmh3Lsrba9NFL%2BZCkDyYnr0j9UWXgCJrMsWTiAZD2Yhdt1mR6O%2Bl4cgJjXbJH7iUeaJtWSXP8BI4sAnm4PkeCJ%2BJxpg%3D"},
        {"name": "Витамины3", "description": "Витамины для женщин", "price": 300, "image": "https://yabs.yandex.ru/count/WoSejI_zOoVX2LdY0yqO05Eifyqui9T61BnB17GGJ2aQK2ftca2Vp-NEdkrtxhpXpjVlUBtX3ZV4zCwbKJo_xJktez2fKogj2Y7PqsSEjN7er7b3UMOSvO3YKrkAJwTurEQf2b5pEA5EfnH_Jd4xlwLFtBQhFqOqW7wGWf9e817z35chHaG_Lg4QHaX6LHm_HzKV9ElrQlHpGWh2VaATKnFIg7HgI-ser2P1mqZ9EWH4LQgTqHf9Y3gZJXeIeXRLHK8qaceagemXewIwI6X6q8oa8kiC73LLQAXQtoWI8g8g2TMeQwMWfQeHqf6K7J1byu0Z40E0O5Jw28mOQuXqW477qKlPJNM1nKngH7IstgcBaYxthSYLtmDP9GLe7yZo5Q1z89ka0Eq3MRq2j2gMcELyJP0zmS3Z7D3BwIPfIKasmr1Md0mWzamw5XSB5wnQU80lYnwVsdxQDNMeXbFwd4xnAHINshRJEPr2xzkkfKyxlsqydzhsVTzIcmKEDeF3B8HKT6E1JJTUlmW6lnr1D095oCqk66Ljmm7I03PmHNHL3Hg9Z3FZQZNi8EpGTRr6tt0bYDdWObsIEXfkasQxo0mXfSHI0YMatFTzttS0NnXqdRk78QES3TbgfLZOEg3hJ3DacYo1A54KjaqT2sRIwaunOcQCNgKnWj807X4OmNIDUWWgvbrZWffwp2QNsTmf7591--44rCYIV303Zut_AsEbxtjbhFHzheKjmhzxB4cWVEq8lI4_Eq9l2DFCX0jZbfbmOMLHZr1qsam1aOumZMwRfBT-IWkPpZ9zsM-HIH9wikSxcsFpOzg33u1imiFpNnnSgfvOUIwjwteabwedLdw_zNn84UjqaNzUwuzCmQBx8DEdwh1K1BcBkLAfLCgme4IZpJnK_X462A5715K38WWb_3a4CpuZDVvpVw1dEYcX9z_0y6o7ZsGAhi4VNH5TAhO6RXmIqS_dcjkCx4qKAzjpDhHfc-eF_ooSpdhrRv7v6RD1ywA-K5Do3Wx5wCec5NeyPKexw1ek3da0k5E6UU1I-eJsYcG9Fa7luVLF7dPTIon7WXywr7K0~2?clid=1648&src_pof=1648&baobab_event_id=m49t7dzo3&wprid=1733311984138127-13359900117459499270-balancer-l7leveler-kubr-yp-vla-121-BAL&icookie=Cmh3Lsrba9NFL%2BZCkDyYnr0j9UWXgCJrMsWTiAZD2Yhdt1mR6O%2Bl4cgJjXbJH7iUeaJtWSXP8BI4sAnm4PkeCJ%2BJxpg%3D"},
        {"name": "Витамины4", "description": "Витамины для детей", "price": 400, "image": "https://yabs.yandex.ru/count/WmOejI_zOoVX2Ld00yKN03Cgdyqui6GJ0jub0Ze8fXHD49GxJQ3Fvt9dp_OxTzvmv-jtlDvmXnj26eLESpkAvq_ydkRIF7f3gq98zlIPGsqSEdNUK9uPHpcW-DIMujCf7hLvgaBK74weqod5drFSpc_f4xVjweyH3Q0VfA0a6aX4FqFMgX7HZrMeXX6IKHN7pr7r1ybwlHhzd922i9zGvzJ44uf7dqxxcPC0eYhLrYeLYNfK3r69X8geTTBIq56TL5kHbfIeHNMj5BHKDK8wmji1KpOFE0hHG4y5IYNCKcpA5XGOT1ozbDrK5rZCf4P4Poi0LPEexMGMHwO7iaeAq3wGvIj0-q0sIG7Q1x9w1MXLB37B-PfekzgmOWi2TpdT92qfoQKEEpgi0SG-Kbzm5f8TN-e6-BBeyQdjfrrJXshW-THvF_4dz8v6ywSjVURHsXbrsaxxTZgVzdtVqWmEin1IqOq5Djru_I8O_7O4qGWK8JUx14n7Qi0m4S06heYkga4ZaN5cNAs67OGTkgxNw1kk134RNAnBKaV3RT9i5vaXf9HOIg24bFk-x_iEu0k3hdDtep1abBCXMwqK2ri7T9rfXaoJ9H15YiAsgMF1J5hTAKRCZD6hD78uRL03iuJf6lKGLCoxnWGrzPXDBhEvKpYaWlR32QYH9VdW4CBV_vs0LlYz4z0AFrS6Y92_ByEmsBvsXqhLp-vGgMAQQQeoPfccAYkBUeIYq-Rb4pGiAxfjajxwAIraEilqPRz59adeoPxlR8xDZsaFFW2o2G_FVt5mgNfYvRcqhkkHNAgUMFdzXijI6UjzX8jUwuzCmQBx8DEdwh1K1BcBkLAfLCgme86bpGGhFmWd9LH0Et63WYRyiGFpEICrwd9_lSx4vw2Vpi3GPzUndWMDmMCQ4SSO6GEn_WsHtt9jFGBdUcWG4kVsWqFJzCFuQD1PeEcpG9PULcXuz8LwoHuYSaegHjVjKzFutspQuPksE8kfEOQJUL0--eGsgsG9BhltSDCc3xkvT096Wa_hkNm0~2?clid=1648&src_pof=1648&baobab_event_id=m49t7rn74&wprid=1733312003101060-6827128663524230984-balancer-l7leveler-kubr-yp-vla-121-BAL&icookie=Cmh3Lsrba9NFL%2BZCkDyYnr0j9UWXgCJrMsWTiAZD2Yhdt1mR6O%2Bl4cgJjXbJH7iUeaJtWSXP8BI4sAnm4PkeCJ%2BJxpg%3D"},
    ]

    message_text = ""
    for product in products:
        message_text += f'Название: {product["name"]} | Описание: {product["description"]} | Цена: {product["price"]}\n'
        FSMContext.bot.send_photo(update.message.chat_id, product["image"])

    keyboard = [
        [InlineKeyboardButton("Витамины1", callback_data='product_buying'),
         InlineKeyboardButton("Витамины2", callback_data='product_buying')],
        [InlineKeyboardButton("Витамины3", callback_data='product_buying'),
         InlineKeyboardButton("Витамины4", callback_data='product_buying')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text += "Выберите продукт для покупки:"
    update.message.reply_text(message_text, reply_markup=reply_markup)


def button(update: Update):
    query = update.callback_query
    query.answer()
    if query.data == 'buy':
        get_buying_list(query.message)


def send_confirm_message(update: Update):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Вы успешно приобрели продукт!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
