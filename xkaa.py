#!/usr/bin/python
'''	There was an Old Man in a boat,
	Who said, 'I'm afloat! I'm afloat!'
		When they said 'No you ain't!'
		He was ready to faint,
	That unhappy Old Man in a boat.
				(E. Lear)


	A python rework of xcowsay, this python script will display
	a character with different balloon styles. He will display custom text,
	or pictures (if in dream mode). Here's a sample on how to run it:

	characters are the pics in the images directory (bat,donkey,snake,chicken etc.)

	instances are created like this :

	Puppet(character='snake',verb="say",text="your Text",font="BonvenoCF-Light.otf",fontcolor=(255,0,0))

	verb can be : say, think, shout or dream

	if dream, you can pass an image as the dream :

	Puppet(character='donkey',verb="dream",dreamed=path_to_your_pic) '''


__version__ = "0.1"
__author__ = "Salvatore Bognanni <s.bognanni@digitaldecay.org>"


import gtk,sys,os
import cairo
import PIL
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import textwrap

imgdir = "images"
fontdir = "fonts"


def combine_sources(posx,posy,img1,img2,final):
	output = final
	s1 = cairo.ImageSurface.create_from_png(img1)
	s2 = cairo.ImageSurface.create_from_png(img2)

	ctx = cairo.Context(s1)
	ctx.set_source_surface(s2, posx,posy)
	ctx.paint()
	s1.write_to_png(final)
	return output

class Puppet():
		
	def __init__(self,character=None,verb=None,text=None,dreamed=None,font=None,fontcolor=(0,0,0)):
		
		self.imgW = 640
		self.imgH = 520
		self.character = character
		self.font = font
		self.imgdir = imgdir
		self.imagefile = os.path.join(self.imgdir,'ab'+self.character+".png")
		self.characterpic = os.path.join(self.imgdir,self.character+".png")
		self.dreamballoon = os.path.join(self.imgdir,"dream.png")
		self.dreambase = os.path.join(self.imgdir,"dreambase.png")
		self.bigbase = os.path.join(self.imgdir,"bigbase.png")
		self.minidream = os.path.join(self.imgdir,"minidream.png")
		self.empty = os.path.join(self.imgdir,"empty.png")
		self.balloonbase = os.path.join(self.imgdir,"balloonbase.png")
		self.fontdir = fontdir
		self.fontfile = os.path.join(self.fontdir,self.font)
		self.title = "xKaa"
		self.dreamed = dreamed
		self.fontcolor = fontcolor

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

	def make_dream(self):
		# combine images together
		posx = 80
		posy = 65
		width = 128
		im = gtk.Image()
		pixbuf = gtk.gdk.pixbuf_new_from_file(self.dreamed)
		scaled_buf = pixbuf.scale_simple(width,(width*3)/4,gtk.gdk.INTERP_BILINEAR)
		scaled_buf.save(self.minidream,'png')
		myimage = combine_sources(posx,posy,self.balloonbase,self.minidream,self.dreamballoon)
		return self.dreamballoon

	def draw_balloons(self,balloontype=None):
		self.balloontype=balloontype
		''' this will create a balloon instead of using a premade one '''
		base = Image.open(self.empty).convert('RGBA')
		overlay = Image.new('RGBA', base.size, (255,255,255,0))
		draw = ImageDraw.Draw(overlay)
		if self.balloontype=='say':
			draw.polygon([(20, 230),(94,195),(54,172)],fill = 'white',outline='black')
			draw.ellipse((20, 20, 280, 220), fill = 'white',outline='black')
			draw.polygon([(20, 230),(94,195),(54,172)],fill = 'white')
		elif ( self.balloontype=='dream')  or ( self.balloontype=='think'):
			draw.ellipse((20, 20, 280, 220), fill = 'white', outline = 'black')
			draw.ellipse((20, 180,100,240), fill = 'white', outline = 'black' )
			draw.ellipse((0, 220,20,240), fill = 'white', outline = 'black' )
		elif self.balloontype=='shout':
			draw.polygon([(3, 237),(29,183),(46,206),(56,156),
					(12,170),(36,131),(3,111),(38,96),
					(8,70),(51,62),(25,22),(85,38),(120,9),
					(147,42),(191,19),(201,57),(252,47),(249,88),
					(282,120),(235,137),(260,172),(210,178),
					(233,218),(170,174),(148,211),(130,185),
					(104,240),(94,200),(47,229),(29,200)],fill = 'white',outline='black')
		else:
			draw.ellipse((20, 20, 280, 220), fill = 'white')
		out = Image.alpha_composite(base, overlay)
		out.save(self.balloonbase)
		return self.balloonbase

	def draw_base(self):
		posx = 80
		posy = 200
		myimage = combine_sources(posx,posy,self.bigbase,self.characterpic,self.imagefile)
	
	def build_popup(self):

		# some positioning of balloons here
		self.baloon=self.draw_balloons(balloontype=self.verb)

		if self.verb == 'say':
			self.origx = 230; self.origy = 50
			self.textX = 310; self.textY = 95
		elif self.verb == 'think':
			self.origx = 220; self.origy = 10
			self.textX = 300; self.textY = 55
		elif self.verb == 'dream':
			self.baloon=self.make_dream()
			self.origx = 220; self.origy = 0
		elif self.verb == 'shout':
			self.origx = 210; self.origy = 10
			self.textX = 280; self.textY = 65
		else:
			self.origx = 190; self.origy = 10
			self.textX = 260; self.textY = 55

		# combine images together - Main 
		self.combo = "images/output.png"
		self.draw_balloons(balloontype=self.verb)
		self.draw_base()
                myimage = combine_sources(self.origx,self.origy,self.imagefile,self.baloon,self.combo)
	
                # draw text
                img = Image.open(self.combo)
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(self.fontfile, 15)

		if self.baloon != self.dreamballoon:
                	# handling the wrap around of text is done via textwrap module
			lines = textwrap.wrap(self.text, width = 20)
			y_text = self.textY
			x_text = self.textX
			for line in lines:
				width, height = font.getsize(line)
				draw.text((x_text, y_text), line, self.fontcolor, font=font)
				y_text += height

                # save image
                img.save(self.combo)
		return self.combo

	def close_application(self,widget,event,data=None):
		gtk.main_quit()
		os.unlink(self.combo)
		os.unlink(self.imagefile)
		os.unlink(self.balloonbase)
		try:
			os.unlink(self.minidream)
			os.unlink(self.dreamballoon)
		except:
			pass


