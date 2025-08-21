# ATLEAST GIVE CREDITS IF YOU STEALING :(((((((((((((((((((((((((((((((((((((
# ELSE NO FURTHER PUBLIC THUMBNAIL UPDATES

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
  
        # Card overlay  
        card_width, card_height = 960, 320  
        card = Image.new("RGBA", (card_width, card_height), (40, 40, 60, 200))  
        mask = Image.new("L", (card_width, card_height), 0)  
        draw_mask = ImageDraw.Draw(mask)  
        draw_mask.rounded_rectangle([0, 0, card_width, card_height], radius=40, fill=255)  
        card_pos = ((1280 - card_width) // 2, (720 - card_height) // 2)  
        blurred_bg.paste(card, card_pos, mask)  
          
        final_bg = blurred_bg.copy()  
        final_bg.paste(card, card_pos, mask)  
        draw = ImageDraw.Draw(final_bg)  
  
        # ✅ Changed font paths  
        font_path_regular = "AviaxMusic/assets/font2.ttf"  
        font_path_bold = "AviaxMusic/assets/font3.ttf"  
  
        # Medium album art   
        thumb_size = 250  
        corner_radius = 40  
        mask = Image.new('L', (thumb_size, thumb_size), 0)  
        draw_mask = ImageDraw.Draw(mask)  
        draw_mask.rounded_rectangle((0, 0, thumb_size, thumb_size), radius=corner_radius, fill=255)  
  
        thumb_square = base_img.resize((thumb_size, thumb_size))  
        thumb_square.putalpha(mask)  
  
        thumb_x = card_pos[0] + 40  
        thumb_y = card_pos[1] + (card_height - thumb_size) // 2  
        final_bg.paste(thumb_square, (thumb_x, thumb_y), thumb_square)  
  
        # Text layout with overflow protection  
        text_x = thumb_x + thumb_size + 40  
        text_y = thumb_y + 20  
        max_text_width = card_width - (text_x - card_pos[0]) - 40  
  
        # Fonts  
        font_small = ImageFont.truetype(font_path_regular, 28)  
        font_medium = ImageFont.truetype(font_path_regular, 36)  
        font_title = fit_text(draw, title, max_text_width, font_path_bold, 48, 32)  
  
        # Channel name (with overflow protection)  
        channel_text = ensure_text_fits(draw, channel, font_small, max_text_width)  
        draw.text((text_x, text_y), "NOW PLAYING", fill=(180, 180, 180), font=font_small)  
  
        # Title (with dynamic sizing and overflow protection)  
        title_text = ensure_text_fits(draw, title, font_title, max_text_width)  
        draw.text(  
            (text_x, text_y + 40),  
            title_text,  
            fill=(255, 255, 255),  
            font=font_title  
        )  
  
        # Artist and duration  
        artist_text = ensure_text_fits(draw, channel, font_medium, max_text_width)  
        draw.text((text_x, text_y + 100), artist_text, fill=(200, 200, 200), font=font_medium)  
  
        duration_text = f"00:00 / {duration}"  
        duration_text = ensure_text_fits(draw, duration_text, font_small, max_text_width)  
        draw.text((text_x, text_y + 150), duration_text, fill=(170, 170, 170), font=font_small)  
  
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
            return f"cache/{videoid}_v4.png"

        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            title = result.get("title")
            if title:
                title = re.sub("\W+", " ", title).title()
            else:
                title = "Unsupported Title"
            duration = result.get("duration")
            if not duration:
                duration = "Live"
            thumbnail_data = result.get("thumbnails")
            if thumbnail_data:
                thumbnail = thumbnail_data[0]["url"].split("?")[0]
            else:
                thumbnail = None
            views_data = result.get("viewCount")
            if views_data:
                views = views_data.get("short")
                if not views:
                    views = "Unknown Views"
            else:
                views = "Unknown Views"
            channel_data = result.get("channel")
            if channel_data:
                channel = channel_data.get("name")
                if not channel:
                    channel = "Unknown Channel"
            else:
                channel = "Unknown Channel"

        
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
        
                content = await resp.read()
                if resp.status == 200:
                    content_type = resp.headers.get('Content-Type')
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        extension = 'jpg'
                    elif 'png' in content_type:
                        extension = 'png'
                    else:
                        logging.error(f"Unexpected content type: {content_type}")
                        return None

                    filepath = f"cache/thumb{videoid}.png"
                    f = await aiofiles.open(filepath, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                    # os.system(f"file {filepath}")
                    
        
        image_path = f"cache/thumb{videoid}.png"
        youtube = Image.open(image_path)
        image1 = changeImageSize(1280, 720, youtube)
        
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(20))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        
        start_gradient_color = random_color()
        end_gradient_color = random_color()
        gradient_image = generate_gradient(1280, 720, start_gradient_color, end_gradient_color)
        background = Image.blend(background, gradient_image, alpha=0.2)
        
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("AviaxMusic/assets/font2.ttf", 30)
        font = ImageFont.truetype("AviaxMusic/assets/font.ttf", 30)
        title_font = ImageFont.truetype("AviaxMusic/assets/font3.ttf", 45)


        circle_thumbnail = crop_center_circle(youtube, 400, 20, start_gradient_color)
        circle_thumbnail = circle_thumbnail.resize((400, 400))
        circle_position = (120, 160)
        background.paste(circle_thumbnail, circle_position, circle_thumbnail)

        text_x_position = 565
        title1 = truncate(title)
        draw_text_with_shadow(background, draw, (text_x_position, 180), title1[0], title_font, (255, 255, 255))
        draw_text_with_shadow(background, draw, (text_x_position, 230), title1[1], title_font, (255, 255, 255))
        draw_text_with_shadow(background, draw, (text_x_position, 320), f"{channel}  |  {views[:23]}", arial, (255, 255, 255))


        line_length = 580  
        line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if duration != "Live":
            color_line_percentage = random.uniform(0.15, 0.85)
            color_line_length = int(line_length * color_line_percentage)
            white_line_length = line_length - color_line_length

            start_point_color = (text_x_position, 380)
            end_point_color = (text_x_position + color_line_length, 380)
            draw.line([start_point_color, end_point_color], fill=line_color, width=9)
        
            start_point_white = (text_x_position + color_line_length, 380)
            end_point_white = (text_x_position + line_length, 380)
            draw.line([start_point_white, end_point_white], fill="white", width=8)
        
            circle_radius = 10 
            circle_position = (end_point_color[0], end_point_color[1])
            draw.ellipse([circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                      circle_position[0] + circle_radius, circle_position[1] + circle_radius], fill=line_color)
    
        else:
            line_color = (255, 0, 0)
            start_point_color = (text_x_position, 380)
            end_point_color = (text_x_position + line_length, 380)
            draw.line([start_point_color, end_point_color], fill=line_color, width=9)
        
            circle_radius = 10 
            circle_position = (end_point_color[0], end_point_color[1])
            draw.ellipse([circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                          circle_position[0] + circle_radius, circle_position[1] + circle_radius], fill=line_color)

        draw_text_with_shadow(background, draw, (text_x_position, 400), "00:00", arial, (255, 255, 255))
        draw_text_with_shadow(background, draw, (1080, 400), duration, arial, (255, 255, 255))
        
        play_icons = Image.open("AviaxMusic/assets/play_icons.png")
        play_icons = play_icons.resize((580, 62))
        background.paste(play_icons, (text_x_position, 450), play_icons)

        os.remove(f"cache/thumb{videoid}.png")

        background_path = f"cache/{videoid}_v4.png"
        background.save(background_path)
        
        return background_path

    except Exception as e:
        logging.error(f"Error generating thumbnail for video {videoid}: {e}")
        traceback.print_exc()
        return None

