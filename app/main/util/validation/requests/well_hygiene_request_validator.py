"""
Created 26/05/2021
"""

from app.main.service.tribe_service import TribeService
from app.main.util.validation.requests import AbstractRequestValidator, CommonRules


class PostWellHygieneValidator(AbstractRequestValidator):
    SCHEMA = {
        "tc_dry": CommonRules.FLOAT.required,
        "tc_wet": CommonRules.FLOAT.required,
        "fc_dry": CommonRules.FLOAT.required,
        "fc_wet": CommonRules.FLOAT.required,
        "turbidity_dry": CommonRules.FLOAT.required,
        "turbidity_wet": CommonRules.FLOAT.required,
        "tds_dry": CommonRules.FLOAT.required,
        "tds_wet": CommonRules.FLOAT.required,
        "electrical_conductivity_dry": CommonRules.FLOAT.required,
        "electrical_conductivity_wet": CommonRules.FLOAT.required,
        "ph_dry": CommonRules.FLOAT.required,
        "ph_wet": CommonRules.FLOAT.required,
        "temperature_dry": CommonRules.FLOAT.required,
        "temperature_wet": CommonRules.FLOAT.required,
        "fluoride_dry": CommonRules.FLOAT.required,
        "fluoride_wet": CommonRules.FLOAT.required,
        "sulphate_dry": CommonRules.FLOAT.required,
        "sulphate_wet": CommonRules.FLOAT.required,
        "hardness_dry": CommonRules.FLOAT.required,
        "hardness_wet": CommonRules.FLOAT.required,
        "nitrate_dry": CommonRules.FLOAT.required,
        "nitrate_wet": CommonRules.FLOAT.required,
        "ammonia_dry": CommonRules.FLOAT.required,
        "ammonia_wet": CommonRules.FLOAT.required,
        "arsonic_dry": CommonRules.FLOAT.required,
        "arsonic_wet": CommonRules.FLOAT.required,
        "nitrate_no2_dry": CommonRules.FLOAT.required,
        "nitrate_no2_wet": CommonRules.FLOAT.required
    }
