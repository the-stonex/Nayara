import os
import re
import aiohttp
import aiofiles
import traceback
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch


def changeImageSize(maxWidth, maxHeight, image):
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newSize = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return image.resize(newSize, Image.Resampling.LANCZOS)


async def get_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Title")
        duration = result.get("duration", "00:00")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        channel = result.get("channel", {}).get("name", "Unknown Channel")

        # download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                        await f.write(await resp.read())

        base_img = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")
        bg_img = changeImageSize(1280, 720, base_img).convert("RGBA")
        blurred_bg = bg_img.filter(ImageFilter.GaussianBlur(30))

        # dark overlay
        overlay = Image.new("RGBA", blurred_bg.size, (0, 0, 0, 160))
        blurred_bg = Image.alpha_composite(blurred_bg, overlay)

        final_bg = blurred_bg.copy()
        draw = ImageDraw.Draw(final_bg)

        # font paths
        font_path_regular = "AviaxMusic/assets/font2.ttf"
        font_path_bold = "AviaxMusic/assets/font3.ttf"

        # Thumbnail (top center)
        thumb_size = 300
        thumb_mask = Image.new("L", (thumb_size, thumb_size), 0)
        mask_draw = ImageDraw.Draw(thumb_mask)
        mask_draw.rounded_rectangle((0, 0, thumb_size, thumb_size), radius=40, fill=255)

        thumb_square = base_img.resize((thumb_size, thumb_size))
        thumb_square.putalpha(thumb_mask)

        thumb_x = (1280 - thumb_size) // 2
        thumb_y = 80
        final_bg.paste(thumb_square, (thumb_x, thumb_y), thumb_square)

        # card area below thumbnail
        card_width, card_height = 1000, 260
        card = Image.new("RGBA", (card_width, card_height), (40, 40, 60, 200))
        mask = Image.new("L", (card_width, card_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, card_width, card_height], radius=40, fill=255)
        card_pos = ((1280 - card_width) // 2, thumb_y + thumb_size + 40)
        final_bg.paste(card, card_pos, mask)

        # text inside card
        text_x = card_pos[0] + 40
        text_y = card_pos[1] + 30
        max_width = card_width - 80

        font_small = ImageFont.truetype(font_path_regular, 32)
        font_medium = ImageFont.truetype(font_path_regular, 40)
        font_title = ImageFont.truetype(font_path_bold, 50)

        # title
        draw.text((text_x, text_y), title[:40], fill=(255, 255, 255), font=font_title)

        # channel
        draw.text((text_x, text_y + 70), channel, fill=(200, 200, 200), font=font_medium)

        # duration
        draw.text((text_x, text_y + 140), f"00:00 / {duration}", fill=(180, 180, 180), font=font_small)

        # save
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
