#!/usr/bin/evn python

from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import subprocess

app = Flask(__name__)

printername = "nadelPrinter"

paper_format = "A5"
default_font = 80

width, height = 768, 1024 # size of saved image

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
    dec = request.form['dec'].upper()  
    
    image_path = create_image(name, pronouns, dec)
    
    send_to_printer(image_path)
    
    return redirect(url_for('index'))


def create_image(name, pronouns, dec):
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    text = f"{name}\n{pronouns}"
    font_size = calculate_max_font_size(draw, width, height, text)

    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'AtkinsonHyperlegible-Bold.ttf')
    font = ImageFont.truetype(font_path, font_size)

    paragraph = [name, pronouns, dec]

    for index, line in enumerate(paragraph):
        bname = draw.textbbox((0, 0), line, font=font)  

        text_width = bname[2] - bname[0]
        text_height = bname[3] - bname[1]
        text_x = (width - text_width) / 2 
        text_y = (height - text_height) / 2 - 30

        text_x += offset_x
        text_y += offset_y

        draw.text((text_x, text_y + index * font_size), line, fill=(0, 0, 0), font=font)

    image_path = os.path.join(os.path.dirname(__file__), 'output.png')
    aliased = image.filter(ImageFilter.ModeFilter(5))
    aliased.save(image_path)
    return image_path

def calculate_max_font_size(draw, width, height, text):
    font_size = default_font  
    min_font_size = default_font // 3   
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'AtkinsonHyperlegible-Bold.ttf')

    while True:
        font = ImageFont.truetype(font_path, font_size)

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

