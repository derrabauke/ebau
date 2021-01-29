import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from caluma.caluma_workflow.models import Task
from django.core import mail
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.caluma.api import CalumaApi
from camac.constants import kt_bern as constants
from camac.instance.models import HistoryEntry


@pytest.fixture
def ebau_number_question(db, camac_question_factory, camac_chapter_factory):
    camac_question_factory(question_id=constants.QUESTION_EBAU_NR)
    camac_chapter_factory(chapter_id=constants.CHAPTER_EBAU_NR)


@pytest.mark.freeze_time("2020-12-03")
@pytest.mark.parametrize("role__name,instance_state__name", [("Municipality", "subm")])
@pytest.mark.parametrize(
    "ebau_number,expected_ebau_number,expected_error",
    [
        ("2020-2", "2020-2", None),
        ("", "2020-3", None),
        ("20-112", None, "Ungültiges Format"),
        (
            "2020-1",
            None,
            "Diese eBau-Nummer wurde durch eine andere Leitbehörde bereits vergeben",
        ),
        ("2020-112", None, "Diese eBau-Nummer existiert nicht"),
    ],
)
def test_set_ebau_number(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_service,
    instance_state,
    role,
    ebau_number_question,
    camac_answer_factory,
    instance_factory,
    instance_service_factory,
    instance_state_factory,
    service_factory,
    ebau_number,
    expected_ebau_number,
    expected_error,
):
    instance_state_factory(name="circulation_init")

    # create existing instance with ebau-number 2020-1 in a different municipality
    instance_other = instance_service_factory(service=service_factory()).instance
    camac_answer_factory(
        instance=instance_other,
        question_id=constants.QUESTION_EBAU_NR,
        chapter_id=constants.CHAPTER_EBAU_NR,
        answer="2020-1",
    )
    workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance_other.pk, "ebau-number": "2020-1"},
        user=caluma_admin_user,
    )

    # create existing instance with ebau-number 2020-2 with same municipality involved
    instance_same = instance_factory()
    instance_service_factory(
        service=instance.responsible_service(filter_type="municipality"),
        instance=instance_same,
        active=0,
    )
    camac_answer_factory(
        instance=instance_same,
        question_id=constants.QUESTION_EBAU_NR,
        chapter_id=constants.CHAPTER_EBAU_NR,
        answer="2020-2",
    )
    workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance_same.pk, "ebau-number": "2020-2"},
        user=caluma_admin_user,
    )

    # instance with different municipality but also ebau-nr 2020-2
    instance_indirect = instance_service_factory(service=service_factory()).instance
    camac_answer_factory(
        instance=instance_indirect,
        question_id=constants.QUESTION_EBAU_NR,
        chapter_id=constants.CHAPTER_EBAU_NR,
        answer="2020-2",
    )
    workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance_indirect.pk, "ebau-number": "2020-2"},
        user=caluma_admin_user,
    )

    # create case for the instance which will be assigned a new ebau number
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    # "submit" instance
    workflow_api.skip_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )

    response = admin_client.post(
        reverse("instance-set-ebau-number", args=[instance.pk]),
        {
            "data": {
                "type": "instance-set-ebau-numbers",
                "attributes": {"ebau-number": ebau_number},
            }
        },
    )

    if expected_error:
        result = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(result["errors"])
        assert expected_error == result["errors"][0]["detail"]
    else:
        case.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert case.meta["ebau-number"] == expected_ebau_number


