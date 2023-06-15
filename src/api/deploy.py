from flask_restx import Namespace, Resource

deploy_ns = Namespace('deploy', description='Terraform and azure deployement related operations')


@deploy_ns.route('/range')
class AzureRangeRunCommand(Resource):
    def post(self):
        # implement your method here
        pass
