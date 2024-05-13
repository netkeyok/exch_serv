from datetime import datetime, timezone

from api_models.Supermag import OR
from api_models.Cleverence.Postuplenie import Postuplenie, DocumentItem
from api_requests.Send_to_CV import send_request
from api_requests.get_from_sm import get_mesabbrev
from config_urls import postuplenie_url



