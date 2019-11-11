import logging
from uuid import uuid4

from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from pyxb import (
    IncompleteElementContentError,
    UnprocessedElementContentError,
    UnprocessedKeywordContentError,
)

from camac.constants.kt_bern import INSTANCE_STATE_EBAU_NUMMER_VERGEBEN
from camac.core.models import Activation

from .data_preparation import get_document
from .formatters import (
    accompanying_report,
    change_responsibility,
    delivery,
    request,
    status_notification,
    submit,
)
from .models import Message
from .signals import instance_submitted, sb1_submitted, sb2_submitted

logger = logging.getLogger(__name__)


class BaseEventHandler:
    def __init__(self, instance, group_pk=None):
        self.instance = instance
        self.group_pk = group_pk

        self.message_date = timezone.now()
        self.message_id = uuid4()

    def get_data(self):
        return get_document(self.instance.pk)

    def get_xml(self, data):  # pragma: no cover
        raise NotImplementedError()

    def create_message(self, xml, receiver=None):
        receiver = receiver if receiver else self.instance.active_service
        message = Message.objects.create(
            body=xml,
            receiver=receiver,
            created_at=self.message_date,
            id=self.message_id,
        )
        return message

    def run(self):
        data = self.get_data()
        xml = self.get_xml(data)
        return self.create_message(xml)


class SubmitEventHandler(BaseEventHandler):
    event_type = "submit"
    uri_instance_resource_id = 20014

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                url=f"{settings.INTERNAL_BASE_URL}/form/edit-page/instance-resource-id/{self.uri_instance_resource_id}/instance-id/{self.instance.pk}",
                eventSubmitPlanningPermissionApplication=submit(
                    self.instance, data, self.event_type
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class FileSubsequentlyEventHandler(BaseEventHandler):
    event_type = "file subsequently"
    uri_instance_resource_id = 40008

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                url=f"{settings.INTERNAL_BASE_URL}/form/edit-pages/instance-resource-id/40008/instance-id/{self.instance.pk}",
                eventSubmitPlanningPermissionApplication=submit(
                    self.instance, data, self.event_type
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class StatusNotificationEventHandler(BaseEventHandler):
    def get_data(self):
        return {"ech-subject": "status notification"}

    def get_xml(self, data):
        url = None
        if (
            self.instance.previous_instance_state.pk
            == INSTANCE_STATE_EBAU_NUMMER_VERGEBEN
        ):
            # send link to Dossierprüfung
            url = (
                f"{settings.INTERNAL_BASE_URL}/form/edit-pages/instance-resource-id/40008/instance-id/{self.instance.pk}",
            )
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                url=url,
                eventStatusNotification=status_notification(self.instance),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class WithdrawPlanningPermissionApplicationEventHandler(BaseEventHandler):
    event_type = "withdraw planning permission application"

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventRequest=request(self.instance, self.event_type),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class TaskEventHandler(WithdrawPlanningPermissionApplicationEventHandler):
    event_type = "task"

    def get_xml(self, data, activation_id):
        # send link to Stellungnahme abgeben
        url = (
            f"{settings.INTERNAL_BASE_URL}/circulation/edit-notice/instance-resource-id/20039/instance-id/{self.instance.pk}/activation-id/{activation_id}",
        )
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                url=url,
                eventRequest=request(self.instance, self.event_type),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise

    def run(self):
        msgs = []
        data = self.get_data()
        for a in Activation.objects.filter(
            circulation__instance=self.instance, ech_msg_created=False
        ):
            self.message_id = uuid4()
            xml = self.get_xml(data, a.pk)
            msgs.append(self.create_message(xml, a.service))
            a.ech_msg_created = True
            a.save()
        return msgs


class ClaimEventHandler(BaseEventHandler):
    event_type = "claim"

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                url=f"{settings.INTERNAL_BASE_URL}/claim/claim/index/instance-resource-id/150000/instance-id/{self.instance.pk}",
                eventRequest=request(self.instance, self.event_type),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class AccompanyingReportEventHandler(BaseEventHandler):
    event_type = "accompanying report"

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        attachments = self.instance.attachments.filter(attachment_sections__pk=7)
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventAccompanyingReport=accompanying_report(
                    self.instance, self.event_type, attachments
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class ChangeResponsibilityEventHandler(BaseEventHandler):
    event_type = "change responsibility"

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventChangeResponsibility=change_responsibility(self.instance),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


@receiver(instance_submitted)
def submit_callback(sender, instance, group_pk, **kwargs):
    if settings.ECH_API:
        handler = SubmitEventHandler(instance, group_pk)
        handler.run()


@receiver(sb1_submitted)
@receiver(sb2_submitted)
def send_status_notification(sender, instance, group_pk, **kwargs):
    if settings.ECH_API:
        handler = StatusNotificationEventHandler(instance, group_pk)
        handler.run()
