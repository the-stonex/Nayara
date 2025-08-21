import os
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

async def get_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Title")
        duration = result.get("duration", "00:00")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
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

        # card box
        card_width, card_height = 950, 400
        card = Image.new("RGBA", (card_width, card_height), (255, 255, 255, 230))
        mask = Image.new("L", (card_width, card_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, card_width, card_height], radius=40, fill=255)
        card_pos = ((1280 - card_width) // 2, (720 - card_height) // 2)
        blurred_bg.paste(card, card_pos, mask)

        final_bg = blurred_bg.copy()
        draw = ImageDraw.Draw(final_bg)

        # fonts
        font_path_regular = "AviaxMusic/assets/font2.ttf"
        font_path_bold = "AviaxMusic/assets/font3.ttf"
        font_small = ImageFont.truetype(font_path_regular, 28)
        font_medium = ImageFont.truetype(font_path_regular, 34)
        font_title = ImageFont.truetype(font_path_bold, 40)

        # album art with rounded corners
        thumb_size = 320
        corner_radius = 40
        mask_thumb = Image.new("L", (thumb_size, thumb_size), 0)
        draw_thumb_mask = ImageDraw.Draw(mask_thumb)
        draw_thumb_mask.rounded_rectangle((0, 0, thumb_size, thumb_size), radius=corner_radius, fill=255)

        thumb_square = base_img.resize((thumb_size, thumb_size))
        thumb_square.putalpha(mask_thumb)

        thumb_x = card_pos[0] + 30
        thumb_y = card_pos[1] + (card_height - thumb_size) // 2
        final_bg.paste(thumb_square, (thumb_x, thumb_y), thumb_square)

        # text
        text_x = thumb_x + thumb_size + 40
        text_y = thumb_y + 20
        max_text_width = card_width - (text_x - card_pos[0]) - 40

        draw.text((text_x, text_y), title[:35] + ("..." if len(title) > 35 else ""), fill=(0, 0, 0), font=font_title)
        draw.text((text_x, text_y + 60), f"YouTube | {views}", fill=(80, 80, 80), font=font_medium)

        # progress bar
        bar_y = text_y + 160
        bar_x1, bar_x2 = text_x, text_x + max_text_width
        draw.line((bar_x1, bar_y, bar_x2, bar_y), fill=(200, 200, 200), width=8)
        progress_pos = bar_x1 + int(max_text_width * 0.3)
        draw.line((bar_x1, bar_y, progress_pos, bar_y), fill=(255, 0, 0), width=8)

        # time indicators
        draw.text((bar_x1, bar_y + 15), "00:00", fill=(100, 100, 100), font=font_small)
        draw.text((bar_x2 - 80, bar_y + 15), duration, fill=(100, 100, 100), font=font_small)

        # control icons
        icon_y = bar_y + 90
        spacing = 110
        center_x = text_x + max_text_width // 2

        # Shuffle icon (X-like)
        draw.text((center_x - spacing * 2, icon_y), "🔀", font=font_medium, fill=(0, 0, 0))
        # Previous
        draw.text((center_x - spacing, icon_y), "⏮", font=font_medium, fill=(0, 0, 0))
        # Play button
        play_radius = 35
        draw.ellipse((center_x - play_radius, icon_y - play_radius, center_x + play_radius, icon_y + play_radius), fill=(0, 0, 0))
        draw.polygon([(center_x - 10, icon_y - 15), (center_x - 10, icon_y + 15), (center_x + 15, icon_y)], fill=(255, 255, 255))
        # Next
        draw.text((center_x + spacing, icon_y), "⏭", font=font_medium, fill=(0, 0, 0))
        # Repeat
        draw.text((center_x + spacing * 2, icon_y), "🔁", font=font_medium, fill=(0, 0, 0))

        output_path = f"cache/{videoid}_final.png"
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
