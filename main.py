# import json
# import asyncio
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# API_TOKEN = "7903740814:AAGa9Xy6WxfNPpX2F2c5Qj8CHlzPIY1ZVrU"  # Bu yerga tokeningizni qo'ying
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()
#
# with open("json.file", "r", encoding="utf-8") as f:
#     questions = json.load(f)
#
# USER_STATE = {}  # Foydalanuvchining hozirgi savol indeksi
# USER_STATS = {}  # Foydalanuvchining to'g'ri/noto'g'ri javoblari statistikasi
#
# BLOCK_SIZE = 30  # Har blokda 30 ta savol
#
#
# @dp.message(Command("start"))
# async def start_quiz(message: types.Message):
#     user_id = message.from_user.id
#     USER_STATE[user_id] = 0  # Savol indeksi
#     USER_STATS[user_id] = {"togri": 0, "notogri": 0, "block_togri": 0, "block_notogri": 0}
#     await message.answer(f"Test boshlanmoqda. Har blokda {BLOCK_SIZE} ta savol bo'ladi.")
#     await send_question(message.chat.id, user_id)
#
#
# async def send_question(chat_id: int, user_id: int):
#     index = USER_STATE.get(user_id, 0)
#
#     if index >= len(questions):
#         # Test yakunlandi
#         await bot.send_message(chat_id, "Test yakunlandi! Umumiy natijalar:\n"
#                                         f"✅ To'g'ri: {USER_STATS[user_id]['togri']}\n"
#                                         f"❌ Noto'g'ri: {USER_STATS[user_id]['notogri']}")
#         return
#
#     # Blok oxirigacha yetganmisiz?
#     if index > 0 and index % BLOCK_SIZE == 0:
#         # Blok natijalarini ko'rsatamiz
#         block_correct = USER_STATS[user_id].get("block_togri", 0)
#         block_wrong = USER_STATS[user_id].get("block_notogri", 0)
#
#         # Blok statistikasini reset qilamiz keyingi blok uchun
#         USER_STATS[user_id]["block_togri"] = 0
#         USER_STATS[user_id]["block_notogri"] = 0
#
#         kb = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="Keyingi blok ➡️", callback_data="next_block")]
#         ])
#         await bot.send_message(chat_id,
#                                f"Blok tugadi. Ushbu blokda:\n✅ To'g'ri javoblar: {block_correct}\n❌ Noto'g'ri javoblar: {block_wrong}\n\n"
#                                f"Keyingi blokni boshlash uchun tugmani bosing.",
#                                reply_markup=kb)
#         return
#
#     # Savolni yuborish
#     q = questions[index]
#     options_dict = q.get("variantlar", {})
#     keys_order = ["a", "b", "c", "d"]
#     # Faqat mavjud variantlarni olish
#     options = [options_dict.get(k, "").strip() for k in keys_order if options_dict.get(k, "").strip() != ""]
#
#     # Variantlar soni 100 dan oshmasligi
#     if len(options) > 100:
#         options = options[:100]
#
#     correct_key = q.get("togri_javob")
#     correct_answer_text = options_dict.get(correct_key, "")
#
#     try:
#         correct_index = options.index(correct_answer_text)
#     except ValueError:
#         correct_index = 0
#
#     question_text = f"[ Savol {index + 1} / {len(questions)} ]\n{q['savol']}"
#
#     await bot.send_poll(
#         chat_id=chat_id,
#         question=question_text,
#         options=options,
#         type="quiz",
#         correct_option_id=correct_index,
#         is_anonymous=False,
#         explanation=f"✅ To‘g‘ri javob: {correct_answer_text}",
#         open_period=30
#     )
#
#
# @dp.poll_answer()
# async def handle_poll_answer(poll_answer: types.PollAnswer):
#     user_id = poll_answer.user.id
#     index = USER_STATE.get(user_id, 0)
#     if index >= len(questions):
#         return
#
#     q = questions[index]
#     keys_order = ["a", "b", "c", "d"]
#     correct_key = q.get("togri_javob", "a")
#     correct_index = keys_order.index(correct_key) if correct_key in keys_order else 0
#
#     selected_option = None
#     if poll_answer.option_ids:
#         selected_option = poll_answer.option_ids[0]
#
#     if selected_option == correct_index:
#         USER_STATS[user_id]["togri"] += 1
#         USER_STATS[user_id]["block_togri"] = USER_STATS[user_id].get("block_togri", 0) + 1
#     else:
#         USER_STATS[user_id]["notogri"] += 1
#         USER_STATS[user_id]["block_notogri"] = USER_STATS[user_id].get("block_notogri", 0) + 1
#
#     USER_STATE[user_id] += 1
#
#     # Javobdan keyin 1 soniya kutamiz va keyingi savolni yuboramiz
#     await asyncio.sleep(1)
#     await send_question(poll_answer.user.id, user_id)
#
#
# @dp.callback_query(lambda c: c.data == "next_block")
# async def process_next_block(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     await callback_query.answer()  # Callbackni tasdiqlash
#
#     await send_question(callback_query.message.chat.id, user_id)
#
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(dp.start_polling(bot))


