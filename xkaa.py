#!/usr/bin/python
''' As a pun with xcowsay, this python script will display
a snake with different balloon styles. He will display custom text,
or pictures (if in dream mode). Here's a sample on how to run it:

Puppet(verb=action,text=yourtext)

where action can be 'say','think' or 'shout'

or if dreaming :

Puppet(verb="dream",picture=path_to_your_pic) '''

import gtk,sys,os
import cairo
import PIL
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import textwrap


def combine_sources(action,posx,posy,img1,img2,final):
	output = final
	s1 = cairo.ImageSurface.create_from_png(img1)
	s2 = cairo.ImageSurface.create_from_png(img2)

	ctx = cairo.Context(s1)
	ctx.set_source_surface(s2, posx,posy)
	ctx.paint()
	s1.write_to_png(final)
	return output

class Puppet():
		
	def __init__(self,verb=None,text=None,dreamed=None):
		
		self.imgW = 640
		self.imgH = 520
		self.imagefile = "images/absnake.png"
		self.sayballoon = "images/say.png"
		self.dreamballoon = "images/dream.png"
		self.thinkballoon = "images/dream.png"
		self.shoutballoon = "images/shout.png"
		self.fontfile = "fonts/BonvenoCF-Light.otf"
		self.title = "xKaa"

		self.verb = verb
                self.text = text

		self.popup = self.build_popup()
		# create the window
		win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		win.set_decorated(False)
		win.set_title(self.title)
		win.set_position(gtk.WIN_POS_MOUSE)
		win.set_default_size(self.imgW, self.imgH)
		
		# handling events. We want it to close on close
		win.connect("delete_event", self.close_application)
		win.set_events(win.get_events()|gtk.gdk.BUTTON_PRESS_MASK)
		win.connect("key_press_event",self.close_application)
		win.connect("button_press_event",self.close_application)
		win.show()

		# load the png into an image object and create the mask
		pixmap, mask = gtk.gdk.pixmap_create_from_xpm(win.window, None, self.popup)
		image = gtk.Image()
		image.set_from_pixmap(pixmap, mask)
		
		# add the image to the window	
		win.add(image)
		win.shape_combine_mask(mask, 0, 0)
		# and show
		win.show_all()
	
	def build_popup(self):

		# some positioning of balloons here
		if self.verb == "say":
			self.baloon=self.sayballoon
			self.origx = 200; self.origy = 0
			self.textX = 260; self.textY = 60
		elif self.verb == "dream":
			self.baloon=self.dreamballoon
			self.origx = 220; self.origy = 0
		elif self.verb == "think":
			self.baloon=self.thinkballoon
			self.origx = 220; self.origy = 0
			self.textX = 280; self.textY = 60
		elif self.verb == "shout":
			self.baloon=self.shoutballoon
			self.origx = 190; self.origy = 0
			self.textX = 250; self.textY = 60
		else:
			self.baloon=self.sayballoon
			self.origx = 200; self.origy = 0
			self.textX = 260; self.textY = 60
		
		# combine images together
		self.combo = "images/output.png"
                myimage = combine_sources(self.verb,self.origx,self.origy,self.imagefile,self.baloon,self.combo)
	
                # draw text
                img = Image.open(self.combo)
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(self.fontfile, 15)
                mytext = self.text

                # handling the wrap around of text is not easy, will have to improve this
                mylimit = 20
                splits=[mytext[x:x+mylimit] for x in range(0,len(mytext),mylimit)]
                for split in splits:
                        num = splits.index(split)
                        num = num * 15
                        draw.text((self.textX, self.textY+num), split.lstrip(),(0,0,0), font=font)

                # save image
                img.save(self.combo)
		return self.combo

	def close_application(self,widget,event,data=None):
		gtk.main_quit()
		os.unlink(self.combo)

