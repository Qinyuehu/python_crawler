import urllib.request
import urllib.parse
import http.cookiejar
import io
from tkinter import *
from PIL import Image, ImageTk


class InputLoginCode:
	def __init__(self, imageData):
		self.window = Tk()
		self.window.title("Please enter the verification code:")
		image1 = Image.open(imageData)
		photo = ImageTk.PhotoImage(image1)
		frame1 = Frame(self.window)
		frame1.pack()
		label1 = Label(frame1, image= photo)
		label1.pack()
		frame2 = Frame(self.window)
		frame2.pack()
		label = Label(frame2, text ="Enter the code: ")
		self.code = StringVar()
		entryName = Entry(frame2, textvariable = self.code)
		button = Button(frame2, text = "Confirm", command = self.processButton)
		label.grid(row=1, column = 1)
		entryName.grid(row=1, column = 2)
		button.grid(row=1, column = 3)

		self.window.mainloop()

	def processButton(self):
		global loginCode
		self.loginCode = self.code.get()
		self.window.destroy()

def login(userName, password):
	cookie = http.cookiejar.CookieJar()
	cookieProc = urllib.request.HTTPCookieProcessor(cookie)
	opener = urllib.request.build_opener(cookieProc)
	urllib.request.install_opener(opener)

	url = "http://my.hfut.edu.cn"
	req = urllib.request.Request(url)
	req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
	req.add_header("Referer", "http://my.hfut.edu.cn/logout.portal")
	req.add_header("Connection", "keep-alive")
	response = urllib.request.urlopen(req)


	loginCodeUrl = "http://my.hfut.edu.cn/captchaGenerate.portal"
	req2 = urllib.request.Request(loginCodeUrl)
	req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
	req.add_header("Referer", "http://my.hfut.edu.cn/login.portal")
	req.add_header("Connection", "keep-alive")
	response2 = urllib.request.urlopen(loginCodeUrl).read()
	 
	imageBuffer = io.BytesIO(response2)

	#InputLoginCode()
	data = {}
	data["Login.Token1"] = userName
	data["Login.Token2"] = password

	loginCode = InputLoginCode(imageBuffer).loginCode
	data["captchaField"] = loginCode

	data["goto"] = "http://my.hfut.edu.cn/loginSuccess.portal"
	data["gotoOnFail"] = "http://my.hfut.edu.cn/loginFailure.portal"

	postURL = "http://my.hfut.edu.cn/userPasswordValidate.portal"
	url_value = urllib.parse.urlencode(data)
	url_value = url_value.encode("utf-8")
	req3 = urllib.request.Request(postURL, url_value)
	req3.add_header("Host", "my.hfut.edu.cn")
	req3.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
	req3.add_header("Referer", "http://my.hfut.edu.cn/login.portal")
	req3.add_header("Connection", "keep-alive")
	response3 = urllib.request.urlopen(req3)

	postURL = "http://bkjw.hfut.edu.cn/StuIndex.asp"
	response = urllib.request.urlopen(postURL)
	postURL = "http://bkjw.hfut.edu.cn/student/asp/grkb1.asp"
	response = urllib.request.urlopen(postURL)
	#return urllib.request.urlopen(req4).read().decode("utf-8")
	return response.read().decode("gb2312")

if __name__ == "__main__":
	#userName = input("Input your student number: ")
	#password = input("Input your password: ")
	userName = "2012214904"
	password = "qinzihan112358"
	print(login(userName, password))


