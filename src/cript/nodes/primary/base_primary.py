from cript.nodes.base import Base


class BasePrimary(Base):
    slug = None
    required = None
    unique_together = None
