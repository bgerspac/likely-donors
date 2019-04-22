import cherrypy
import json
import os
import argparse

import predictions

class HelloCherryPy(object):

	@cherrypy.expose
	@cherrypy.tools.allow(methods=["POST"])
	def predict(self,
			age=40,
			workclass="?",
			education_num=1,
			marital_status="?",
			occupation="?",
			relationship="?",
			race="?",
			sex="Male",
			capital_gain=0,
			capital_loss=0,
			hours_per_week=0,
			native_country="?"):
		likely = predictions.get_donor_class(
			age=int(age),
			workclass=workclass,
			education_num=int(education_num),
			marital_status=marital_status,
			occupation=occupation,
			relationship=relationship,
			race=race,
			sex=sex,
			capital_gain=int(capital_gain),
			capital_loss=int(capital_loss),
			hours_per_week=int(hours_per_week),
			native_country=native_country)
		return json.dumps(likely)


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
