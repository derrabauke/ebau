export default {
  columns: {
    caluma: {
      service: [
        "instanceId",
        "dossierNumber",
        "form",
        "address",
        "inquiryCreated",
        "instanceState",
        "intent",
        "applicants",
      ],
      "construction-control": [
        "instanceId",
        "dossierNumber",
        "form",
        "address",
        "decisionDate",
        "instanceState",
        "intent",
        "applicants",
      ],
      default: [
        "instanceId",
        "dossierNumber",
        "form",
        "address",
        "submitDate",
        "instanceState",
        "intent",
        "applicants",
      ],
    },
  },
  activeFilters: {
    caluma: {
      service: [
        "form",
        "instanceId",
        "dossierNumber",
        "municipality",
        "responsibleMunicipality",
        "responsibleServiceUser",
        "address",
        "parcel",
        "personalDetails",
        "inquiryState",
        "inquiryAnswer",
        "inquiryCreatedAfter",
        "inquiryCreatedBefore",
        "inquiryCompletedAfter",
        "inquiryCompletedBefore",
        "tags",
        "instanceState",
        "paper",
      ],
      "construction-control": [
        "form",
        "instanceId",
        "dossierNumber",
        "municipality",
        "responsibleMunicipality",
        "responsibleServiceUser",
        "address",
        "parcel",
        "personalDetails",
        "decisionDateAfter",
        "decisionDateBefore",
        "tags",
        "instanceState",
        "decision",
        "paper",
      ],
      default: [
        "form",
        "instanceId",
        "dossierNumber",
        "municipality",
        "responsibleMunicipality",
        "responsibleServiceUser",
        "address",
        "parcel",
        "personalDetails",
        "submitDateAfter",
        "submitDateBefore",
        "tags",
        "instanceState",
        "decision",
        "paper",
      ],
    },
  },
  filterPresets: {
    service: {
      pending: { instanceState: ["20004"], inquiryState: "pending" },
      paper: { paper: "1" },
    },
    "construction-control": {
      pending: { instanceState: ["20011", "20013", "20014"] },
      paper: { paper: "1" },
    },
    municipality: {
      pending: {
        instanceState: [
          "20000",
          "20003",
          "20004",
          "20005",
          "20007",
          "120001",
          "120002",
        ],
      },
      paper: { paper: "1" },
    },
  },
  availableOrderings: {
    instanceId: {
      caluma: [{ meta: "camac-instance-id" }],
    },
    dossierNumber: {
      caluma: [{ meta: "ebau-number" }],
    },
    submitDate: {
      caluma: [{ meta: "submit-date" }],
    },
  },
  defaultOrder: "instanceId",
};
