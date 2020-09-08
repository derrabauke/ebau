import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import createWorkItem from "camac-ng/gql/mutations/create-work-item";
import allCases from "camac-ng/gql/queries/all-cases";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

class NewWorkItem {
  @tracked case;
  @tracked addressedGroups = [];
  @tracked assignedUsers = [];
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = moment().add(10, "days");
  @tracked notificationCompleted = true;
  @tracked notificationDeadline = true;
}

export default class WorkItemNewController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked instance = null;
  @tracked case = null;
  @tracked users = [];

  @tracked workItem = new NewWorkItem();

  get responsibleService() {
    return this.services.find(service =>
      this.workItem.addressedGroups.includes(service.id)
    );
  }

  set responsibleService(service) {
    this.workItem.addressedGroups = [String(service.id)];

    if (parseInt(service.id) !== this.shoebox.content.serviceId) {
      this.workItem.assignedUsers = [];
    }
  }

  get responsibleUser() {
    return this.users.find(user =>
      this.workItem.assignedUsers.includes(user.username)
    );
  }

  set responsibleUser(user) {
    this.workItem.assignedUsers = [user.username];
  }

  get selectedOwnService() {
    return (
      parseInt(this.responsibleService?.id) === this.shoebox.content.serviceId
    );
  }

  get services() {
    return this.instance?.involvedServices || [];
  }

  @dropTask
  *getData() {
    this.instance = yield this.store.findRecord("instance", this.model.id, {
      include: "involved_services",
      reload: true
    });

    this.users = yield this.store.query("user", {
      service: this.shoebox.content.serviceId
    });

    this.case = yield this.apollo.query(
      {
        query: allCases,
        variables: {
          metaValueFilter: [{ key: "camac-instance-id", value: this.model.id }]
        }
      },
      "allCases.edges.firstObject.node.id"
    );
  }

  @dropTask
  *createWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: this.case,
            multipleInstanceTask: "create-manual-workitems",
            name: this.workItem.title,
            description: this.workItem.description,
            addressedGroups: this.workItem.addressedGroups,
            controllingGroups: [this.shoebox.content.serviceId],
            deadline: this.workItem.deadline,
            meta: JSON.stringify({
              "notify-complete": this.workItem.notificationCompleted,
              "notify-deadline": this.workItem.notificationDeadline
            }),
            ...(this.workItem.assignedUsers.length
              ? { assignedUsers: this.workItem.assignedUsers }
              : {})
          }
        }
      });

      this.notifications.success(this.intl.t("workItem.saveSuccess"));

      this.transitionToRoute("work-items.instance.index");
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  @action
  setDeadline(value) {
    this.workItem.deadline = value;
  }
}