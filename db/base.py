from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__[1:]
        _name = cls.__name__[0]
        for i in name:
            if i.isupper():
                _name += '_'
            _name += i
        _name = _name.lower()

        if _name.endswith('y'):
            _name = _name[:-1] + 'ie'
        return _name + 's'

