"""
Created 20/05/2021
GenerateTribeToken API Resource
"""

import base64
import json

from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.models.tribe import Tribe
from app.main.service.tribe_service import create_tribe_join_token
from app.main.util.decorator import AuthDecorators

api = TribeDto.api


@api.route("/<string:tribe_id>/generate-token")
class GenerateTribeToken(Resource):
    """ Resource for /tribes/<tribe_id>/generate-token """

    @api.doc("Creates a Join Token for a Tribe")
    @AuthDecorators.ensure_logged_in
    def get(self, tribe: Tribe, **_):
        """
        GET /tribes/<tribe_id>/gneerate-token
        Creates a Join Token that can be standard users can use to join a tribe
        """
        token = create_tribe_join_token(tribe.public_id, tribe.name)

        encoded_token = str(base64.encodebytes(
            json.dumps(token).encode()), "utf-8")

        return self.format_success(200, {"token": encoded_token})
