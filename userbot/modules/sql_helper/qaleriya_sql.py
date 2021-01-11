import threading
from sqlalchemy import func, distinct, Column, String, Integer, UnicodeText
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError


class Qaleriya(BASE):
    __tablename__ = "qaleriya"
    
    g_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    foto = Column(UnicodeText, nullable=False)

    def __init__(self, foto):
        self.foto = foto

    def __repr__(self):
        return "<Qaleriya '%s' için %s>" % (self.g_id, self.foto)

    def __eq__(self, other):
        return bool(isinstance(other, Qaleriya)
            and self.foto == other.foto
            and self.g_id == other.g_id)


Qaleriya.__table__.create(checkfirst=True)

KOMUT_INSERTION_LOCK = threading.RLock()
TUM_QALERIYA = SESSION.query(Qaleriya).all()

def ekle_foto(foto):
    with KOMUT_INSERTION_LOCK:
        try:
            SESSION.query(Qaleriya).filter(Qaleriya.foto == foto).delete()
        except:
            pass

        ekleme = Qaleriya(foto)
        SESSION.merge(ekleme)
        SESSION.commit()


def getir_foto():
    global TUM_QALERIYA
    TUM_QALERIYA = SESSION.query(Qaleriya).all()

def sil_foto(gid):
    try:
        SESSION.query(Qaleriya).filter(Qaleriya.g_id == gid).delete()
        SESSION.commit()
    except Exception as e:
        return e
    return True
