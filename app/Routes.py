import Endpoints


def initialize_routes(api):
    api.add_resource(
        Endpoints.RunTest,
        '/RunTest'
        )
