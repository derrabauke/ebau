"use strict";

module.exports = function (environment) {
  // eslint-disable-next-line no-console
  console.log(
    `build env: APPLICATION: ${process.env.APPLICATION}, KEYCLOAK_HOST: ${process.env.KEYCLOAK_HOST}`
  );
  const app = process.env.APPLICATION || "kt_bern";
  const appConfig = {
    kt_bern: {
      name: "be",
      realm: "ebau",
      locales: ["de", "fr"],
      supportGroups: [10000],
      useConfidential: false,
      selectableGroups: {
        roles: [
          3, // Leitung Leitbehörde
          5, // Leitung Baukontrolle
          20004, // Sachbearbeiter Leitbehörde
          20005, // Sachbearbeiter Baukontrolle
          10000, // System-Betrieb
        ],
      },
      documents: {
        feedbackSection: 3,
      },
    },
    kt_uri: {
      name: "ur",
      realm: "urec",
      locales: ["de"],
      supportGroups: [1070],
      useConfidential: true,
      selectableGroups: {
        roles: [
          1131, // Support
        ],
      },
      documents: {},
    },
  }[app];

  const oidcHost =
    process.env.KEYCLOAK_HOST || "http://camac-ng-keycloak.local";

  const ENV = {
    modulePrefix: "ember-caluma-portal",
    environment,
    rootURL: "/",
    locationType: "auto",
    historySupportMiddleware: true,
    "ember-simple-auth-oidc": {
      host: `${oidcHost}/auth/realms/${appConfig.realm}/protocol/openid-connect`,
      clientId: "portal",
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      endSessionEndpoint: "/logout",
      userinfoEndpoint: "/userinfo",
      afterLogoutUri: "/login",
      forwardParams: ["kc_idp_hint"],
    },
    apollo: {
      apiURL: "/graphql/",
    },
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. EMBER_NATIVE_DECORATOR_SUPPORT: true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false,
      },
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },
    moment: {
      includeLocales: appConfig.locales,
    },

    languages: appConfig.locales,
    fallbackLanguage: "de",

    APPLICATION: appConfig,

    ebau: {
      internalURL: "http://camac-ng.local",
      attachments: {
        allowedMimetypes: ["image/png", "image/jpeg", "application/pdf"],
        buckets: [
          "dokument-grundstucksangaben",
          "dokument-gutachten-nachweise-begrundungen",
          "dokument-projektplane-projektbeschrieb",
          "dokument-weitere-gesuchsunterlagen",
        ],
      },
      supportGroups: appConfig.supportGroups,
      selectableGroups: appConfig.selectableGroups,
      paperInstances: {
        allowedGroups: {
          roles: [
            3, // Leitung Leitbehörde
            20004, // Sachbearbeiter Leitbehörde
          ],
          serviceGroups: [
            2, // Gemeinde
            20000, // Regierungsstatthalteramt
          ],
        },
      },
      instanceStates: {
        new: 1,
        rejected: 10000,
        archived: 20009,
        inCorrection: 20007,
        finished: 120000,
        sb1: 20011,
        sb2: 20013,
      },
      internalForms: [
        "migriertes-dossier",
        "baupolizeiliches-verfahren",
        "zutrittsermaechtigung",
        "klaerung-baubewilligungspflicht",
      ],
    },
  };

  if (environment === "development") {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === "test") {
    // Testem prefers this...
    ENV.locationType = "none";

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = "#ember-testing";
    ENV.APP.autoboot = false;
  }

  if (environment === "production") {
    // here you can enable a production-specific feature
  }

  return ENV;
};
