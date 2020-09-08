import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import completeWorkItem from "camac-ng/gql/mutations/complete-workitem";
import saveWorkItem from "camac-ng/gql/mutations/save-workitem";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import moment from "moment";

export default class WorkItemsInstanceEditController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;
  @service moment;

  get isCreator() {
    return (this.model.createdByGroup || []).includes(
      this.shoebox.content.serviceId
    );
  }

  get responsibleUser() {
    return this.userChoices?.find(user =>
      this.model.assignedUsers.includes(user.username)
    );
  }

  set responsibleUser(user) {
    this.model.assignedUsers = [user.username];
  }

  get isAddressed() {
    return this.model.addressedServices
      .map(s => parseInt(s.id))
      .includes(this.shoebox.content.serviceId);
  }

  get isManualWorkItem() {
    return this.model.raw.task.slug === "create-manual-workitems";
  }

  get isWorkItemCompleted() {
    return this.model.raw.status === "COMPLETED";
  }

  @lastValue("fetchUserChoices") userChoices;

  @dropTask
  *fetchUserChoices() {
    try {
      return (yield this.store.query("user", {
        service: this.shoebox.content.serviceId
      })).toArray();
    } catch (error) {
      this.notifications.error(this.intl.t("workItem.fetchError"));
    }
  }

  @dropTask
  *workItemAssignUsers(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.model.id,
            assignedUsers: this.model.assignedUsers
          }
        }
      });

      this.notifications.success(this.intl.t("workItem.saveSuccess"));

      this.transitionToRoute("work-items.instance.index");
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  @dropTask
  *finishWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.model.id,
            meta: JSON.stringify(this.model.meta)
          }
        }
      });

      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: {
          input: {
            id: this.model.id
          }
        }
      });

      this.notifications.success(this.intl.t("workItem.finishSuccess"));

      this.transitionToRoute("work-items.instance.index");
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  @dropTask
  *saveManualWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.model.id,
            description: this.model.description,
            deadline: this.model.deadline,
            meta: JSON.stringify(this.model.meta)
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
    this.model.deadline = moment(value);
  }
}