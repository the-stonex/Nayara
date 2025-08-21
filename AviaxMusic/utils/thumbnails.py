import os
import re
import aiohttp
import aiofiles
import traceback
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.future import VideosSearch

# Resize image maintaining aspect ratio
def changeImageSize(maxWidth, maxHeight, image):
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newSize = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return image.resize(newSize, Image.ANTIALIAS)

# Ensure text fits within max width
def ensure_text_fits(draw, text, font, max_width):
    text_width = draw.textlength(text, font=font)
    if text_width <= max_width:
        return text
    while text and draw.textlength(text + "...", font=font) > max_width:
        text = text[:-1]
    return text + "..."

# Fit text with font size range
def fit_text(draw, text, max_width, font_path, start_size, min_size):
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(font_path, min_size)

async def get_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Title")
        duration = result.get("duration", "00:00")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        channel = result.get("channel", {}).get("name", "Unknown Channel")
        views = result.get("viewCount", {}).get("short", "0 views")

        # download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", "wb") as f:
                        await f.write(await resp.read())

        base_img = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")
        bg_img = changeImageSize(1280, 720, base_img).convert("RGBA")
        blurred_bg = bg_img.filter(ImageFilter.GaussianBlur(25))

        # card box (rounded rectangle)
        card_width, card_height = 1050, 400
        card = Image.new("RGBA", (card_width, card_height), (255, 255, 255, 235))
        mask = Image.new("L", (card_width, card_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, card_width, card_height], radius=50, fill=255)
        card_pos = ((1280 - card_width) // 2, (720 - card_height) // 2)
        blurred_bg.paste(card, card_pos, mask)

        final_bg = blurred_bg.copy()
        draw = ImageDraw.Draw(final_bg)

        # fonts
        font_path_regular = "AviaxMusic/assets/font2.ttf"
        font_path_bold = "AviaxMusic/assets/font3.ttf"

        # album art with rounded corners
        thumb_size = 350
        corner_radius = 40
        mask_thumb = Image.new("L", (thumb_size, thumb_size), 0)
        draw_thumb_mask = ImageDraw.Draw(mask_thumb)
        draw_thumb_mask.rounded_rectangle((0, 0, thumb_size, thumb_size), radius=corner_radius, fill=255)

        thumb_square = base_img.resize((thumb_size, thumb_size))
        thumb_square.putalpha(mask_thumb)

        thumb_x = card_pos[0] + 40
        thumb_y = card_pos[1] + (card_height - thumb_size) // 2
        final_bg.paste(thumb_square, (thumb_x, thumb_y), thumb_square)

        # text layout
        text_x = thumb_x + thumb_size + 40
        text_y = thumb_y + 30
        max_text_width = card_width - (text_x - card_pos[0]) - 40

        font_small = ImageFont.truetype(font_path_regular, 30)
        font_medium = ImageFont.truetype(font_path_regular, 36)
        font_title = fit_text(draw, title, max_text_width, font_path_bold, 48, 32)

        # title
        title_text = ensure_text_fits(draw, title, font_title, max_text_width)
        draw.text((text_x, text_y), title_text, fill=(0, 0, 0), font=font_title)

        # channel + views
        info_text = f"YouTube | {views}"
        draw.text((text_x, text_y + 70), info_text, fill=(80, 80, 80), font=font_medium)

        # progress bar
        bar_y = text_y + 160
        bar_x1, bar_x2 = text_x, text_x + max_text_width
        draw.line((bar_x1, bar_y, bar_x2, bar_y), fill=(200, 200, 200), width=8)

        # time indicators
        draw.text((bar_x1, bar_y + 15), "00:00", fill=(100, 100, 100), font=font_small)
        draw.text((bar_x2 - 80, bar_y + 15), duration, fill=(100, 100, 100), font=font_small)

        # controls (shuffle, prev, play, next, repeat)
        icon_y = bar_y + 90
        spacing = 120
        center_x = text_x + max_text_width // 2

        # Draw play button circle
        play_radius = 35
        draw.ellipse((center_x - play_radius, icon_y - play_radius, center_x + play_radius, icon_y + play_radius), fill=(0, 0, 0))
        draw.polygon([(center_x - 10, icon_y - 15), (center_x - 10, icon_y + 15), (center_x + 15, icon_y)], fill=(255, 255, 255))

        output_path = f"cache/{videoid}_styled.png"
        final_bg.save(output_path)

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass

        return output_path

    except Exception as e:
        print(f"[get_thumb Error] {e}")
        traceback.print_exc()
        return None
