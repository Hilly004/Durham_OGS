from fastapi import APIRouter, HTTPException

from Utilities.Observatory_Logger import ObservatoryLogger


router = APIRouter(
    prefix="/api/activity",
    tags=["activity"]
)


logger: ObservatoryLogger | None = None


def set_logger(
    activity_logger: ObservatoryLogger
):
    global logger
    logger = activity_logger


def get_logger() -> ObservatoryLogger:

    if logger is None:
        raise HTTPException(
            status_code=503,
            detail="Activity logger unavailable"
        )

    return logger


@router.get("")
def get_activity(limit: int = 100):

    activity_logger = get_logger()

    messages = activity_logger.get_messages(
        limit=min(max(limit, 1), 500)
    )

    return {
        "success": True,
        "data": [
            {
                "id": index,
                "timestamp": entry.timestamp.isoformat(),
                "level": entry.level.lower(),
                "source": entry.source,
                "message": entry.message
            }
            for index, entry in enumerate(messages)
        ]
    }


@router.delete("")
def clear_activity():

    activity_logger = get_logger()

    activity_logger.clear_messages()

    return {
        "success": True
    }