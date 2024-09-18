from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from locallibrary_frontend.db import gen_dbsession

DbSession = Annotated[Session, Depends(gen_dbsession)]
