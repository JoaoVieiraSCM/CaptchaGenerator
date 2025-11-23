import os
import random
from PIL import Image, ImageDraw, ImageFont
import time
import sys
import config

os.makedirs(config.OUTPUT_DIR, exist_ok=True)

def get_random_captcha_text(length, chars):
    return ''.join(random.choices(chars, k=length))

def generate_and_save_captcha(text, filename):
    
    image = Image.new('RGB', (config.CAPTCHA_WIDTH, config.CAPTCHA_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    try:
        font_size = config.FONT_SIZE
        font = ImageFont.truetype(config.FONT_PATH, font_size)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    bbox = font.getbbox('A')
    char_height = bbox[3] - bbox[1]
    y_center = 35
    y_offset = y_center - (char_height / 2)
    
    num_circles = random.randint(6, 8)
    circle_colors = [(0x4f, 0x4f, 0x4f), (0x66, 0x66, 0x66), (0x5e, 0x5e, 0x5e)]
    for _ in range(num_circles):
        x_center = random.randint(0, config.CAPTCHA_WIDTH)
        y_center = random.randint(0, config.CAPTCHA_HEIGHT)
        radius = random.randint(25, 45)
        color = random.choice(circle_colors)
        
        draw.ellipse(
            [x_center - radius, y_center - radius, 
             x_center + radius, y_center + radius], 
            outline=color, 
            width=1
        )

    total_content_width = config.CAPTCHA_WIDTH - 20
    char_width_estimate = 25
    total_char_width = char_width_estimate * config.CAPTCHA_LENGTH
    available_space = total_content_width - total_char_width
    spacing = available_space / (config.CAPTCHA_LENGTH - 1) if config.CAPTCHA_LENGTH > 1 else 0
    
    start_x = 10
    
    char_colors = [
        (0x3a, 0x3a, 0x3a),
        (0x4d, 0x4d, 0x4d),
        (0x5e, 0x5e, 0x5e),
        (0x6f, 0x6f, 0x6f),
        (0x7f, 0x7f, 0x7f),
        (0x8d, 0x8d, 0x8d),
        (0x9a, 0x9a, 0x9a),
        (0x52, 0x52, 0x52),
    ]
    
    for i, char in enumerate(text):
        
        x = int(start_x + (i * (char_width_estimate + spacing))) + random.randint(-2, 2)
        y = int(y_offset) + random.randint(-3, 3)
        
        angle = random.randint(-8, 8)
        char_color = random.choice(char_colors)
        
        char_img = Image.new('RGBA', (50, 60), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((8, 8), char, font=font, fill=char_color + (255,))
        
        char_img = char_img.rotate(angle, expand=False, fillcolor=(255, 255, 255, 0))
        
        image.paste(char_img, (x, y), char_img)
    
    image = image.convert('RGB')
    image.save(os.path.join(config.OUTPUT_DIR, filename))

if __name__ == '__main__':
    num_captchas = config.DEFAULT_NUM_CAPTCHAS
    if len(sys.argv) > 1:
        try:
            num_captchas = int(sys.argv[1])
            if num_captchas <= 0:
                print("Error: number must be greater than 0")
                sys.exit(1)
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid number")
            print(f"Usage: python {sys.argv[0]} [count]")
            sys.exit(1)
    
    print(f"Generating {num_captchas} images...")

    start_time = time.time()
    images_saved = 0
    
    for i in range(num_captchas):
        captcha_text = get_random_captcha_text(config.CAPTCHA_LENGTH, config.CHARACTERS)
        filename = f"{captcha_text}.png"
        generate_and_save_captcha(captcha_text, filename)
        images_saved += 1

        if (i + 1) % 1000 == 0:
            print(f"{i + 1} generated in {time.time() - start_time:.2f}s")
    
    end_time = time.time()
    print(f"\nDone. {images_saved} images saved in {end_time - start_time:.2f} seconds.")
