from .upload import router as upload_post_router
from .home import router as home_router
from .bulk_action import router as bulk_action_router
from .move_to_bin import router as move_to_bin_router
from .restore import router as restore_router
from .bin import router as bin_router
from .single_manual_final_deleteon import router as single_manual_final_deleteon_router
from .transcribe import router as transcribe_router
from .go_transcribation import router as go_transcribatrion_router
from .update_segment import router as update_segment_router
from .fetch_status import router as fetch_status_router
from .download_file import router as download_file_router


all_routers = [
    upload_post_router,
    home_router,
    # deleteon_router,
    single_manual_final_deleteon_router,
    bulk_action_router,
    move_to_bin_router,
    restore_router,
    bin_router,
    transcribe_router,
    go_transcribatrion_router,
    update_segment_router,
    fetch_status_router,
    download_file_router,


]


