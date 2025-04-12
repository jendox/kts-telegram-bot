from data_service.web.jwt_utils import UserRole


def required_roles(*roles: UserRole):
    def decorator(cls):
        cls.required_roles = set(roles)
        return cls

    return decorator
