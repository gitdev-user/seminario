from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EntidadBase(BaseModel):
    """Representa una entidad base con su identificador."""
    
    id: int = Field(default=0, description="Identificador único de la entidad")
