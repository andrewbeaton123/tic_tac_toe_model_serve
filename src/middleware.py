import time
from fastapi import Request
from loguru import logger

async def log_request_performance(request: Request, call_next):
    start_time = time.time()
    response = None
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request processing failed: {e}", exc_info=True)
        raise
    finally:
        duration = time.time() - start_time
        status_code = response.status_code if response and hasattr(response, 'status_code') else 500
        logger.info({
            "path": request.url.path,
            "method": request.method,
            "status_code": status_code,
            "duration_ms": int(duration * 1000)
        })
    return response
