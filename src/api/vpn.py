from flask_restx import Namespace, Resource

vpn_ns = Namespace('vpn', description='vpn related operations')


@vpn_ns.route('/range/users/get')
class AzureRangeRunCommand(Resource):
    def get(self):
        # implement your method here
        pass


