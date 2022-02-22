import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";

import config from "camac-ng/config/environment";

export default class LinkedInstancesTableComponent extends Component {
  @queryManager apollo;

  @service store;
  @service intl;

  @calumaQuery({ query: allCases, options: "options" }) casesQuery;

  tableColumns = ["instanceId", "dossierNr", "form", "intent", "instanceState"];

  get options() {
    return {
      pageSize: 15,
      processNew: (cases) => this.processNew(cases),
    };
  }

  get paginationInfo() {
    return htmlSafe(
      this.intl.t("global.paginationInfo", {
        count: this.casesQuery.value.length,
        total: this.casesQuery.totalCount,
      })
    );
  }

  async processNew(cases) {
    if (!cases.length) {
      return [];
    }
    const instanceIds = cases.map((_case) => _case.meta["camac-instance-id"]);

    await this.store.query("instance", {
      instance_id: instanceIds.join(","),
      include: "instance_state,user,form",
    });
    return cases;
  }

  get linkedInstanceIds() {
    return this.args.linkedInstances.map((instance) => parseInt(instance.id));
  }

  get instanceIdAsInt() {
    return parseInt(this.args.currentInstanceId);
  }

  @action
  setup() {
    this.casesQuery.fetch({
      filter: [{ hasAnswer: this.args.filters }],
      order: config.APPLICATION.casesQueryOrder,
    });
  }

  @action
  loadNextPage() {
    this.casesQuery.fetchMore();
  }

  @action
  redirectToCase(caseRecord) {
    location.assign(
      `/index/redirect-to-instance-resource/instance-id/${caseRecord.instanceId}/`
    );
  }
}