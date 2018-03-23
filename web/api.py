from aiohttp import web
from datetime import datetime
import aiohttp_jinja2
import os

from web import utils
from config import config
from sql import sql


async def get_enrollment_data(request):
    if 'TOKEN' in request.cookies.keys():
        if request.cookies['TOKEN'] == config.USER_TOKEN:
            success, result = sql.get_course_enrollments(config=config.envs)
            if success:
                result = utils.object_to_text(result, replace_id=True)
                filename = f"course_enrollment" \
                           f"{datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime('%d%m%Y_%H%M')}.txt"
                with open(os.path.join('/data', filename), 'w') as f:
                    f.write(result)
                    f.close()
                headers = {
                    "Content-Disposition": f"attachment; filename={filename}"
                }
                return web.Response(body=open(os.path.join('/data', filename), 'rb').read(), headers=headers)
            else:
                return web.Response(body=str(result))

    response = aiohttp_jinja2.render_template('login.jinja2', request, {})
    response.headers['Content-Language'] = 'ru'
    return response


async def get_users_data(request):
    if 'TOKEN' in request.cookies.keys():
        if request.cookies['TOKEN'] == config.USER_TOKEN:
            success, result = sql.get_user_data(config=config.envs)
            if success:
                result = utils.object_to_text(result,
                                              replace_id=True,
                                              replace_gender=True,
                                              replace_none=True,
                                              replace_education=True)
                filename = f"users" \
                           f"{datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime('%d%m%Y_%H%M')}.txt"
                with open(os.path.join('/data', filename), 'w') as f:
                    f.write(result)
                    f.close()
                headers = {
                    "Content-Disposition": f"attachment; filename={filename}"
                }
                return web.Response(body=open(os.path.join('/data', filename), 'rb').read(), headers=headers)
            else:
                return web.Response(body=str(result))

    response = aiohttp_jinja2.render_template('login.jinja2', request, {})
    response.headers['Content-Language'] = 'ru'
    return response


async def authorization(request: web.Request):
    json = await request.json()
    token = json['token']
    if token:
        if token == config.envs['token']:
            headers = {
                'Set-Cookie': f'TOKEN={config.USER_TOKEN}'
            }
            return web.Response(body="{'result': True}", headers=headers)
    return web.Response(body="{'result': False}")


async def admin_panel(request: web.Request):
    if 'TOKEN' in request.cookies.keys():
        if request.cookies['TOKEN'] == config.USER_TOKEN:
            response = aiohttp_jinja2.render_template('admin.jinja2', request, {})
            response.headers['Content-Language'] = 'ru'
            return response
    response = aiohttp_jinja2.render_template('login.jinja2', request, {})
    response.headers['Content-Language'] = 'ru'
    return response
