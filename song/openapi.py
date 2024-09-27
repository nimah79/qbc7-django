import json
from drf_yasg import openapi
from drf_yasg.utils import filter_none
from drf_yasg.utils import force_real_str
from drf_yasg.inspectors import SwaggerAutoSchema

class CustomAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys=None):
        operation_keys = operation_keys or self.operation_keys

        consumes = self.get_consumes()
        produces = self.get_produces()

        body = self.get_request_body_parameters(consumes)
        query = self.get_query_parameters()
        parameters = body + query
        parameters = filter_none(parameters)
        parameters = self.add_manual_parameters(parameters)

        operation_id = self.get_operation_id(operation_keys)
        summary, description = self.get_summary_and_description()
        security = self.get_security()
        assert security is None or isinstance(security, list), "security must be a list of security requirement objects"
        deprecated = self.is_deprecated()
        tags = self.get_tags(operation_keys)

        responses = self.get_responses()

        parameters_dict = {}

        if 'exmaple_paramters' in self.overrides:
            parameter_names = list(
                map(
                    lambda parameter: parameter.name,
                    self.get_request_form_parameters(self.get_view_serializer()),
                )
            )
            for parameter_name in parameter_names:
                if parameter_name in self.overrides['exmaple_paramters']:
                    parameters_dict[parameter_name] = self.overrides['exmaple_paramters'][parameter_name]

        languages = [
            'Bash',
            'Python',
        ]
        code_samples = []
        for language in languages:
            generator = getattr(self, f'generate_{language.lower()}_code', None)
            if not generator:
                continue
            code_samples.append({
                'lang': language,
                'source': generator(
                    self.method,
                    self.get_consumes()[0],
                    self.request.scheme + '://' + self.request.META['HTTP_HOST'] + self.path,
                    parameters_dict,
                )
            })

        return openapi.Operation(
            operation_id=operation_id,
            description=force_real_str(description),
            summary=force_real_str(summary),
            responses=responses,
            parameters=parameters,
            consumes=consumes,
            produces=produces,
            tags=tags,
            security=security,
            deprecated=deprecated,
            **{'x-code-samples': code_samples}
        )

    @staticmethod
    def generate_bash_code(method, content_type, url, parameters):
        return f'''curl -X {method} --location '{url}' \\
     --header 'Content-Type: {content_type}' \\
     --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9xxxx' \\
     --data '{json.dumps(parameters, indent=4)}\''''

    @staticmethod
    def generate_python_code(method, content_type, url, parameters):
        return f'''import requests

r = request.{method.lower()}(
    \'{url}\',
    headers={{'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9xxxx'}},
    json={str(parameters)},
)'''

change_password_responses = {
    '200': openapi.Response(
        description='Change password is successful',
        examples={
            'application/json': {
                'success': True,
            }
        }
    ),
    '400': openapi.Response(
        description='Unsuccessful operation',
        examples={
            'application/json': {
                'errors': {
                    'field_1_name': 'field_1_name error description',
                    'field_2_name': 'field_2_name error description',
                    'field_3_name': 'field_3_name error description',
                }
            }
        }
    ),
}
