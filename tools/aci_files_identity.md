# ACI state volumes with Azure Files managed identity

`aci_files_identity.py` converts existing canonical ACI state templates to
SMB managed-identity mounts. It retains storage account names, file shares,
mount paths, state-file settings and existing broker identities. It does not
change event contracts or feeder code.

> Candidate deployment path, not release acceptance. All six full native USGS
> templates passed Azure ARM validation with Shared Key disabled. Three initial
> probes failed to mount. A subsequent supported Linux control mounted the
> share, wrote and remounted/read its marker; ACI then reported
> `SuccessfulMountAzureFileVolume` and completed its write against the same
> account and identity. The earlier failure was not reproduced in this control,
> and its cause remains unproven. Further tests failed standalone cold-share
> startup and the native/WQ mounts. IV delivered 51 schema-validated Service
> Bus events across all four required families and read its persisted
> checkpoint after the actual ACI Restart API. This successful IV path does
> not establish reliable cold startup or acceptance of every template.

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

The subsequent control used Ubuntu 24.04 with Microsoft's `azfilesauth` and
CIFS client. It completed write/fsync/remount/read with the same keyless
account and identity later supplied to ACI. A separate stateless ACI resolved
the service endpoint and connected to TCP 445. The managed-volume ACI then
reported a successful mount and completed the application write, without
changing the candidate's authentication configuration or feeder dependencies.
New resources, placement and prior Linux share access differ from the failed
probes; the control does not identify which difference matters, prove that a
VM is needed, or justify an NFS migration. Storage logs verify the Linux
control's SMB operations, but the recovered snapshot contains no ACI-phase
requests. Keep diagnostic collection open long enough to observe the expected
requests before deleting its workspace.

Further November 25 verification used a fresh share without Linux access.
After at least 35 minutes for direct roles, ACI failed its additional
20-minute mount window. Diagnostics remained available for another 15 minutes:
23 HTTPS OAuth `GetKerbTicket` operations succeeded, but no SMB rows appeared.
Write/fsync and generic marker restart-read were unreachable.

Separate fresh stacks used digest-pinned current AMQP images and Entra-only
Service Bus authentication. Native and WQ groups reached deployment timeout
with repeated `FailedMountAzureFileVolume` events and never started their
feeders. IV ran as UID 10001, emitted all four required reference/telemetry
families, passed payload/envelope validation on 51 consumed events and saved
a checkpoint. A test-only hold-open wrapper kept its one-shot group Running
for the actual Restart API; the restarted process read the existing checkpoint
and completed another feeder cycle. The initial restart request against its
completed one-shot group returned `ContainerGroupStopped`; that harness error
was corrected without changing the feeder, identity, image or state path.
All owned cloud resources were removed and absence independently verified.
The contrasting outcomes do not identify the failed hosts' mount cause.

Run `python -m pytest tools\tests\test_aci_files_identity.py` and
`pwsh tools\validate-arm-templates.ps1 -FeederSlug <source>`.
Static validation does not establish that the target region's ACI host supports
the new mount. Before release, deploy in an isolated resource group, observe a
write and a subsequent restart reading the same file with Shared Key disabled,
then verify the actual feeder still emits and saves acknowledged checkpoints.
Keep deployment coordinates and evidence outside Git. Never clear existing
checkpoint files to make the test pass.
