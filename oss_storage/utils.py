from django.conf import settings

def aliyun_setting(name, value=None):
    env_value = getattr(settings, name, None)
    value = env_value if value is None else value
    if value is None:
        assert value, '{} should not be None'.format(name)
    return value
