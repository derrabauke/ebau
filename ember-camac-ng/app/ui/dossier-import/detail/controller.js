import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { timeout } from "ember-concurrency";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class DossierImportDetailController extends Controller {
  @service intl;
  @service notifications;
  @service store;
  @service router;

  @tracked user;

  @lastValue("fetchImport") import;
  @dropTask
  *fetchImport() {
    try {
      this.notifications.clear();

      return yield this.store.findRecord("dossier-import", this.model, {
        include: "user",
      });
    } catch (e) {
      this.notifications.error(
        this.intl.t("dossierImport.detail.fetchImportError")
      );
      this.router.transitionTo("index");
    }
  }

  @dropTask
  *deleteImport() {
    try {
      this.notifications.clear();

      yield this.import.destroyRecord();

      this.notifications.success(
        this.intl.t("dossierImport.detail.actions.deleteImport.success")
      );
      this.router.transitionTo("dossier-import.index");
    } catch (e) {
      this.notifications.error(
        this.intl.t("dossierImport.detail.actions.deleteImport.error")
      );
    }
  }

  @dropTask
  *startImport() {
    // TODO as soon as workflow is implemented in backend
    yield timeout(1000);
  }

  get summary() {
    const messages = this.import?.messages;
    return this.isValidated
      ? messages?.validation.summary
      : this.isImported
      ? messages?.import.summary
      : null;
  }

  get isValidated() {
    return (
      this.import?.status === "verified" || this.import?.status === "failed"
    );
  }

  get isImported() {
    return this.import?.status === "done";
  }

  get validationVerified() {
    return this.import?.status === "verified";
  }

  get validationFailed() {
    return this.import?.status === "failed";
  }
}