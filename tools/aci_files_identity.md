# ACI state volumes with Azure Files managed identity

`aci_files_identity.py` converts existing canonical ACI state templates to
SMB managed-identity mounts. It retains storage account names, file shares,
mount paths, state-file settings and existing broker identities. It does not
change event contracts or feeder code.

> Candidate deployment path, not release acceptance. All six full native USGS
> templates passed Azure ARM validation with Shared Key disabled. Three isolated
> live ACI probes reported `FailedMountAzureFileVolume`. The latest allowed
> 35 minutes for role propagation before ACI creation and collected eight
> successful OAuth `GetKerbTicket` requests for the expected identity, followed
> by mount warnings. No SMB requests appeared in the collected logs. Successful
> mount, restart persistence and feeder checkpoint acceptance remain required.

```powershell
python tools\aci_files_identity.py feeders\<source>\azure-template.json
```

Pass all template paths to convert a source's transport variants together.
The tool validates every input before writing any template. Reapplying it
produces the same JSON. Run it after ordinary ARM generation; the native USGS
`generate-template.ps1` includes this step.

## Resources and permissions

- Storage API `2025-08-01` enables
  `azureFilesIdentityBasedAuthentication.smbOAuthSettings.isSmbOAuthEnabled`
  and sets `allowSharedKeyAccess=false`.
  The default file service explicitly permits Kerberos authentication; enabling
  SMB OAuth does not configure this separate setting. Empty SMB settings do
  not mean Kerberos is disabled: Azure Files permits all authentication methods
  by default. Explicit Kerberos-only configuration also prevents NTLMv2
  storage-key mounts.
- A separate user-assigned managed identity is attached to ACI for state access.
  Existing Event Grid or Service Bus publisher identities remain attached.
- The identity receives **Storage File Data SMB MI Admin**
  (`a235d3ee-5935-4cfb-8cc5-a3303ad5995e`) at the dedicated state account.
  Azure Files currently requires this administrator role for managed-identity
  SMB mounts. Ordinary SMB Share Contributor does not provide the required
  built-in administrator permission. Do not reuse the account for unrelated
  data: this role grants access across its shares and bypasses file-level ACLs.
- ACI API `2026-07-01` selects the identity through the volume's
  `userManagedIdentityClientId`. ACI depends on its identity and role assignment.
  Role propagation can still delay a first mount; do not fall back to keys.
- No storage account key or Key Vault key reference is supplied to the volume.
  Broker authentication and Log Analytics diagnostics are separate and unchanged.

The host performs SMB authentication; no mount helper or credential refresh
process is added to the feeder image. SMB must permit Kerberos, and the ACI
host must be able to reach Azure Files. Existing storage firewall restrictions
are not changed by this tool.

Only unconditional templates with one dedicated canonical state account and
Linux ACI groups are supported. Other topologies fail explicitly. Stateful
sources must not copy a stateless template's storage removal.

## Sources and validation

- [Azure Files managed identities](https://learn.microsoft.com/azure/storage/files/files-managed-identities)
  documents SMB OAuth, the required role and client behavior.
- [Stable ACI managed-identity mount example](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/containerinstance/resource-manager/Microsoft.ContainerInstance/ContainerInstance/stable/2026-07-01/examples/ContainerGroupsCreateOrUpdateManagedIdentityAzureFileshare.json)
  uses `userManagedIdentityClientId`. The ARM reference currently spells this
  `userAssignedIdentityClientId`. The service team confirmed in
  [Azure/azure-rest-api-specs#47379](https://github.com/Azure/azure-rest-api-specs/pull/47379#issuecomment-6641081961)
  that the latter spelling was never supported; keep the REST field. The
  documentation discrepancy is tracked in
  [Azure/azure-rest-api-specs#48501](https://github.com/Azure/azure-rest-api-specs/issues/48501).
- [Storage account reference](https://learn.microsoft.com/azure/templates/microsoft.storage/2025-08-01/storageaccounts)
  defines SMB OAuth settings.
- [Azure Files SMB settings](https://learn.microsoft.com/azure/storage/files/files-smb-protocol#smb-protocol-settings)
  documents authentication defaults and Kerberos-only configuration.
- [Share-permission propagation](https://learn.microsoft.com/azure/storage/files/storage-files-identity-assign-share-level-permissions#share-level-permissions-for-specific-microsoft-entra-users-or-groups)
  usually takes up to 30 minutes and sometimes longer. `dependsOn` establishes
  management-plane ordering, not data-plane authorization readiness.

For a controlled first-mount test, provision the account, share, identity and
role separately from ACI, allow propagation, and retain those same prerequisites
across attempts. The first two probes ended after only 15.75 and 7.71 minutes
from role assignment. The third allowed 35 minutes before ACI creation and
then observed mounting for 15 minutes; it still failed before application
startup. Successful ticket requests narrow this result to a later stage, but
do not prove SMB share authorization or TCP 445 connectivity. Obtain ACI
host-side CIFS/SMB diagnostics rather than changing feeder dependencies,
broadening roles or enabling keys. AppLens and Resource Health reported that
they do not support this ACI resource type.

Run `python -m pytest tools\tests\test_aci_files_identity.py` and
`pwsh tools\validate-arm-templates.ps1 -FeederSlug <source>`.
Static validation does not establish that the target region's ACI host supports
the new mount. Before release, deploy in an isolated resource group, observe a
write and a subsequent restart reading the same file with Shared Key disabled,
then verify the actual feeder still emits and saves acknowledged checkpoints.
Keep deployment coordinates and evidence outside Git. Never clear existing
checkpoint files to make the test pass.
