#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chimera.core.chimeraobject import ChimeraObject
from chimera.core.constants import SYSTEM_CONFIG_DIRECTORY

import cherrypy

import threading
import os


class WebAdminRoot (object):

    def __init__(self, controller):
        self.controller = controller

    @cherrypy.expose
    def index(self):
        return open(
            os.path.join(os.path.dirname(__file__), "webadmin.html")).read()

    @cherrypy.expose
    def start(self):

        if self.controller["start_action"] is None:
            return "No START action configured. Skipping..."

        try:
            self.controller.supervisor.runAction(self.controller["start_action"])
        except Exception, e:
            return "Error trying to START the system! %s" % str(e)

        return "Success!"

    @cherrypy.expose
    def stop(self):

        if self.controller["stop_action"] is None:
            return "No STOP action configured. Skipping..."

        try:
            self.controller.supervisor.runAction(self.controller["stop_action"])
        except Exception, e:
            return "Error trying to STOP the system! %s" % str(e)

        return "Success!"

    @cherrypy.expose
    def pause(self):

        if self.controller["resume_action"] is None:
            return "No RESUME action configured. Skipping..."

        try:
            self.controller.supervisor.runAction(self.controller["resume_action"])
        except Exception, e:
            return "Error trying to RESUME the observations! %s" % str(e)

        return "Success!"


class WebAdmin (ChimeraObject):

    __config__ = {"supervisor": "/Supervisor/0",
                  "start_action": None,
                  "resume_action": None,
                  "stop_action": None,
                  "socket_host": "default",
                  "socket_port": 5000}

    def __init__(self):
        ChimeraObject.__init__(self)

    def __start__(self):

        try:
            self.supervisor = self.getManager().getProxy(self["supervisor"])
        except Exception:
            self.log.warning(
                "Supervisor not found, Web Admin will be disabled.")
            return False

        if self["socket_host"] == "default":
            self["socket_host"] = self.getManager().getHostname()

        self.log.info("lisetning on '%s'" % self['socket_host'])

        cherrypy.config.update({"engine.autoreload.on": False,
                                "server.socket_host": self['socket_host'],
                                "server.socket_port": self["socket_port"],
                                "log.screen": False,
                                "log.error_file": os.path.join(SYSTEM_CONFIG_DIRECTORY, "webadmin_error.log"),
                                "log.access_file": os.path.join(SYSTEM_CONFIG_DIRECTORY, "webadmin_access.log")})

        current_dir = os.path.dirname(os.path.abspath(__file__))

        app_config = {"/": {},
                      "/jquery-1.11.3.min.js": {"tools.staticfile.on": True,
                                                "tools.staticfile.filename": os.path.join(current_dir, "jquery-1.11.3.min.js")}
                      }

        def start():
            cherrypy.quickstart(WebAdminRoot(self), "/", app_config)

        threading.Thread(target=start).start()

        return True

    def __stop__(self):
        cherrypy.engine.exit()
