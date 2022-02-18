from fastapi import APIRouter, Depends, BackgroundTasks, status
from pydantic import UUID4

from app.api.schemas import DefaultSuccessResponse
from app.api.v1.schemas import FilmProgressInputSchema
from app.services.progress import ProgressService, get_progress_service

router = APIRouter()


@router.post(
    "/films/{film_id}/",
    responses={
        status.HTTP_202_ACCEPTED: {"model": DefaultSuccessResponse},
    },
    status_code=status.HTTP_202_ACCEPTED,
    description="Receives a message with the progress of watching a "
    "movie and reload it into the analytical storage.",
)
async def send_film_progress(
    film_id: UUID4,
    film_progress: FilmProgressInputSchema,
    background_tasks: BackgroundTasks,
    progress_service: ProgressService = Depends(get_progress_service),
):
    background_tasks.add_task(progress_service.send_to_topic, film_id, film_progress)
    return DefaultSuccessResponse()
