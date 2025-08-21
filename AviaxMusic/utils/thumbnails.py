import os 
import aiohttp 
import aiofiles 
import traceback from PIL 
import Image, ImageDraw, ImageFilter, ImageFont from youtubesearchpython.future import VideosSearch

def changeImageSize(maxWidth, maxHeight, image): ratio = min(maxWidth / image.size[0], maxHeight / image.size[1]) newSize = (int(image.size[0] * ratio), int(image.size[1] * ratio)) return image.resize(newSize, Image.ANTIALIAS)

def rounded_rectangle_mask(size, radius): w, h = size mask = Image.new("L", (w, h), 0) draw = ImageDraw.Draw(mask) draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255) return mask

def add_shadow(base, box, radius=46, blur=32, opacity=110): x, y, w, h = box shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0)) ImageDraw.Draw(shadow).rounded_rectangle([0, 0, w, h], radius=radius, fill=(0, 0, 0, opacity)) shadow = shadow.filter(ImageFilter.GaussianBlur(blur)) base.alpha_composite(shadow, (x, y + 6))

def draw_controls(draw, base_y, center_x): gap = 120 color = (0, 0, 0) # Shuffle draw.line([(center_x-2gap-20, base_y-8),(center_x-2gap+15, base_y-8)], width=4, fill=color) draw.polygon([(center_x-2gap+15, base_y-14),(center_x-2gap+28, base_y),(center_x-2gap+15, base_y+14)], fill=color) # Previous draw.polygon([(center_x-gap+20,base_y-15),(center_x-gap-30,base_y),(center_x-gap+20,base_y+15)], fill=color) draw.rectangle([center_x-gap+28, base_y-15, center_x-gap+36, base_y+15], fill=color) # Play button r = 30 draw.ellipse([center_x-r, base_y-r, center_x+r, base_y+r], outline=color, width=4) draw.polygon([(center_x-10, base_y-18),(center_x-10, base_y+18),(center_x+18, base_y)], fill=color) # Next draw.polygon([(center_x+gap-20,base_y-15),(center_x+gap+30,base_y),(center_x+gap-20,base_y+15)], fill=color) draw.rectangle([center_x+gap-36, base_y-15, center_x+gap-28, base_y+15], fill=color) # Repeat draw.arc([center_x+gap2-24, base_y-20, center_x+gap2+24, base_y+20], start=210, end=20, width=4, fill=color) draw.polygon([(center_x+gap2+26, base_y-2),(center_x+gap2+10, base_y-10),(center_x+gap2+6, base_y+10)], fill=color)

async def get_thumb(videoid: str): url = f"https://www.youtube.com/watch?v={videoid}" try: results = VideosSearch(url, limit=1) result = (await results.next())["result"][0]

title = result.get("title", "Unknown Title")
    duration = result.get("duration", "00:00") or "00:00"
    thumbnail = result["thumbnails"][0]["url"].split("?")[0]
    views = result.get("viewCount", {}).get("short", "0 views")

    os.makedirs("cache", exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                async with aiofiles.open(f"cache/thumb{videoid}.png", "wb") as f:
                    await f.write(await resp.read())

    base_img = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")

    bg = changeImageSize(1280, 720, base_img)
    bg = bg.filter(ImageFilter.GaussianBlur(25))
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 90))
    bg = Image.alpha_composite(bg, overlay)

    card_w, card_h = 980, 420
    card_x, card_y = (1280 - card_w)//2, (720 - card_h)//2
    add_shadow(bg, (card_x, card_y, card_w, card_h))

    card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 210))
    mask = rounded_rectangle_mask((card_w, card_h), 46)
    bg.paste(card, (card_x, card_y), mask)

    draw = ImageDraw.Draw(bg)

    font_path_regular = "AviaxMusic/assets/font2.ttf"
    font_path_bold = "AviaxMusic/assets/font3.ttf"
    font_title = ImageFont.truetype(font_path_bold, 44)
    font_sub = ImageFont.truetype(font_path_regular, 28)
    font_small = ImageFont.truetype(font_path_regular, 24)

    art_size = 280
    art = base_img.resize((art_size, art_size))
    art_mask = rounded_rectangle_mask((art_size, art_size), 30)
    art_x, art_y = card_x + 32, card_y + 32
    bg.paste(art, (art_x, art_y), art_mask)

    text_x = art_x + art_size + 32
    draw.text((text_x, art_y + 6), title, fill=(0, 0, 0), font=font_title)
    draw.text((text_x, art_y + 66), f"YouTube | {views}", fill=(70, 70, 70), font=font_sub)

    bar_left, bar_right = text_x, card_x + card_w - 32
    bar_y = art_y + 140
    pr_ratio = 0.40
    pr_x = int(bar_left + (bar_right - bar_left) * pr_ratio)

    draw.rounded_rectangle([bar_left, bar_y, bar_right, bar_y + 10], radius=5, fill=(190, 190, 190))
    draw.rounded_rectangle([bar_left, bar_y, pr_x, bar_y + 10], radius=5, fill=(234, 36, 36))
    draw.ellipse([pr_x - 12, bar_y - 2, pr_x + 12, bar_y + 22], fill=(234, 36, 36))

    draw.text((bar_left, bar_y + 24), "00:00", fill=(70, 70, 70), font=font_small)
    dur_w = draw.textlength(duration, font=font_small)
    draw.text((bar_right - int(dur_w), bar_y + 24), duration, fill=(70, 70, 70), font=font_small)

    draw_controls(draw, card_y + card_h - 70, card_x + card_w // 2)

    output_path = f"cache/{videoid}_styled.png"
    bg.save(output_path)

    os.remove(f"cache/thumb{videoid}.png")
    return output_path

except Exception as e:
    print(f"[get_thumb Error] {e}")
    traceback.print_exc()
    return None

async def gen_thumb(videoid: str): return await get_thumb(videoid)

