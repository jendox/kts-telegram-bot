from data_service.web.app import Request


async def get_random_question(request: Request):
    accessor = request.app.store
