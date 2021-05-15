"""
Created 05/02/2021
__init__.py for the controllers
"""

from app.main.controllers.auth_controller import api as auth_ns
from app.main.controllers.tribe_controller import api as tribe_ns
from app.main.controllers.well_controller import api as well_ns
from flask_restx import Api


def bind_controllers(api: Api) -> None:
    """ Binds each controller to its own namespace """
    api.add_namespace(tribe_ns, "/tribes")
    api.add_namespace(auth_ns, "/auth")
    api.add_namespace(well_ns, "/wells")
