# import asyncio
# import json
# from aiogram import Bot, Dispatcher, types
# from aiogram.client.session.aiohttp import AiohttpSession
# from aiogram.enums import PollType
# from aiogram.filters import Command
#
# API_TOKEN = "7903740814:AAH88sXFDLUNd2GQjR5rS1R3Q3Dl5XPLuiI"
#
# bot = Bot(token=API_TOKEN, session=AiohttpSession())
# dp = Dispatcher()
#
# with open("short_questions_randomized.json", "r", encoding="utf-8") as f:
#     questions = json.load(f)
#
# USER_TESTS = {}     # user_id -> savollar ro'yxati
# USER_STATE = {}     # user_id -> savol indeksi
# USER_STATS = {}     # user_id -> to'g'ri/noto'g'ri hisoblari
# current_options = {}  # user_id -> hozirgi savol variantlari
#
# BLOCK_SIZE = 30
# ANSWER_TIMEOUT = 30  # sekund
#
# # Bu yerda userga vaqt haqida xabar berish uchun yordamchi funksiya
# async def countdown_message(chat_id: int):
#     for remaining in range(ANSWER_TIMEOUT, 0, -5):  # har 5 sekundda yangilansin
#         await bot.send_message(chat_id, f"Javob uchun qolgan vaqt: {remaining} soniya")
#         await asyncio.sleep(5)
#
# @dp.message(Command("start"))
# async def start(message: types.Message):
#     user_id = message.from_user.id
#     USER_TESTS[user_id] = questions
#     USER_STATE[user_id] = 0
#     USER_STATS[user_id] = {"togri": 0, "notogri": 0, "block_togri": 0, "block_notogri": 0}
#
#     await message.answer(f"Test boshlanmoqda. Har blokda {BLOCK_SIZE} ta savol bo‘ladi.\n"
#                          f"Har bir savolga javob berish uchun {ANSWER_TIMEOUT} soniya vaqtingiz bor.")
#
#     await send_next_question(message.chat.id, user_id)
#
# async def send_next_question(chat_id: int, user_id: int):
#     if USER_STATE[user_id] >= len(USER_TESTS[user_id]):
#         await bot.send_message(chat_id, "Test yakunlandi!\n"
#                                         f"To‘g‘ri javoblar: {USER_STATS[user_id]['togri']}\n"
#                                         f"Noto‘g‘ri javoblar: {USER_STATS[user_id]['notogri']}")
#         return
#
#     question_data = USER_TESTS[user_id][USER_STATE[user_id]]
#     await send_question(chat_id, user_id, question_data)
#
#     # 30 soniyadan keyin agar user javob bermagan bo'lsa, keyingi savolga o'tamiz
#     try:
#         await asyncio.wait_for(wait_for_answer(user_id), timeout=ANSWER_TIMEOUT)
#     except asyncio.TimeoutError:
#         USER_STATS[user_id]["notogri"] += 1
#         USER_STATS[user_id]["block_notogri"] += 1
#         USER_STATE[user_id] += 1
#         await bot.send_message(chat_id, "Vaqt tugadi! Keyingi savolga o'tamiz.")
#         await send_next_question(chat_id, user_id)
#
# # Bu yerda javob kelishini kutamiz (asyncio.Future kabi ishlatish uchun)
# pending_answers = {}
#
# async def wait_for_answer(user_id):
#     future = asyncio.get_event_loop().create_future()
#     pending_answers[user_id] = future
#     await future  # Bu yerda javob kelsa, future bajariladi
#     pending_answers.pop(user_id, None)
#
# async def send_question(chat_id: int, user_id: int, question_data: dict):
#     question = question_data.get("question", "").strip()
#     options = question_data.get("options", [])
#
#     if not question or not options:
#         await bot.send_message(chat_id, "Xatolik: savol yoki variantlar yo‘q.")
#         return
#
#     trimmed_options = [option.strip()[:100] for option in options if option.strip()]
#     if not trimmed_options:
#         await bot.send_message(chat_id, "Xatolik: variantlar bo‘sh.")
#         return
#
#     correct_option_id = question_data.get("correct_option_id", 0)
#     if correct_option_id >= len(trimmed_options):
#         correct_option_id = 0
#
#     await bot.send_poll(
#         chat_id=chat_id,
#         question=question[:300],
#         options=trimmed_options,
#         is_anonymous=False,
#         type=PollType.QUIZ,
#         correct_option_id=correct_option_id
#     )
#
#     current_options[user_id] = {
#         "correct_text": trimmed_options[correct_option_id],
#         "options": trimmed_options
#     }
#
#
# @dp.poll_answer()
# async def handle_poll_answer(poll_answer: types.PollAnswer):
#     user_id = poll_answer.user.id
#     questions = USER_TESTS.get(user_id)
#     if not questions:
#         return
#
#     index = USER_STATE.get(user_id, 0)
#     if index >= len(questions):
#         return
#
#     user_data = current_options.get(user_id)
#     if not user_data:
#         return
#
#     correct_text = user_data["correct_text"]
#     options = user_data["options"]
#
#     try:
#         correct_index = options.index(correct_text)
#     except ValueError:
#         correct_index = 0
#
#     selected_option = poll_answer.option_ids[0] if poll_answer.option_ids else None
#
#     if selected_option == correct_index:
#         USER_STATS[user_id]["togri"] += 1
#         USER_STATS[user_id]["block_togri"] += 1
#         reply_text = "To‘g‘ri javob!"
#     else:
#         USER_STATS[user_id]["notogri"] += 1
#         USER_STATS[user_id]["block_notogri"] += 1
#         reply_text = "Noto‘g‘ri javob!"
#
#     await bot.send_message(poll_answer.user.id, reply_text)
#
#     USER_STATE[user_id] += 1
#
#     # Javob kelganda wait_for_answer uchun future ni bajarish
#     future = pending_answers.get(user_id)
#     if future and not future.done():
#         future.set_result(True)
#
#     # Keyingi savolga o'tishni kutish o‘rniga, send_next_question funksiya start dan chaqiradi va timeout bilan boshqariladi
#
#
# if __name__ == "__main__":
#     import logging
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(dp.start_polling(bot))

