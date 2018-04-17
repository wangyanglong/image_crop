#!/bin/python
#encoding=utf-8

from PIL import Image
from os import path

def handle_imag(file_name):
    file = Image.open(file_name)
    img_src = file.convert('RGBA')
    pixels = img_src.load()
    width, height = img_src.size
    

    all_pixels = []
    max_x_count = 0
    max_end_x = 0
    max_y_count =0
    max_end_y = 0
    start_x = 0
    start_y = 0

    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            if cpixel[0]!=255 or cpixel[1]!=255 or cpixel[2]!=255:
                end_x,count = search_lines(x,width,y,pixels,cpixel)
                if end_x<1:
                    continue
                if max_x_count<count:
                    start_x = x
                    max_x_count = count
                    max_end_x = end_x
                end_y,count = search_rows(y,height,x,pixels)
                if end_y<1:
                    continue
                if max_y_count<count:
                    start_y = y
                    max_y_count = count
                    max_end_y = end_y
    # print "start_x:",start_x,",start_y:",start_y
    # print "max_end_x:",max_end_x,",max_x_count:",max_x_count
    # print "max_end_y:",max_end_y,",max_y_count:",max_y_count
    region=(start_x,start_y,max_end_x,max_end_y)
    cropImage=file.crop(region)
    save_name = path.splitext(file_name)[0]+"_small"+path.splitext(file_name)[1]
    cropImage.save(save_name)
    print "crop image successful:",save_name
    return save_name

def search_lines(start_x,width,y,pixels,p):
    count = 0
    end_x = 0
    for x in range(width-start_x):
        cpixel=pixels[x+start_x,y]
        if cpixel[0]<100 or cpixel[1]<100 or cpixel[2]<100:
            end_x = start_x+x
            count+=1
        else:
            break
    if count <20 or end_x<20:
        end_x = 0
        count = 0
    return end_x,count


def search_rows(start_y,height,x,pixels):
    count = 0
    end_y = 0
    for y in range(height-start_y):
        cpixel = pixels[x,start_y+y]
        if cpixel[0]<100 or cpixel[1]<100 or cpixel[2]<100:
            count+=1
            end_y = start_y+y
        else:
            break
    if count<10:
        end_y = 0
    return end_y,count

if __name__ == "__main__":
    handle_imag("./test.png")