@pytest.mark.freeze_time("2020-12-03")
@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status,caluma_workflow,instance_state__name,expected_instance_state,expect_completed_work_item",
    [
        (
            "Municipality",
            status.HTTP_204_NO_CONTENT,
            "building-permit",
            "subm",
            "circulation_init",
            True,
        ),
        (
            "Municipality",
            status.HTTP_204_NO_CONTENT,
            "preliminary-clarification",
            "subm",
            "circulation_init",
            True,
        ),
        (
            "Municipality",
            status.HTTP_204_NO_CONTENT,
            "internal",
            "in_progress_internal",
            "in_progress_internal",
            True,
        ),
        (
            "Municipality",
            status.HTTP_403_FORBIDDEN,
            "building-permit",
            "circulation_init",
            None,
            None,
        ),
        (
            "Support",
            status.HTTP_204_NO_CONTENT,
            "building-permit",
            "subm",
            "subm",
            False,
        ),
        (
            "Support",
            status.HTTP_204_NO_CONTENT,
            "preliminary-clarification",
            "subm",
            "subm",
            False,
        ),
        (
            "Support",
            status.HTTP_204_NO_CONTENT,
            "internal",
            "in_progress_internal",
            "in_progress_internal",
            False,
        ),
        (
            "Applicant",
            status.HTTP_403_FORBIDDEN,
            "building-permit",
            "subm",
            None,
            None,
        ),
    ],
)
def test_set_ebau_number_workflow(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_service,
    instance_state,
    role,
    ebau_number_question,
    instance_state_factory,
    expected_status,
    caluma_workflow,
    expected_instance_state,
    expect_completed_work_item,
):
    instance_state_factory(name="circulation_init")

    workflow = caluma_workflow_models.Workflow.objects.get(pk=caluma_workflow)
    case = workflow_api.start_case(
        workflow=workflow,
        form=workflow.allow_forms.first(),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    workflow_api.skip_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )

    response = admin_client.post(
        reverse("instance-set-ebau-number", args=[instance.pk]),
        {
            "data": {
                "type": "instance-set-ebau-numbers",
                "attributes": {"ebau-number": ""},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        case.refresh_from_db()
        instance.refresh_from_db()

        assert instance.instance_state.name == expected_instance_state
        assert case.meta["ebau-number"] == "2020-1"
        assert (
            case.work_items.filter(
                task_id="ebau-number",
                status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
            ).exists()
            == expect_completed_work_item
        )


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Support", status.HTTP_204_NO_CONTENT),
        ("Municipality", status.HTTP_403_FORBIDDEN),
    ],
)
def test_archive(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_service,
    role,
    instance_state_factory,
    expected_status,
):
    instance_state_factory(name="archived")
    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")

    case = workflow_api.start_case(
        workflow=workflow,
        form=workflow.allow_forms.first(),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    response = admin_client.post(reverse("instance-archive", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        case.refresh_from_db()
        instance.refresh_from_db()

        assert case.status == caluma_workflow_models.Case.STATUS_CANCELED
        assert instance.instance_state.name == "archived"


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,current_form_slug,new_form_slug,expected_status",
    [
        ("Support", "baugesuch", "baugesuch-generell", status.HTTP_204_NO_CONTENT),
        ("Support", "baugesuch", "baugesuch-mit-uvp", status.HTTP_204_NO_CONTENT),
        ("Support", "baugesuch-generell", "baugesuch", status.HTTP_204_NO_CONTENT),
        (
            "Support",
            "baugesuch-generell",
            "baugesuch-mit-uvp",
            status.HTTP_204_NO_CONTENT,
        ),
        ("Support", "baugesuch-mit-uvp", "baugesuch", status.HTTP_204_NO_CONTENT),
        (
            "Support",
            "baugesuch-mit-uvp",
            "baugesuch-generell",
            status.HTTP_204_NO_CONTENT,
        ),
        ("Support", "einfache-vorabklaerung", "baugesuch", status.HTTP_400_BAD_REQUEST),
        ("Support", "baugesuch", "einfache-vorabklaerung", status.HTTP_400_BAD_REQUEST),
        ("Municipality", "baugesuch", "baugesuch-generell", status.HTTP_403_FORBIDDEN),
    ],
)
def test_change_form(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_service,
    role,
    current_form_slug,
    new_form_slug,
    expected_status,
):
    current_form, _ = caluma_form_models.Form.objects.get_or_create(
        pk=current_form_slug
    )
    new_form, _ = caluma_form_models.Form.objects.get_or_create(pk=new_form_slug)

    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
    workflow.allow_forms.add(current_form, new_form)

    case = workflow_api.start_case(
        workflow=workflow,
        form=current_form,
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    response = admin_client.post(
        reverse("instance-change-form", args=[instance.pk]),
        {
            "data": {
                "type": "instance-change-forms",
                "id": instance.pk,
                "attributes": {"form": new_form_slug},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        case.refresh_from_db()

        assert case.document.form_id == new_form_slug


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "instance_state__name,should_sync", [("circulation", True), ("sb1", False)]
)
def test_change_responsible_service_circulations(
    db,
    admin_client,
    admin_user,
    role,
    instance_state,
    instance_service,
    caluma_workflow_config_be,
    service_factory,
    circulation_factory,
    activation_factory,
    work_item_factory,
    should_sync,
    caluma_admin_user,
):
    instance = instance_service.instance
    instance.instance_state = instance_state
    instance.save()

    old_service = instance.responsible_service()
    sub_service = service_factory(service_parent=old_service)
    new_service = service_factory()
    some_service = service_factory()

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    c1 = circulation_factory(instance=instance, service=old_service)
    c2 = circulation_factory(instance=instance, service=old_service)

    # from the old service to some service, stays
    a1 = activation_factory(circulation=c1, service_parent=old_service)
    # from some other service to some other service, stays
    a2 = activation_factory(circulation=c1, service_parent=some_service)
    # should be deleted since the new service is now responsible
    a3 = activation_factory(
        circulation=c1, service_parent=old_service, service=new_service
    )
    # should be deleted since it's to a sub service of the old services
    activation_factory(circulation=c2, service_parent=old_service, service=sub_service)

    for task_id in ["submit", "ebau-number", "init-circulation"]:
        workflow_api.complete_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    for circulation in [c1, c2]:
        work_item_factory(
            task=Task.objects.get(pk="circulation"),
            meta={"circulation-id": circulation.pk},
        )

        CalumaApi().sync_circulation(circulation, caluma_admin_user)

    response = admin_client.post(
        reverse("instance-change-responsible-service", args=[instance.pk]),
        {
            "data": {
                "type": "instance-change-responsible-services",
                "attributes": {"service-type": "municipality"},
                "relationships": {
                    "to": {"data": {"id": new_service.pk, "type": "services"}}
                },
            }
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    if should_sync:
        assert instance.circulations.filter(pk=c1.pk).exists()
        assert not instance.circulations.filter(pk=c2.pk).exists()

        c1.refresh_from_db()

        assert c1.activations.filter(pk=a1.pk).exists()
        assert c1.activations.filter(pk=a2.pk).exists()
        assert not c1.activations.filter(pk=a3.pk).exists()

        a1.refresh_from_db()
        a2.refresh_from_db()

        assert a1.service_parent == new_service
        assert a2.service_parent == some_service


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "service_type,expected_status",
    [
        ("municipality", status.HTTP_204_NO_CONTENT),
        ("construction_control", status.HTTP_204_NO_CONTENT),
        ("invalidtype", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_change_responsible_service(
    db,
    admin_client,
    admin_user,
    instance,
    instance_service,
    notification_template,
    role,
    group,
    service_factory,
    user_factory,
    user_group_factory,
    caluma_workflow_config_be,
    application_settings,
    service_type,
    expected_status,
    caluma_admin_user,
):
    application_settings["NOTIFICATIONS"]["CHANGE_RESPONSIBLE_SERVICE"] = {
        "template_slug": notification_template.slug,
        "recipient_types": ["leitbehoerde"],
    }

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    if expected_status == status.HTTP_400_BAD_REQUEST:
        old_service = instance.responsible_service()
    else:
        old_service = instance.responsible_service(filter_type=service_type)
    new_service = service_factory()

    group.service = old_service
    group.save()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.complete_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    # other user is no member of the new service
    other_user = user_factory()
    # admin user is a member of the new service
    user_group_factory(user=admin_user, group__service=new_service)

    init_circulation = case.work_items.get(task_id="init-circulation")
    init_circulation.assigned_users = [admin_user.username, other_user.username]
    init_circulation.save()

    assert (
        case.work_items.filter(
            status="ready", addressed_groups__contains=[str(old_service.pk)]
        ).count()
        == 5
    )
    assert (
        case.work_items.filter(
            status="ready", addressed_groups__contains=[str(new_service.pk)]
        ).count()
        == 0
    )

    response = admin_client.post(
        reverse("instance-change-responsible-service", args=[instance.pk]),
        {
            "data": {
                "type": "instance-change-responsible-services",
                "attributes": {"service-type": service_type},
                "relationships": {
                    "to": {"data": {"id": new_service.pk, "type": "services"}}
                },
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        instance.refresh_from_db()

        # responsible service changed
        assert not instance.instance_services.filter(
            active=1, service=old_service
        ).exists()
        assert instance.responsible_service(filter_type=service_type) == new_service

        # notification was sent
        assert len(mail.outbox) == 1
        assert new_service.email in mail.outbox[0].recipients()

        # history entry was created
        history = HistoryEntry.objects.filter(instance=instance).last()
        assert (
            history.trans.get(language="de").title
            == f"Neue Leitbehörde: {new_service.trans.get(language='de').name}"
        )

        # caluma work items are reassigned
        assert (
            case.work_items.filter(
                status="ready", addressed_groups__contains=[str(old_service.pk)]
            ).count()
            == 0
        )
        assert (
            case.work_items.filter(
                status="ready", addressed_groups__contains=[str(new_service.pk)]
            ).count()
            == 5
        )

        # assigned users are filtered
        init_circulation.refresh_from_db()
        assert admin_user.username in init_circulation.assigned_users
        assert other_user.username not in init_circulation.assigned_users
    elif expected_status == status.HTTP_400_BAD_REQUEST:
        assert (
            response.data[0]["detail"]
            == f"{service_type} is not a valid service type - valid types are: municipality, construction_control"
        )
