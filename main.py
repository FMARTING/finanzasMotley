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

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

Jugadores = dict([(0,'N/A'),(1,'Pablo'),(2,'Facu'),(3,'Agus B.'),(4,'Cesar'),(5,'Martin'),(6,'Seba'),(7,'Chino'),(8,'Marian'),(9,'Facu H.'),(10,'Jony'),
	(11,'Alan'),(12,'Beli'),(13,'Diego'),(14,'Ryan'),(15,'Gabi'),(16,'Extra'),(17,'liga')])

class Handler(webapp2.RequestHandler):
	def write (self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
class MotleyMensual(db.Model):
	deuda = db.IntegerProperty(required = True)
	pago = db.IntegerProperty(required = True)
	saldo = db.IntegerProperty(required = True)
	mes = db.IntegerProperty(required = True)
	ano = db.IntegerProperty(required = True)
class Pago(db.Model):
	fecha = db.DateTimeProperty(auto_now_add = True)
	jugador = db.StringProperty(required = True)
	monto = db.IntegerProperty(required = True)
	descr = db.StringProperty()
class Input(Handler):
	
	def renderPagos(self, error = "" , ijugador = "" , imonto = "" , idescr = "" , errorJugador = ""):
		self.render("pagos.html", error = error, ijugador = ijugador, imonto = imonto, idescr = idescr, errorJugador = errorJugador)

	def get(self):
		self.renderPagos()

	def post(self):
		ijugador = self.request.get("ijugador")
		imonto = self.request.get("imonto")
		idescr = self.request.get("idescripcion")
		if ijugador and imonto and idescr:
			for i in range(17):
				if ijugador == Jugadores[i]:
					intMonto = int(imonto)
					p = Pago(jugador = ijugador, monto = intMonto, descr = idescr)
					p.put()
					self.redirect('/')
				else:
					errorJugador = "el jugador no se encuentra registrado, comunicate con Facu"
					self.renderPagos(ijugador = ijugador, imonto = imonto, idescr = idescr, errorJugador = errorJugador)
					break
			# intMonto = int(imonto)
			# p = Pago(jugador = ijugador, monto = intMonto, descr = idescr)
			# p.put()
			# self.redirect('/')
		else:
			error = "Todas las cajas deben completarse"
			self.renderPagos(ijugador = ijugador, imonto = imonto, idescr = idescr, error = error)

class Login(Handler):
	def get(self):
		self.render("login.html")
	def post(self):
		usuario = self.re

class MainPage(Handler):
    def get(self):
		# saldop = Pago(jugador = Jugadores[1], monto = 313, descr = "saldo de Pablo cuando deja de llevar las finanzas")
		# saldof = Pago(jugador = Jugadores[2], monto = 20, descr = "saldo de Facu cuando Pablo dejo de llevar las finanzas")
		# mov1 = Pago(jugador = Jugadores[15], monto = 50, descr = "Gastos del partido Gabi")
		# mov2 = Pago(jugador = Jugadores[5], monto = 420, descr = "Pago de Martin N para ponerse al dia")
		# mov3 = Pago(jugador = Jugadores[17], monto = -450, descr = "Pago gastos de partido")
		# mov4 = Pago(jugador = Jugadores[12], monto = 300, descr = "Pago Beli 5 de Octubre")
		# mov5 = Pago(jugador = Jugadores[15], monto = 50, descr = "Gastos del partido Gabi")
		# mov6 = Pago(jugador = Jugadores[11], monto = 100, descr = "Gastos Octubre Alan")
		# mov7 = Pago(jugador = Jugadores[17], monto = -450, descr = "Pago gastos de partido")
		# saldop.put()
		# saldof.put()
		# mov1.put()
		# mov2.put()
		# mov3.put()
		# mov4.put()
		# mov5.put()
		# mov6.put()
		# mov7.put()
		#son todos pagos viejos que ya agregue asi que los comento para que no se dupliquen
		cursorPago = db.GqlQuery("Select * from Pago order by fecha desc")
		cursorMensual = db.GqlQuery("Select * from MotleyMensual order by mes desc")
		deudaTotal = 0
		pagosTotal = 0
		saldoTotal = 0
		for i in cursorMensual:
			deudaTotal = deudaTotal + i.deuda
			pagosTotal = pagosTotal + i.pago
			saldoTotal = saldoTotal + i.saldo
		self.render("front.html", cursorMensual = cursorMensual, cursorPago = cursorPago, deudaTotal = deudaTotal, pagosTotal = pagosTotal, saldoTotal = saldoTotal)

app = webapp2.WSGIApplication([('/', Login),('/pago', Input),('/main', MainPage)], debug=True)