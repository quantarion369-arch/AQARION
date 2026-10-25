import torch
from torch import nn
from torch.autograd import gradcheck

torch.set_num_threads(1)


class CandidateDefectLoss(nn.Module):
    """
    Experimental finite-state defect loss.
    Uses a supplied transition operator, not a learned one.
    """

    def __init__(self, ridge=1e-4):
        super().__init__()
        if ridge < 0:
            raise ValueError("ridge must be nonnegative")
        self.ridge = ridge

    def forward(self, assignments, koopman):
        if assignments.ndim != 2:
            raise ValueError(
                "assignments must have shape [states, clusters]"
            )

        n, clusters = assignments.shape

        if n == 0 or clusters == 0:
            raise ValueError("assignments cannot be empty")

        if koopman.shape != (n, n):
            raise ValueError(
                "koopman must have shape [states, states]"
            )

        cluster_eye = torch.eye(
            clusters,
            dtype=assignments.dtype,
            device=assignments.device,
        )

        state_eye = torch.eye(
            n,
            dtype=assignments.dtype,
            device=assignments.device,
        )

        gram = assignments.T @ assignments

        coefficients = torch.linalg.solve(
            gram + self.ridge * cluster_eye,
            assignments.T,
        )

        projection = assignments @ coefficients
        defect = (state_eye - projection) @ koopman @ projection

        return defect.square().mean()


# Four-state cycle: 0 -> 1 -> 2 -> 3 -> 0.
dtype = torch.float64
successors = torch.tensor([1, 2, 3, 0])
koopman = torch.eye(4, dtype=dtype)[successors]


def hard_assignments(labels):
    indices = torch.tensor(labels, dtype=torch.long)
    return torch.nn.functional.one_hot(indices).to(dtype=dtype)


hard_loss = CandidateDefectLoss(ridge=0.0)

# Closed nontrivial partition.
closed = hard_loss(
    hard_assignments([0, 1, 0, 1]),
    koopman,
)
assert abs(closed.item()) < 1e-12
print("CLOSED_PARTITION_ZERO_DEFECT=PASS")

# Nonclosed partition.
nonclosed = hard_loss(
    hard_assignments([0, 0, 1, 1]),
    koopman,
)
assert nonclosed.item() > 1e-12
print("NONCLOSED_PARTITION_POSITIVE_DEFECT=PASS")

# Zero defect alone does not exclude trivial partitions.
for labels in ([0, 0, 0, 0], [0, 1, 2, 3]):
    result = hard_loss(hard_assignments(labels), koopman)
    assert abs(result.item()) < 1e-12
print("TRIVIAL_PARTITION_LIMITATION_CONFIRMED=PASS")

# Differentiable soft assignments.
torch.manual_seed(369)

logits = torch.randn(
    4, 2,
    dtype=dtype,
    requires_grad=True,
)

soft_loss = CandidateDefectLoss(ridge=1e-4)


def objective(values):
    assignments = values.softmax(dim=-1)
    return soft_loss(assignments, koopman)


value = objective(logits)
gradient, = torch.autograd.grad(value, logits)

assert torch.isfinite(value).item()
assert torch.isfinite(gradient).all().item()
assert gradient.norm().item() > 1e-12
print("FINITE_NONZERO_GRADIENT=PASS")

gradient_check_passed = gradcheck(
    objective,
    (logits,),
    eps=1e-6,
    atol=1e-5,
    rtol=1e-3,
)
assert gradient_check_passed
print("FINITE_DIFFERENCE_GRADCHECK=PASS")

print()
print("SOFT_DEFECT_LOSS:", value.item())
print("GRADIENT_NORM:", gradient.norm().item())
print("CANDIDATE_SMOKE_TEST=PASS")
print("MODEL_TRAINING=NOT_STARTED")
print("HUGGING_FACE_FILES_CHANGED=NO")