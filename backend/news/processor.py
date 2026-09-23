from transfers.models import (
    Club,
    Player,
    TransferClaim,
    TransferRumour,
)
from news.models import Source
from news.ai_processor import extract_transfer_info
from news.reliability import update_claim_reliability


def get_or_create_club(name, country="Unknown"):
    if not name:
        return None

    club, created = Club.objects.get_or_create(
        name=name,
        defaults={
            "country": country
        }
    )

    return club


def get_or_create_player(name, current_club):
    if not name:
        return None

    player, created = Player.objects.get_or_create(
        name=name,
        defaults={
            "age": 0,
            "position": "Unknown",
            "current_club": current_club,
        }
    )

    return player

def get_or_create_transfer_claim(player, destination_club):
    if not player or not destination_club:
        return None

    claim, created = TransferClaim.objects.get_or_create(
        player=player,
        destination_club=destination_club
    )

    return claim

def create_transfer_rumour(article, ai_result, claim, source):
    if not claim or not source:
        return None

    article_url = article.get("link")

    if not article_url:
        return None

    # Prevent duplicate articles
    if TransferRumour.objects.filter(article_url=article_url).exists():
        return None

    rumour = TransferRumour.objects.create(
        claim=claim,
        source=source,
        from_club=claim.player.current_club,
        to_club=claim.destination_club,
        transfer_stage=ai_result.get("transfer_stage"),
        article_title=article.get("title"),
        article_url=article_url,
        published_at=article.get("published_at"),
        evidence=ai_result.get("evidence"),
        probability=ai_result.get("confidence", 0),
    )

    return rumour


def process_article(article):
    # Find the Source database record
    source = get_or_create_source(article.get("source"))

    if not source:
        return None

    ai_result = extract_transfer_info(article)

    # Ignore articles that are not genuine transfer reports
    if not ai_result.get("is_transfer_rumour"):
        return None

    # Ignore low-confidence AI results
    if ai_result.get("confidence", 0) < 60:
        return None

    player_name = ai_result.get("player_name")
    current_club_name = ai_result.get("current_club")
    destination_club_name = ai_result.get("destination_club")

    if not player_name or not destination_club_name:
        return None

    # Find/create destination club
    destination_club = get_or_create_club(destination_club_name)

    # Find/create current club
    current_club = get_or_create_club(current_club_name)

    # Find/create player
    player = get_or_create_player(
        player_name,
        current_club
    )

    if not player:
        return None

    # Find/create transfer claim
    claim = get_or_create_transfer_claim(
        player,
        destination_club
    )

        # Create individual rumour
    rumour = create_transfer_rumour(
        article,
        ai_result,
        claim,
        source
    )

    if rumour:
        update_claim_reliability(claim)

    return rumour

    return rumour

def get_or_create_source(source_name):
    if not source_name:
        return None

    source, created = Source.objects.get_or_create(
        name=source_name,
        defaults={
            "url": "",
            "source_type": "MEDIA",
        }
    )

    return source