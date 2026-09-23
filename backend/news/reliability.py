from datetime import timedelta
from django.utils import timezone


def calculate_recency_score(published_at):
    if not published_at:
        return 30

    now = timezone.now()
    age = now - published_at

    if age < timedelta(hours=12):
        return 100

    elif age < timedelta(hours=24):
        return 95

    elif age < timedelta(days=3):
        return 90

    elif age < timedelta(days=5):
        return 80

    elif age < timedelta(days=7):
        return 70

    elif age < timedelta(days=14):
        return 50

    else:
        return 30


def calculate_reliability(
    source_score,
    evidence_score,
    independent_sources_score,
    stage_score,
    recency_score,
    contradiction_score,
):
    score = (
        source_score * 0.25
        + evidence_score * 0.25
        + independent_sources_score * 0.20
        + stage_score * 0.15
        + recency_score * 0.10
        + contradiction_score * 0.05
    )

    return round(score)

def calculate_rumour_reliability(
    rumour,
    source_score,
    evidence_score,
    independent_sources_score,
    stage_score,
    contradiction_score,
):
    recency_score = calculate_recency_score(
        rumour.published_at
    )

    return calculate_reliability(
        source_score=source_score,
        evidence_score=evidence_score,
        independent_sources_score=independent_sources_score,
        stage_score=stage_score,
        recency_score=recency_score,
        contradiction_score=contradiction_score,
    )

def calculate_source_reliability(source):
    # No historical results yet
    if source.total_rumours == 0:
        return source.initial_reliability

    confirmed = source.confirmed_rumours
    failed = source.failed_rumours

    resolved = confirmed + failed

    # No resolved rumours yet
    if resolved == 0:
        return source.initial_reliability

    success_rate = confirmed / resolved

    # Convert success rate to a 0-100 score
    historical_score = success_rate * 100

    # Blend initial belief with historical performance
    score = (
        source.initial_reliability * 0.30
        + historical_score * 0.70
    )

    return round(score, 2)

def calculate_evidence_score(ai_result):
    confidence = ai_result.get("confidence", 0)

    if not ai_result.get("evidence"):
        return 30

    return min(max(confidence, 0), 100)

def calculate_stage_score(stage):
    stage_scores = {
        "linked": 40,
        "interested": 50,
        "in talks": 60,
        "negotiation": 65,
        "bid": 75,
        "offer": 75,
        "agreement": 90,
        "medical": 95,
        "completed": 100,
    }

    if not stage:
        return 30

    return stage_scores.get(stage.lower(), 30)

def calculate_independent_sources_score(claim):
    if not claim:
        return 0

    rumours = claim.rumours.select_related("source")

    # Count unique non-official sources
    source_ids = set()

    for rumour in rumours:
        if rumour.source.source_type != "OFFICIAL":
            source_ids.add(rumour.source.id)

    source_count = len(source_ids)

    if source_count == 0:
        return 0

    if source_count == 1:
        return 40

    if source_count == 2:
        return 70

    if source_count == 3:
        return 85

    return 100

def calculate_contradiction_score(claim):
    if not claim:
        return 100

    rumours = claim.rumours.all()

    if not rumours.exists():
        return 100

    stages = set()

    for rumour in rumours:
        if rumour.transfer_stage:
            stages.add(rumour.transfer_stage.lower())

    # No meaningful disagreement
    if len(stages) <= 1:
        return 100

    # Some disagreement
    if len(stages) == 2:
        return 70

    # Significant disagreement
    if len(stages) == 3:
        return 40

    # Many conflicting reports
    return 20

def calculate_claim_reliability(
    claim,
    source_score,
    evidence_score,
    stage_score,
    contradiction_score,
):
    independent_sources_score = calculate_independent_sources_score(
        claim
    )

    recency_scores = []

    for rumour in claim.rumours.all():
        recency_scores.append(
            calculate_recency_score(
                rumour.published_at
            )
        )

    if recency_scores:
        recency_score = max(recency_scores)
    else:
        recency_score = 30

    return calculate_reliability(
        source_score=source_score,
        evidence_score=evidence_score,
        independent_sources_score=independent_sources_score,
        stage_score=stage_score,
        recency_score=recency_score,
        contradiction_score=contradiction_score,
    )

def calculate_claim_source_score(claim):
    if not claim:
        return 50

    scores = []

    for rumour in claim.rumours.select_related("source"):
        if rumour.source.source_type != "OFFICIAL":
            scores.append(
                calculate_source_reliability(
                    rumour.source
                )
            )

    if not scores:
        return 50

    return sum(scores) / len(scores)

def update_claim_reliability(claim):
    if not claim:
        return None

    source_score = calculate_claim_source_score(claim)

    rumours = claim.rumours.all()

    if not rumours.exists():
        return None

    # Use the strongest evidence currently available
    latest_rumour = rumours.order_by("-published_at").first()

    evidence_score = calculate_evidence_score({
        "confidence": latest_rumour.probability,
        "evidence": latest_rumour.evidence,
    })

    stage_score = calculate_stage_score(
        latest_rumour.transfer_stage
    )

    contradiction_score = calculate_contradiction_score(
        claim
    )

    final_score = calculate_claim_reliability(
        claim=claim,
        source_score=source_score,
        evidence_score=evidence_score,
        stage_score=stage_score,
        contradiction_score=contradiction_score,
    )

    claim.reliability_score = final_score
    claim.save(
        update_fields=["reliability_score", "updated_at"]
    )

    return final_score