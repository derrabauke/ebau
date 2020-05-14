import { render, settled } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | notifications", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function(assert) {
    const service = this.owner.lookup("service:notifications");

    await render(hbs`<Notifications />`);

    assert.dom(".hinweisbox.buttonstyle").doesNotExist();

    service.error("Test");
    await settled();

    assert.dom(".hinweisbox.buttonstyle.error").exists();
    assert.dom(".hinweisbox.buttonstyle.error").hasText("Test");

    service.success("Test");
    await settled();

    assert.dom(".hinweisbox.buttonstyle.success").exists();
    assert.dom(".hinweisbox.buttonstyle.success").hasText("Test");

    assert.dom(".hinweisbox.buttonstyle").exists({ count: 2 });

    await render(hbs``);
    await settled();

    // clears on destroy
    assert.equal(service.all.length, 0);
  });
});