import cherrypy
import json
import os
import argparse

class HelloCherryPy(object):
	#@cherrypy.expose("index")
	#@cherrypy.tools.allow(methods=["GET"])
	#def interface(self):
	#	return "TODO: Interface"

	@cherrypy.expose
	@cherrypy.tools.allow(methods=["POST"])
	def predict(self, age="20", height="175"):
		age = int(age)
		return json.dumps(age > 30)

class Empty(): pass

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--socket_host", required=False, default="127.0.0.1")
	parser.add_argument("--socket_port", required=False, type=int, default=8080)
	args = parser.parse_args()

	staticdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
	print(staticdir)

	cherrypyconfig={
		"/" : {
			"tools.staticdir.on": True,
			"tools.staticdir.dir": staticdir,
			"tools.staticdir.index": "index.htm",
		},
	}
	cherrypy.server.socket_host = args.socket_host
	cherrypy.server.socket_port = args.socket_port
	cherrypy.quickstart(HelloCherryPy(), config=cherrypyconfig)