# import json
# import os
#
# print("Current working directory:", os.getcwd())
#
# def convert_test_file_to_json(input_file, output_file):
#     with open(input_file, "r", encoding="utf-8") as f:
#         lines = [line.strip() for line in f]
#
#     questions = []
#     i = 0
#     total_lines = len(lines)
#
#     while i < total_lines:
#         if lines[i] == "":
#             i += 1
#             continue
#
#         savol = lines[i]
#         i += 1
#
#         variantlar = []
#         correct_index = None
#
#         while i < total_lines:
#             line = lines[i]
#
#             if line == "+++++":
#                 i += 1
#                 break
#             elif line.startswith("#"):
#                 variant = line[1:].strip()
#                 correct_index = len(variantlar)
#                 variantlar.append(variant)
#             elif line == "=====" or line == "":
#                 i += 1
#                 continue
#             else:
#                 variantlar.append(line)
#             i += 1
#
#         if not variantlar:
#             continue
#
#         keys = ["a", "b", "c", "d", "e", "f", "g", "h"]
#         variant_dict = {}
#         for idx, var in enumerate(variantlar):
#             key = keys[idx] if idx < len(keys) else f"var{idx}"
#             variant_dict[key] = var
#
#         correct_key = keys[correct_index] if correct_index is not None else "a"
#
#         questions.append({
#             "savol": savol,
#             "variantlar": variant_dict,
#             "togri_javob": correct_key
#         })
#
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(questions, f, ensure_ascii=False, indent=2)
#
#     print(f"✅ Jarayon tugadi, savollar soni: {len(questions)}")
#     print(f"JSON fayl saqlandi: {output_file}")
#

# 7903740814:AAGa9Xy6WxfNPpX2F2c5Qj8CHlzPIY1ZVrU
# # To'liq to'g'ri yo'lni kiriting:
# convert_test_file_to_json("/home/oybek/PycharmProjects/Test/sorovnoma.txt", "json.file")


import json
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = "7903740814:AAGa9Xy6WxfNPpX2F2c5Qj8CHlzPIY1ZVrU"  # o'zingizning tokeningizni yozing

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Savollarni yuklash
with open("json.file", "r", encoding="utf-8") as f:
    questions = json.load(f)

USER_STATE = {}   # Foydalanuvchi -> qaysi savolga keldi
USER_STATS = {}   # Foydalanuvchi -> to‘g‘ri/noto‘g‘ri
current_options = {}  # Foydalanuvchi -> hozirgi savoldagi aralashtirilgan variantlar

BLOCK_SIZE = 30


@dp.message(Command("start"))
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    USER_STATE[user_id] = 0
    USER_STATS[user_id] = {"togri": 0, "notogri": 0, "block_togri": 0, "block_notogri": 0}
    await message.answer(f"Test boshlanmoqda. Har blokda {BLOCK_SIZE} ta savol bo'ladi.")
    await send_question(message.chat.id, user_id)


async def send_question(chat_id: int, user_id: int):
    index = USER_STATE.get(user_id, 0)

    if index >= len(questions):
        await bot.send_message(chat_id, "Test yakunlandi!\n"
                                        f"✅ To‘g‘ri: {USER_STATS[user_id]['togri']}\n"
                                        f"❌ Noto‘g‘ri: {USER_STATS[user_id]['notogri']}")
        return

    # Blok tugadi
    if index > 0 and index % BLOCK_SIZE == 0:
        block_correct = USER_STATS[user_id]["block_togri"]
        block_wrong = USER_STATS[user_id]["block_notogri"]
        USER_STATS[user_id]["block_togri"] = 0
        USER_STATS[user_id]["block_notogri"] = 0

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Keyingi blok ➡️", callback_data="next_block")]
        ])
        await bot.send_message(chat_id,
                               f"Blok tugadi.\n✅ To‘g‘ri: {block_correct}\n❌ Noto‘g‘ri: {block_wrong}\n\n"
                               f"Keyingi blokni boshlash uchun tugmani bosing.",
                               reply_markup=kb)
        return

    q = questions[index]
    options_dict = q.get("variantlar", {})
    correct_key = q.get("togri_javob", "a")
    correct_text = options_dict.get(correct_key, "").strip()

    keys_order = ["a", "b", "c", "d"]
    original_options = [(k, options_dict.get(k, "").strip()) for k in keys_order if options_dict.get(k, "").strip()]
    random.shuffle(original_options)
    options = [text for _, text in original_options]

    correct_index = options.index(correct_text)

    # ✅ Saqlaymiz: foydalanuvchining hozirgi variantlar ro‘yxatini
    current_options[user_id] = {
        "correct_text": correct_text,
        "options": options
    }

    question_text = f"[Savol {index + 1} / {len(questions)}]\n{q['savol']}"

    await bot.send_poll(
        chat_id=chat_id,
        question=question_text,
        options=options,
        type="quiz",
        correct_option_id=correct_index,
        is_anonymous=False,
        explanation=f"✅ To‘g‘ri javob: {correct_text}",
        open_period=30
    )


@dp.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id
    index = USER_STATE.get(user_id, 0)
    if index >= len(questions):
        return

    user_data = current_options.get(user_id)
    if not user_data:
        return

    correct_text = user_data["correct_text"]
    options = user_data["options"]

    correct_index = options.index(correct_text)
    selected_option = poll_answer.option_ids[0] if poll_answer.option_ids else None

    if selected_option == correct_index:
        USER_STATS[user_id]["togri"] += 1
        USER_STATS[user_id]["block_togri"] += 1
    else:
        USER_STATS[user_id]["notogri"] += 1
        USER_STATS[user_id]["block_notogri"] += 1

    USER_STATE[user_id] += 1
    await asyncio.sleep(1)
    await send_question(poll_answer.user.id, user_id)


@dp.callback_query(lambda c: c.data == "next_block")
async def process_next_block(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.answer()
    await send_question(callback_query.message.chat.id, user_id)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
