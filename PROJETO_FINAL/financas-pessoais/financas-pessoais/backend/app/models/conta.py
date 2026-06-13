from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship

from app.database import Base

class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)            #ex: corrente, carteira, poupanca
    saldo_inicial = Column(Numeric(10, 2), default=0)

    transacoes = relationship("Transacao", back_populates="conta")
