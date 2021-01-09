from typing import Any
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from restaurant.backend.db import create_session, UserReserve

app = FastAPI()
templates = Jinja2Templates(directory='restaurant/frontend/html')
app.mount('/css', StaticFiles(directory="restaurant/frontend/css"), name="static")
app.mount('/images', StaticFiles(directory="restaurant/frontend/images"), name="static")
app.mount('/js', StaticFiles(directory="restaurant/frontend/js"), name="static")


@app.get('/')
async def get_main_page(request: Request) -> Any:
    """
    Эндпоинт, по которому возвращается главная страница сайта.
    """
    return templates.TemplateResponse(
        'main-page.html', {'request': request}
    )


@app.get('/reservation')
async def get_reservation_page(request: Request) -> Any:
    """
    Эндпоинт, по которому возвращается страница с формой бронирования столика.
    """
    return templates.TemplateResponse(
        'reservation.html', {'request': request}
    )


@app.post('/reservation-action')
async def do_reservation(request: Request) -> Any:
    """
    Обработка данных из формы, проверка возможности забронировать стол.
    Если успешно, то в базу попадает запись с данными формы и пользователю сообщается об успешном бронировании.
    Если в базе есть запись брони с той же датой и номером столика, то пользователю сообщается о том, что бронь
    не прошла и рекомендуется попробовать перебронировать.
    """
    data_from_form = dict(await request.form())
    with create_session() as session:
        check_available_table = session.query(UserReserve).filter(data_from_form.get('date') == UserReserve.date)\
            .filter(data_from_form.get('table') == UserReserve.table_number).first()

        if check_available_table is not None:
            return templates.TemplateResponse(
                'reservation.html', {'request': request, 'result': "Столик на эту дату уже занят, попробуйте другую."}
            )
        else:
            session.add(UserReserve(data_from_form.get('name'), data_from_form.get('phone'),
                                    data_from_form.get('mail'), data_from_form.get('date'), data_from_form.get('table')))
            return templates.TemplateResponse(
                'reservation.html', {'request': request, 'result': "Столик успешно забронирован, ждем вас!"}
            )


@app.get('/menu')
async def get_menu_page(request: Request) -> Any:
    """
    Эндпоинт, по которому возвращается страница с меню.
    """
    return templates.TemplateResponse(
        'menu.html', {'request': request}
    )


@app.get('/about')
async def get_about_page(request: Request) -> Any:
    """
    Эндпоинт, по которому возвращается страница с информацией о ресторане.
    """
    return templates.TemplateResponse(
        'about.html', {'request': request}
    )
