import functools
from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from camac.core.models import WorkflowEntry


@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Canton", 0), ("Municipality", 1), ("Service", 0)],
)
def test_publication_list(admin_client, publication_entry, activation, size):
    url = reverse("publication-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(publication_entry.pk)


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_200_OK),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
    ],
)
def test_publication_update(
    application_settings,
    admin_client,
    publication_entry,
    workflow_item,
    activation,
    status_code,
):
    application_settings["WORKFLOW_ITEMS"]["PUBLICATION"] = workflow_item.pk

    url = reverse("publication-detail", args=[publication_entry.pk])
    data = {
        "data": {
            "type": "publication-entries",
            "id": publication_entry.pk,
            "attributes": {"is-published": 1},
        }
    }
    response = admin_client.patch(url, data=data)

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert WorkflowEntry.objects.filter(
            instance=publication_entry.instance, workflow_item=workflow_item
        ).exists()


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_201_CREATED),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
    ],
)
def test_publication_create(
    admin_client, instance, group, service, activation, status_code
):
    url = reverse("publication-list")

    data = {
        "data": {
            "type": "publication-entries",
            "id": None,
            "attributes": {"publication-date": datetime.now(), "is-published": 0},
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["relationships"]["instance"]["data"]["id"] == (
            str(instance.pk)
        )


@pytest.mark.parametrize(
    "role__name", ["Applicant", "Municipality", "Canton", "Service"]
)
def test_publication_destroy(admin_client, publication_entry, activation):
    url = reverse("publication-detail", args=[publication_entry.pk])

    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("role__name", [("Municipality")])
def test_publication_publish(
    requests_mock, settings, admin_client, publication_entry, form_field_factory
):
    requests_mock.post(
        settings.PUBLICATION_API_URL,
        text="New Baugesuch for Schwyz in Amtsblatt 41/2019 vom 11.10.2019, Redaktionsschluss 09.10.2019 11:00 Uhr created.",
    )

    url = reverse("publication-publish", args=[publication_entry.pk])
    add_field = functools.partial(
        form_field_factory, instance=publication_entry.instance
    )

    add_field(name="lage", value="beides")
    persons = [
        {
            "anrede": "Herr",
            "vorname": "Max",
            "name": "Muster",
            "strasse": "Musterstrasse 3",
            "plz": "1234",
            "ort": "Musterort",
            "email": "example@example.com",
        },
        {
            "anrede": "Frau",
            "vorname": "Erika",
            "name": "Muster",
            "strasse": "Musterstrasse 3",
            "plz": "1234",
            "ort": "Musterort",
            "tel": "1234567",
        },
        {
            "anrede": "Firma",
            "firma": "Firma",
            "name": "Muster",
            "strasse": "Musterstrasse 3",
            "plz": "1234",
            "ort": "Musterort",
        },
    ]
    add_field(name="bauherrschaft", value=persons)
    add_field(name="projektverfasser-planer", value=persons)
    add_field(name="grundeigentumerschaft", value=persons)
    add_field(name="grundeigentumerschaft-override", value=persons)
    add_field(name="bezeichnung", value="Ein Auto")
    add_field(name="bezeichnung-override", value="Ein Haus")
    add_field(name="parzellen", value=[{"number": 6}])
    add_field(name="punkte", value=[{"lat": 47.024328, "lng": 8.653836}])
    add_field(name="publikation-bemerkung", value="Ein grosses Haus")

    response = admin_client.post(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
