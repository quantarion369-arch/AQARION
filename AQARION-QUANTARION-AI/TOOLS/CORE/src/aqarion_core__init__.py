
### `src/aqarion_core/__init__.py`

```python
from .models import Claim, EvidenceRecord
from .status import Status
from .audit import audit_claim

__all__ = ["Claim", "EvidenceRecord", "Status", "audit_claim"]
