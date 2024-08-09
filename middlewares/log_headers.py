from fastapi import Request


async def log_headers(request: Request, call_next):
    print(f"Headers: {request.headers}")
    response = await call_next(request)
    return response
