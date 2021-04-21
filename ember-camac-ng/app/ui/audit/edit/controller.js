import Controller, { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency-decorators";

export default class AuditEditController extends Controller {
  @service materialExamSwitcher;

  @controller("audit") auditController;
  @controller("audit.index") auditIndexController;

  queryParams = ["displayedForm"];

  get audit() {
    return [
      ...(this.auditIndexController.audits || []),
      ...(this.auditIndexController.auditsWithSameEbauNumber || []).flatMap(
        (group) => group.audits
      ),
    ].find((audit) => audit.id === this.model);
  }

  get isMaterialExam() {
    return this.audit?.form === "mp-form";
  }

  get disabled() {
    // audits from the same ebau number should be read-only
    if (
      !this.audit ||
      !this.auditIndexController.audits.find((audit) => audit.id === this.model)
    ) {
      return true;
    }

    return this.auditController.disabled || !this.audit.canEdit;
  }

  @dropTask
  *back(event) {
    event.preventDefault();

    yield this.auditController.fetchAudit.perform();
    yield this.transitionToRoute("audit.index");
  }

  @action
  toggleIrrelevant() {
    if (!this.isMaterialExam) return;

    this.materialExamSwitcher.toggle();
  }
}
