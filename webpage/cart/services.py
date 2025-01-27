from typing import List

from flask_login import current_user

from webpage.adapters.db_methods.db_repository import SqlAlchemyRepository
from webpage.domain_model.domain_model import Cart, CartItem, Cologne, db
import webpage.adapters.repository as repo

from flask import abort

from webpage import db

repo.repo_instance = SqlAlchemyRepository(db.session)



