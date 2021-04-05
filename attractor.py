import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as Bg
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.clock import Clock
from random import randint, choice
import math
import time
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
kivy.require("2.0.0")


class Drw(Widget):
	Window.size = (500, 500)
	Im = Image.new("RGB", (Window.size[0], Window.size[1]), (0,0,0))
	byte_io = BytesIO()
	Im.save(byte_io, 'PNG')
	draw = ImageDraw.Draw(Im)
	coords = []
	check = False

	

	def __init__(self,**kwargs):
		super(Drw, self).__init__(**kwargs)
		with self.canvas:
			self.Key = Window.request_keyboard(None, self) #keyboard function
			self.Key.bind(on_key_up= self.Keyaction) 
			self.bg = Bg(texture = self.ImageByte(self, self.byte_io.getvalue()).texture, pos=(0, 0), size = (Window.size[0], Window.size[1]))
	def ImageByte(self, instance, ImageByte):
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CoreImage(self.Buffer, ext= 'png')
		return self.BgIm

	def save(self, instance):
		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		with self.canvas:
			self.bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture

	def Keyaction(self, window, keycode):
		if keycode[1] == "l":
			try:

				self.Startevent.cancel()
				self.Im = Image.new("RGB", (Window.size[0], Window.size[1]), (0,0,0))
				self.byte_io = BytesIO()
				self.Im.save(self.byte_io, 'PNG')
				self.draw = ImageDraw.Draw(self.Im)
				self.save(self)
				print("h")
			except:
				pass
			self.start(self, self.Lplot)

		if keycode[1] == "c":
			if self.check == False:
				self.check = True
			else:
				self.check = False
		
			
	def start(self, instance,func):
		self.coords = []
		for el in range(10000):
			self.coords.append([[randint(-25,25),randint(-25,25),randint(-25,25)], [randint(0,255),randint(0,255),randint(0,255)]])
		self.Startevent = Clock.schedule_interval(func, 0.001)
		self.TStart = time.time()
		
		self.Startevent()
	
	def Lplot(self, instance):
		
		for element in self.coords:

			xder = 10 * (element[0][1] - element[0][0])
			yder = element[0][0] * (28 - element[0][2]) - element[0][1]
			zder = element[0][0] * element[0][1] - (8/3) * element[0][2]
			
			if self.check == False:
				self.draw.point([((element[0][0]/60)*500)+250, ((element[0][1]/60)*500)+250], (0,0,0))
			
			element[0][0] = element[0][0] + (xder * 0.005)
			element[0][1] = element[0][1] + (yder * 0.005)
			element[0][2] = element[0][2] + (zder * 0.005)

			self.draw.point([((element[0][0]/60)*500)+250, ((element[0][1]/60)*500)+250], tuple(element[1]))
		self.save(self)
		


class Diff(App):
	def build(self):
		return Drw()
