import CustomCaseBaseModel from "camac-ng/caluma-query/models/-case";
import getAnswer from "camac-ng/utils/get-answer";

export default class CustomCaseModel extends CustomCaseBaseModel {
  get dossierNumber() {
    return this.raw.meta["ebau-number"];
  }

  get form() {
    return this.instance?.name;
  }

  get address() {
    const street = getAnswer(this.raw.document, "strasse-flurname")?.node
      .stringValue;
    const number = getAnswer(this.raw.document, "nr")?.node.stringValue;
    const city = getAnswer(this.raw.document, "ort-grundstueck")?.node
      .stringValue;
    const migrated = getAnswer(this.raw.document, "standort-migriert")?.node
      .stringValue;

    return (
      [[street, number].filter(Boolean).join(" ").trim(), (city ?? "").trim()]
        .filter(Boolean)
        .join(", ") || (migrated ?? "").trim()
    );
  }

  get decisionDate() {
    const decisionDate =
      this.raw.workItems.edges[0]?.node.document.answers.edges[0]?.node.value;

    return decisionDate
      ? this.intl.formatDate(decisionDate, {
          format: "date",
        })
      : null;
  }

  get instanceState() {
    return this.instance?.get("instanceState.name");
  }

  get applicants() {
    const applicants =
      getAnswer(this.raw.document, "personalien-gesuchstellerin")?.node.value ??
      [];

    const applicantNames = applicants.map((row) => {
      const firstName = getAnswer(row, "vorname-gesuchstellerin")?.node
        .stringValue;
      const lastName = getAnswer(row, "name-gesuchstellerin")?.node.stringValue;
      const juristicName = getAnswer(
        row,
        "name-juristische-person-gesuchstellerin"
      )?.node.stringValue;

      return (
        juristicName?.trim() ??
        [lastName, firstName]
          .filter(Boolean)
          .map((name) => name.trim())
          .join(", ")
      );
    });

    return applicantNames.filter(Boolean).join("\n");
  }

  static fragment = `{
    meta
    id
    workItems(
      filter: [
        { task: "decision" }
        { status: CANCELED, invert: true }
        { status: READY, invert: true }
      ]
    ) {
      edges {
        node {
          id
          document {
            id
            answers(filter: [{ question: "decision-date" }]) {
              edges {
                node {
                  id
                  ... on DateAnswer {
                    value
                  }
                }
              }
            }
          }
        }
      }
    }
    document {
      form {
        id
        slug
        name
      }
      answers(
        filter: [
          {
            questions: [
              "strasse-flurname"
              "nr"
              "ort-grundstueck"
              "standort-migriert"
              "beschreibung-bauvorhaben"
              "personalien-gesuchstellerin"
            ]
          }
        ]
      ) {
        edges {
          node {
            question {
              id
              slug
            }
            ... on TableAnswer {
              value {
                answers {
                  edges {
                    node {
                      question {
                        slug
                      }
                      ... on StringAnswer {
                        stringValue: value
                      }
                    }
                  }
                }
              }
            }
            ... on StringAnswer {
              stringValue: value
            }
            ... on IntegerAnswer {
              integerValue: value
            }
          }
        }
      }
    }
  }`;
}