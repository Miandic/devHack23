import urlextract
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
from qrdetector import detect
from checker import CheckURL
from secret import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


'''
———————————No secret.py?———————————
⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
—————————————————————————————
'''


bLike = InlineKeyboardButton('👍', callback_data='Liked')
bDislike = InlineKeyboardButton('👎', callback_data='Disliked')
rateButtons = [bLike, bDislike]
rateKeyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(rateButtons)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Hi!\nSend me a photo of any QR code or a link in the form of text, and I will check it for security')

@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    num = randint(0, 1e9)
    name = str(num) + '.jpg'
    await message.photo[-1].download(name)
    msg = await message.reply("I'm checking your QR code")
    val = detect(name)
    os.remove(name)
    if val[0]:
        for i in val[1]:
            extractor = urlextract.URLExtract()
            url = extractor.find_urls(i)
            if url:
                try:
                    res = CheckURL(url[0])
                    ans = (
                        'Checked\n'
                        + res['URL']
                        + '\n\nSSL certificate: ' + res['SSL']
                        + '\nProtocol: ' + res['Protocol']
                        + '\nRedirects: ' + res['Redirects']
                        + '\n\n' + 'Result: ' + res['Result']
                    )
                    await bot.send_message(message.from_user.id, ans, parse_mode='HTML')
                except Exception:
                    await bot.send_message(message.from_user.id, 'Sorry, something went wrong ＞﹏＜', parse_mode='HTML')
            else:
                ans = str(
                    '<b>' + i + '</b>'
                    + ' is not a URL\n¯\_(ツ)_/¯'
                )
                await bot.send_message(message.from_user.id, ans, parse_mode='HTML')
    else:
        await msg.edit_text('<b>QR code</b> is not detected ＞﹏＜', parse_mode='HTML')


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    extractor = urlextract.URLExtract()
    urls = extractor.find_urls(message.text)
    if urls:
        for i in urls:
            res = CheckURL(i)
            await message.reply(
                res['URL']
                + '\nChecked:\n\nSSL certificate: ' + res['SSL']
                + '\nProtocol: ' + res['Protocol']
                + '\nRedirects: ' + res['Redirects']
                + '\n\n' + 'Result: ' + res['Result']
                + '\n\n'
            , parse_mode='HTML')
    else:
        await message.reply('No URLs in your message', parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)