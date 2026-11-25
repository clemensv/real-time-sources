# ACI checkpoints with Azure Files managed identity

`aci_files_identity.py` converts existing canonical ACI state templates to
managed-identity HTTPS checkpoints by default. It retains storage account names,
file shares, share-relative checkpoint paths and existing broker identities.
The USGS runtime supplies the corresponding `azure-files-rest` backend.
No event contract or generated producer changes are required.

> HTTPS removes the dependency on the ACI host's SMB mount. It does not fix
> or explain the host defect. Fresh-share write/read, actual Restart API
> readback and acknowledged feeder delivery are separate acceptance gates.
> Their current verdicts are in the
> [USGS migration ledger](../feeders/USGS-WATERSERVICES-MIGRATION-LEDGER.md).

```powershell
python tools\aci_files_identity.py feeders\<source>\azure-template.json
```

Pass all template paths to convert a source's transport variants together.
The tool validates every input before writing any template. Reapplying it
produces the same JSON. Run it after ordinary ARM generation; the native USGS
`generate-template.ps1` includes this step.

Use `--mode smb` only for the explicit legacy mount variant. The Python
`configure(template)` API retains its SMB default for existing callers;
`configure(template, mode="azure-files-rest")` selects HTTPS.

## Resources and permissions

- `allowSharedKeyAccess=false` remains mandatory. No key is read or supplied.
- A dedicated user-assigned managed identity is attached to ACI for state.
  Existing Event Grid or Service Bus publisher identities remain attached.
- HTTPS uses **Storage File Data Privileged Contributor**
  (`69566ab7-960f-475b-8e7c-b3118f30c6bd`) on the dedicated state account.
  Azure Files OAuth requires backup intent; the SDK sets `token_intent="backup"`.
  This permission bypasses file ACLs. Do not use the account or identity for
  unrelated data.
- REST templates remove Azure Files host volumes and their mounts. The runtime
  reads the account's service-issued HTTPS endpoint from ARM configuration and
  selects `ManagedIdentityCredential` with the explicit state client ID.
  Neither SAS nor a delegated user token is a storage fallback.
- Role assignment dependencies establish management-plane ordering only.
  Allow data-plane propagation before first startup; do not interpret an
  authorization failure as an absent checkpoint.
- Incremental deployment does not remove old SMB role assignments. After
  confirming the REST cutover, explicitly remove the superseded SMB MI Admin
  assignment for the dedicated identity. Do not remove unrelated broker roles.

### Runtime configuration and persistence

| Variable | Meaning |
|---|---|
| `STATE_BACKEND` | `local` by default; explicit `azure-files-rest` selects HTTPS. |
| `STATE_FILE` | Existing absolute logical checkpoint path, under the preserved root. |
| `STATE_AZURE_FILES_ROOT` | Former mount root; used only to derive the share-relative path. |
| `STATE_AZURE_FILES_ACCOUNT_URL` | Service-issued HTTPS account endpoint, without credentials or query parameters. |
| `STATE_AZURE_FILES_SHARE` | Existing dedicated share name. |
| `STATE_AZURE_FILES_CLIENT_ID` | Explicit dedicated user-assigned managed identity client ID. |

An existing `/mnt/bridge-state/checkpoint.json` with root
`/mnt/bridge-state` still names `checkpoint.json` in the same share.
JSON layout and dedupe history are preserved. A missing file is a first run;
missing shares, authentication errors and corrupt JSON fail explicitly.
Writes serialize before upload, stage a unique sibling file and atomically
rename it over the checkpoint. A failed write does not advance in-memory state.
Use **one writer per checkpoint**: this backend does not provide distributed
locking, and concurrent writers can overwrite each other's state.

HTTPS checkpoint support does not mount enrollment files, TLS certificates
or other application inputs. Supply those separately as local readable files.
Fabric notebooks explicitly use `STATE_BACKEND=local` for OneLake state.

### Optional SMB variant

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

For the default REST path, use the Azure Files
[OAuth REST authorization](https://learn.microsoft.com/azure/storage/files/authorize-oauth-rest)
and [Rename File](https://learn.microsoft.com/rest/api/storageservices/rename-file)
contracts. Atomic rename applies to SMB shares accessed through HTTPS, not NFS.

Run `python -m pytest tools\tests\test_aci_files_identity.py` and
`pwsh tools\validate-arm-templates.ps1 -FeederSlug <source>`.
Static validation does not establish data-plane acceptance. Before release,
deploy in an isolated resource group, observe a
write and a subsequent restart reading the same file with Shared Key disabled,
then verify the actual feeder still emits and saves acknowledged checkpoints.
Keep deployment coordinates and evidence outside Git. Never clear existing
checkpoint files to make the test pass.
