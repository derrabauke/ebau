"use strict";

const EmberApp = require("ember-cli/lib/broccoli/ember-app");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    sourcemaps: {
      enabled: true,
      extensions: ["js"],
    },
    "ember-cli-babel": {
      includePolyfill: true,
    },
    emberApolloClient: {
      keepGraphqlFileExtension: false,
    },
  });

  // intersection observer polyfill
  app.import("node_modules/intersection-observer/intersection-observer.js");

  return app.toTree();
};
