from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        _name = cls.__name__[:1]
        for i in _name:
            if i.isupper():
                _name += '_'
            _name += i
        _name = _name.lower()

        if _name.endswith('y'):
            _name = _name[:-1] + 'ies'
        return _name + 's'

