import re
from glob import glob

from PIL import Image, ImageFont, ImageDraw

font = ImageFont.truetype("zh-cn.ttf", 24)
font_grade = ImageFont.truetype("zh-cn.ttf", 14)
font_title = ImageFont.truetype("zh-cn.ttf", 36)


def parse_admins(filename="admins.txt"):
    result = {"sr_admin": [], "admin": [], "jnr_admin": [], "moderator": [], "helper": []}
    counter = 0
    index = 0
    with open(filename, "r", encoding="utf8") as fp:
        align = "sr_admin"
        for line in fp.readlines():
            if len(line) < 3:
                continue

            if "ГЛАВНАЯ" in line:
                align = "sr_admin"
                index = 0
                continue
            if "ЧЕТВЁРТОГО" in line:
                align = "admin"
                index = 0
                continue
            if "ТРЕТЬЕГО" in line:
                align = "jnr_admin"
                index = 0
                continue
            if "ВТОРОГО" in line:
                align = "moderator"
                index = 0
                continue
            if "ПЕРВОГО" in line:
                align = "helper"
                index = 0
                continue

            if align == "moderator" or align == "helper":
                index = 0

            parsed = re.findall("(.*) \[(.*)] - (.*)", line)[0]
            result[align].append({
                "nickname": parsed[0],
                "short": parsed[1],
                "grade": parsed[2],
                "index": index
            })
            counter += 1
            index += 1
        return result, counter


def generate_single_admin(admin, level):
    global font, font_grade

    files = glob("img/" + level + "/*")
    img = Image.open(files[admin["index"]])
    draw = ImageDraw.Draw(img)

    w, h = draw.textsize(admin['nickname'], font=font)
    w2, h2 = draw.textsize(admin['grade'], font=font_grade)
    offset_y = (256 - h2) / 1.25

    if w > w2:
        rect = (0, offset_y - 5, 255, offset_y + 55)
    else:
        rect = (0, offset_y - 5, 255, offset_y + 55)

    draw.rounded_rectangle(rect, fill=(255, 255, 255), outline=(24, 24, 24), radius=4)
    draw.text(((256 - w) / 2, offset_y), admin['nickname'], (44, 44, 44), font=font)
    draw.text(((256 - w2) / 2, offset_y + 30), admin['grade'], (44, 44, 44), font=font_grade)

    return img


def generate_picture(admin_list, count):
    titles = {
        "sr_admin": "ГЛАВНАЯ АДМИНИСТРАЦИЯ",
        "admin": "АДМИНИСТРАЦИЯ ЧЕТВЁРТОГО УРОВНЯ",
        "jnr_admin": "АДМИНИСТРАЦИЯ ТРЕТЬЕГО УРОВНЯ",
        "moderator": "АДМИНИСТРАЦИЯ ВТОРОГО УРОВНЯ",
        "helper": "АДМИНИСТРАЦИЯ ПЕРВОГО УРОВНЯ"
    }
    background = Image.new(mode="RGB", size=(256 * 3 + 150, int(count / 3) * (256 + 120)))
    draw = ImageDraw.Draw(background)

    y = 0
    prev_grade = ""
    for key, value in admin_list.items():
        if prev_grade != key:
            prev_grade = key
            y += 100
            w, h = draw.textsize(titles[key], font=font_title)
            draw.text(((256 * 3 + 150 - w) / 2, y - 70), titles[key], (255, 255, 255), font=font_title)

        row = 0
        x = 25

        remain = len(value) % 3
        if remain == 1:
            x = int(75 + (256 * 3) / 3)
        if remain == 2:
            x = int(30 + (256 * 3) / 5)

        for admin in value:
            if row == 3 or (row == remain and row != 0):
                row = 0
                x = 25
                y += 256 + 50
                remain = 0

            single = generate_single_admin(admin, key)
            background.paste(single, (x, y), mask=single)

            x += 256 + 50
            row += 1
        y += 256 + 50

    text_count = "Общее количество администраторов - {}.".format(count)
    y += 200
    w, h = draw.textsize(text_count, font=font_title)
    draw.text(((256 * 3 + 150 - w) / 2, y - 70), text_count, (255, 255, 255), font=font_title)

    background.show()


def main():
    admins, count = parse_admins()
    generate_picture(admins, count)


if __name__ == '__main__':
    main()
