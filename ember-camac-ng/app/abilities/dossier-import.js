import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import isProd from "camac-ng/utils/is-prod";

export default class extends Ability {
  @service shoebox;

  get canDoSomething() {
    return (
      this.canStart ||
      this.canConfirm ||
      this.canTransmit ||
      this.canDelete ||
      this.canUndo
    );
  }

  get canStart() {
    return (
      this.model?.status === "verified" &&
      (!isProd() || this.shoebox.isSupportRole)
    );
  }

  get canConfirm() {
    return !isProd() && this.model?.status === "imported";
  }

  get canTransmit() {
    return (
      !isProd() &&
      this.shoebox.isSupportRole &&
      this.model?.status === "confirmed"
    );
  }

  get canUndo() {
    if (isProd()) {
      return false;
    }
    if (this.shoebox.isSupportRole) {
      return ["imported", "import-failed", "confirmed"].includes(
        this.model?.status
      );
    }
    if (this.shoebox.baseRole === "municipality") {
      return ["imported", "import-failed"].includes(this.model?.status);
    }
    return false;
  }

  get canDelete() {
    return ["verified", "failed"].includes(this.model?.status);
  }
}
