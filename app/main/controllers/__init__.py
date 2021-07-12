"""
Created 05/02/2021
__init__.py for the controllers
"""

import app.main.dto as dto
from app.main.controllers.auth import *
from app.main.controllers.villages import *
from app.main.controllers.users import *
from app.main.controllers.root import *
# from app.main.controllers.wells import *
from flask_restx import Api


def bind_controllers(api_instance: Api) -> None:
    """ Binds each controller to its own namespace """
    api_instance.add_namespace(dto.RootDto.api, "/")
    api_instance.add_namespace(dto.VillageDto.api, "/villages")
    api_instance.add_namespace(dto.AuthDto.api, "/auth")
    api_instance.add_namespace(dto.WellDto.api, "/wells")
    api_instance.add_namespace(dto.UserDto.api, "/users")
