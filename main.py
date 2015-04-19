#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import re
import cgi
import random
import string
import hashlib
import time
import datetime
import calendar

"""falta ingresar una forma de distribuir los gastos de partido acorde a los jugadores que fueron.
Por ultimo con toda esta informacion que se muestre un resumen por jugador por mes de cada jugador con debe y haber. De esto ultimo falta configuarar la parte de
haber, sumar los pagos realizados en cada mes y mostrarlos. Y en base a esto ultimo tambien calcular el mensual total del equipo por mes
Por ultimo poner una pagina mas donde solo yo, como administrador o la liga, podamos determinar quien es el administrador de cada equipo que va a poder ingresar
pagos y hacer modificaciones a los montos

Otra cosa para ver es como hacer el display de la suma de los pagos dentro de un mismo mes de un mismo jugador. Por ejemplo, si yo en el mismo mes pago 300 un dia y 500 otro que me aparezcan 800 en el mismo mes, que lo sume el sistema y que no lo haga figurar como en meses separados
"""
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), extensions = ['jinja2.ext.autoescape'], autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASS_RE = re.compile(r"^.{3,20}$")

def loginCheck(u,p,h):
	salt = h.split('|')[1]
	return h == make_pw_hash(u,p,salt)
	
def uniqueUser(nombre): # Si el usuario es unico devuelve Verdadero
	x = db.GqlQuery("Select * from Jugadores where nombre= :1", nombre).get()
	if x:
		return False
	return True

def uniqueEquipo(nombre): # Si el equipo es unico devuelve Verdadero
	x = db.GqlQuery("Select * from Equipos where nombre= :1", nombre).get()
	if x:
		return False
	return True

def idEquipo(equipo): #devuelve el id del equipo del nuevo usuario, si ya existe del equipo existente, sino del nuevo equipo
	if uniqueEquipo(equipo):
		a = Equipos(nombre = equipo)
		a.put()
		return a.key().id()
	else:
		return db.GqlQuery("Select * from Equipos where nombre= :1", equipo).get().key().id()

def tamano_equipo(equipo):#devuelve el tamano de un equipo
	x = db.GqlQuery("Select * from Jugadores where equipo= :1", equipo).fetch(None)
	cantidad_jugadores = 0
	for i in x:
		cantidad_jugadores +=1
	return cantidad_jugadores
	
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def escape(s):
	return cgi.escape(s, quote = True)

def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' %(h, salt)

def valid_pass(password):
   return PASS_RE.match(password)
  
def valid_username(username):
   return USER_RE.match(username)

def matched_password(password, verify):
	if password == verify: return True
	else: return False

def obtainInt(self, campo):
	if self.request.get(str(campo)) == "":
		return 0
	else:
		return int(self.request.get(str(campo)))

