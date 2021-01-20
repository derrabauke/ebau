# Configuration models that do not have any foreign key relationships
# to non-config models (direct or indirect).
# These models can be safely deleted and re-imported anytime.
DUMP_CONFIG_MODELS = [
    "core.ACheckquery",
    "core.ACirculationEmail",
    "core.ACirculationEmailT",
    "core.ACirculationtransition",
    "core.ACopyanswer",
    "core.ACopyanswerMapping",
    "core.ACopydata",
    "core.ACopydataMapping",
    "core.Action",
    "core.ActionT",
    "core.ADeleteCirculation",
    "core.AEmail",
    "core.AEmailT",
    "core.AFormtransition",
    "core.AirAction",
    "core.ALocation",
    "core.ALocationQc",
    "core.ANotice",
    "core.ANotification",
    "core.AnswerList",
    "core.APageredirect",
    "core.APhp",
    "core.AProposal",
    "core.AProposalT",
    "core.AProposalHoliday",
    "core.ArAction",
    "core.ASavepdf",
    "core.AttachmentExtension",
    "core.AttachmentExtensionRole",
    "core.AttachmentExtensionService",
    "core.Authority",
    "core.AuthorityAuthorityType",
    "core.AuthorityLocation",
    "core.AuthorityType",
    "core.AnswerListT",
    "core.AvailableAction",
    "core.AvailableInstanceResource",
    "core.AvailableResource",
    "core.AValidate",
    "core.BillingConfig",
    "core.BRoleAcl",
    "core.BServiceAcl",
    "core.BuildingAuthorityDoc",
    "core.BuildingAuthorityEmail",
    "core.Button",
    "core.ButtonT",
    "core.ChapterT",
    "core.ChapterPage",
    "core.ChapterPageGroupAcl",
    "core.ChapterPageRoleAcl",
    "core.ChapterPageServiceAcl",
    "core.CirculationAnswerT",
    "core.CirculationAnswerTypeT",
    "core.CirculationReason",
    "core.DocgenActivationAction",
    "core.DocgenActivationactionAction",
    "core.DocgenDocxAction",
    "core.DocgenPdfAction",
    "core.DocgenTemplate",
    "core.DocgenTemplateClass",
    "core.CirculationStateT",
    "core.CirculationTypeT",
    "core.FormGroup",
    "core.FormGroupT",
    "core.FormGroupForm",
    "core.GroupPermission",
    "core.InstanceResource",
    "core.InstanceResourceT",
    "core.InstanceResourceAction",
    "core.IrAllformpages",
    "core.IrEditcirculation",
    "core.IrEditcirculationT",
    "core.IrEditcirculationSg",
    "core.IrEditformpage",
    "core.IrEditformpages",
    "core.IrEditletter",
    "core.IrEditletterAnswer",
    "core.IrEditletterAnswerT",
    "core.IrEditnotice",
    "core.IrFormerror",
    "core.IrFormpage",
    "core.IrFormpages",
    "core.IrFormwizard",
    "core.IrFormwizardT",
    "core.IrGroupAcl",
    "core.IrLetter",
    "core.IrNewform",
    "core.IrPage",
    "core.IrRoleAcl",
    "core.IrServiceAcl",
    "core.Municipality",
    "core.NoticeTypeT",
    "core.Page",
    "core.PageT",
    "core.PageAnswerActivation",
    "core.PageForm",
    "core.PageFormGroup",
    "core.PageFormGroupT",
    "core.PageFormGroupAcl",
    "core.PageFormMode",
    "core.PageFormRoleAcl",
    "core.PageFormServiceAcl",
    "core.PublicationSetting",
    "core.QuestionChapter",
    "core.QuestionChapterGroupAcl",
    "core.QuestionChapterRoleAcl",
    "core.QuestionChapterServiceAcl",
    "core.RApiListCirculationState",
    "core.RApiListCirculationType",
    "core.RApiListInstanceState",
    "core.Resource",
    "core.ResourceT",
    "core.REmberList",
    "core.RFormlist",
    "core.RGroupAcl",
    "core.RList",
    "core.RListColumn",
    "core.RListColumnT",
    "core.RPage",
    "core.RRoleAcl",
    "core.RSearch",
    "core.RSearchColumn",
    "core.RSearchColumnT",
    "core.RSearchFilter",
    "core.RSearchFilterT",
    "core.RServiceAcl",
    "core.RSimpleList",
    "core.RCalumaList",
    "core.ServiceAnswerActivation",
    "core.TemplateGenerateAction",
    "core.WorkflowAction",
    "core.WorkflowRole",
    "document.AttachmentSectionRoleAcl",
    "document.AttachmentSectionServiceAcl",
    "responsible.IrEditresponsibleuser",
    "responsible.IrEditresponsiblegroup",
    "responsible.ASetresponsiblegroup",
    "responsible.ResponsibleServiceAllocation",
    "core.HistoryActionConfig",
    "core.HistoryActionConfigT",
    "core.ActionWorkitem",
    "core.ActionCase",
    "caluma_form.Option",
    "caluma_form.QuestionOption",
    "caluma_form.FormQuestion",
    "caluma_workflow.TaskFlow",
    "caluma_workflow.Flow",
]

