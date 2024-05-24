from enum import Enum

class Status(Enum):
    BOOKED = 'reservado'
    CHECKEDOUT = 'retirado'
    RETURNED = 'devolvido'
    CANCELED = 'cancelado'
    EXPIRED = 'expirado'
    
def validate_status_enum(status):
    if status == 'reservado': return Status.BOOKED
    elif status == 'retirado': return Status.CHECKEDOUT
    elif status == 'devolvido': return Status.RETURNED
    elif status == 'cancelado': return Status.CANCELED
    elif status == 'expirado': return Status.EXPIRED
    else: return None