import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import PollType
from aiogram.filters import Command

API_TOKEN = "7903740814:AAH88sXFDLUNd2GQjR5rS1R3Q3Dl5XPLuiI"

bot = Bot(token=API_TOKEN, session=AiohttpSession())
dp = Dispatcher()

with open("short_questions_randomized.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

USER_TESTS = {}     # user_id -> savollar ro'yxati
USER_STATE = {}     # user_id -> savol indeksi
USER_STATS = {}     # user_id -> to'g'ri/noto'g'ri hisoblari
current_options = {}  # user_id -> hozirgi savol variantlari
pending_answers = {}  # user_id -> asyncio.Future

BLOCK_SIZE = 30
ANSWER_TIMEOUT = 30  # sekund

# BLOCK_SIZE = 30 (oldingi kodingda bor)

async def send_next_question(chat_id: int, user_id: int):
    # Savollar tugadi
    if USER_STATE[user_id] >= len(USER_TESTS[user_id]):
        await bot.send_message(chat_id, "Test yakunlandi!\n"
                                        f"To‘g‘ri javoblar: {USER_STATS[user_id]['togri']}\n"
                                        f"Noto‘g‘ri javoblar: {USER_STATS[user_id]['notogri']}")
        return

    # Agar blok tugagan bo'lsa (masalan, 30 ta savoldan keyin)
    if USER_STATE[user_id] > 0 and USER_STATE[user_id] % BLOCK_SIZE == 0:
        # Blok natijalarini beramiz
        togri = USER_STATS[user_id]["block_togri"]
        notogri = USER_STATS[user_id]["block_notogri"]
        await bot.send_message(chat_id,
                               f"Blok tugadi! To‘g‘ri javoblar: {togri}, noto‘g‘ri javoblar: {notogri}\n"
                               f"Keyingi blokni boshlash uchun /continue ni bosing.")

        # Blok statistikasini qayta tiklaymiz
        USER_STATS[user_id]["block_togri"] = 0
        USER_STATS[user_id]["block_notogri"] = 0
        return  # keyingi savolni hozircha jo'natmaymiz, foydalanuvchidan /continue komandasi kutamiz

    question_data = USER_TESTS[user_id][USER_STATE[user_id]]
    await send_question(chat_id, user_id, question_data)

    try:
        await asyncio.wait_for(wait_for_answer(user_id), timeout=ANSWER_TIMEOUT)
    except asyncio.TimeoutError:
        USER_STATS[user_id]["notogri"] += 1
        USER_STATS[user_id]["block_notogri"] += 1
        USER_STATE[user_id] += 1
        await bot.send_message(chat_id, "Vaqt tugadi! Keyingi savolga o'tamiz.")
        await send_next_question(chat_id, user_id)

@dp.message(Command("continue"))
async def continue_test(message: types.Message):
    user_id = message.from_user.id
    if user_id not in USER_STATE or user_id not in USER_TESTS:
        await message.answer("Siz hali testni boshlamagansiz. /start komandasini bosing.")
        return

    # Blok yakunlangandan keyin keyingi savolga o‘tish uchun indexni oshiramiz
    USER_STATE[user_id] += 1

    await send_next_question(message.chat.id, user_id)


async def wait_for_answer(user_id):
    future = asyncio.get_event_loop().create_future()
    pending_answers[user_id] = future
    await future
    pending_answers.pop(user_id, None)

async def send_question(chat_id: int, user_id: int, question_data: dict):
    question = question_data.get("question", "").strip()
    options = question_data.get("options", [])

    if not question or not options:
        await bot.send_message(chat_id, "Xatolik: savol yoki variantlar yo‘q.")
        return

    trimmed_options = [option.strip()[:100] for option in options if option.strip()]
    if not trimmed_options:
        await bot.send_message(chat_id, "Xatolik: variantlar bo‘sh.")
        return

    correct_option_id = question_data.get("correct_option_id", 0)
    if correct_option_id >= len(trimmed_options):
        correct_option_id = 0

    await bot.send_poll(
        chat_id=chat_id,
        question=question[:300],
        options=trimmed_options,
        is_anonymous=False,
        type=PollType.QUIZ,
        correct_option_id=correct_option_id
    )

    current_options[user_id] = {
        "correct_text": trimmed_options[correct_option_id],
        "options": trimmed_options
    }

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    USER_TESTS[user_id] = questions
    USER_STATE[user_id] = 0
    USER_STATS[user_id] = {"togri": 0, "notogri": 0, "block_togri": 0, "block_notogri": 0}

    await message.answer(f"Test boshlanmoqda. Har blokda {BLOCK_SIZE} ta savol bo‘ladi.\n"
                         f"Har bir savolga javob berish uchun {ANSWER_TIMEOUT} soniya vaqtingiz bor.")

    await send_next_question(message.chat.id, user_id)

@dp.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id
    questions = USER_TESTS.get(user_id)
    if not questions:
        return

    index = USER_STATE.get(user_id, 0)
    if index >= len(questions):
        return

    user_data = current_options.get(user_id)
    if not user_data:
        return

    correct_text = user_data["correct_text"]
    options = user_data["options"]

    try:
        correct_index = options.index(correct_text)
    except ValueError:
        correct_index = 0

    selected_option = poll_answer.option_ids[0] if poll_answer.option_ids else None

    if selected_option == correct_index:
        USER_STATS[user_id]["togri"] += 1
        USER_STATS[user_id]["block_togri"] += 1
        reply_text = "To‘g‘ri javob!"
    else:
        USER_STATS[user_id]["notogri"] += 1
        USER_STATS[user_id]["block_notogri"] += 1
        reply_text = "Noto‘g‘ri javob!"

    await bot.send_message(user_id, reply_text)

    USER_STATE[user_id] += 1

    # Javob kelganda wait_for_answer uchun future ni bajarish
    future = pending_answers.get(user_id)
    if future and not future.done():
        future.set_result(True)

    # Keyingi savolga o'tish
    await send_next_question(user_id, user_id)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    import asyncio
    asyncio.run(dp.start_polling(bot))
