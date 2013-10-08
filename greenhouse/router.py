from django.db import connections


class DBRouter(object):
    "Route our models to the correct db."

    def db_for_read(self, model, **hints):
        if hasattr(model, 'connection_name'):
            return model.connection_name
        return None

    def db_for_write(self, model, **hints):
        if hasattr(model, 'connection_name'):
            return model.connection_name
        return None

    def allow_syncdb(self, db, model):
        if hasattr(model, 'connection_name'):
            return model.connection_name
        return None
