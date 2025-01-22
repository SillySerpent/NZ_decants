from abc import ABC
from typing import Type

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from webpage.adapters.repository import AbstractRepository
from webpage.domain_model.domain_model import Cologne, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Cologne data
    def get_all_colognes(self, sorting: bool = False) -> list[Type[Cologne]]:
        """Retrieve all colognes from the database, optionally sorting by price."""
        query = self._session_cm.session.query(Cologne)
        if sorting:
            query = query.order_by(Cologne.price.asc())
        return query.all()

    def get_cologne_by_id(self, cologne_id: int) -> Type[Cologne] | None:
        """Retrieve a specific cologne by its ID."""
        cologne = None
        try:
            query = self._session_cm.session.query(Cologne).filter(Cologne.id == cologne_id)
            cologne = query.one()
        except NoResultFound:
            print(f'Cologne with ID {cologne_id} was not found.')
        return cologne

    def get_colognes_by_season(self, season: str) -> list[Type[Cologne]]:
        """Retrieve colognes matching a specific season."""
        return self._session_cm.session.query(Cologne).filter(Cologne.season.ilike(f'%{season}%')).all()

    def get_colognes_by_category(self, category: str) -> list[Type[Cologne]]:
        """Retrieve colognes matching a specific category."""
        return self._session_cm.session.query(Cologne).filter(Cologne.category.ilike(f'%{category}%')).all()

    def get_featured_colognes(self) -> list[Type[Cologne]]:
        """Retrieve all featured colognes."""
        return self._session_cm.session.query(Cologne).filter(Cologne.featured.is_(True)).all()

    def add_cologne(self, cologne: Cologne):
        """Add or update a cologne in the database."""
        with self._session_cm as scm:
            scm.session.merge(cologne)
            scm.commit()

    def add_multiple_colognes(self, colognes: list[Type[Cologne]]):
        """Add multiple colognes to the database."""
        with self._session_cm as scm:
            for cologne in colognes:
                scm.session.add(cologne)
            scm.commit()

    def search_cologne_by_name(self, name: str) -> list[Type[Cologne]]:
        """Search for colognes by their name (case-insensitive partial match)."""
        query = self._session_cm.session.query(Cologne).filter(Cologne.name.ilike(f'%{name}%'))
        return query.all()

    def filter_colognes_by_price(self, min_price: float, max_price: float) -> list[Type[Cologne]]:
        """Retrieve colognes within a specific price range."""
        return self._session_cm.session.query(Cologne).filter(
            Cologne.price.between(min_price, max_price)
        ).all()

    def get_number_of_colognes(self) -> int:
        """Get the total number of colognes in the database."""
        return self._session_cm.session.query(Cologne).count()

    def get_colognes_by_availability(self) -> list[Type[Cologne]]:
        """Retrieve all colognes currently available."""
        return self._session_cm.session.query(Cologne).filter(Cologne.availability.is_(True)).all()
    # endregion

    # region Reviews (assuming there’s a Review model for colognes)
    def add_review(self, review: Review):
        """Add a new review to the database."""
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews_by_cologne_id(self, cologne_id: int) -> list[Type[Review]]:
        """Retrieve all reviews for a specific cologne."""
        return self._session_cm.session.query(Review).filter(Review.cologne_id == cologne_id).all()

    def get_average_rating_for_cologne(self, cologne_id: int) -> float:
        """Calculate the average rating for a cologne."""
        ratings = self._session_cm.session.query(Review.rating).filter(Review.cologne_id == cologne_id).all()
        if ratings:
            return sum(r[0] for r in ratings) / len(ratings)
        return 0
    # endregion

    # region Filtering by attributes
    def filter_colognes_by_notes(self, note: str) -> list[Type[Cologne]]:
        """Retrieve colognes that contain a specific note."""
        return self._session_cm.session.query(Cologne).filter(Cologne.notes.like(f'%{note}%')).all()

    def get_colognes_by_sex(self, sex: str) -> list[Type[Cologne]]:
        """Retrieve colognes targeted for a specific sex (e.g., 'male', 'female', 'unisex')."""
        return self._session_cm.session.query(Cologne).filter(Cologne.sex.ilike(f'%{sex}%')).all()
    # endregion


