import secrets
import string

from flask import request

alphabet = string.ascii_letters + string.digits


def gen_id(length=8):
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def with_pagination(model, parent_id_args=None):
    sort = request.args.get('sort', default=None, type=str)
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)

    if parent_id_args is None:
        collection = model.objects.skip(offset).limit(limit)
    else:
        collection = model.objects(**parent_id_args).skip(offset).limit(limit)
    if sort is not None:
        collection = collection.order_by(sort)

    return collection
