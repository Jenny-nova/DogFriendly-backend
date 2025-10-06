from db import SessionLocal, engine, Base
from models import Place

Base.metadata.create_all(bind=engine)

db = SessionLocal()

places = [
    Place(name="Restaurante Patitas Felices", address="Calle Mayor 1", city="Bilbao", country="España"),
    Place(name="Café Peludo", address="Plaza Nueva 5", city="Bilbao", country="España"),
    Place(name="La Huella", address="Calle del Sol 10", city="Madrid", country="España"),
    Place(name="Perrito Feliz", address="Avenida Libertad 20", city="Sevilla", country="España"),
]

db.add_all(places)
db.commit()
db.close()

print("Datos de ejemplo insertados correctamente.")