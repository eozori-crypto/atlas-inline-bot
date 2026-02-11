import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

TOKEN = os.getenv("BOT_TOKEN", "").strip()

bot = Bot(token=TOKEN)
dp = Dispatcher()

def fmt(x: float) -> str:
    return f"{x:.2f}"

@dp.inline_query()
async def inline_calc(q: types.InlineQuery):
    raw = (q.query or "").strip().replace(",", ".")
    if not raw:
        await q.answer([], cache_time=0)
        return

    try:
        # Форматы:
        # 2500 2.25
        # 2500/2.25
        if "/" in raw:
            total_str, percent_str = raw.split("/", 1)
        else:
            parts = raw.split()
            if len(parts) < 2:
                raise ValueError
            total_str, percent_str = parts[0], parts[1]

        total = float(total_str)
        percent = float(percent_str)

        net = total / (1 + percent / 100)

        # USDT сумма в коде, чтобы удобно копировать
        text = f"{fmt(net)} USDT + {fmt(percent)}% = {fmt(total)} USD"

        result = InlineQueryResultArticle(
            id="calc",
            title="Exchange calculation",
            description=f"{fmt(net)} USDT + {fmt(percent)}% = {fmt(total)} USD",
            input_message_content=InputTextMessageContent(
                text,
                parse_mode="Markdown"
            )
        )

        await q.answer([result], cache_time=0)

    except:
        await q.answer([], cache_time=0)

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN not set")
    await dp.start_polling(bot)

if _name_ == "_main_":
    asyncio.run(main()
