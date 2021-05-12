import { setContext } from "@apollo/client/link/context";
import { inject as service } from "@ember/service";
import ApolloService from "ember-apollo-client/services/apollo";
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default class CustomApolloService extends ApolloService.extend(
  CalumaApolloServiceMixin
) {
  @service session;
  @service shoebox;

  link(...args) {
    const httpLink = super.link(...args);

    const middleware = setContext(async (_, context) => ({
      ...context,
      headers: {
        authorization: await this.session.getAuthorizationHeader(),
        "accept-language": this.shoebox.content.language,
        "x-camac-group": this.shoebox.content.groupId,
        ...context.headers,
      },
    }));

    return middleware.concat(httpLink);
  }
}
