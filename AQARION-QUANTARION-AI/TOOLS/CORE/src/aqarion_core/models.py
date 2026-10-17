from dataclasses import dataclass, field
from typing import Dict, List

from .status import Status


@dataclass(frozen=True)
class EvidenceRecord:
    kind: str
    reference: str
    verified: bool = False


@dataclass
class Claim:
    claim_id: str
    statement: str
    status: Status = Status.OPEN
    dependencies: List[str] = field(default_factory=list)
    evidence: List[EvidenceRecord] = field(default_factory=list)
    provenance: Dict[str, str] = field(default_factory=dict)
