import Model, { attr, belongsTo } from "@ember-data/model";

export default class DossierImportModel extends Model {
  @attr createdAt;
  @attr status;
  @attr messages;
  @attr sourceFile;
  @attr mimeType;
  @attr dossierLoaderType;

  @belongsTo user;
  @belongsTo group;
  @belongsTo location;
  @belongsTo service;
}