
class WhaleDatabaseRouter(object):

    def db_for_read(self, model, **hints):
        """Send all read operations on whalesdb app models to `whalesdb`."""
        if model._meta.app_label == 'whalesdb':
            return 'whalesdb'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on whalesdb app models to `whalesdb`."""
        if model._meta.app_label == 'whalesdb':
            return 'whalesdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the Example app.
        if obj1._meta.app_label == 'whalesdb' and obj2._meta.app_label == 'whalesdb':
            return True
        # No opinion if neither object is in the Example app (defer to default or other routers).
        elif 'whalesdb' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

            # Block relationship if one object is in the Example app and the other isn't.
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the whalesdb app's models get created on the right database."""
        if app_label == 'whalesdb':
            # The Example app should be migrated only on the example_db database.
            return db == 'whalesdb'
        elif db == 'whalesdb':
            # Ensure that all other apps don't get migrated on the example_db database.
            return False

        # No opinion for all other scenarios
        return None


# useful piece of code:
#         if MY_ENVR == 'dev':
#             if model._meta.app_label == 'auth' or model._meta.app_label == 'sessions' or model._meta.app_label == 'inventory' or model._meta.app_label == 'projects':
#                 return None
#             else:
#                 return 'dev'
#         else:
#             return None