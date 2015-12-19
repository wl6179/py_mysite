# -*- coding: utf-8 -*-
# Django settings for mysite project.
#生产环境.
from settings import *


DEBUG = TEMPLATE_DEBUG = False

ADMINS = (
    ('Chris Wang', 'wangliang6179@163.com'),
)
MANAGERS = ADMINS