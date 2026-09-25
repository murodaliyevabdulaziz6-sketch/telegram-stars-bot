from .start import router as start_router
from .referral import router as referral_router
from .profile import router as profile_router
from .leaderboard import router as leaderboard_router
from .help import router as help_router
from .admin import router as admin_router

routers = [
    start_router,
    referral_router,
    profile_router,
    leaderboard_router,
    help_router,
    admin_router,
]

__all__ = ["routers"]
