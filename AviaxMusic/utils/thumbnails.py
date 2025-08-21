import os
import re
import random
import aiohttp
import aiofiles
import traceback

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from youtubesearchpython.future import VideosSearch


def changeImageSize(maxWidth, maxHeight, image):
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newSize = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return image.resize(newSize, Image.ANTIALIAS)


def truncate_ellipsis(text, max_chars=20):
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    if ' ' in truncated:
        truncated = truncated[:truncated.rfind(' ')]
    return truncated + "..." if len(truncated) > 0 else text[:max_chars-3] + "..."


def ensure_text_fits(draw, text, font, max_width):
    """Ensure text doesn't exceed max width by truncating with ellipsis"""
    text_width = draw.textlength(text, font=font)
    if text_width <= max_width:
        return text
    
    # Binary search for optimal truncation
    low = 1
    high = len(text)
    best = ""
    while low <= high:
        mid = (low + high) // 2
        truncated = truncate_ellipsis(text, mid)
        truncated_width = draw.textlength(truncated, font=font)
        if truncated_width <= max_width:
            best = truncated
            low = mid + 1
        else:
            high = mid - 1
    return best if best else "..."


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

        # Download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                        await f.write(await resp.read())

        base_img = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")
        bg_img = changeImageSize(1280, 720, base_img).convert("RGBA")
        blurred_bg = bg_img.filter(ImageFilter.GaussianBlur(30))

        # Card
        card_width, card_height = 950, 360
        card = Image.new("RGBA", (card_width, card_height), (255, 255, 255, 240))
        mask = Image.new("L", (card_width, card_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, card_width, card_height], radius=40, fill=255)
        card_pos = ((1280 - card_width) // 2, (720 - card_height) // 2)
        blurred_bg.paste(card, card_pos, mask)

        final_bg = blurred_bg.copy()
        final_bg.paste(card, card_pos, mask)
        draw = ImageDraw.Draw(final_bg)

        # Font paths
        font_path_regular = "AviaxMusic/assets/font2.ttf"
        font_path_bold = "AviaxMusic/assets/font3.ttf"

        # Album Art (left)
        art_size = 340
        art_mask = Image.new('L', (art_size, art_size), 0)
        draw_art = ImageDraw.Draw(art_mask)
        draw_art.rounded_rectangle((0, 0, art_size, art_size), radius=35, fill=255)

        thumb_square = base_img.resize((art_size, art_size))
        thumb_square.putalpha(art_mask)

        art_x = card_pos[0] + 25
        art_y = card_pos[1] + (card_height - art_size) // 2
        final_bg.paste(thumb_square, (art_x, art_y), thumb_square)

        # Text
        text_x = art_x + art_size + 40
        text_y = art_y + 20
        max_text_width = card_width - (text_x - card_pos[0]) - 40

        font_title = fit_text(draw, title, max_text_width, font_path_bold, 52, 34)
        font_artist = ImageFont.truetype(font_path_regular, 38)
        font_small = ImageFont.truetype(font_path_regular, 30)

        # Title
        draw.text((text_x, text_y), ensure_text_fits(draw, title, font_title, max_text_width), fill=(0, 0, 0), font=font_title)

        # Artist
        draw.text((text_x, text_y + 70), ensure_text_fits(draw, channel, font_artist, max_text_width), fill=(70, 70, 70), font=font_artist)

        # Progress Bar
        bar_y = text_y + 150
        bar_width = max_text_width
        bar_height = 12
        bar_x = text_x
        draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], radius=6, fill=(220, 220, 220))
        draw.rounded_rectangle([bar_x, bar_y, bar_x + int(bar_width * 0.2), bar_y + bar_height], radius=6, fill=(30, 144, 255))

        draw.text((bar_x, bar_y + 20), "00:00", fill=(100, 100, 100), font=font_small)
        draw.text((bar_x + bar_width - 100, bar_y + 20), duration, fill=(100, 100, 100), font=font_small)

        # Controls (PNG icons डालने के लिए assets/icons में रखो)
        try:
            play_icon = Image.open("AviaxMusic/assets/icons/play.png").resize((60, 60))
            prev_icon = Image.open("AviaxMusic/assets/icons/prev.png").resize((50, 50))
            next_icon = Image.open("AviaxMusic/assets/icons/next.png").resize((50, 50))

            ctrl_y = bar_y + 70
            final_bg.paste(prev_icon, (bar_x + bar_width//2 - 120, ctrl_y), prev_icon)
            final_bg.paste(play_icon, (bar_x + bar_width//2 - 30, ctrl_y), play_icon)
            final_bg.paste(next_icon, (bar_x + bar_width//2 + 70, ctrl_y), next_icon)
        except:
            pass  # अगर icons न हों तो crash ना हो

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
