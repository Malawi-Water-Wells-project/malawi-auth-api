from app.main.models.well import Well


def get_all_wells():
    return Well.query.all()
