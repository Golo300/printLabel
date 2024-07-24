from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

app = Flask(__name__)

printername = "nadelPrinter"

paper_format = "A5"
default_font = 60

width, height = 430, 550 # size of saved image

offset_x = 0 
offset_y = -90

padding = 60

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/print', methods=['POST'])
def print_info():
    name = request.form['name'].upper()  
    pronouns = request.form['pronouns'].upper()  
    color = request.form['color']
    
    image_path = create_image(name, pronouns, color.lstrip('#'))
    
    send_to_printer(image_path)
    
    return redirect(url_for('index'))


def create_image(name, pronouns, color):
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    text = f"{name}\n{pronouns}"
    font_size = calculate_max_font_size(draw, width, height, text)
    font = ImageFont.load_default(size=font_size)

    bname = draw.textbbox((0, 0), name, font=font)  
    bprononus = draw.textbbox((0, 0), pronouns, font=font)  

    n_text_width = bname[2] - bname[0]
    n_text_height = bname[3] - bname[1]
    n_text_x = (width - n_text_width) / 2 
    n_text_y = (height - n_text_height) / 2 - 30

    n_text_x += offset_x
    n_text_y += offset_y

    p_text_width = bprononus[2] - bprononus[0]
    p_text_height = bprononus[3] - bprononus[1]
    p_text_x = (width - p_text_width) / 2 
    p_text_y = (height - p_text_height) / 2 - 30

    p_text_x += offset_x
    p_text_y += offset_y

    color_rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    draw.text((n_text_x, n_text_y), name, fill=color_rgb, font=font)
    draw.text((p_text_x, p_text_y + font_size), pronouns, fill=color_rgb, font=font)

    image_path = os.path.join(os.path.dirname(__file__), 'output.png')
    image.save(image_path)
    return image_path

def calculate_max_font_size(draw, width, height, text):
    font_size = default_font  
    min_font_size = 3   

    while True:
        font = ImageFont.load_default(font_size)
        bbox = draw.textbbox((0, 0), text, font=font)  
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width < (width - padding) and text_height < height:
            break
        font_size -= 1
        if font_size < min_font_size:
            break
    return font_size - 1  


def send_to_printer(image_path):
    subprocess.run(["lp", "-d", printername, "-o", f"media={paper_format} ColorModel=Color", image_path])

if __name__ == '__main__':
    app.run(debug=True)

