from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models

class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def get_or_create(self, session, model, filter_field, data):
        # instance = session.query(model).filter_by(**{filter_field:data[filter_field]}).first() # первый вариант фильтрации
        instance = session.query(model).filter(getattr(model, filter_field) == data[filter_field]).first() # второй вариант фильтрации (getattr - возврат значения атриута)
        if not instance:
            instance = model(**data)
        return instance

    def add_post(self, data):
        session = self.maker()
        post = self.get_or_create(session, models.Post, 'id', data['post_data']) # вариант для 3-го урока
        # post = models.Post(**data['post_data']) # вариант для 2-го урока
        author = self.get_or_create(session, models.Author, 'url', data['author_data']) # вариант для 3-го урока
        author = models.Author(**data['author_data']) # вариант для 2-го урока
        post.author = author
        session.add(post)
        try:
            session.commit()
        except Exception:
            session.rollback()
        session.close()