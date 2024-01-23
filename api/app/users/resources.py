from flask_restx import Namespace, Resource

# Create a namespace for user operations
user_namespace = Namespace("user", description="User operations")


@user_namespace.route("/")
class AllUsers(Resource):
    def get(self):
        """Get all users."""
        pass
