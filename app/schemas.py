
from rest_framework.schemas.openapi import AutoSchema

class CustomSchema(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        if method == "GET":
            operation["summary"] = f"GET operation for {path}"
        elif method == "POST":
            operation["summary"] = f"POST operation for {path}"
        return operation