# List of models that have foreign keys referencing non-config tables
# (directly or indirectly). All models which are not in this list can
# be safely flushed and re-imported.
DUMP_CONFIG_MODELS_REFERENCING_DATA = [
    "core.AnswerQuery",
    "core.BGroupAcl",
    "core.BuildingAuthoritySection",
    "core.BuildingAuthorityButton",
    "core.Chapter",
    "core.CirculationAnswer",
    "core.CirculationAnswerType",
    "core.CirculationState",
    "core.CirculationType",
    "core.IrCirculation",
    "core.Mapping",
    "core.NoticeType",
    "core.PublicationType",
    "core.Question",
    "core.QuestionT",
    "core.QuestionType",
    "core.WorkflowItem",
    "core.WorkflowSection",
    "document.AttachmentSection",
    "document.AttachmentSectionT",
    "document.Template",
    "instance.Form",
    "instance.FormT",
    "instance.FormState",
    "instance.InstanceState",
    "instance.InstanceStateT",
    "instance.InstanceStateDescription",
    "user.Group",
    "user.GroupT",
    "user.GroupLocation",
    "user.Location",
    "user.LocationT",
    "user.Role",
    "user.RoleT",
    "user.Service",
    "user.ServiceT",
    "user.ServiceGroup",
    "user.ServiceGroupT",
    "notification.NotificationTemplate",
    "notification.NotificationTemplateT",
    "caluma_form.Question",
    "caluma_form.Form",
    "caluma_workflow.Workflow",
    "caluma_workflow.Task",
]

# Exclude models which are managed by the customer alone from sync - instead it
# will be dumped as data. This will most likely be configured in the
# application config in settings.py
DUMP_CONFIG_EXCLUDED_MODELS = [
    # Example:
    # "user.Group",
    # "user.GroupT",
]

# Define custom config groups that will be dumped in an extracted fixture file.
# This will most likely be configured in the application config in settings.py
DUMP_CONFIG_GROUPS = {
    # Example:
    # "custom_form": {
    #     "caluma_form.Option": Q(questions__forms__pk="custom_form"),
    #     "caluma_form.Question": Q(forms__pk="custom_form"),
    #     "caluma_form.Form": Q(pk="custom_form"),
    #     "caluma_form.QuestionOption": Q(question__forms__pk="custom_form"),
    #     "caluma_form.FormQuestion": Q(form__pk__in="custom_form"),
    # },
}

DUMP_DATA_APPS = [
    "circulation",
    "core",
    "document",
    "instance",
    "notification",
    "user",
    "applicants",
    "caluma_form",
    "caluma_workflow",
]

DUMP_DATA_EXCLUDED_MODELS = [
    "caluma_form.HistoricalOption",
    "caluma_form.HistoricalQuestion",
    "caluma_form.HistoricalForm",
    "caluma_form.HistoricalQuestionOption",
    "caluma_form.HistoricalFormQuestion",
    "caluma_workflow.HistoricalWorkflow",
    "caluma_workflow.HistoricalTask",
    "caluma_workflow.HistoricalTaskFlow",
    "caluma_workflow.HistoricalFlow",
]
