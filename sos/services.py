"""
Emergency notification dispatch.

In this prototype, `notify_emergency_contacts` just logs what it *would*
send. Wire in Twilio once you have credentials:

    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=contact.phone_number, from_=settings.TWILIO_FROM_NUMBER, body=body)

Kept as a separate service (not called directly from the view) so it can
later be swapped for a Celery task without touching SOSIncidentViewSet.
"""
import logging

from django.conf import settings

logger = logging.getLogger("railoo.sos")


def notify_emergency_contacts(incident) -> int:
    contacts = incident.user.emergency_contacts.all()
    body = (
        f"RAILOO SOS: {incident.user.get_full_name() or incident.user.username} "
        f"triggered a {incident.get_incident_type_display()} alert on {incident.get_mode_of_transport_display()}. "
        f"Location: {incident.latitude},{incident.longitude}"
    )

    sent = 0
    for contact in contacts:
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            # Real send would happen here once Twilio creds are configured.
            logger.info("Would SMS %s (%s): %s", contact.name, contact.phone_number, body)
        else:
            logger.info("[DEV, no Twilio configured] Would SMS %s: %s", contact.phone_number, body)
        sent += 1

    return sent
