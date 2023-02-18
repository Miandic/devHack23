import urlextract
from aiogram import Bot, Dispatcher, executor, types
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

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nSend me a photo of any QR code or a link in the form of text, and I will check it for security")

@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    num = randint(0, 1e9)
    name = str(num) + ".jpg"
    await message.photo[-1].download(name)
    msg = await message.reply("I'm checking your QR code")
    val = detect(name)
    if val[0]:
        ans = ""
        for i in val[1]:
            extractor = urlextract.URLExtract()
            url = extractor.find_urls(i)
            if url:
                res = CheckURL(url[0])
                ans += res["URL"] + "\nChecked:\n\nSSL certificate: " + res["SSL"] + "\nProtocol: " + res["Protocol"] + "\nRedirects: " + res["Redirects"] + "\n\n" + "Result: " + res["Result"] + "\n\n"
            else:
                ans += i +" is not a URL ¯\_(ツ)_/¯" + "\n\n"
        
        await msg.edit_text(ans)
    else:
        await msg.edit_text("QR code is not detected ＞﹏＜")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    extractor = urlextract.URLExtract()
    urls = extractor.find_urls(message.text)
    if urls:
        for i in urls:
            res = CheckURL(i)
            await message.reply(res["URL"] + "\nChecked:\n\nSSL certificate: " + res["SSL"] + "\nProtocol: " + res["Protocol"] + "\nRedirects: " + res["Redirects"] + "\n\n" + "Result: " + res["Result"] + "\n\n")
    else:
        await message.reply("No URLs in your message :)")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)