from flask_restx import Namespace


class TribeDto:
    api = Namespace("tribe", description="Tribe Operations")
