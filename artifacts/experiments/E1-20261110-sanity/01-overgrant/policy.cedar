permit (
  principal is User,
  action == Action::"editDocument",
  resource is Document
)
when {
  (Role::"Author" in principal.roles || Role::"Editor" in principal.roles) &&
  resource.status == "draft" &&
  principal in resource.shareList
};