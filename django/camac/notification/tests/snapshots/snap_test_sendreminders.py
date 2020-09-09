# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_sendreminders_caluma 1"] = [
    {
        "body": """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Überfällige Aufgaben:
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 08.08.2020
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."
 - Aufgabe "Prof. Brunhild Süßebier B.A."


Freundliche Grüsse
""",
        "subject": "Erinnerung an Aufgaben",
        "to": ["andersonhoward@griffin.com"],
    },
    {
        "body": """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Überfällige Aufgaben:
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 08.08.2020
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020


Freundliche Grüsse
""",
        "subject": "Erinnerung an Aufgaben",
        "to": ["cmiller@hotmail.com"],
    },
    {
        "body": """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."
 - Aufgabe "Prof. Brunhild Süßebier B.A."


Freundliche Grüsse
""",
        "subject": "Erinnerung an Aufgaben",
        "to": ["craig69@hotmail.com"],
    },
    {
        "body": """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."
 - Aufgabe "Prof. Brunhild Süßebier B.A."


Freundliche Grüsse
""",
        "subject": "Erinnerung an Aufgaben",
        "to": ["kingmelanie@yahoo.com"],
    },
    {
        "body": """Guten Tag


Diese Ihnen unterstehenden Aufgaben wurden noch nicht abgeschlossen.

Überfällige Aufgaben:
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 08.08.2020
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."
 - Aufgabe "Prof. Brunhild Süßebier B.A."


Freundliche Grüsse
""",
        "subject": "Erinnerung an Aufgaben",
        "to": ["nroberts@hotmail.com"],
    },
    {
        "body": """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Überfällige Aufgaben:
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 08.08.2020
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."
 - Aufgabe "Prof. Brunhild Süßebier B.A."


Freundliche Grüsse
""",
        "subject": "Erinnerung an Aufgaben",
        "to": ["rfields@yahoo.com"],
    },
    {
        "body": """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Überfällige Aufgaben:
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 08.08.2020
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020

---

Diese Ihnen unterstehenden Aufgaben wurden noch nicht abgeschlossen.

Überfällige Aufgaben:
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 08.08.2020
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."
 - Aufgabe "Prof. Brunhild Süßebier B.A."


Freundliche Grüsse
""",
        "subject": "Erinnerung an Aufgaben",
        "to": ["william71@richardson.com"],
    },
]
