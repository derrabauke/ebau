export default {
  columns: {
    caluma: ["dossierNr", "caseDocumentFormName", "intent", "caseStatus"],
    "camac-ng": [
      "dossierNr",
      "instanceFormDescription",
      "locationSZ",
      "builderSZ",
      "intentSZ",
      "instanceStateDescription",
    ],
  },
  activeFilters: {
    caluma: ["dossierNumber", "intent", "caseStatus", "caseDocumentFormName"],
    "camac-ng": [
      "instanceIdentifier",
      "instanceStateDescription",
      "locationSZ",
      "responsibleServiceUser",
      "addressSZ",
      "plotSZ",
      "builderSZ",
      "landownerSZ",
      "applicantSZ",
      "submitDateAfterSZ",
      "submitDateBeforeSZ",
      "serviceSZ",
      "formSZ",
    ],
  },
  formFields: [
    "bauherrschaft",
    "bauherrschaft-v2",
    "bauherrschaft-override",
    "bezeichnung",
    "bezeichnung-override",
  ],
  order: [{ meta: "dossier-number" }],
};