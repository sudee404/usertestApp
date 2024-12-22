from .base_model import GenericBaseModel

class Status(GenericBaseModel):
    def __str__(self):
        return self.name