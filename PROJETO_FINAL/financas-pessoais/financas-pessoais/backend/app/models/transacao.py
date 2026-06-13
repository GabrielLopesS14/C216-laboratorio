from sqlalchemy import (
    Column, Integer, String, Numeric, Date, ForeignKey, Table,
)
from sqlalchemy.orm import relationship

from app.database import Base



#Tabela de associacao que materializa o relacionamento
#N:M entre TRANSACOES e TAGS.
transacao_tags = Table(
    "transacao_tags",
    Base.metadata,
    Column("transacao_id", Integer, ForeignKey("transacoes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)            # 'receita' ou 'despesa'

    # Chaves estrangeiras — o lado "N" dos relacionamentos N:1.
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    # Relacionamentos N:1
    conta = relationship("Conta", back_populates="transacoes")
    categoria = relationship("Categoria", back_populates="transacoes")

    # Relacionamento N:M (atraves da tabela de juncao)
    tags = relationship(
        "Tag",
        secondary=transacao_tags,
        back_populates="transacoes",
    )
