import webapp2
import jinja2
import os 
import codecs
import re
temp_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(temp_dir), autoescape = True)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(u):
	return USER_RE.match(u)
PASSWORD_RE = re.compile("^.{3,20}$")
def valid_password(p):
	return PASSWORD_RE.match(p)
EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(e):
	return EMAIL_RE.match(e)



class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw):

		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render_html(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(Handler):

	def get(self):

		self.render_html("signup.html")

	
	def post(self):

		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		incorrect_u=incorrect_p=incorrect_v=incorrect_e = 5
		empty_u=empty_p=empty_v=empty_e=5
		if not username:
		 	empty_u = 2
		else:
			if not valid_username(username):
				empty_u = 2
			else:
				empty_u = 5

		if not password:
		 	empty_p = 2
		else:
			if not valid_password(password):
				empty_p = 2
			else:
				empty_p = 5
		if not email:
		 	empty_e = 2
		else:
			if not valid_email(email):
				empty_e = 2
			else:
				empty_e = 5

		if not verify:
		 	incorrect_v = 2
		else:
			if not password==verify:
				incorrect_v = 2
			else:
				incorrect_v =5

		a = empty_u + empty_p + incorrect_v
		if  a != 15:
			self.render_html("signup.html", empty_u=empty_u, empty_p=empty_p,
			empty_v=empty_v, empty_e=empty_e , incorrect_u=incorrect_u,
			incorrect_p=incorrect_p, incorrect_v=incorrect_v, incorrect_e=incorrect_e, username=username, email=email)
		else:

			self.redirect("/welcome?username=%s" %username)		


class Welcome(Handler):

	def get(self):

		username = self.request.get("username")
		if valid_username(username):
			self.render_html("welcome.html", username=username)
		else:
			self.render_html("signup.html")
		

		

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/welcome', Welcome)], debug=True)

