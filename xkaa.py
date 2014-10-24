#!/usr/bin/python

import gtk,sys,os
import cairo
import PIL
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import textwrap

imgW = 640
imgH = 520
imgfile = "images/absnake.png"
baloonfile = "images/baloon.png"
combo = "images/output.png"
global textX
global textY
textX = 260
textY = 60
myfont = "fonts/BonvenoCF-Light.otf"
title = "xKaa"

def combine_sources(img1,img2,final):
	output = final
	s1 = cairo.ImageSurface.create_from_png(img1)
	s2 = cairo.ImageSurface.create_from_png(img2)

	ctx = cairo.Context(s1)
	ctx.set_source_surface(s2, 200,0)
	ctx.paint()
	s1.write_to_png(final)
	return output

class Snake():
	def close_application(self,widget,event,data=None):
		gtk.main_quit()
		os.unlink(combo)
		
	def __init__(self,text):
		
		self.text = text
		# create the window
		win = gtk.Window(gtk.WINDOW_POPUP)
		#win.set_decorated(False)
		win.set_title(title)
		win.set_position(gtk.WIN_POS_MOUSE)
		win.set_default_size(imgW, imgH)
		
		# handling events. We want it to close on close
		win.connect("delete_event", self.close_application)
		win.set_events(win.get_events()|gtk.gdk.BUTTON_PRESS_MASK)
		win.connect("key_press_event",self.close_application)
		win.connect("button_press_event",self.close_application)
		win.show()

		# combine the image
                myimage = combine_sources(imgfile,baloonfile,combo)
		# draw text
		img = Image.open(combo)
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype(myfont, 15)
		mytext = self.text
		# handling the wrap around of text is not easy
		mylimit = 20
		splits=[mytext[x:x+mylimit] for x in range(0,len(mytext),mylimit)]
		for split in splits:
			num = splits.index(split)
			num = num * 15
			draw.text((textX, textY+num), split.lstrip(),(0,0,0), font=font)
		# save image
		img.save(combo)
		
		# load the png into an image object and create the mask
		pixmap, mask = gtk.gdk.pixmap_create_from_xpm(win.window, None, myimage)
		image = gtk.Image()
		image.set_from_pixmap(pixmap, mask)
		
	
		# add the image to the window	
		win.add(image)
		win.shape_combine_mask(mask, 0, 0)
		# and show
		win.show_all()

# main
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: " + sys.argv[0] + "Your text here"
		sys.exit()
	else:
		text = sys.argv[1]
		Snake(text)
		gtk.main()
