"""Optional cited context. Neighboring text is not adjudicated support."""
import retrieve


def _identity(item):
    return (
        item["path"], item["commit_sha"],
        item["char_start"], item["char_end"],
    )


def _paragraphs(entry, text):
    records = []
    offset = 0
    for raw in text.split(retrieve.PARA_BREAK):
        passage = raw.strip()
        start = offset + len(raw) - len(raw.lstrip())
        if passage:
            records.append({
                "doc": entry["doc"],
                "path": entry["path"],
                "commit_sha": entry["sha"],
                "char_start": start,
                "char_end": start + len(passage),
                "passage": passage,
            })
        offset += len(raw) + len(retrieve.PARA_BREAK)
    return records


def _expand_context(seeds):
    if len(seeds) > 3:
        raise ValueError("Context expansion accepts at most three seeds")
    if len({_identity(seed) for seed in seeds}) != len(seeds):
        raise ValueError("Duplicate seed citation")
    for rank, seed in enumerate(seeds, 1):
        if seed["rank"] != rank:
            raise ValueError("Seed ranks must be consecutive and one-based")

    entries = {}
    if seeds:
        for entry in retrieve.load_manifest():
            source = (entry["path"], entry["sha"])
            if source in entries:
                raise ValueError("Duplicate manifest source")
            entries[source] = entry

    documents = {}
    positions = {}
    for seed in seeds:
        source = (seed["path"], seed["commit_sha"])
        if source not in entries:
            raise ValueError("Seed source is not in the pinned manifest")
        if seed.get("doc") != entries[source]["doc"]:
            raise ValueError("Seed document label does not match manifest")
        if source not in documents:
            text = retrieve.load_at_sha(*source)
            records = _paragraphs(entries[source], text)
            documents[source] = records
            positions[source] = {
                _identity(record): index
                for index, record in enumerate(records)
            }
        index = positions[source].get(_identity(seed))
        if index is None:
            raise ValueError("Seed does not identify an exact source paragraph")
        if documents[source][index]["passage"] != seed["passage"]:
            raise ValueError("Seed passage does not reconstruct")

    seed_ids = {_identity(seed) for seed in seeds}
    supplements = {}
    for seed in seeds:
        source = (seed["path"], seed["commit_sha"])
        records = documents[source]
        index = positions[source][_identity(seed)]
        for delta, direction in ((-1, "previous"), (1, "following")):
            neighbor_index = index + delta
            if not 0 <= neighbor_index < len(records):
                continue
            neighbor = records[neighbor_index]
            key = _identity(neighbor)
            if key in seed_ids:
                continue
            if key not in supplements:
                supplements[key] = {
                    **neighbor,
                    "context_only": True,
                    "seed_links": [],
                }
            supplements[key]["seed_links"].append({
                "seed_rank": seed["rank"],
                "seed_char_start": seed["char_start"],
                "seed_char_end": seed["char_end"],
                "direction": direction,
            })

    extra = list(supplements.values())
    if len(extra) > 6:
        raise RuntimeError("Supplementary passage budget exceeded")

    return {
        "seed_results": seeds,
        "supplementary_context": extra,
        "expansion_metadata": {
            "rule": "immediate_nonempty_neighbors_v1",
            "seed_top_k": 3,
            "previous_paragraphs": 1,
            "following_paragraphs": 1,
            "recursive": False,
            "maximum_supplements": 6,
            "seed_count": len(seeds),
            "supplementary_count": len(extra),
            "seed_characters": sum(len(item["passage"]) for item in seeds),
            "supplementary_characters": sum(
                len(item["passage"]) for item in extra
            ),
            "support_adjudicated": False,
        },
    }


def retrieve_with_context(query, source_id=None):
    """Keep top-three cited search unchanged; return neighbors separately.

    Offsets are half-open decoded-text positions, not byte offsets.
    Supplement order follows seed rank, then previous/following direction.
    Expansion is nonrecursive and confined to each seed's pinned source.
    """
    if source_id is None:
        return _expand_context(retrieve.retrieve_cited(query, top_k=3))
    entry = retrieve.resolve_source_id(source_id)
    seeds = retrieve.retrieve_cited(query, top_k=3, source_id=source_id)
    expected = (entry["path"], entry["sha"])
    if any((s["path"], s["commit_sha"]) != expected for s in seeds):
        raise ValueError("Scoped seed crossed source boundary")
    return _expand_context(seeds)