class Handler(webapp2.RequestHandler):
	def write (self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
		
def ingresarGastoPorPartido(lista, mes, monto): #acorde a cada mes pasa a la base de datos los gastos de partido para cada jugador
	if mes == "1":
		for a in lista:
			a.gastos_p1 = monto
			a.put()
	if mes == "2":
		for a in lista:
			a.gastos_p2 = monto
			a.put()
	if mes == "3":
		for a in lista:
			a.gastos_p3 = monto
			a.put()
	if mes == "4":
		for a in lista:
			a.gastos_p4 = monto
			a.put()
	if mes == "5":
		for a in lista:
			a.gastos_p5 = monto
			a.put()
	if mes == "6":
		for a in lista:
			a.gastos_p6 = monto
			a.put()
	if mes == "7":
		for a in lista:
			a.gastos_p7 = monto
			a.put()
	if mes == "8":
		for a in lista:
			a.gastos_p8 = monto
			a.put()
	if mes == "9":
		for a in lista:
			a.gastos_p9 = monto
			a.put()	
	if mes == "10":
		for a in lista:
			a.gastos_p10 = monto
			a.put()
	if mes == "11":
		for a in lista:
			a.gastos_p11 = monto
			a.put()
	if mes == "12":
		for a in lista:
			a.gastos_p12 = monto
			a.put()

class Equipos (db.Model):
	nombre = db.StringProperty(required = True)
	gastos_total = db.IntegerProperty()
	gastos_inscr = db.IntegerProperty()
	gastos_admin = db.IntegerProperty()
	gastos_otros = db.IntegerProperty()
	
class MontoMensual(db.Model):
	deuda = db.IntegerProperty(required = True)
	pago = db.IntegerProperty(required = True)
	saldo = db.IntegerProperty(required = True)
	mes = db.IntegerProperty(required = True)
	ano = db.IntegerProperty(required = True)

class Pagos(db.Model):
	jugador_id = db.IntegerProperty(required = True)
	nombre = db.StringProperty(required = True)
	monto = db.IntegerProperty(required = True)
	comentario = db.StringProperty(required = True)
	equipo = db.IntegerProperty(required = True)
	year = db.IntegerProperty(required = True)
	month = db.IntegerProperty(required = True)

class Jugadores (db.Model):
	nombre = db.StringProperty(required = True)
	apellido = db.StringProperty(required = True)
	usuario = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	equipo = db.IntegerProperty(required = True)
	gastos_p1 = db.IntegerProperty(default = 0)
	gastos_p2 = db.IntegerProperty(default = 0)
	gastos_p3 = db.IntegerProperty(default = 0)
	gastos_p4 = db.IntegerProperty(default = 0)
	gastos_p5 = db.IntegerProperty(default = 0)
	gastos_p6 = db.IntegerProperty(default = 0)
	gastos_p7 = db.IntegerProperty(default = 0)
	gastos_p8 = db.IntegerProperty(default = 0)
	gastos_p9 = db.IntegerProperty(default = 0)
	gastos_p10 = db.IntegerProperty(default = 0)
	gastos_p11 = db.IntegerProperty(default = 0)
	gastos_p12 = db.IntegerProperty(default = 0)
	admin = db.BooleanProperty(default=False)

class Haberes_mes (db.Model):
	Jugador = db.StringProperty(required = True)
	H1 = db.IntegerProperty(default = 0)
	H2 = db.IntegerProperty(default = 0)
	H3 = db.IntegerProperty(default = 0)
	H4 = db.IntegerProperty(default = 0)
	H5 = db.IntegerProperty(default = 0)
	H6 = db.IntegerProperty(default = 0)
	H7 = db.IntegerProperty(default = 0)
	H8 = db.IntegerProperty(default = 0)
	H9 = db.IntegerProperty(default = 0)
	H10 = db.IntegerProperty(default = 0)
	H11 = db.IntegerProperty(default = 0)
	H12 = db.IntegerProperty(default = 0)

class Pago(Handler):
	
	def renderPagos(self, error = "" , ijugador = "" , imonto = "" , idescr = "" , errorJugador = "", equipo = ""):
		self.render("pagos.html", error = error, ijugador = ijugador, imonto = imonto, idescr = idescr, errorJugador = errorJugador, equipo = equipo)

	def get(self):
		user_equipo_id = self.request.cookies.get('equipo',0)
		equipo = Equipos.get_by_id(int(self.request.cookies.get('equipo',0)))
		user_equipo = str(equipo.nombre)
		self.renderPagos(equipo = user_equipo.upper())

	def post(self):
		ijugador = self.request.get("ijugador")
		imonto = self.request.get("imonto")
		idescr = self.request.get("idescripcion")
		titular_pago = self.request.get("pjugador")
		user = Jugadores.get_by_id(int(self.request.cookies.get('jugador',0)))
		user_id = user.key().id()
		user_nombre = str(user.nombre)
		user_equipo_id = self.request.cookies.get('equipo',0)
		equipo = Equipos.get_by_id(int(self.request.cookies.get('equipo',0)))
		user_equipo = equipo.nombre
		fecha_actual = datetime.datetime.today()
		year = fecha_actual.year
		month = fecha_actual.month
		if imonto and idescr:
			if titular_pago == "otro":
				if not ijugador:
					errorJugador = "No ingresaste un jugador valido"
					self.renderPagos(ijugador = ijugador, imonto = imonto, idescr = idescr, errorJugador = errorJugador)
				if ijugador:
					user_monto = int(imonto)
					user_nombre = str(ijugador)
					user_comentario = str(idescr)
					nPago = Pagos(nombre = user_nombre, jugador_id = user_id, monto = user_monto, comentario = user_comentario, equipo = int(user_equipo_id), year = year, month = month)
					nPago.put()
					#agregar aca las lineas para que genere si no existe el db haberes_mes y para que calcule cada uno de los pagos totales por mes segun corresponda
					""" Aca algunas lineas que ya pense, quizas el ID del jugador se puede sacar de la cooie
					x = db.GqlQuery("Select * from Jugadores where usuario= :1", usuario).get()
					if x:
						id_jugador = x.key().id()
					h = Haberes_mes(Jugador = str(id_jugador))
					h.put()
					"""
					self.redirect('/main')
				else:
					errorJugador = "Hubo un problema, contactate con Facu"
					self.renderPagos(ijugador = ijugador, imonto = imonto, idescr = idescr, errorJugador = errorJugador)
			elif titular_pago == "propio":
				if imonto and idescr:
					user_monto = int(imonto)
					user_comentario = str(idescr)
					nPago = Pagos(nombre = user_nombre, monto = user_monto, jugador_id = user_id, comentario = user_comentario, equipo = int(user_equipo_id), year = year, month = month)
					nPago.put()
					self.redirect('/main')
				else:
					errorJugador = "Hubo un problema, saca un screenshot y habla con Facu"
					self.renderPagos(ijugador = ijugador, imonto = imonto, idescr = idescr, errorJugador = errorJugador)	
			else:
				errorJugador = "Hubo un problema, saca un screenshot y habla con Facu"
				self.renderPagos(ijugador = ijugador, imonto = imonto, idescr = idescr, errorJugador = errorJugador)
		else:
			error = "Todas las cajas deben completarse"
			self.renderPagos(ijugador = ijugador, imonto = imonto, idescr = idescr, error = error)

class Login(Handler):
	def get(self):
		self.render("login.html")
	def post(self):
		usuario = self.request.get("iusuario")
		password = self.request.get("ipassword")
		x = db.GqlQuery("Select * from Jugadores where usuario= :1", usuario).get()
		if x:
			hashedPassword = x.password
			uequipo = x.equipo
			id_jugador = x.key().id()
		fecha_actual = datetime.datetime.today()
		year = fecha_actual.year
		month = fecha_actual.month
		if not x:
			errorUsuario = "La clave o el usuario ingresado son incorrectos"
			self.render("login.html", errorUsuario = errorUsuario, ijugador = usuario)
		elif loginCheck(usuario, password, hashedPassword):
			self.response.headers.add_header('Set-Cookie', 'equipo = %s; Path=/' %(uequipo))
			self.response.headers.add_header('Set-Cookie', 'jugador = %s; Path=/' %(str(id_jugador)))
			self.response.headers.add_header('Set-Cookie', 'fecha = %s; Path=/' %(str(year)))
			self.redirect('/main')
		else:
			errorUsuario = "La clave o el usuario ingresado son incorrectos"
			self.render("login.html", errorUsuario = errorUsuario, ijugador = usuario)

class nuevoUsuario(Handler):
	def renderNuevo(self, errorUsuario = "", errorVerif = "" , inombre = "" , iapellido = "" , iusuario = "" , ipass = "", iverif = "", errorPass = "", iequipo=""):
		self.render("nuevo_usuario.html", errorUsuario = errorUsuario, errorVerif = errorVerif, inombre = inombre, iapellido = iapellido, iusuario = iusuario, ipass = ipass, iverif = iverif, errorPass = errorPass, iequipo = iequipo)

	def get(self):
		self.renderNuevo()

	def post(self):
		nombre = escape(self.request.get('inombre'))
		apellido = escape(self.request.get('iapellido'))
		usuario = escape(self.request.get('iusuario'))
		password = escape(self.request.get('ipass'))
		verify = escape(self.request.get('iverif'))
		equipo = escape(self.request.get('iequipo'))
		checked_verify = matched_password(password, verify)
		hpassword = make_pw_hash(usuario, password)
		if valid_username(usuario) and valid_pass(password) and checked_verify:
			usuario = str(usuario)
			if uniqueUser(usuario):#verdadero si el usuario es unico
				id_equipo = idEquipo(equipo)
				a = Jugadores(nombre = nombre, apellido = apellido, usuario = usuario, password = hpassword, equipo = id_equipo)
				a.put()
				self.response.headers.add_header('Set-Cookie', 'name = %s; Path=/' %(usuario))
				self.response.headers.add_header('Set-Cookie', 'pass = %s; Path=/' %(hpassword))
				self.redirect('/')
			elif not uniqueUser(usuario):
				errorUsuario = "El usuario ya existe"
				self.renderNuevo(errorUsuario = errorUsuario, inombre = nombre, iapellido = apellido)
		elif not checked_verify:
			errorVerificacion = "Las claves no son iguales"
			self.renderNuevo(errorVerif = errorVerificacion, inombre = nombre, iapellido = apellido, iusuario = usuario)
		elif not valid_pass(password):
			errorPass = "La clave debe ser mas compleja"
			self.renderNuevo(errorPass = errorPass, inombre = nombre, iapellido = apellido, iusuario = usuario)
		elif not valid_username(usuario):
			errorUsuario = "El usuario debe ser mas largo"
			self.renderNuevo(errorUsuario = errorUsuario, inombre = nombre, iapellido = apellido)

class MainPage(Handler):
	def renderMain(self, gasto_mes_jugador="", equipo = "", cursorNombres="", cursorPago = "", deudaTotal="", pagosTotal="", saldoTotal="", cal = ""):
		self.render("front.html", gasto_mes_jugador = gasto_mes_jugador, equipo = equipo, cursorNombres = cursorNombres, cursorPago = cursorPago, deudaTotal = deudaTotal, pagosTotal = pagosTotal, saldoTotal = saldoTotal, cal = cal)

	def get(self):
		equipo = Equipos.get_by_id(int(self.request.cookies.get('equipo',0)))
		equipo_id = equipo.key().id()
		deudaTotal = 0
		pagosTotal = 0
		saldoTotal = 0
		year = int(self.request.cookies.get('fecha',0))
		user_equipo = equipo.nombre
		htmlcal = calendar.HTMLCalendar(calendar.MONDAY)
		cal =  htmlcal.formatyear(year)
		cursorPago = db.GqlQuery("Select * from Pagos where equipo = %s" %(str(equipo_id)))
		cursorMensual = db.GqlQuery("Select * from MontoMensual order by mes desc")
		jugadores = db.GqlQuery("Select * from Jugadores where equipo = %s" %(str(equipo_id)))
		for i in cursorMensual:
			deudaTotal = deudaTotal + i.deuda
			pagosTotal = pagosTotal + i.pago
			saldoTotal = saldoTotal + i.saldo
		#Vieja linea para calcular la cantidad de fines de semana en el mes, al final no la use
		#domingos = str(len([1 for i in calendar.monthcalendar(year, datetime.datetime.today().month) if i[6] != 0]))
		try:
			gasto_mes_jugador = int(equipo.gastos_total/12/tamano_equipo(equipo_id))
		except:
			gasto_mes_jugador = 0
		self.renderMain(cal = cal, cursorNombres = jugadores, equipo = user_equipo, gasto_mes_jugador = gasto_mes_jugador, cursorPago = cursorPago)

class Logout (Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'name =; Path=/')
		self.response.headers.add_header('Set-Cookie', 'pass =; Path=/')
		self.response.headers.add_header('Set-Cookie', 'equipo =; Path=/')
		self.response.headers.add_header('Set-Cookie', 'fecha =; Path=/')
		self.response.headers.add_header('Set-Cookie', 'jugador =; Path=/')
		self.redirect('/')

class GastosF (Handler):
	def renderGastosF(self, equipo = "", cantidad_jugadores = "", gastos_total = "", gastos_jug_ano = "", gastos_jug_mes = "", gastos_inscr = "", gastos_admin="", gastos_otros = ""):
		self.render("gastos_fijos.html", equipo = equipo, cantidad_jugadores = cantidad_jugadores, gastos_total = gastos_total, gastos_jug_ano = gastos_jug_ano, gastos_jug_mes = gastos_jug_mes, gastos_inscr = gastos_inscr, gastos_admin = gastos_admin, gastos_otros = gastos_otros)

	def get(self):
		equipo = Equipos.get_by_id(int(self.request.cookies.get('equipo',0)))
		equipo_id = equipo.key().id()
		user_equipo = equipo.nombre
		cantidad_jugadores = tamano_equipo(equipo_id)
		gastos_total = 0
		gastos_inscr = 0
		gastos_admin = 0
		gastos_otros = 0
		if equipo.gastos_total != None:
			gastos_total = equipo.gastos_total
		if equipo.gastos_inscr !=None:
			gastos_inscr = equipo.gastos_inscr
		if equipo.gastos_admin !=None:
			gastos_admin = equipo.gastos_admin
		if equipo.gastos_otros !=None:
			gastos_otros = equipo.gastos_otros
		gastos_jug_ano = gastos_total/cantidad_jugadores
		gastos_jug_mes = gastos_jug_ano/12
		self.renderGastosF(equipo = user_equipo, cantidad_jugadores = cantidad_jugadores, gastos_total = gastos_total, gastos_jug_ano = gastos_jug_ano, gastos_jug_mes = gastos_jug_mes, gastos_inscr = gastos_inscr, gastos_admin = gastos_admin, gastos_otros = gastos_otros)
		
	def post(self):
		equipo = Equipos.get_by_id(int(self.request.cookies.get('equipo',0)))
		equipo_id = equipo.key().id()
		gastos_inscr = self.request.get("gastos_inscr")
		gastos_admin = self.request.get("gastos_admin")
		gastos_otros = self.request.get("gastos_otros")
		gastos_total = int(gastos_inscr) + int(gastos_admin) + int(gastos_otros)
		equipo.gastos_inscr = int(gastos_inscr)
		equipo.gastos_admin = int(gastos_admin)
		equipo.gastos_otros = int(gastos_otros)
		equipo.gastos_total = int(gastos_total)
		equipo.put()
		self.redirect('/main')

class GastosP (Handler):
	def renderGastosP(self, jugadores="", equipo="", qjugadores = "", gastos1="", mes = ""):
		self.render("gastos_p.html", jugadores = jugadores, equipo = equipo, qjugadores=qjugadores, gastos1 = gastos1, mes = mes)

	def get(self):
		equipo = Equipos.get_by_id(int(self.request.cookies.get('equipo',0)))
		equipo_id = equipo.key().id()
		user_equipo = equipo.nombre
		jugadores = db.GqlQuery("Select * from Jugadores where equipo = %s" %(str(equipo_id)))
		self.renderGastosP(equipo = user_equipo, jugadores = jugadores)
	
	def post(self):
		equipo = Equipos.get_by_id(int(self.request.cookies.get('equipo',0)))
		equipo_id = equipo.key().id()
		user_equipo = equipo.nombre
		mes = self.request.get("mes")
		participantes1 = self.request.get("1participantes", allow_multiple=True)
		participantes2 = self.request.get("2participantes", allow_multiple=True)
		participantes3 = self.request.get("3participantes", allow_multiple=True)
		participantes4 = self.request.get("4participantes", allow_multiple=True)
		participantes5 = self.request.get("5participantes", allow_multiple=True)
		participantes6 = self.request.get("6participantes", allow_multiple=True)
		participantes7 = self.request.get("7participantes", allow_multiple=True)
		participantes8 = self.request.get("8participantes", allow_multiple=True)
		participantes9 = self.request.get("9participantes", allow_multiple=True)
		participantes10 = self.request.get("10participantes", allow_multiple=True)
		Gastos_p1 = obtainInt(self, "1Gastos_p")
		Gastos_p2 = obtainInt(self, "2Gastos_p")
		Gastos_p3 = obtainInt(self, "3Gastos_p")
		Gastos_p4 = obtainInt(self, "4Gastos_p")
		Gastos_p5 = obtainInt(self, "5Gastos_p")
		Gastos_p6 = obtainInt(self, "6Gastos_p")
		Gastos_p7 = obtainInt(self, "7Gastos_p")
		Gastos_p8 = obtainInt(self, "8Gastos_p")
		Gastos_p9 = obtainInt(self, "9Gastos_p")
		Gastos_p10 = obtainInt(self, "10Gastos_p")
		Gastos_mes = Gastos_p1+Gastos_p2+Gastos_p3+Gastos_p4+Gastos_p5+Gastos_p6+Gastos_p7+Gastos_p8+Gastos_p9+Gastos_p10
		jugadores = db.GqlQuery("Select * from Jugadores where equipo = %s" %(str(equipo_id)))
		cant_jug = tamano_equipo(equipo_id)
		#hacer un diccionario para que para cada clave, el nombre de un jugador, se le asignen varios valores de gastos acorde a cada partido. Y despues al final
		#sumo todos esos valores y los ingreso a la base de datos
		#por ahora lo voy a dejar para que siempre se divida entre todos, hasta que pueda encontrarle una solucion
		Gasto_p_part = Gastos_mes/cant_jug
		ingresarGastoPorPartido(jugadores, mes, Gasto_p_part)
		#self.renderGastosP(equipo = user_equipo, jugadores = jugadores, gastos1 = Gastos_mes, qjugadores = str(cant_jug), mes = mes)
		#deje la linea de arriba por si en el futuro quiero probar como funcinoa la formula, la actual que es solo para todos o eventualmente una que 
		#guarde montos distintso para cada jugador si cada fin de semana es un grupo distinto de jugadores
		#para mi la clave de esa solucion es usar un diccionario, acumular valores para c/jugador, sumarlo al final y subirlo a la base en el mes adecuado
		self.redirect('/main')

app = webapp2.WSGIApplication([('/', Login),('/pago', Pago),('/main', MainPage),('/nuevo_usuario', nuevoUsuario),('/logout', Logout),('/gastos_f', GastosF),
('/gastos_p', GastosP)], debug=True)