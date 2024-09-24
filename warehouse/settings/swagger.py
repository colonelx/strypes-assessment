
import django
SWAGGER_SETTINGS = {
   # default inspector classes, see advanced documentation
   'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
   'DEFAULT_FIELD_INSPECTORS': [
      'drf_yasg.inspectors.CamelCaseJSONFilter',
      'drf_yasg.inspectors.ReferencingSerializerInspector',
      'drf_yasg.inspectors.RelatedFieldInspector',
      'drf_yasg.inspectors.ChoiceFieldInspector',
      'drf_yasg.inspectors.FileFieldInspector',
      'drf_yasg.inspectors.DictFieldInspector',
      'drf_yasg.inspectors.SimpleFieldInspector',
      'drf_yasg.inspectors.StringDefaultFieldInspector',
   ],
#    'DEFAULT_FILTER_INSPECTORS': [
#      'drf_yasg2.inspectors.CoreAPICompatInspector',
#    ],
   'DEFAULT_PAGINATOR_INSPECTORS': [
      'drf_yasg.inspectors.DjangoRestResponsePagination',
      'drf_yasg.inspectors.CoreAPICompatInspector',
   ],
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
   # default api Info if none is otherwise given; should be an import string to an openapi.Info object
   'DEFAULT_INFO': None,
   # default API url if none is otherwise given
   'DEFAULT_API_URL': '',

   'USE_SESSION_AUTH': True,  # add Django Login and Django Logout buttons, CSRF token to swagger UI page
   'LOGIN_URL': 'rest_framework:login',  # URL for the login button
   'LOGOUT_URL': 'rest_framework:logout',  # URL for the logout button

   # Swagger security definitions to include in the schema;
   # see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object
   'SECURITY_DEFINITIONS': {
      'basic': {
         'type': 'basic'
      }
   },

   # url to an external Swagger validation service; defaults to 'http://online.swagger.io/validator/'
   # set to None to disable the schema validation badge in the UI
   'VALIDATOR_URL': '',

   # swagger-ui configuration settings, see https://github.com/swagger-api/swagger-ui/blob/112bca906553a937ac67adc2e500bdeed96d067b/docs/usage/configuration.md#parameters
   'OPERATIONS_SORTER': None,
   'TAGS_SORTER': None,
   'DOC_EXPANSION': 'list',
   'DEEP_LINKING': False,
   'SHOW_EXTENSIONS': True,
   'DEFAULT_MODEL_RENDERING': 'model',
   'DEFAULT_MODEL_DEPTH': 3,
}