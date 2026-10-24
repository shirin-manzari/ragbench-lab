# ragbench-lab — progress

Last updated: 2026-10-19 (Asia/Tehran).

## 2026-10-19 — v4 analysis, archives and live dashboard verified

B50.4 done for the authorized expansion. No additional model requests occurred.
Raw archive `artifacts/archives/ragbench-core-v4-50.zip` independently verified:
236 files, 1,539,518,473 bytes, SHA
`d913eb355f56a6143687341d1600572e7abd28265f521392458413528958cd68`.
All six run families passed complete hash-chain/matrix/control checks: Stage A
9,000/18,000; v4 main 7,200; baselines 1,200; development gates 144/24. Historical
v1/v2/v3 aggregates were not imported. Exact saved local measurement source is
archived under its revision/fingerprint; source-snapshot support was the only
runtime source change and does not change runner behavior or measurements.

Paired report `reports/stage-b-analysis-v4-50` has 8,400 observations, 100 question
units, 56 cells and 220 contrasts; report SHA
`216853d86240bc842f175d6e9df8cdd6249ca4766cf27db0e1bd48dd78ec8ad2`.
Analysis retains declared 2,000-draw paired source-cluster/bootstrap sensitivity
methods, with 14 SQuAD and 50 Hotpot clusters. Independent point/table/contrast/
macro/CSV/raw-link/provenance checks passed; this checker verifies interval shape,
while numerical bootstrap replay is checked separately below. Six SVG/PDF plots
passed independent stage/evidence arithmetic, vector structure and file checks.
Proofs `artifacts/stage-b-{analysis,figures}-verification-v4-50.json`.
Short measured findings/limits: `reports/stage-b-analysis-v4-50/RESULTS.md`.

Dashboard snapshot `reports/dashboard-snapshot-v4-50` contains four separate run
views, 176 cells and 2,920 examples. Independent checker verified every saved
question, answer score, packed source offset, request link, aggregate/interval and
new Stage A vector bar; proof `artifacts/dashboard-snapshot-verification-v4-50.json`.
Read-only viewer PID 42814 is running at http://127.0.0.1:8050; page, Dash layout
and dependencies all returned HTTP 200. No timed writer is active. Old v3 snapshot,
reports, public results and archives remain unchanged; this viewer selects v4.

Fresh isolated local-checkout replay extracted the pinned prepared inputs and
v4 records and recomputed the complete paired analysis. Observations, cluster
mapping, cells.csv and contrasts.csv matched byte-for-byte; all report fields
except analysis provenance/hash matched, including all intervals. All 43 focused
archive/local-source/analysis/figure tests passed in that extracted workspace.
Proof `artifacts/analysis-replay-verification-v4-50.json`; log
`artifacts/analysis-replay-v4-50.log`. Temporary checkout removed by its own
TemporaryDirectory cleanup. Existing installed environment used; no fresh
installation, model rerun or cross-platform replication claimed.

Companion package `artifacts/archives/ragbench-analysis-v4-50.zip` contains current
source, specs, local validation, report, figures, snapshot and replay proof:
246 files, 14,860,363 bytes, SHA
`cbec32a45b5bd729572b3d7db639cf411e380fad797d822caf47ffb612de9fec`.
Fresh-process member verification and exact raw companion binding passed; proof
`artifacts/analysis-package-independent-verification-v4-50.json`. Raw and overlay
are immutable local artifacts; this completion note/protocol update is newer.

Relevant local checks: 3 new saved-source tests + 11 archive + 14 analysis + 15
figure tests passed; 45 dashboard tests passed in isolated viewer environment
(core environment skipped 31 optional viewer cases). Eight checkout groups passed.
Ruff for changed source/new tests/replay/package helpers and git diff --check passed;
staged diff empty. README/deep dive/architecture and PLAN/protocol updated locally.
No staging, commit, push, public publishing or off-device backup. V4 qualitative
case review and extended narrative synthesis remain optional and unproduced.
Next smallest task: user review of the v4 report/dashboard and backup of the two
local archives; no further benchmark compute is required for this expansion.

## 2026-10-19 — separate v4 archive and analysis in progress

User requested the next step after completed main/baseline verification. Declared
new archive, analysis, figure and dashboard protocols under `configs/*-v4-50.json`
before inspecting v4 aggregates. Reuse the existing paired source-cluster methods,
2,000 bootstrap draws, seed and repetitions; explicitly disclose post-results
expansion and exclude historical aggregate pooling. Old outputs remain immutable.

Archive inspection found committed-source-only snapshots could not reproduce the
recorded local v4 source. Before editing, copied all 56 fingerprinted source/config/
dependency inputs to `artifacts/measurement-source-v4-50`, verified exact SHA
`1c6592262a4518917fef328a89946e8609e4f528a3b28bdcefa73234e5f54237`.
Added explicit local_source_snapshots specification support to archiving.py:
only a declared revision/fingerprint pair can select a saved tree, which must
reproduce the exact measurement hash. No implicit current-source substitution.
Clean Git snapshot path remains supported; changed/missing/extra/symlinked source
is rejected. Three focused local-source tests and 11 existing archive tests passed;
14 analysis and 15 figure tests passed. Ruff passed changed source/new tests.
Initial snapshot helper lacked PYTHONPATH and failed before writes; rerun with
PYTHONPATH=src verified and saved the exact source. No measurements or identities
were rewritten, and no model requests launched. Raw archive audit/build is running:
`artifacts/archive-build-v4-50.log`; output `artifacts/archives/ragbench-core-v4-50.zip`.
Next: verify archive, compute/check separate paired report and figures, then export
and verify `reports/dashboard-snapshot-v4-50`. B50.4 remains in_progress.

## 2026-10-19 — all 1,200 baseline requests complete and verified

Baseline evaluation finished at 16:30:04 Asia/Tehran (13:00:04 UTC), about
39 minutes 7 seconds after worker launch. All 1,200/1,200 requests succeeded,
with zero request/setup failures, zero remaining and a zero worker exit code.
Supervisor verified all records, baseline controls, paired inputs and unchanged
execution/source identity before writing the saved proof:
`artifacts/baseline-evaluation-v4-50-operations/verified-summary.json`.
Run `9f935b7e-70b8-4a2f-a106-d77e4d2f9614`; manifest SHA
`d8e80942498d31c3858b194f786d15eec231a0c5733497269c06552e9538fc51`.
Dedicated backend 32126 stopped and supervisor exited; writer lock is absent.

Status checks inspected lifecycle, final request output, saved proof and lock.
PLAN/protocol updated. All 8,400 v4 evaluation measurements are now complete:
7,200 main plus 1,200 separate baselines. No pooling with historical studies.
B50.4 stays in_progress because separate v4 archive/analysis and dashboard export
remain pending. No further compute, analysis/export or dashboard launch started;
no source/scientific settings changed, staging, commit or push.
Next smallest task: prepare the separate v4 archive/analysis specifications.

## 2026-10-19 — baseline evaluation started: bounded 1,200 requests

User requested the next step after the 1,200 baseline requests and estimated
37–50 minute runtime were proposed. Supervisor reverified complete main records,
unchanged frozen baseline plan, current source/environment and the fresh compatible
24-request baseline development gate before starting compute. Gate SHA
`207380fba62aed35fed4ba136d197cf4e848d26dd4222c8fc75ea83d81a97267`.

Ignored helper `artifacts/run-baselines-v4-50.py` passed Ruff after a line wrap.
Supervisor 32114 launched dedicated backend 32126 and worker 32129 at 15:50:58
Asia/Tehran (12:20:58 UTC). New output `runs/baseline-evaluation-v4-50`;
CLI uses evaluation mode, the fresh gate and `--max-requests 1200`, with no retry
flag. Stop at first failure or completion; 90-minute safety bound and cleanup.
Operations/authorization: `artifacts/baseline-evaluation-v4-50-operations/`;
startup: `artifacts/baseline-evaluation-v4-50-startup.log`. Supervisor writes
`verified-summary.json` only after checking all 1,200 records and then shuts down
its dedicated backend. No automatic next session, analysis/export or viewer launch.
No source/dependency/model/scientific setting changes; v3 and all main records
preserved. PLAN and protocol updated; B50.4 remains in_progress. No staging,
commit or push. Next: verify baseline completion before separate v4 archive/analysis.

## 2026-10-19 — fresh baseline development gate passed: 24/24

Dedicated worker 31411 completed 24 diagnostic requests with zero request/setup
failures. Supervisor 31387 verified all saved baseline input, cache, token-count,
resource, paired-context and provenance checks, plus the compatible baseline gate.
Proof: `artifacts/baseline-validation-v4-50-operations/verified-summary.json`.
Run `16117b1b-dc7e-4119-9a12-48316b4f3f8c`, manifest SHA
`207380fba62aed35fed4ba136d197cf4e848d26dd4222c8fc75ea83d81a97267`.
Worker started 15:41:59 Asia/Tehran; proof and backend shutdown 15:43:44.
Dedicated backend 31408 stopped; no held-out follow-on or retry launched.

Measured mean request wall 1.796s and total block setup 45.954s project
about 36.7 minutes for 1,200 evaluation baselines. This is an estimate
from two development questions; held-out contexts may take longer. Protocol and
PLAN updated; B50.4 stays in_progress. Helper Ruff and git diff whitespace checks
passed; staged diff is empty. No source/settings changes, commit or push.
Next: explicitly bounded 1,200-request baseline evaluation using this fresh gate,
then separate v4 archive/analysis; no evaluation allowance inferred from this gate.

## 2026-10-19 — baseline plan frozen; fresh development gate starting

User approved the next step after the 24-request development check was proposed.
Created `manifests/stage-b-baselines-v4-50.json` using the real baseline-plan CLI;
all 7,200 saved parent rows were verified before freezing the separate 1,200-slot
plan. Plan SHA `68782afb9fa238f73cec78183f3f31c75c53be4cac7a6415cc99b4bd00ee8525`,
parent records SHA `b206dd2228fa8f814d1e738157eb569a4709b0e1157e8b8da2d67a95d4325c81`.
Prepared ignored supervisor `artifacts/validate-baselines-v4-50.py`: fresh paths,
24 diagnostic requests only, no retry or held-out follow-on, dedicated pinned
backend, first-failure stop and 20-minute safety bound with cleanup. Ruff passed
after import sorting. Check logs/proof: `artifacts/baseline-validation-v4-50-operations/`.
B50.4 stays in_progress; no source/scientific settings changed. Next: verify the
24-request gate and measured runtime before a separately bounded baseline session.

## 2026-10-19 — all 7,200 main requests complete and verified

Final session completed its 700 new requests successfully. Worker exited zero at
15:28:48 Asia/Tehran; final checkpoint verified at 15:29:02 (11:59:02 UTC).
All 7,200/7,200 main requests succeeded, with zero request/setup failures and zero
remaining. Supervisor verified the complete saved records and unchanged manifest,
then stopped dedicated backend 18009 and exited. Writer lock is absent.
Proof: `artifacts/stage-b-main-v4-50-session-027/verified-checkpoint-7200.json`;
run `619b1390-3d64-489a-9f53-657f64a716c9`, manifest SHA
`415d11324f803f0c7c4e847d92ee98c8839c6410dc5d35db917d3d1bc1bbc9e3`.

Checks: inspected lifecycle tail, final request output and saved checkpoint;
confirmed clean worker/backend/supervisor shutdown and absent writer lock.
Updated protocol and PLAN status. B50.4 remains in_progress: the 1,200 separate
baseline requests, their fresh 24-request development gate, and v4 archive/analysis
are pending. No baseline compute, dashboard restart or follow-on session launched.
No source/scientific settings changed; no staging, commit or push.
Next smallest task: freeze the separate baseline plan against the completed v4
parent, then obtain a bounded allowance for its fresh development gate.

## 2026-10-19 — final main session started: 700 attempts, targeting 7,200

User explicitly requested final 700 main requests. Stopped only the verified
read-only dashboard PID 17865 before timed work. Supervisor confirmed clear
ports/no active writers and reverified all 6,500 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`bf9497e5bba74f61ee2dbed76f03c78fad2ca5ed0d1307bc09f25fb7505aabbd`.

Local helper `artifacts/resume-stage-b-v4-final-700.py` passed Ruff. Reviewed
700-attempt bound, 6,500-to-7,200 calculation and final completion/zero-remaining
guards. Supervisor 18001 launched dedicated backend 18009 and worker 18012
at 2026-10-19 14:09:41 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 700`, no retry flag. Stop-on-failure and existing
90-minute safety interrupt preserve records. No automatic continuation, baselines,
export regeneration or dashboard restart. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-027/`; startup log:
`artifacts/stage-b-v4-final-700-startup.log`. Supervisor writes
`verified-checkpoint-7200.json` only after complete 7,200-slot success verification,
then stops its dedicated backend. Completion not yet claimed. Protocol status
updated; B50.4 remains in_progress because baselines/archive/analysis are pending.
No source/dependency/model/scientific setting/frozen manifest changes; no staging,
commit or push. Next: verify completed main records, then prepare separate
baseline parent plan and its own development gate under a separate allowance.

## 2026-10-19 — 6,500 main successes verified; twenty-sixth session paused

Session twenty-six completed at 13:52:50 Asia/Tehran (10:22:50 UTC), about
55 minutes 26 seconds after worker launch. All 500 new attempts succeeded:
6,500/7,200 total, 700 remaining, zero request/setup failures. Supervisor verified
the full saved chain/request/pairing controls and unchanged evaluation identity;
proof `artifacts/stage-b-main-v4-50-session-026/verified-checkpoint-6500.json`.
Dedicated backend 6795 stopped; writer lock is absent. Status inspection confirmed
the checkpoint and clean supervisor exit. No next session or baselines launched.
Protocol status updated; B50.4 remains in_progress. No source, dependencies,
scientific settings, staging, commits or pushes changed. Next: another explicitly
bounded session for remaining main work; stop the viewer before timed work.

## 2026-10-19 — twenty-sixth main session started: 500 attempts, targeting 6,500

User requested next 500. Supervisor reverified all 6,000 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`dbcf28dbd2243d8fbc5f64913d8d9eb04850b03065ee026b37abee8790201cfd`.

Local helper `artifacts/resume-stage-b-v4-to-6500.py` passed Ruff; reviewed CLI
bound, starting count, target and new-attempt calculation for the 500 allowance.
Supervisor 6767 launched dedicated backend 6795 and worker 6803
at 2026-10-19 12:57:24 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 500`, no retry flag. Target: 6,500 successes;
no automatic next session or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-026/`; startup log:
`artifacts/stage-b-v4-resume-to-6500-startup.log`. Supervisor writes
`verified-checkpoint-6500.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — 6,000 main successes verified; twenty-fifth session paused

Session twenty-five completed at 12:49:50 Asia/Tehran (09:19:50 UTC), about
22 minutes 22 seconds after worker launch. All 200 new attempts succeeded:
6,000/7,200 total, 1,200 remaining, zero request/setup failures. Supervisor verified
the full saved chain/request/pairing controls and unchanged evaluation/source
identity, then wrote
`artifacts/stage-b-main-v4-50-session-025/verified-checkpoint-6000.json`.
Dedicated backend 2336 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-19 — twenty-fifth main session started: 200 attempts, targeting 6,000

Previous session completed 12:22:06 Asia/Tehran with 5,800 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-024/verified-checkpoint-5800.json`.
User requested next 200. Supervisor reverified all 5,800 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`bff725a29b7933bfb97c50718fabafe15ee0fd4cea3781885cc5658458556678`.

Local helper `artifacts/resume-stage-b-v4-to-6000.py` passed Ruff. Supervisor
2322 launched dedicated backend 2336 and worker 2339 at
2026-10-19 12:27:28 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 6,000 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-025/`; startup log:
`artifacts/stage-b-v4-resume-to-6000-startup.log`. Supervisor writes
`verified-checkpoint-6000.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — twenty-fourth main session started: 200 attempts, targeting 5,800

Previous session completed 11:52:46 Asia/Tehran with 5,600 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-023/verified-checkpoint-5600.json`.
User requested next 200. Supervisor reverified all 5,600 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`bf39c470cd7369eb56f9f63b078025cb7618a8b4724cf08a527b16f6679db968`.

Local helper `artifacts/resume-stage-b-v4-to-5800.py` passed Ruff. Supervisor
97920 launched dedicated backend 97934 and worker 97937 at
2026-10-19 12:01:15 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 5,800 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-024/`; startup log:
`artifacts/stage-b-v4-resume-to-5800-startup.log`. Supervisor writes
`verified-checkpoint-5800.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — twenty-third main session started: 200 attempts, targeting 5,600

Previous session completed 11:21:09 Asia/Tehran with 5,400 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-022/verified-checkpoint-5400.json`.
User requested next 200. Supervisor reverified all 5,400 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`b0bc222588ee470f2575cd0856d3c0e8d4265aeceda7c5b3cb7f6d7567605dac`.

Local helper `artifacts/resume-stage-b-v4-to-5600.py` passed Ruff. Supervisor
93643 launched dedicated backend 93657 and worker 93660 at
2026-10-19 11:31:23 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 5,600 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-023/`; startup log:
`artifacts/stage-b-v4-resume-to-5600-startup.log`. Supervisor writes
`verified-checkpoint-5600.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — twenty-second main session started: 200 attempts, targeting 5,400

Previous session completed 10:48:22 Asia/Tehran with 5,200 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-021/verified-checkpoint-5200.json`.
User requested next 200. Supervisor reverified all 5,200 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`67937849aa15e062b3b1ea6367355411692267ed46fcda9913e26f3332979112`.

Local helper `artifacts/resume-stage-b-v4-to-5400.py` passed Ruff. Supervisor
89141 launched dedicated backend 89156 and worker 89159 at
2026-10-19 10:59:05 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 5,400 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-022/`; startup log:
`artifacts/stage-b-v4-resume-to-5400-startup.log`. Supervisor writes
`verified-checkpoint-5400.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — twenty-first main session started: 200 attempts, targeting 5,200

User requested next 200. Supervisor reverified all 5,000 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`ee411fd9932884c796b00f6e600f525c46f8450dbc72ed29bb6b20b076ab945c`.

Local helper `artifacts/resume-stage-b-v4-to-5200.py` passed Ruff. Supervisor
84983 launched dedicated backend 84997 and worker 85001 at
2026-10-19 10:28:32 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 5,200 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-021/`; startup log:
`artifacts/stage-b-v4-resume-to-5200-startup.log`. Supervisor writes
`verified-checkpoint-5200.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — 5,000 main successes verified; twentieth session paused

Session twenty completed at 10:20:51 Asia/Tehran (06:50:51 UTC), about 22 minutes
41 seconds after worker launch. All 200 new attempts succeeded: 5,000/7,200 total,
2,200 remaining, zero request/setup failures. Supervisor verified the full saved
chain/request/pairing controls and unchanged evaluation/source identity, then
wrote `artifacts/stage-b-main-v4-50-session-020/verified-checkpoint-5000.json`.
Dedicated backend 80371 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-19 — twentieth main session started: 200 attempts, targeting 5,000

User requested next 200 while previous session was at 4,797 successes. Waited
for its clean 4,800-success checkpoint, absent writer lock and supervisor shutdown
before launching another writer. Previous session verified at
2026-10-19 09:57:45 Asia/Tehran, with zero request/setup failures; proof:
`artifacts/stage-b-main-v4-50-session-019/verified-checkpoint-4800.json`.

New supervisor reverified all 4,800 chain/request/paired controls, unchanged
source/environment/study identity and the complete compatible development gate.
Parent records SHA `e495146875ae441a6571e354dc249d0396e491f1e477763d67cd580eb5140ad0`.
Local helper `artifacts/resume-stage-b-v4-to-5000.py` passed Ruff. Supervisor
80351 launched dedicated backend 80371 and worker 80374 at
2026-10-19 09:58:10 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 5,000 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-020/`; startup log:
`artifacts/stage-b-v4-resume-to-5000-startup.log`. Supervisor writes
`verified-checkpoint-5000.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — nineteenth main session started: 200 attempts, targeting 4,800

Previous session completed 09:27:24 Asia/Tehran with 4,600 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-018/verified-checkpoint-4600.json`.
User requested next 200. Supervisor reverified all 4,600 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`9a7f7168a1ed1f3a98b93c2b6c127831130f77a92ed5897f4cab7e7c6a9db2e9`.

Local helper `artifacts/resume-stage-b-v4-to-4800.py` passed Ruff. Initial launcher
contained an `openopen` typo and failed before creating a log/process; corrected
launcher started exactly one supervisor. Supervisor 76050 launched dedicated
backend 76064 and worker 76067 at
2026-10-19 09:34:57 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 4,800 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-019/`; startup log:
`artifacts/stage-b-v4-resume-to-4800-startup.log`. Supervisor writes
`verified-checkpoint-4800.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — eighteenth main session started: 200 attempts, targeting 4,600

Previous session completed 09:01:38 Asia/Tehran with 4,400 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-017/verified-checkpoint-4400.json`.
User requested next 200. Supervisor reverified all 4,400 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`ab495b69bce79c26283bb3f4d363c92a4b6d41c828737c58d0228fa03041e045`.

Local helper `artifacts/resume-stage-b-v4-to-4600.py` passed Ruff. Supervisor
71549 launched dedicated backend 71563 and worker 71566 at
2026-10-19 09:04:15 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 4,600 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-018/`; startup log:
`artifacts/stage-b-v4-resume-to-4600-startup.log`. Supervisor writes
`verified-checkpoint-4600.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — seventeenth main session started: 200 attempts, targeting 4,400

Previous session completed 08:23:27 Asia/Tehran with 4,200 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-016/verified-checkpoint-4200.json`.
User requested next 200. Supervisor reverified all 4,200 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`01212d35dae3e7e437105665d926cb1d98394f911d2dfe240c1e1026c4816c84`.

Local helper `artifacts/resume-stage-b-v4-to-4400.py` passed Ruff. Supervisor
67180 launched dedicated backend 67194 and worker 67197 at
2026-10-19 08:39:13 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 4,400 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-017/`; startup log:
`artifacts/stage-b-v4-resume-to-4400-startup.log`. Supervisor writes
`verified-checkpoint-4400.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — sixteenth main session started: 200 attempts, targeting 4,200

User requested next 200. Supervisor reverified all 4,000 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`f089b07be4f506453cc91364994f6e0d9d3dfb5d69844878d12d17b4aa024d30`.

Local helper `artifacts/resume-stage-b-v4-to-4200.py` passed Ruff; reviewed the
200-attempt bound and 4,000-to-4,200 checkpoint calculation. Supervisor 62448
launched dedicated backend 62462 and worker 62465 at
2026-10-19 08:00:18 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target: 4,200 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-016/`; startup log:
`artifacts/stage-b-v4-resume-to-4200-startup.log`. Supervisor writes
`verified-checkpoint-4200.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — 4,000 main successes verified; fifteenth session paused

Session fifteen completed at 01:24:26 Asia/Tehran on 19 October (21:54:26 UTC
on 18 October), about 55 minutes 53 seconds after worker launch. All 500 new
attempts succeeded: 4,000/7,200 total, 3,200 remaining, zero request/setup failures.
Supervisor verified the full saved chain/request/pairing controls and unchanged
evaluation/source identity, then wrote
`artifacts/stage-b-main-v4-50-session-015/verified-checkpoint-4000.json`.
Dedicated backend 52935 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-19 — fifteenth main session started: 500 attempts, targeting 4,000

User requested next 500. Supervisor reverified all 3,500 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`28dc2e32fc915730266028e902596ff0dfba7aa45a25e3c47b41af6484a0ea6d`.

Local helper `artifacts/resume-stage-b-v4-to-4000.py` passed Ruff; reviewed CLI
bound, starting count, target and new-attempt calculation for the 500 allowance.
Supervisor 52927 launched dedicated backend 52935 and worker 52938
at 2026-10-19 00:28:32 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 500`, no retry flag. Target: 4,000 successes;
no automatic next session or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-015/`; startup log:
`artifacts/stage-b-v4-resume-to-4000-startup.log`. Supervisor writes
`verified-checkpoint-4000.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-19 — 3,500 main successes verified; fourteenth session paused

Session fourteen completed at 00:21:33 Asia/Tehran on 19 October (20:51:33 UTC
on 18 October), about 32 minutes 7 seconds after worker launch. All 300 new
attempts succeeded: 3,500/7,200 total, 3,700 remaining, zero request/setup failures.
Supervisor verified the full saved chain/request/pairing controls and unchanged
evaluation/source identity, then wrote
`artifacts/stage-b-main-v4-50-session-014/verified-checkpoint-3500.json`.
Dedicated backend 47967 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-18 — fourteenth main session started: 300 attempts, targeting 3,500

Previous session completed 23:20:43 Asia/Tehran with 3,200 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-013/verified-checkpoint-3200.json`.
User requested next 300. Supervisor reverified all 3,200 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`e87cdfdd8fece6902663962f6d6ccbf5a95fc6696c4d9281b0b431ba2a9689ea`.

Local helper `artifacts/resume-stage-b-v4-to-3500.py` passed Ruff; reviewed CLI
bound, starting count, target and new-attempt calculation for the 300 allowance.
Supervisor 47953 launched dedicated backend 47967 and worker 47970
at 2026-10-18 23:49:25 Asia/Tehran. Same run and execution manifest retained;
CLI uses `--resume --max-requests 300`, no retry flag. Target: 3,500 successes;
no automatic next session or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-014/`; startup log:
`artifacts/stage-b-v4-resume-to-3500-startup.log`. Supervisor writes
`verified-checkpoint-3500.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — thirteenth main session started: 200 attempts, targeting 3,200

User requested next 200. Supervisor reverified all 3,000 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Parent records SHA
`d0afc6b3bdeed7f55a0ab4c224f9f27b76525b2b25219503e9a9e0449cbdb3cb`.

Local helper `artifacts/resume-stage-b-v4-to-3200.py` passed Ruff; reviewed the
200-attempt bound and 3,000-to-3,200 checkpoint calculation. Supervisor 43574
launched dedicated backend 43587 and worker 43591 at
2026-10-18 23:00:27 Asia/Tehran. Same run and immutable execution manifest retained.
CLI uses `--resume --max-requests 200`, no retry flag. Target: 3,200 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-013/`; startup log:
`artifacts/stage-b-v4-resume-to-3200-startup.log`. Supervisor writes
`verified-checkpoint-3200.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — 3,000 main successes verified; twelfth session paused

Session twelve completed at 22:43:57 Asia/Tehran (19:13:57 UTC), about 65 minutes
34 seconds after worker launch. All 600 new attempts succeeded: 3,000/7,200 total,
4,200 remaining, zero request/setup failures. Supervisor verified the full saved
chain/request/pairing controls and unchanged evaluation/source identity, then
wrote `artifacts/stage-b-main-v4-50-session-012/verified-checkpoint-3000.json`.
Dedicated backend 30892 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-18 — twelfth main session started: 600 attempts, targeting 3,000

User requested next 600. Supervisor reverified all 2,400 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before backend startup. Prior writer lock and dedicated ports
were clear. Parent records SHA
`aea7454cdb8fe66ebf8c6a0d9958a2f2f1124474972be6a60d25cd09e7245a85`.

Local helper `artifacts/resume-stage-b-v4-to-3000.py` passed Ruff; reviewed CLI
bound, starting count, target and new-attempt calculation for the 600 allowance.
Supervisor 30878 launched dedicated backend 30892 and worker 30896
at 2026-10-18 21:38:23 Asia/Tehran. Same main run and immutable manifest retained;
CLI uses `--resume --max-requests 600`, no retry flag. Target: 3,000 successes;
no automatic next session or baselines. Stop-on-failure and unchanged 90-minute
safety interrupt preserve failed/interrupted attempts. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-012/`; startup log:
`artifacts/stage-b-v4-resume-to-3000-startup.log`. Supervisor writes
`verified-checkpoint-3000.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — 2,400 main successes verified; eleventh session paused

Session eleven completed at 15:29:17 Asia/Tehran (11:59:17 UTC), about 23 minutes
36 seconds after worker launch. All 200 new attempts succeeded: 2,400/7,200 total,
4,800 remaining, zero request/setup failures. Supervisor verified the full saved
chain/request/pairing controls and unchanged evaluation/source identity, then
wrote `artifacts/stage-b-main-v4-50-session-011/verified-checkpoint-2400.json`.
Dedicated backend 25621 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-18 — eleventh main session started: 200 attempts, targeting 2,400

User requested next 200. Supervisor reverified all 2,200 saved chain/request/paired
controls, unchanged source/environment/study identity and the complete compatible
development gate before starting the backend. Parent records SHA
`3132065b42b821143f2f604d78350867f25b0189e2cc651f9a500d68ad4a2140`.

Local helper `artifacts/resume-stage-b-v4-to-2400.py` passed Ruff. Supervisor
25608 launched dedicated backend 25621 and worker 25624 at
2026-10-18 15:05:40 Asia/Tehran. Same run and immutable execution manifest retained.
CLI uses `--resume --max-requests 200`, no retry flag. Target: 2,400 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs and authorization:
`artifacts/stage-b-main-v4-50-session-011/`; startup log:
`artifacts/stage-b-v4-resume-to-2400-startup.log`. Supervisor writes
`verified-checkpoint-2400.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — 2,200 main successes verified; tenth session paused

Session ten completed at 14:20:58 Asia/Tehran (10:50:58 UTC), about 21 minutes
48 seconds after worker launch. All 200 new attempts succeeded: 2,200/7,200 total,
5,000 remaining, zero request/setup failures. Supervisor verified the full saved
chain/request/pairing controls and unchanged evaluation/source identity, then
wrote `artifacts/stage-b-main-v4-50-session-010/verified-checkpoint-2200.json`.
Dedicated backend 21425 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-18 — tenth main session started: 200 attempts, targeting 2,200

User requested next 200. Before launch supervisor reverified all 2,000 saved
chain/request/paired controls, unchanged source/environment/study identity and
the complete compatible development gate. Parent records SHA
`032f7002e526fa8700230204c69f522a1c1c4e04e823cc6366fe635c6c9905b4`.

Local helper `artifacts/resume-stage-b-v4-to-2200.py` passed Ruff; reviewed the
reduced 200-attempt bound and 2,000-to-2,200 checkpoint calculation. Supervisor
21413 launched dedicated backend 21425 and worker 21428 at
2026-10-18 13:59:09 Asia/Tehran. Same run and immutable manifest retained.
CLI uses `--resume --max-requests 200`, no retry flag. Target: 2,200 successes;
no automatic next session or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs/authorization:
`artifacts/stage-b-main-v4-50-session-010/`; startup log:
`artifacts/stage-b-v4-resume-to-2200-startup.log`. Supervisor writes
`verified-checkpoint-2200.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — 2,000 main successes verified; ninth session paused

Session nine completed at 13:57:29 Asia/Tehran (10:27:29 UTC), about 43 minutes
21 seconds after worker launch. All 400 new attempts succeeded: 2,000/7,200 total,
5,200 remaining, zero request/setup failures. Supervisor verified the full saved
chain/request/pairing controls and unchanged evaluation/source identity, then
wrote `artifacts/stage-b-main-v4-50-session-009/verified-checkpoint-2000.json`.
Dedicated backend 13405 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same run/manifest preserved;
no next session or baseline requests launched. Protocol status updated; B50.4
remains in_progress. No source/dependency/scientific setting changes or staging,
commit or push. Next: another explicitly bounded resume session if requested.

## 2026-10-18 — ninth main session started: 400 attempts, targeting 2,000

User requested next 400. Before launch supervisor reverified all 1,600 saved
chain/request/paired controls, unchanged source/environment/study identity and
the compatible complete development gate. No prior session remained active;
writer lock and dedicated ports were clear. Parent records SHA
`c2a85847f5a693abed6366e7ee7e7caaecefacb611bdce36330c5a67dc755e40`.

Local helper `artifacts/resume-stage-b-v4-to-2000.py` passed Ruff; reviewed CLI
bound, starting count, target and new-attempt calculation for the 400 allowance.
Supervisor 13393 launched dedicated backend 13405 and worker 13418
at 2026-10-18 13:14:07 Asia/Tehran. Same run/manifest retained;
CLI uses `--resume --max-requests 400`, no retry flag. Target: 2,000 successes;
no automatic next session or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Logs/authorization:
`artifacts/stage-b-main-v4-50-session-009/`; startup log:
`artifacts/stage-b-v4-resume-to-2000-startup.log`. Supervisor writes
`verified-checkpoint-2000.json` only after clean verification, then stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — 1,600 main successes verified; eighth session paused

Session eight completed at 12:45:42 Asia/Tehran (09:15:42 UTC), about 23 minutes
24 seconds after worker launch. All 200 new attempts succeeded: 1,600/7,200 total,
5,600 remaining, zero request/setup failures. Supervisor verified the full saved
chain/request/pairing controls and unchanged evaluation/source identity, then
wrote `artifacts/stage-b-main-v4-50-session-008/verified-checkpoint-1600.json`.
Dedicated backend 8733 stopped; writer lock is absent. Status inspection confirmed
the saved checkpoint and clean supervisor exit. Same main run/manifest preserved.
No next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/dependency/scientific setting changes or staging/commit/push.
Next: another explicitly bounded resume session if requested.

## 2026-10-18 — eighth 200-attempt main session started, targeting 1,600

Previous session completed 11:30:44 Asia/Tehran with 1,400 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-007/verified-checkpoint-1400.json`.
User requested next 200. Before launch supervisor reverified all 1,400 saved
chain/request/paired controls, unchanged source/environment/study identity and
the complete compatible development gate. Parent records SHA
`16e1f43ac090bf0eea5a015b2639d96668946ac6bb6ee2b520438628b314dce3`.

Local helper `artifacts/resume-stage-b-v4-to-1600.py` passed Ruff. Supervisor 8722
launched dedicated backend 8733 and worker 8736 at
2026-10-18 12:22:18 Asia/Tehran. Same run and execution manifest retained.
CLI uses `--resume --max-requests 200`, no retry flag. Target: 1,600 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Operation logs and authorization:
`artifacts/stage-b-main-v4-50-session-008/`; startup log:
`artifacts/stage-b-v4-resume-to-1600-startup.log`. Supervisor writes
`verified-checkpoint-1600.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — seventh 200-attempt main session started, targeting 1,400

Previous session completed 10:58:36 Asia/Tehran with 1,200 cumulative successes,
zero request/setup failures, released writer lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-006/verified-checkpoint-1200.json`.
User requested next 200. Before launch supervisor reverified all 1,200 saved
chain/request/paired controls, unchanged source/environment/study identity and
the complete compatible development gate. Parent records SHA
`8a62af1250bbf63a399cb2c6c43a3e7bc5fc599663303af114be263be5287563`.

Local helper `artifacts/resume-stage-b-v4-to-1400.py` passed Ruff. Supervisor 4209
launched dedicated backend 4217 and worker 4220 at
2026-10-18 11:07:38 Asia/Tehran. Same run/immutable execution manifest retained.
CLI uses `--resume --max-requests 200`, no retry flag. Target: 1,400 successes;
no automatic follow-on or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Operations, authorization and logs:
`artifacts/stage-b-main-v4-50-session-007/`; startup log:
`artifacts/stage-b-v4-resume-to-1400-startup.log`. Supervisor writes
`verified-checkpoint-1400.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — local architecture guide complete

D.4 done at user's request. Created `ARCHITECTURE.md` describing the current
implementation: CLI/configuration, dataset records and label isolation, indexes,
retrieval/reranking/context mapping, two-stage design, local generation and timing,
append-only persistence and gates, separate baselines, offline analysis/delivery,
viewer isolation and validation boundaries. Includes Mermaid component and request
sequence diagrams and links to implementing modules. Completed v3 is distinguished
from ongoing v4; no fixed live request count or unimplemented extension is claimed.

The existing `.gitignore` line 2 (`*.[mM][dD]`) already ignores the exact file;
no ignore-rule change needed. All local links resolve, Markdown diagram fences
and whitespace checks passed, and the document is untracked/unstaged. No tests
run for this documentation-only change. No source, dependency, scientific setting,
manifest or measurement changes; no new benchmark launches, commits or pushes.
The authorized 200-attempt session continues independently; B50.4 stays in_progress.
Next experiment task remains review of its 1,200-success checkpoint.

## 2026-10-18 — sixth 200-attempt main session started, targeting 1,200

Previous session completed 10:21:02 Asia/Tehran with 1,000 cumulative successes,
zero request/setup failures, released lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-005/verified-checkpoint-1000.json`.
User requested next 200. Before launch supervisor reverified all 1,000 existing
chain/request/paired controls, unchanged source/environment/study identity and
the complete compatible development gate. Parent records SHA
`aa8c93006acbe073515e13a911ece5755ca2bdbce65c7460617b36fea9df4767`.

Local helper `artifacts/resume-stage-b-v4-to-1200.py` passed Ruff. Supervisor 311
launched dedicated backend 327 and worker 330 at
2026-10-18 10:38:18 Asia/Tehran. Same main run and immutable execution manifest
retained. CLI uses `--resume --max-requests 200`, no retry flag. Target: 1,200
cumulative successes, no automatic follow-on or baselines. Stop-on-failure and
90-minute safety interrupt preserve records. Operation logs and authorization:
`artifacts/stage-b-main-v4-50-session-006/`; startup output:
`artifacts/stage-b-v4-resume-to-1200-startup.log`. Supervisor writes
`verified-checkpoint-1200.json` only after clean verification and stops its
backend. Completion not yet claimed. Protocol status updated; B50.4 remains
in_progress. No source/dependency/model/scientific setting/frozen manifest changes;
no staging/commit/push. Next: inspect checkpoint before further bounded work.

## 2026-10-18 — fifth 200-attempt main session started, targeting 1,000

Previous session completed 09:39:45 Asia/Tehran with 800 cumulative successes,
zero request/setup failures, released writer lock and stopped backend. Proof:
`artifacts/stage-b-main-v4-50-session-004/verified-checkpoint-800.json`.
User requested next 200. Before launch supervisor reverified all 800 saved
chain/request/paired controls, unchanged source/environment/study identity and
the linked complete development gate. Parent records SHA
`c4ce6051ff6f52f9a1b7c59190ef0d7e2ca2d1fa19471ba2217108a5dfdaa4bd`.

Local helper `artifacts/resume-stage-b-v4-to-1000.py` passed Ruff. Supervisor
96323 launched dedicated backend 96335 and worker 96338 at
2026-10-18 09:59:44 Asia/Tehran. Same main run and immutable execution manifest
retained. CLI uses `--resume --max-requests 200`, no retry flag. Target: 1,000
cumulative successes, no automatic follow-on or baselines. Stop-on-failure and
90-minute safety interrupt preserve failed/interrupted attempts. Operation logs
and authorization: `artifacts/stage-b-main-v4-50-session-005/`; startup log:
`artifacts/stage-b-v4-resume-to-1000-startup.log`. Supervisor will write
`verified-checkpoint-1000.json` only after clean verification, then stop its
backend. Completion not yet claimed. B50.4 remains in_progress; protocol status
updated. No source/dependency/model/scientific setting or frozen manifest changes;
no staging/commit/push. Next: inspect this checkpoint before further bounded work.

## 2026-10-18 — fourth 200-attempt main session started, targeting 800

Previous session completed at 23:39:54 Asia/Tehran on 17 October, with 600 total
successes, zero request/setup failures, released writer lock and stopped backend.
Saved proof: `artifacts/stage-b-main-v4-50-session-003/verified-checkpoint-600.json`.
User requested next 200. Before resume, supervisor reverified all 600 saved
chain/request/paired controls, unchanged source/environment/study identity and
the complete linked development gate. Parent records SHA
`8de0b3e05910a3808633e8cc3e7cf95a27d55da95e0c4bb4cea8153ae2b2184f`.

Local helper `artifacts/resume-stage-b-v4-to-800.py` passed Ruff. Supervisor 92115
launched dedicated backend 92125 and worker 92129
at 2026-10-18 09:18:00 Asia/Tehran. Same run
`619b1390-3d64-489a-9f53-657f64a716c9` and immutable execution manifest retained.
CLI uses `--resume --max-requests 200`, no retry flag. Target: 800 total successes;
no automatic next session or baselines. Stop-on-failure and 90-minute safety
interrupt preserve records. Proof/log directory:
`artifacts/stage-b-main-v4-50-session-004/`; startup output:
`artifacts/stage-b-v4-resume-to-800-startup.log`. Supervisor writes
`verified-checkpoint-800.json` only on clean verification and stops its backend.
Completion not yet claimed. Protocol status updated; B50.4 remains in_progress.
No source, dependencies, scientific settings or frozen manifests changed; no
staging/commit/push. Next: inspect this checkpoint before further bounded work.

## 2026-10-17 — third 200-attempt main session started, targeting 600

User requested next 200. Local helper `artifacts/resume-stage-b-v4-to-600.py`
passed Ruff. First launch request was rejected because automatic permission
review did not finish before its deadline; it did not launch a process. The tool
explicitly permitted one retry, and that retry succeeded without changing scope.

Supervisor revalidated all 400 existing chain/request/paired records, unchanged
source/environment/study identity and the matching development gate. Parent
records SHA `f7b4d0c786102abfbe337b4982cc529715fb6813d18150c72d34f9672443f14c`.
Supervisor 86617 launched dedicated backend 86628 and worker 86631 at
23:18:44 Asia/Tehran (19:48:44 UTC). Existing run and manifest retained;
CLI uses `--resume --max-requests 200`, no retry flag. Target 600 total successes;
no automatic next session or baselines. A 90-minute safety timeout and
stop-on-failure preserve interrupted/failed attempts.

Logs and launch authorization are under
`artifacts/stage-b-main-v4-50-session-003/`; startup log is
`artifacts/stage-b-v4-resume-to-600-startup.log`. Supervisor writes
`verified-checkpoint-600.json` only after a clean 600-success verification and
then stops its dedicated backend. Session completion is not yet claimed.
No source/dependency/model settings, old manifests or prior records rewritten.
No staging/commit/push. B50.4 remains in_progress; next inspect this checkpoint
before any further explicitly bounded work.

## 2026-10-17 — 400 main successes verified; second session paused

Second authorized 200-attempt session finished at 22:52:34 Asia/Tehran
(19:22:34 UTC), about 22 minutes 28 seconds after worker launch. All 200 new
attempts succeeded: 400/7,200 cumulative successes, 6,800 remaining, zero
request/setup failures. Checkpoint:
`artifacts/stage-b-main-v4-50-session-002/verified-checkpoint-400.json`.
Supervisor independently verified the full saved chain/request/pairing controls
and unchanged evaluation identity, then stopped dedicated backend 82375. Writer
lock is absent. Follow-up status inspection independently verified all 400 records,
the current implementation provenance and linked development gate. Same run ID
`619b1390-3d64-489a-9f53-657f64a716c9` and execution manifest
`415d11324f803f0c7c4e847d92ee98c8839c6410dc5d35db917d3d1bc1bbc9e3`.
No next session or baselines launched. Protocol status updated; B50.4 remains
in_progress. No source/settings/dependency edits, staging, commits or pushes.
Next: further explicitly bounded resume session if requested.

## 2026-10-17 — next 200 main attempts started, targeting 400

User requested next 200. Before launch, supervisor independently verified all
200 existing success records, their chain/request/paired controls, unchanged
source/environment/study identity and the matching stopped development gate.
Parent records SHA `024f1e3d2f35c0802011fc5299d54dfe463dcc2045cce9bd51b3e913caa3f1d9`.

Launched local `artifacts/resume-stage-b-v4-next-200.py`: supervisor 82350,
dedicated backend 82375, worker 82378. Started 22:30:06 Asia/Tehran (19:00:06 UTC).
Same run `619b1390-3d64-489a-9f53-657f64a716c9` and execution manifest retained;
CLI uses `--resume --max-requests 200` without retry flags. Target is 400 total
successes; no automatic next session or baseline launch. New operations directory
`artifacts/stage-b-main-v4-50-session-002/` holds authorization, parent checksum,
lifecycle, requests/backend logs and, only on clean pause, the future
`verified-checkpoint-400.json`. Startup log:
`artifacts/stage-b-v4-resume-to-400-startup.log`.

Stop-on-failure and a 90-minute safety timeout preserve failed/interrupted
attempts; the supervisor stops only its own backend. Source, model settings,
dependencies and frozen manifests are unchanged. Helper Ruff reported one E501
long authorization string; this is a formatting issue in the ignored supervisor,
not an experiment/runtime failure, and its launched contents are preserved.
No commits/pushes or staging. B50.4 remains in_progress; session completion is
not yet claimed. Next: verify this checkpoint before further bounded work.

First resumed live checkpoint: 203 cumulative successes, zero request/setup failures;
all saved chain/request controls independently verified. Evidence:
`artifacts/stage-b-main-v4-50-session-002/first-checkpoint.json`.

## 2026-10-17 — first 200 main requests verified; paused

The authorized first v4 main session finished 21:08:08 Asia/Tehran (17:38:08 UTC),
about 21 minutes 17 seconds after worker launch. All 200 attempts succeeded;
zero request/setup failures, 7,000/7,200 main slots remain. Supervisor verified
raw chains, request/pairing controls and unchanged evaluation/source identity,
wrote `artifacts/stage-b-main-v4-50-session-001/verified-checkpoint-200.json`,
then stopped dedicated backend 78285. Writer lock is absent; no automatic next
session or baseline launch. Independent status inspection revalidated all 200
records, the matching development gate and current implementation provenance.
Run ID `619b1390-3d64-489a-9f53-657f64a716c9`; execution manifest SHA
`415d11324f803f0c7c4e847d92ee98c8839c6410dc5d35db917d3d1bc1bbc9e3`.
B50.4 remains in_progress for the complete matrix; current session is done.
Protocol status updated. No source/dependency/measurement changes, staging,
commit or push. Next: another explicitly bounded resume session if requested.

## 2026-10-17 — first bounded 200-attempt main session started

User approved exactly one session of 200 main request attempts. B50.4 in_progress;
no automatic follow-on or retries. Local supervisor
`artifacts/start-stage-b-v4-main-200.py` passed Ruff. Before backend startup it
revalidated both prepared datasets and pinned assets/index manifests, current
source/environment provenance and the complete compatible 144-request gate.

Fresh output is `runs/stage-b-evaluation-v4-50`; operations/logs are under
`artifacts/stage-b-main-v4-50-session-001/`. Supervisor 78278 launched dedicated
backend 78285 and worker 78288 at
2026-10-17 20:46:51 Asia/Tehran (17:16:51 UTC). Exact CLI uses evaluation mode,
`--validation-run runs/phase7-validation-v4-50 --max-requests 200`, without resume
or retry flags. Entire frozen matrix remains 7,200 slots, with only this initial
200-attempt session authorized. No baseline launch is authorized.

The supervisor stops at the request bound or first failure, independently verifies
the resulting records/paired controls and unchanged source identity, writes
`verified-checkpoint-200.json` only on a clean 200-success pause, then stops its
own backend. It has a 90-minute safety timeout with interrupt/record preservation.
Startup log is `artifacts/stage-b-v4-main-200-startup.log`; lifecycle and exact
command/provenance are saved alongside worker/backend logs. No source, model,
dependency, experiment settings or previous run records changed. No commit/push;
staging remains empty. Session completion is not yet claimed. Next: inspect this
checkpoint before any further explicitly authorized session.

First main live checkpoint: 3 successes, zero request/setup
failures; saved prefix chain and request controls independently verified.
Run ID `619b1390-3d64-489a-9f53-657f64a716c9`; execution manifest SHA
`415d11324f803f0c7c4e847d92ee98c8839c6410dc5d35db917d3d1bc1bbc9e3`.
Evidence: `artifacts/stage-b-main-v4-50-session-001/first-checkpoint.json`.
This is a partial checkpoint, not completion of the 200-attempt session.

## 2026-10-17 — v4 development gate passed

B50.3 done. Validation finished at 18:10:18 Asia/Tehran (14:40:18 UTC), about
38 minutes 23 seconds after worker launch. All 144 development requests passed;
zero request/setup failures and zero remaining slots. Supervisor verified raw
chains, pairing, native/cache/resource controls, source/environment stability and
the full development gate, then stopped dedicated backend 74051. Writer lock is
absent. Summary: `artifacts/stage-b-validation-v4-50/verified-summary.json`.
Run ID `ffc1d0a8-0789-4550-a245-f56e128fde5c`; execution manifest SHA
`ab81373e9f592ef7022c6b1f73ab6d0651ade28fba63e9455e1563a4e18a6131`.

Measured development mean online latency is 5.417 seconds; mean per-request
cache isolation is 1.035 seconds. Peak sampled summed RSS is 5,627,707,392 bytes
(about 5.24 GiB), with the existing unified-memory/counter limitations. These
are development integration measurements, not held-out findings or a guaranteed
main runtime. Independent follow-up `validate_gate` and current implementation
provenance equality passed on status inspection. No main or baseline requests
launched automatically. Planning/protocol status updated; no source, dependencies,
scientific settings, commits or staging changed. Next smallest task: B50.4,
explicitly bounded fresh main session after allowance, preserving all prior runs.

## 2026-10-17 — bounded v4 development validation started

User explicitly approved the proposed 144-request development gate. B50.3 is
in_progress; no held-out allowance or baseline launch is implied.

- Added local supervisor `artifacts/start-stage-b-v4-validation.py`; Ruff passed.
  It checks fresh paths, no active writers, stopped dashboard/free dedicated port,
  exact v4 study identity and pinned backend version. It records current dirty
  source/environment provenance before startup and verifies it again at completion.
- Stopped only the verified dashboard process 69089 on port 8050. Launched
  supervisor 74047, dedicated backend 74051 and worker 74054. Validation started
  2026-10-17 17:31:55 Asia/Tehran (14:01:55 UTC); mode diagnostic, one development
  ID per dataset, all 48 conditions/144 blocks, `--max-requests 144`. New run path:
  `runs/phase7-validation-v4-50`. Historical studies and records remain unchanged.
- Authorization, exact command/provenance and lifecycle records are in
  `artifacts/stage-b-validation-v4-50/authorization.json` and `lifecycle.jsonl`;
  worker/backend logs are `requests.log` and `backend.log` in that directory.
  Startup output: `artifacts/stage-b-v4-validation-startup.log`. A 90-minute safety
  timeout interrupts the worker while preserving records; ordinary request failure
  stops the session. No automatic resume/retry, held-out or baseline follow-on.
- Supervisor will verify raw chain, full request/pairing/native/cache/resource
  controls and the development gate, then write `verified-summary.json` and stop
  its dedicated backend. Completion is not yet claimed. Historical 37-minute
  estimate remains an estimate; no new runtime conclusion before completion.
- First live checkpoint independently verified three successful requests, zero
  request/setup failures and valid chains/request controls. Run ID
  `ffc1d0a8-0789-4550-a245-f56e128fde5c`; execution manifest SHA
  `ab81373e9f592ef7022c6b1f73ab6d0651ade28fba63e9455e1563a4e18a6131`.
  Evidence: `artifacts/stage-b-validation-v4-50/first-checkpoint.json`.
  This verifies only the saved prefix, not completion or future attempts.
- Planning/protocol status updated to reflect the explicit diagnostic allowance.
  No source/dependency/model settings changed during launch. No commit/push or
  staged files; ignored docs/tests/artifacts remain unstaged. Next: inspect the
  stopped gate and measured runtime/resources before proposing main sessions.

## 2026-10-17 — 50-question preparation and local preflight complete

B50.1/B50.2 done; B50.3 pending a bounded development-compute allowance.

- Added explicit 50-ID subset support in `stage_b.py`, count-derived 25/50 baseline
  plans/identities and parent-completion checks in `baseline_runner.py`, and a
  frozen-plan-derived baseline archive count in `archiving.py`. Existing 25/100
  main plans remain valid; full-100 baseline execution remains unsupported.
  No scientific factor, prompt/evidence formatting, dependency or lockfile changed.
- New deterministic preparation command `python3 scripts/prepare_stage_b_50.py`
  creates a new manifest exclusively. Actual v4 study SHA
  `414d1c2eabf849d3a215ab76842f2d7a00031001e1c67c918fda6f7cfc749208`.
  `configs/stage-b-50-protocol.json` records critical validation invariants,
  post-results limitations, separate measurement policy and exact proposed commands.
  Added v4 to the distributable checkout verifier and its configuration metadata.
- Actual CLI enumeration wrote `artifacts/stage-b-plan-v4-50.json`: 48 conditions,
  144 blocks, 7,200 unique slots; plan SHA
  `b2fd62cc242dbf68c3629355a65245e50d7b77844cb8da7cd41bc6784dd5b346`.
  Seven focused expansion tests additionally verify 1,200 unique baseline slots,
  paired models, strict ID/count/version rejection, deterministic nesting/order,
  preparation reproducibility and rejection of old parent/development identities.
  No actual baseline manifest is frozen before completed v4 main records exist.
- Local preflight command `TOKENIZERS_PARALLELISM=false PYTHONPATH=src
  .venv/bin/python artifacts/preflight-stage-b-50.py` passed. Evidence:
  `artifacts/stage-b-50-preflight-v1.json`. Both prepared corpora, native tokenizer,
  reranker and embedding asset identities, reference tokenizer and all twelve
  required index manifests match. No server or generator was started; backend
  residency/model digest and full index loading remain checks for the fresh gate.
  Selected IDs span 14 SQuAD articles and 50 Hotpot components. About 32.5 GB free
  disk was observed, not a reserved allowance.
- Chain-verified historical records project 12.625 main hours, 0.679 baseline hours
  and 0.615 main-development-gate hours from recorded request wall/setup costs.
  These are estimates, not v4 measurements; session gaps/startup and some
  preflight/serialization are excluded. The separate baseline gate is additional.
  Protocol records a proposed 144-request diagnostic session, with no automatic
  held-out follow-on or retries. No new benchmark/generator requests launched.
- `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p
  'test_stage_b*.py' -v`: all 35 passed. Initial full-suite invocation lacked the
  documented macOS DYLD library setup: one failure and six errors, 31 skips,
  retained at `/private/tmp/ragbench-stage-b-50-tests.log`. Reran in a subprocess
  setting DYLD_LIBRARY_PATH to the installed Torch `torch/lib` directory before
  interpreter startup: 305 discovered, 274 passed, 31 optional dashboard skips
  in 25.537 seconds; `/private/tmp/ragbench-stage-b-50-tests-native.log`. Existing
  local encoder tests ran as validation; no experiment/model-server launch.
- Normal and optimized isolated checkout verification each passed all eight
  groups, including legacy matrices and v4's 7,200 slots. Actual preparation CLI
  create/no-overwrite check passed in temporary storage. Legacy v3 baseline plan
  recomputed exactly equal to frozen `stage-b-baselines-v1.json`. Changed source,
  scripts and local tests passed Ruff; `git diff --check` passed. No staged files,
  commits or pushes. Prior README/deep-dive edits preserved and appended locally;
  docs/tests/artifacts remain unstaged. Old study manifests, measurements, public
  results, dashboard snapshots and archives were not rewritten.

Next smallest task: B50.3, stop the local viewer and run only the fresh compatible
144-request development gate into `runs/phase7-validation-v4-50` under an explicit
bounded allowance; review measured runtime/resources before main sessions.

## 2026-10-17 — 50-question Stage B expansion started

User selected 50 evaluation questions per dataset. B50.1 in_progress; preparation
only so far. Target: 7,200 main and 1,200 separate baseline requests, plus fresh
144/24-request development gates. Existing v1/v2/v3 studies, Stage A selection,
results and archives stay unchanged. Use the same ID-only hash ordering as v3,
taking 50 instead of 25, so every v3 question is included without outcome-based
selection. All 8,400 held-out measurements will be fresh, not imported/poolable
historical requests. This expansion follows inspection of existing results and
is not an independent untouched confirmatory evaluation. Source/asset preflight,
validation, runtime allowance and bounded model compute remain pending.

## 2026-10-16 — verification command committed and pushed

User requested commit/push. Created 9145e27 (`add automatic checkout verification`)
with exactly .github/workflows/verify.yml, configs/checkout-verification.json and
scripts/verify_checkout.py. Reviewed the full staged diff, explicit file inventory,
privacy/path scan and whitespace; no Markdown, ignored tests or generated assets
were staged. Used the existing public GitHub username/noreply identity for this
commit only, without changing repository/global configuration.

Rechecked the isolated eight-group verifier, all 13 focused local regressions
(7.004 seconds), Ruff and whitespace; all passed. Fetched origin before staging,
confirmed no local/remote divergence, then normal push to origin/main succeeded
from 0ee9f96 to 9145e27. HEAD and origin/main match. README/deep-dive edits remain
local and unstaged; index is empty. No benchmark/model calls or archive rewrites.
Read-only `gh run list` for the exact pushed SHA confirmed workflow run
38932496632 completed with conclusion success:
https://github.com/shirin-manzari/ragbench-lab/actions/runs/38932496632.
V.1 handoff is complete; model/tokenizer validation remains separate.

## 2026-10-16 — fresh-checkout verification complete

V.1a/V.1b done. User authorized the fresh-checkout verification improvement.
Added scripts/verify_checkout.py, .github/workflows/verify.yml and
configs/checkout-verification.json. Updated local README/deep dive/plan guidance.
No runtime algorithm, scientific setting, dependency/lockfile, frozen manifest,
public result, raw measurement or immutable archive changed.

The command uses Python 3.11+ standard library only, inserts its own checkout
source paths, disables bytecode writes and creates synthetic inputs/records only
in auto-cleaned temporary storage. Eight independently reported groups check all
52 source/script files for syntax, five experiment TOMLs and unsupported settings,
60 Stage A conditions, v1/v2/v3 Stage B factorials/exact unique request pairing,
both synthetic adapters and source-isolated deterministic splits, Unicode offsets,
chunk bounds/fallback, BM25/RRF, actual packed evidence/scoring and append-only
resume/rejection behavior. It reuses the original public verifier for the 56
conditions/448 metric rows/1,760 contrast rows/three figures. Named failures return
status 1; --json emits one summary; explicit checks survive Python -O.

Runtime audit guards reject neural/viewer dependencies, socket operations beyond
object creation and process launches. The synthetic character counter verifies
algorithm contracts, not BGE/native tokenizer behavior. Public aggregate checking
is not raw-chain/bootstrap reconstruction; these temporary synthetic run chains
are not new study measurements or a fresh model-backed development gate.

CI runs the isolated command and its optimized variant from outside the checkout,
without installing the package/dependencies. Four configured jobs: Linux Python
3.11/3.14 and macOS/Windows Python 3.14, each bounded to ten minutes, contents: read,
no persisted checkout credentials and official actions pinned to verified release
commit IDs. No external CI job was launched. Source/Python provisioning may use
network; the actual Python verifier is offline. Hosted cross-platform success is
pending commit/push and real job execution, not inferred from local YAML checking.

Actual verification:

- `python3 scripts/verify_checkout.py`,
  `python3 -I -S -B scripts/verify_checkout.py --json` and the optimized
  `python3 -I -S -B -O scripts/verify_checkout.py --json`: eight groups passed
  under local Python 3.14.7. Minimum-version isolated and optimized executions
  under /opt/homebrew/bin/python3.11 (3.11.7) also passed all eight groups.
- `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
  -p test_checkout_verification.py -q`: 13 passed (7.327 seconds). The same
  discovery under /opt/homebrew/bin/python3.11: 13 passed (7.878 seconds).
  Each scenario copies tracked checkout files plus the three new deliverables,
  without .git, tests, data, models, indexes, runs, reports or artifacts, and runs
  from an unrelated working directory with -I -S -B. Normal success leaves every
  checkout byte and file inventory unchanged. Mutation cases detect syntax errors
  in unloaded model modules, wrong Unicode/truncated offsets, removed RRF
  deduplication, bypassed resume identity and damaged/missing public results.
  Additional cases block attempted Torch imports and actual socket connections.
- After broadening socket/process audit events, the final standard-library command
  passed on 3.14 and optimized 3.11; both targeted runtime-guard regressions passed.
- PyYAML BaseLoader structural validation checked events, read-only permissions,
  four matrix entries, timeout, pinned SHA syntax, credentials, shell, working
  directory and both isolated commands. JSON metadata matches all eight check names.
  This is local structure checking, not a hosted runner/actionlint success claim.
- `.venv/bin/ruff check scripts/verify_checkout.py tests/test_checkout_verification.py`
  and `git diff --check` passed. Index is empty; ignored local tests and PLAN/
  PROGRESS remain excluded. No staging, commit or push.

Initial local regressions detected a too-specific expected error string: the
corrupted adapter was correctly rejected by earlier evidence validation. Fixed
that assertion; initial Python line-length findings were also fixed before the
passing checks. No remaining validation failures. The full native/model-backed
suite was not rerun for this standalone command; existing library code is unchanged.
Next smallest task: user review of the command and workflow before an explicitly
requested commit/push. No additional experiment compute is needed.

## 2026-10-16 — public aggregate bundle prepared locally

P.1a/P.1b done. User selected compact results and verification scripts (repeated
script item treated as one request), explicitly without pushing. Prepared
`results/stage-b-v3/` with eight files/637,007 bytes: conditions.csv (56 profiles),
unchanged cells.csv (448 metric rows), contrasts.csv (1,760 rows), stage-times.csv,
original quality/latency main and baseline SVGs, original main stage-time SVG,
and a manifest with exact source/file hashes and scientific scope/limitations.
No question IDs/text, answers, source passages, request-level observations,
personal paths, process details or raw provenance were exported. Stage A, pilots,
development gates and historical v1/v2 results are explicitly outside this bundle.

Added `scripts/export_public_results.py` and `scripts/verify_public_results.py`.
Both use the standard library only. Export checks report/proof/figure/study
bindings, validates the full public payload before writing, refuses existing
output directories and offers read-only `--check`. Verification checks inventory,
hashes, fixed methods/scope, exact 48+8 matrix, all 220 declared contrast pairs,
units/counts, finite values/ordered intervals, left-minus-right arithmetic,
nonnegative stage means reconstructing online latency, private-looking content,
and restricted static SVG elements/attributes. Explicit errors survive Python -O.
Neither script loads models or executes benchmarks. These checks are aggregate
consistency/byte comparisons, not raw-chain audits or recomputed bootstrap proofs.

The old operational/checker scripts and historical proofs stay untouched under
ignored artifacts/. They require local raw/archive environments and are not
pretended to work in an ordinary public clone. Public scripts verify this smaller
bundle without requiring those assets. Added a narrow .gitignore allowlist for
exact public filenames; other results, all original reports/archives and tests
stay ignored. Added .gitattributes to preserve the reviewed export bytes across
Git newline settings. README/deep dive link the public outputs and commands;
report.md is unchanged.

Actual checks:

- `.venv/bin/python scripts/export_public_results.py` created the new bundle;
  `.venv/bin/python scripts/export_public_results.py --check` and
  `.venv/bin/python scripts/verify_public_results.py` passed (56/448/1,760/3).
- `.venv/bin/python -m unittest discover -s tests -p test_public_results.py -v`:
  24 passed in 3.247 seconds. Tests cover original-source byte parity, standalone
  isolated execution, file/manifest corruption, extra/missing data, incomplete or
  duplicated matrices, reversed/incorrect contrasts, invalid numbers/units/counts,
  stage totals, privacy/active SVG rejection, symlinks, no-overwrite and failed
  source handling, and validation under optimization. Tests remain ignored.
- `.venv/bin/ruff check scripts/export_public_results.py scripts/verify_public_results.py tests/test_public_results.py`
  passed. Initial lint-only import/wrapping findings were fixed before final checks.
- Independent inline CSV comparison matched every public estimate and source
  interval against report.json (448+1,760 rows), and original figure bytes match.
  A temporary directory containing only public results/scripts passed verification
  under Python `-I -S -B`, with no source package, private data or dependencies.
- Inline `git -c core.autocrlf=true hash-object --path=... --stdin` checks preserved
  all eight public files exactly; `git check-attr text` reports unset for exports.
  README/deep-dive links resolve. `git diff --check` passed. The untracked file set
  is exactly the eleven intended public files (eight results, two scripts,
  attributes); report unchanged, index empty. `git check-ignore -v` confirms tests,
  raw/extra result paths, original reports and archives remain ignored.

No scientific settings, runtime source, dependencies, measured data, frozen
manifests or archives changed. No experiments, model calls, staging, commit or
push. Next smallest task is user review of the public package before publishing.

## 2026-10-16 — expanded implementation deep dive

D.5 done. Used the user's CACHEUS deep dive as a structural/depth reference,
not as a source of RAG methods or measurements. Expanded PROJECT_DEEP_DIVE.md
from 79 lines/482 words to 766 lines/5,176 words. Covered the
repository and environment, two-stage factorial design and reduction history,
data contracts/adapters/splits, offset-preserving chunking, BM25/Dense/RRF and
reranking, exact context packing, a single-request walkthrough, native prompting,
cache/timing/resource scope, bounded sessions and hash-chained resume, scoring,
source-cluster statistics, exports, dashboard architecture, archives and extensions.

Grounded implementation descriptions in current source and study claims in
frozen manifests/saved analysis. The source-offset illustration is explicitly
synthetic. Kept the user's exact AI-use sentence and README dashboard anchor.
Preserved report.md byte-for-byte, including the preceding requested removal of
its date and AI-use section (SHA-256 remains
518a6307df80bca92889d32dc763b4e7bbf2abef2afccdbcecbec7def16e46bd).

Actual documentation checks:

- Inline Python validation: all 49 file/anchor links resolve, linked files are
  tracked, fences are balanced, three shell blocks pass `zsh -n`, and all six
  command examples parse against the real CLI. Required interpreter/artifact
  paths exist; personal paths, email addresses and raw identifier patterns are
  absent. AI wording and report hash match the preserved values.
- `PYTHONPATH=src .venv/bin/python -m ragbench_lab validate configs/stage-a-study.toml`
  passed with the existing config hash. The corresponding `stage-a-plan` returned
  60 conditions; `stage-b-plan configs/stage-a-study.toml --study
  manifests/stage-b-study-v3-reduced.json` returned 48 conditions, 144 blocks and
  3,600 main requests. Planning only; no model/backend calls or new outputs.
- Inline JSON checks confirmed the frozen E5/sentence-aware selection, reduced
  25-ID samples, 600 baseline requests, 12/25 source-cluster counts, 48/8 analysis
  cells and all stated model/reranking result directions and latency range.
- Final recheck read the actual saved snapshot: four runs, 176 cells, 1,520
  examples and 31,200 request metadata rows; analysis has 4,200 measurements and
  fifty question units. Structural/CLI/privacy/preservation checks passed again.
  `git diff --check` passed; staging is empty, and `git check-ignore PLAN.md
  PROGRESS.md` confirms both planning files remain ignored.

README, runtime source/configs, measurements and immutable archives are unchanged.
No full runtime tests, benchmark rerun, dependency installation, staging, commit
or push belongs to this prose edit. PLAN.md/PROGRESS.md remain ignored and local.
Next smallest task is user review; publishing needs an explicit request.

## 2026-10-16 — selected documentation pushed

D.4 done. User explicitly requested publishing only the deep dive and report,
excluding unnecessary/private data. Reviewed both complete documents and scanned
for credentials, personal addresses/paths and private key material. Only the local
loopback URL and project-relative artifact references remain. Converted links to
ignored local documents/handoffs to plain references to avoid broken public links.
Kept the user's current prose/table formatting and AI disclosures.

Explicitly force-added only `PROJECT_DEEP_DIVE.md` and `report.md` under the
selected-Markdown exception. Reviewed full staged diff/names/stat/whitespace;
local links and shell syntax passed. Created `38e8600` (`add study report and deep dive`)
with exactly those two files, using the public GitHub username/noreply address for
both author and committer without changing repository/global identity settings.
Normal push to the authorized origin/main succeeded from `35c6adf` to `38e8600`.
No earlier unpushed commits were present. Raw records, archives, models, indexes,
tests, other Markdown and local verification files were excluded. The two selected
documents are now tracked; remaining ignore rules and local contents are unchanged.

## 2026-10-16 — report and deep dive minimized

D.3 done. Reduced `report.md` from 1,947 to 665 words (about 66%) and
`PROJECT_DEEP_DIVE.md` from 997 to 482 (about 52%). Report now focuses on design,
measured findings, inference limits and saved work; deep dive covers the code,
controls, dashboard command and verification/replay. Both retain AI-use disclosure.
Kept post-start reduction/history, source dependence, scoring/timing limits and
separate baselines. Removed repeated dashboard details and stale test counts;
background references and detailed operations link to existing project documents.

Local links/anchors, listed module paths, README dashboard anchor, shell-block
syntax and whitespace passed. Recomputed all four F1/latency ranges and the
24 positive reranking timing contrasts/range from saved synthesis; completed
request totals match the existing snapshot. No runtime tests or experiments
rerun. Only ignored documentation/planning changed; staging empty, no commit/push.

## 2026-10-16 — shorter deep dive and AI disclosure

D.2 done. User requested a shorter, more human PROJECT_DEEP_DIVE.md and disclosure
of AI use. Rewrote it from 248 lines/1,836 words to 146 lines/997 words (about 46%
fewer words). Kept the two-stage design and counts, reduced-study history, core
controls, architecture map, interpretation limits, dashboard startup and archive
verification/replay links. Detailed offline installation stays in the existing
handoff. Removed stale test counts and repetitive operational prose.

The new AI-use section states assistance with planning, coding, debugging, tests,
analysis scripts, dashboard work and documentation; identifies the qualitative
case notes as AI-authored; and distinguishes saved measurements from authorship.
It does not claim independent human review or undisclosed verification.

Checked all six local links, listed Python module paths, the existing README
dashboard anchor, both shell blocks with `zsh -n`, and whitespace. All passed.
No runtime tests, model calls or archive verification were rerun for this prose
edit. README/source/configs and saved artifacts are unchanged; deep dive and
planning docs remain local/ignored, staging empty, no commit or push.

## 2026-10-16 — conservative frontend cleanup

C.2a/C.2b done following the attached UI-specific brief. Source started clean at
`e299b0c` (the previous cleanup was committed outside this turn). Reviewed current
layout, CSS, JavaScript, dependency declarations and source/test/script/config/doc
references. The existing dark sidebar, light panels and rounded navigation are the
established visual language; no gradients, glass layers, decorative icons, generic
landing-page copy or animation library needed removal. Sites guidance was used for
local browser verification only, with the already running viewer on port 8050.

Only three runtime files changed:

- `dashboard.py` and `dashboard_assets/dashboard.js`: compute each facet's full-run
  values once per callback and reuse them for single-value defaults and disabled
  states. This removes repeated scans without adding persistent state, caching
  between selections, asynchronous effects or dependencies.
- `dashboard_assets/dashboard.css`: grouped three identical min-width rules and
  the duplicate 850px media block, retaining every selector and breakpoint. Fixed
  the existing search focus rule: Dash 4 assigns `search-input` to a surrounding
  container, so `:focus` never matched it. Scoped `:focus-within` now applies the
  intended teal border/ring when the actual input receives keyboard focus. Native
  focus and input interaction remain intact; idle styling/layout are unchanged.

Retained DOM wrappers/classes/IDs used by Dash, CSS, testing or possible external
automation. Kept native Details, labels, scrollable-table focus regions, Dash state,
the user's established fade/slide animation and its geometry observers. No safe
unused state/listener/dependency removal was identified. No layout restructuring,
copy rewrite, visual system change, frontend library, benchmark, snapshot/export,
archive, commit or push. README and prior source changes remain untouched.

Actual checks:

- `PYTHONPATH=src artifacts/dashboard-env/bin/python artifacts/check-ui-filters-v1.py`:
  500 deterministic cases across four real runs plus an empty run matched old and
  new Python and JavaScript implementations, including reset/incompatible values.
  Reference source is pinned to `e299b0c`; this ignored helper is QA-only.
- `PYTHONPATH=src artifacts/dashboard-env/bin/python artifacts/check-cleanup-v1.py check /private/tmp/ragbench-cleanup-baseline-20261016.json`:
  all 4,812 original layout/dependency/saved rendering/scoring fingerprints match.
- `PYTHONPATH=src artifacts/dashboard-env/bin/python -m unittest discover -s tests -p 'test_dashboard*.py' -q`:
  all 45 passed in 0.782 s. Whole-source Ruff, JavaScript syntax and whitespace passed.
- `node artifacts/check-ui-cleanup-v1.mjs`: passed 18 current/reference computed
  style/layout comparisons (all six tabs at 1440/850/390px), no page overflow,
  associated labels, real dataset selection/reset, search focus ring and reduced
  motion; no runtime JavaScript exceptions. Screenshot inspected at
  `artifacts/ui-cleanup-desktop-20261016.png`. The first QA attempt tried serializing
  a DOM node; fixed the helper to return a Boolean. The second focused the real
  input and exposed the wrapper mismatch described above; the corrected selector
  and wrapper-specific assertion passed on the final run.
- `node artifacts/check-tab-motion-v1.mjs v20261016`: passed slide alignment,
  rapid switching, idle observer stability, mobile scrolling/resizing, no overflow
  and reduced motion. Screenshot `artifacts/dashboard-tab-motion-v20261016.png`.
  Owned QA browser closed; only the existing user dashboard remains on 8050.

No validation failures remain. Checks exercise the saved viewer and configuration
facets, not new model/benchmark work. Ignored docs/checkers/screenshots are unstaged;
next smallest task is review/commit of the three-file UI cleanup if requested.

## 2026-10-16 — behavior-preserving cleanup

C.1a/C.1b done. Read the attached cleanup brief and project instructions/design/
plan/history; audited source definitions, imports, duplicate bodies and references
in source, ignored tests, operational scripts, configs, docs and saved snapshots.
The working tree was clean at the start. README remains tracked under the user's
explicit exception; no files were staged, committed or pushed.

Changed ten source files in small edits:

- `dashboard.py`: five dropdown retention/default paths share one private helper;
  raw disclosures reuse the existing notes constructor; removed two unused `side`
  comprehension variables. Serialized layout, callback dependencies, text and
  saved comparison results remain identical.
- `dashboard_snapshot.py`: the condition lookup now also supplies membership and
  duplicate checks, replacing a parallel set without removing any validation.
- `dashboard_assets/dashboard.css`: removed obsolete brand/eyebrow/uncertainty
  classes and paragraph/footer rules for elements absent from the current viewer.
- `answer_metrics.py`: compute prediction tokens/counts once per prediction rather
  than again for every reference answer; scoring formulas/order remain unchanged.
- `generator_assets.py`: vocabulary comparison reuses the tokenizer already loaded
  and configured in the same correction path instead of parsing the original again.
- `data/adapters.py`, `data/preparation.py`, `chunking.py`: fixed the five existing
  whole-source Ruff findings with import layout and line wrapping only.
- `config.py`, `stage_b.py`: corrected two stale phase/task descriptions. Preserved
  comments explaining offsets, statistical units, cache isolation, security,
  compatibility and native-library constraints; no broad comment purge.

Kept the old BM25 rebuild fallback because the Phase 2 index and historical replay
use it. Kept `inspect_prepared`, `planned_requests`, tokenizer export/correction
helpers and viewer test/callback hooks after finding CLI/script/test/framework
references. Broad exception handlers at request/setup/cleanup boundaries preserve
failure records and resource release, so they were not narrowed for style. No
public symbol, CLI/configuration/protocol, dependency, manifest or saved artifact
was removed or changed. Source provenance naturally changes with these edits;
existing frozen runs still require their original source or a fresh validation gate.

Actual verification:

- Before/after core command: `DYLD_LIBRARY_PATH=/Users/shirinmanzari/Desktop/ragbench-lab/.venv/lib/python3.14/site-packages/torch/lib PYTHONPATH=src TOKENIZERS_PARALLELISM=false .venv/bin/python -m unittest discover -s tests -q`.
  Baseline: 261 run, 31 skipped, otherwise passed (15.158 s). Final: same counts,
  passed (14.615 s). Logs `/private/tmp/ragbench-cleanup-{baseline,final}-20261016.log`.
  Expected position-ID/overlength warnings and mocked notification permission errors
  are retained in logs, not test failures.
- `PYTHONPATH=src artifacts/dashboard-env/bin/python -m unittest discover -s tests -p 'test_dashboard*.py' -q`: all 45 passed before (0.746 s) and after (0.613 s).
- Ignored differential helper `artifacts/check-cleanup-v1.py` recorded 4,812 output
  fingerprints before source edits and checked exact equality afterward, using
  `/private/tmp/ragbench-cleanup-baseline-20261016.json`. Covers the real v3 layout,
  callback dependency graph, four run overviews/results, all configuration/example
  renderings, stored comparisons in both directions, saved-answer rescoring and
  1,458 short-answer/reference edge combinations. Snapshot loading reverified its
  existing asset hashes. This is offline comparison, not benchmark execution.
- `.venv/bin/ruff check src`, `node --check src/ragbench_lab/dashboard_assets/dashboard.js`,
  `git diff --check`, CLI `--help` and `validate configs/stage-a-study.toml`: passed.
  Config hash remains `2d94038ed1ffa0ea93becb277a1136c7addd7341e5d3eb7bb13f83b93421292b`.

No benchmark, downloads, dependency/build changes, model-backed study validation,
browser visual check or archive regeneration was performed. Existing tests cover
the tokenizer correction path; no native model conversion was rerun. Next smallest
task is review of this uncommitted cleanup diff; core study remains complete.

## Current state

Status: Phases 0–8, optional dashboard XD.1–XD.9 and all review fixes/improvements XD.10a–g done. Revised viewing archive and fresh offline replay verified. Model/context extensions remain pending; no new benchmark compute.

Active phase: none; XD.12a–d guided dashboard improvements done, local/uncommitted.
Previous dashboard source/configuration remains committed/pushed through `647fe16`.
Markdown/tests remain ignored; unrelated user `.gitignore` edit preserved.

Next task: **Review README.md/report.md and back up the verified archives when ready. No required benchmark work remains. Old snapshots/archives remain unchanged.**

Latest completed implementation: XD.12 overview, metric/uncertainty guidance and
side-by-side saved comparisons and concise copy; all 44 isolated dashboard tests passed. The latest
full suite has 258 tests: 230 passed and 28 optional viewer skips in the benchmark
environment. Guided-view source changes and current documentation remain local.

The active matrices contain 31,200 successful requests, excluding pilots,
development diagnostics and stopped historical v1/v2 attempts. E5 sentence-aware
selection remains frozen; no required benchmark requests remain. SmolLM, new
context budgets and concurrent-load studies are optional and unrun.

This file is a work-evidence log, not a live process monitor. Current state and
the current experiment ledger supersede earlier dated checkpoints; original
session histories, failures and decisions are retained below. The external CACHEUS
README was consulted only as a writing-style reference for D.1, not as study data.

## 2026-10-15 — faster slide and reset hover

User requested slightly faster transitions: selection slide/width now 280ms
(previously 380ms), height 160ms. Added Reset filters hover with a lighter blue
background/border; tab hover remains disabled. Whitespace checks passed; CSS-only
changes, no new test/browser run or commit.

## 2026-10-15 — tab hover removal

Removed the tab hover background/color rule at the user's request. Smooth selected
highlight, keyboard focus and other controls remain unchanged. CSS whitespace
check passed; no new test/browser run, benchmark changes or commit.

## 2026-10-15 — smooth slide without shake

User requested smoother tab movement with no after-shake. Removed jelly keyframes,
animation class/restart logic and forced layout; changed slide/width timing to a
380ms non-overshooting ease. Selection geometry observers and reduced-motion
support remain. Updated local browser helper and validation invariant for the new
behavior. All 45 focused tests passed (0.584 seconds), syntax/whitespace clean;
no new browser run claimed. Existing viewer serves CSS/JS on refresh; no data,
dependency, benchmark or Git changes.

## 2026-10-15 — stable navigation above summary/content

User authorized fixing the shared summary appearing above the tab bar. Separated
Dash navigation labels from their panel bodies, kept stable explicit view keys,
and placed navigation before the shared summary and view panels in actual DOM
order. A presentation-only callback shows exactly one panel; summary visibility,
filters and existing result callbacks remain unchanged. The animated bar no longer
moves vertically when switching tabs.

45 focused tests passed (0.674 seconds), including DOM order and all-six-panel
visibility checks. Ruff/whitespace passed. Browser assertions confirmed all six
tab bar positions and summary/panel bounds. The first mobile check exposed
intrinsic content-width overflow; fixed with a zero-minimum mobile grid track,
zero-minimum panel wrappers and wrapping long download links. Final browser run
passed all navigation, slide/jelly alignment, rapid switching, idle stability,
390px scrolling/no page overflow and reduced-motion checks without exceptions.
Helper `artifacts/check-tab-motion-v1.mjs v3`; screenshot
`artifacts/dashboard-tab-motion-v3.png`. Failed v2 check/screenshot retained.

Refreshed user viewer on port 8050, PID 47890/session 39387; isolated test browser
closed. No benchmark/model calls, measurements, source intervals, snapshot/archive
changes, dependencies, commit or push. Current documentation/tests stay ignored.

## 2026-10-15 — reference-inspired sliding tab highlight

User supplied https://codepen.io/flavio_amaral/pen/xxgYGrR (Jello Tab Bar).
Read the reference and independently implemented its sliding-highlight/jelly
motion for existing text tabs; no copied layout, icons, photos, fonts or external
runtime resources. Sites local-only guidance used; no publishing or dependencies.

CSS decorative pill translates/resizes under the Dash-selected tab, then settles
with a brief scale animation. Existing rounded styling/labels and Dash click/state
ownership remain unchanged; fallback selected-tab styling works without the pill.
Local JavaScript observes selection classes and resize geometry, including mobile
scroll coordinates, with requestAnimationFrame batching and no polling. Guards
prevent own class changes causing an idle mutation loop. Reduced-motion preference
disables both slide and jelly motion, including preference changes while open.

Actual checks: 44 focused tests passed (0.660 seconds), JavaScript syntax and
whitespace passed. Browser helper `artifacts/check-tab-motion-v1.mjs` observed
actual animation, final alignment, rapid-click settling, idle observer stability,
390px resize/scroll alignment without page overflow and zero-duration/no-animation
reduced-motion behavior; no browser exceptions. Screenshot
`artifacts/dashboard-tab-motion-v1.png` inspected. Test browser closed; existing
viewer at port 8050 serves local CSS/JS on refresh. Validation metadata updated.
No benchmark requests, snapshot/archive changes, commit or push.

## 2026-10-15 — tab animation undone

User requested undoing the last request. Restored the exact pre-animation tab CSS:
rounded styling and original color-only hover transition remain; hover transforms,
press reset, selection animation and keyframes removed. Whitespace check passed.
Other uncommitted work preserved; no commit/push or benchmark changes.

## 2026-10-15 — tab animation

Added a 1px hover lift, press reset and 180ms selection fade/settle to the tab bar
at the user's request. Reduced-motion preference disables transitions, animation
and transforms. CSS-only change; whitespace check passed. No browser QA or new
test run claimed; no callback, data, dependency or Git changes.

## 2026-10-15 — rounded tab bar

User requested modernizing the tab container with a radius border. Added a rounded
bordered track, rounded tabs, white active state, subtle shadow and restrained
hover transition. Keyboard focus retained; reduced-motion preference disables
transitions. No labels, callbacks or data changes. All 44 focused tests passed
(0.699 seconds), whitespace clean; CSS served by existing viewer on refresh.
No new browser QA, model requests, dependencies, commit or push.

## 2026-10-15 — title and configuration cleanup

User requested main title RAGBench and removal of sidebar branding; applied.
Then removed the duplicated selected-configuration heading below its dropdown,
retaining counts, metrics and provenance. All 44 focused tests passed (0.603
seconds), whitespace clean; refreshed existing viewer on port 8050. No scientific,
snapshot or dependency changes; no commit/push.

## 2026-10-15 — comparison spacing correction

User screenshot showed previous CSS margin was not taking effect. Replaced the
selector-dependent rule with direct 32px top padding on the contrast dropdown
wrapper only. All 44 focused tests passed (0.675 seconds), whitespace clean;
refreshed viewer and confirmed padding in served layout on port 8050.
No data, scientific behavior or other control spacing changes; no commit/push.

## 2026-10-15 — second dashboard copy reduction

Further minimized text at the user's request: shorter header/tab/filter labels,
shorter findings and question/reference headings, no duplicate comparison heading
or overview description. Run-wide totals/status/legend moved under Run details;
full interval/count explanations remain accessible. Visible cards still explicitly
refer to filtered requests; full-run findings retain scope and limitations.
No layout, scoring, interval, example or benchmark changes. 44 focused tests passed
(0.633 seconds); Ruff and whitespace passed. Viewer refreshed on port 8050.
No new browser QA, commit/push, dependencies or artifact regeneration.

## 2026-10-15 — comparison spacing and tab removal

Added 24px top spacing above Left minus right, then removed the Context & extensions
tab at the user's request. Snapshot metadata and optional-study status remain
unchanged. All 44 focused tests passed (0.676 seconds), whitespace clean; viewer
refreshed on port 8050. No experiments, artifact changes, commit or push.

## 2026-10-15 — concise dashboard copy

User requested minimizing dashboard text/explanations. Removed the redundant header
subtitle and START HERE label, shortened overview/compare/scope/download wording,
and moved detailed limitations, selected-metric definitions, uncertainty and plot
keys into closed native expandable notes. Kept question/timing counts, units,
original intervals, real errors and short evidence-highlight caveat visible.
Removed routine no-error messages; scientific safeguards and source text unchanged.

44 focused tests passed (0.581 seconds), including a new check that full metric/
interval/validity guidance remains available but closed by default. Its first draft
incorrectly required the small sample-count table to be closed; corrected the test
to target explanation controls only, preserving visible counts for small selections.
Ruff/whitespace passed. Existing server refreshed on 8050, PID 3411/session 14962.
Updated validation metadata and local README/deep dive/plan; no new browser QA,
full-suite run, model requests, dependencies, snapshot changes, commit or push.
Sites workflow stays local-only; the original styling/sidebar behavior is retained.

## 2026-10-15 — header label and footer message removal

Removed only EXPERIMENT EXPLORER and the selected footer message from dashboard.py
at the user's request. Existing metric/uncertainty explanations and timing guards
remain intact. All 43 focused tests passed (0.692 seconds), whitespace clean;
refreshed viewer on port 8050. No measurement, snapshot, dependency or Git changes.

## 2026-10-15 — sidebar height and scrolling fix

User reported a sidebar bottom gap in a screenshot. Browser verification exposed
the global footer rule padding Dash's empty framework footer outside the app,
creating 52 CSS pixels of unwanted page height. Scoped footer styling to .shell.
Desktop sidebar now sticks at the top, fills the viewport and scrolls independently
so the final filter/reset button remains reachable on short windows. Mobile
retains always-visible filters in normal page flow; no overlapping fixed panel.

Used Sites local-only preview guidance. Initial browser check failed at page bottom;
the footer leak was diagnosed rather than counted as success. Final checker
`artifacts/check-dashboard-sidebar-v1.mjs` passed viewport bounds and last-filter
reachability at 1440×900/1440×600, plus 390px normal flow/no horizontal overflow.
Screenshot `artifacts/dashboard-sidebar-desktop-v1.png` inspected. All 43 focused
tests passed; whitespace clean. Existing server 8050 serves updated CSS on refresh;
no restart needed. Test browser closed, no models/benchmarks/snapshot changes,
dependency changes or commit. Other uncommitted work and .gitignore edit preserved.

## 2026-10-15 — sidebar footer removal

Removed the LOCAL · READ ONLY label and its border-top divider exactly as requested.
Deleted its unused CSS rule; read-only safeguards remain unchanged. All 43 focused
tests passed (0.641 seconds), whitespace clean; viewer refreshed on port 8050.
No benchmark requests, snapshot changes or commit.

## 2026-10-15 — always-visible sidebar filters

User requested removing the Filters & display menu, not its controls. Replaced
the collapsible wrapper with a normal Div, removed its title and viewport-collapse
JavaScript, and retained label associations/filter behavior. Filters now remain
visible on all screen sizes; this explicitly supersedes the old mobile-collapse
presentation rule. Updated validation metadata/report locally. 43 focused tests
passed (0.649 seconds), including a new wrapper regression; JavaScript syntax and
whitespace checks passed. Sites workflow remains local-only; no publication,
benchmark work, dependency changes or commit. Refreshed existing viewer on 8050.

## 2026-10-15 — sidebar text removal

XD.13 done: user explicitly selected the RESULTS LAB label and the sentence
"A view into the frozen study. No models. No new requests." for removal. Deleted
only those two layout elements from dashboard.py; no style or behavior changes.
All 42 focused dashboard tests passed (0.811 seconds), whitespace clean. Refreshed
the viewer at port 8050; no benchmark requests, snapshot changes or commit.

## 2026-10-15 — visual experiment reverted

User interrupted the subsequent visual/copy restyle and explicitly requested undo.
Restored the pre-restyle CSS, wording, tabs, configuration labels, chart styling,
formatting helpers and local browser checker. XD.12 overview/explanations/compatible
comparison/uncertainty features remain intact; no Git reset or unrelated changes.
All 42 focused tests pass (0.580 seconds), whitespace is clean, and HTTP checks
confirm the original styling plus guided features on port 8050. Temporary preview
8051 and isolated test browser closed. No benchmarks, snapshot changes or commits.
Retained ignored screenshots are historical QA outputs, not the active design.

## 2026-10-15 — guided dashboard and side-by-side comparisons

XD.12a–d done following explicit authorization for improvements 1–4. Split into
overview, explanations, compatible comparison and validation slices before coding.
Used Sites skill local-only workflow; no hosted Site, source sync or publishing.
New `dashboard_guidance.py` contains metric definitions, interval explanation and
single-run descriptive observations. `dashboard.py` adds a default study overview,
visible Results guidance/count support and same-run/same-dataset comparison selectors.
Side-by-side shows original cell metrics, shared saved questions, answers, highlighted
exact evidence, offsets and raw records. Stored paired intervals retain original
direction, including when screen positions reverse; absent pairs stay unavailable.
No new bootstrap, winner ranking, cross-run pooling, model import or inference.

CSS stacks comparisons at narrow widths; mobile tabs scroll horizontally rather
than burying content. Overview/results counters remain explicitly scoped; the
filtered counter card is hidden on introduction/comparison views. Recorded critical
invariants in `configs/dashboard-validation.json`; updated README, deep dive, PRD,
report, PLAN and this log locally. Tests remain ignored.

Actual checks:

- `PYTHONPATH=src artifacts/dashboard-env/bin/python -m unittest discover -s tests
  -p 'test_dashboard*.py' -q`: 42 passed, including seven new synthetic regressions.
- Full final suite with existing Torch library path: 258 discovered, 230 passed,
  28 optional viewer skips; 15.058 seconds. All viewer tests passed in isolation.
  Log: `/private/tmp/ragbench-guided-dashboard-final-tests.log`.
- Changed-source/test Ruff, browser helper syntax and `git diff --check`: passed.
- Verified real snapshot: all four run overviews and all 248 original pair
  directions render; no Torch/Transformers/exporter/runner modules imported.
- Local headless Chrome checks passed with no JavaScript exceptions: default
  overview, original 24/24 reranking timing signs, metric/interval guidance,
  local-only plots, exact two-answer equality against snapshot, evidence highlights,
  same-dataset comparison and 390px stacked layout without page overflow.
  Helper `artifacts/check-dashboard-guided-v1.mjs`; final screenshots
  `artifacts/dashboard-guided-{overview,comparison,mobile,mobile-evidence}-v3.png`.
  First screenshots were retained; an empty intro counter card and tall stacked
  mobile tabs prompted the final layout refinement and repeated checks.
- Refreshed user viewer at http://127.0.0.1:8050, PID 1644/session 21052; HTTP
  layout confirms guided components. Temporary preview 8051/browser closed.

No new benchmark requests, dependency changes, snapshot/export regeneration,
archive overwrites, commit or push. Snapshot loader still verifies original v3
manifest `dafbc9c28f7f87707b6b7c5076e416988b26fd940519edb5e18dcdb9fb45d3d0`.
Latest features are newer than immutable viewer ZIPs. Next smallest task is user
review of the guided views; packaging/commit require direction, no compute needed.

## 2026-10-15 — dashboard commits and push

User requested focused commits and push. Created `3466fd2` (`export verified
dashboard snapshots`), `28b0d65` (`add local results dashboard`) and `647fe16`
(`record dashboard validation rules`). Reviewed explicit staged paths/diffs and
whitespace for each commit; no Markdown, tests, artifacts or unrelated `.gitignore`
edit included. Normal push to origin/main succeeded from `abb714d` to `647fe16`.

Pre-commit checks: 35 isolated dashboard tests passed; full suite ran 251 tests
with 230 passed and 21 optional viewer skips (those viewer tests passed in the
isolated suite). Full log: `/private/tmp/ragbench-dashboard-precommit-tests.log`.
Changed-source Ruff and JavaScript syntax checks passed. Staging is empty; only
the preserved `.gitignore` edit remains visible. No benchmark requests, snapshot
regeneration or immutable archive changes. Saved provenance retains its original
pre-commit identity.

## 2026-10-15 — documentation refresh

D.1 done. User requested current Markdown files with a short practical README,
using https://github.com/shirin-manzari/reproducibility-study-of-CACHEUS as a style
reference. Its public README was read; no code, measurements or result claims were
imported from that project.

All seven root files updated: README (67 lines/350 words), PROJECT_DEEP_DIVE,
report, PRD, PLAN, PROGRESS and AGENTS. README now covers scope, setup, dashboard,
results and limits without an operational-history wall. Deep dive separates
architecture/controls from offline setup/replay. The rewritten report describes
the completed reduced core, real result ranges, source-cluster uncertainty,
historical amendments, controls, dashboard and bounded conclusions.

Removed stale pending-phase prose from current summaries, not from chronological
session evidence. PLAN retains task IDs, completed checkboxes, optional XG/XC
gates and the original context predeclaration. Current progress/open-items/ledger
now distinguish completed work from unverified supervisor acceptance, off-device
backup and public sharing clearance. Contributor/Git/scientific rules are unchanged;
AGENTS only clarifies current dashboard status and the existing Markdown override.

Actual documentation checks:

- `validate configs/stage-a-study.toml`: passed, 30 Stage A conditions/dataset,
  unchanged config hash `2d94038ed1ffa0ea93becb277a1136c7addd7341e5d3eb7bb13f83b93421292b`.
- Main CLI help, isolated `dashboard --help` and `delivery-verify --help`: passed;
  all documented flags correspond to implemented commands. No generic run/report
  command is claimed. No benchmark was launched by these help/config checks.
- Five local Markdown links/anchors and all shell-block syntax: passed. Referenced
  core setup/output/archive paths exist. Installation snippets were syntax-checked,
  not executed again; previous fresh-viewer/core-replay evidence stays labeled.
- Four F1/mean-latency ranges recomputed from saved 48 main cells and matched the
  report. Request totals/run IDs and dashboard example counts matched saved v3.
- The five research-reference title/metadata pages were checked on ACL/arXiv;
  the chunk-size paper's full title/author citation was corrected. This is reference
  checking, not a new literature experiment or change to the study's design.
- Whitespace check passed; all seven Markdown files remain ignored, staging empty.
  Source/config/lockfiles/tests/results were not changed by this documentation task;
  existing dashboard changes and user `.gitignore` edit remain preserved.

No new dependency installation, model calls, benchmark runs, archive rewrites,
commit or push. Current root docs are newer than immutable release ZIPs. The
latest recorded implementation tests remain 251 discovered/230 passed/21 optional
viewer skips plus 35 isolated tests; no new full-suite run is claimed for prose edits.

## 2026-10-15 — question dropdown text

XD.11 done: user requested question text without the dataset ID prefix. Changed
only the displayed option label in `dashboard.py` and its focused assertion; IDs
remain option values and raw details, and ID/text search and selection still work.
All 35 focused isolated tests passed (0.693 s); whitespace check passed. Existing
archives/snapshots unchanged; this small viewer follow-up is newer than dashboard
v2's archived source. No benchmark requests or commit/push. User server refreshed
on 8050 to load the new label.

## 2026-10-15 — dashboard review fixes and improvements

User asked to record all findings in PLAN.md and fix/improve them. XD.10a–f are
done; XD.10g packaging remains in_progress at this checkpoint. The seven review
findings and six usability improvements are itemized in PLAN.md. No benchmark
requests, model downloads, scientific choices, dependency changes, commit or push.

Changes: `dashboard_snapshot.py` now validates stage-required metric keys, explicit
nulls, nonnegative counts, completion/request/cell totals, example/request links,
typed text and included-evidence offsets. Missing/invalid schemas fail with DataError;
valid unavailable metrics render labeled empty plots. Shared graph configuration
disables both cloud actions and their destination, and exports SVG locally.

Dataset-qualified labels remove configuration ambiguity. Overview cards follow
selected conditions, while whole-run totals are explicit. Facets preserve valid
selections, resolve incompatible family/recipe choices and reset. Baseline contrasts
default to valid run-specific choices. Browser QA caught a rapid-click race in the
initial server-side facet callback; synchronous client-side normalization replaced
it. The memory-only store contains configuration fields only, not measurements or
question text. A Node-assisted parity test verifies Python/browser normalization.
Idle request logs settled after interaction; no continuing callback loop observed.

Readable answer/reference cards, score tables, per-question retrieval coverage,
question text/ID search and cross-configuration question retention replace mandatory
JSON reading; original JSON/lineage remain expandable. Safe annotation/source/context
intersections highlight text with plain React components, not HTML parsing or
generation changes. Retrieval scores are labeled as original retrieval scores,
not reranker scores. Paired effect plots/tables display existing source intervals,
question/source counts and pp/second differences without recomputing inference.
Existing EM/F1/coverage/rate and mean/median/p95 selectors use saved metrics only.

Filtered CSV is in-memory and formula-neutralized; full-snapshot downloads remain
separate. CSV metadata now carries uncertainty/source counts. Stage A vectors include
exact per-cell question/timing counts. Unknown hosts and invalid download filters
are rejected. Local JS associates labels with controls and collapses mobile filters;
390px views have no horizontal overflow. No new runtime package was added.

Fresh output `reports/dashboard-snapshot-v3`, manifest
`dafbc9c28f7f87707b6b7c5076e416988b26fd940519edb5e18dcdb9fb45d3d0`.
All four run objects equal v2 exactly: 176 cells, 31,200 metadata rows and 1,520
examples, including original intervals/raw links/offsets. Twelve original core
vector files and Stage A bar geometry are unchanged; only eight Stage A vectors'
captions and CSV metadata differ. Original v1/v2 snapshots/archives are preserved.

Actual verification:

- Isolated focused discovery: 35 passed, 0.494 s;
  `artifacts/dashboard-improvements-tests-v5.log`.
- Full core regression after final UI logic: 251 discovered, 230 passed,
  21 optional viewer tests skipped (Dash absent from core), 15.399 s;
  `artifacts/dashboard-improvements-core-tests-v3.log`. All 21 viewer tests passed
  in the isolated suite above. Node is optional QA-only; parity skips if unavailable.
- Changed Python/focused tests Ruff passed; local JS syntax check passed.
- `artifacts/check-dashboard-improvements-v1.py` passed all 808 CSV metric rows,
  exact original run/example/offset/lineage equality, unchanged geometry/core vectors
  and exact caption counts. Proof manifest
  `0e19fc079ab1c5fe146f4024a78f16fd52c28abc4dda1554b3340e07e0419d50`.
- Final Chrome checks against v3 passed: cloud action/destination disabled, rapid
  filters/scoped 75-request count, metric/CSV choices, search/reset/question retention,
  coverage/highlighting, baseline pairs, Stage A, 390px/collapsed filters/labels and
  no JavaScript exceptions. `artifacts/dashboard-improvements-browser-verification-v2.json`.
  Earlier quoting/DOM-serialization test-helper failures and the actual filter-race
  failure were corrected before this passing run; failed runs are not counted passed.

Guides updated: README, deep dive and `reports/dashboard-handoff-v2/README.md`.
`configs/dashboard-validation.json` records critical commands/invariants outside
ignored tests/docs. The user server was refreshed on 8050 with snapshot v3; a
separate owned 8051 preview/browser is used for QA and will be stopped at handoff.
Markdown/tests remain ignored, nothing staged, user `.gitignore` edit untouched.
Next: separate `ragbench-dashboard-v2.zip` verification and fresh offline replay;
the archived progress will retain this pre-packaging checkpoint, with final outcome
in external proof/current progress rather than rewriting delivered files.

Final packaging outcome — XD.10g done:

- `artifacts/archives/ragbench-dashboard-v2.zip`: 126 inventoried payloads,
  30,916,016 bytes, SHA-256
  `ec26d922cbc52fcfa0ec0bbdce3a75d028551286eb1a55a349cedf452dcbfa1f`.
  Every member checked; external proof
  `artifacts/dashboard-improvements-archive-verification-v1.json`, manifest
  `fff658f77a25a23a2a3fd863f788d27f7d8648db2fc55ad5f54dcc1d5b2874b8`.
- `PYTHONPATH=src .venv/bin/python artifacts/replay-dashboard-v2.py`: passed.
  Fresh safe extraction/new temporary venv, no-index/hash-required wheel-only
  installation, pip check, all 35 archived tests, live Flask layout/dependency/
  CSS/JavaScript/CSV endpoints and isolated imports passed. External replay proof
  `artifacts/dashboard-improvements-replay-verification-v1.json`, manifest
  `48a4d703b8a4549ebb8105494344aebdc0064c244fa6ca50a2124959ba64f00c`.
- Replay rehashed both original core ZIPs and dashboard v1 ZIP; all retain their
  exact original identities. Temporary extraction/environment were removed by its
  context manager. The delivered ZIP is immutable; its archived progress records
  the checkpoint before these subsequent external verification results.
- Final source/focused tests Ruff, JS syntax and whitespace checks passed. No
  Torch/Transformers/runner/exporter modules load in the fresh isolated viewer.
  Ignored docs/tests absent from staging; user `.gitignore` edit preserved.
- User dashboard is refreshed on 8050 with v3; refresh the browser to load changed
  callbacks/assets. Owned QA preview/browser are stopped separately at handoff;
  the requested user server remains running. No commit/push or new benchmark run.

## 2026-10-14–15 — optional results dashboard

XD.1–XD.9: done for available core data and explicit pending extension views.
User authorization: “lets go for Results dashboard”, followed by “continue”. No
benchmark, model download, scientific amendment, commit or push was launched.

Changed source: `dashboard_snapshot.py` validates schema/units/condition links,
identities, hashes and safe asset paths; `dashboard_export.py` exports only from
checked saved data; `dashboard.py` supplies the local read-only Dash shell,
linked filters, question explorer, original paired comparisons, pending context
views and guarded downloads. CLI has deferred `dashboard-export`/`dashboard`
commands. CSS is local. Optional Dash 4.4.1/Plotly 7.1.0 and 28 dependencies have
their own hash-pinned lockfile; the benchmark lock/environment are unchanged.

Gates were sequenced schema/export/loader first, optional dependencies/interface
afterward. The isolated environment is `artifacts/dashboard-env`. Official PyPI
wheel-host DNS failed; downloading through official `pypi.org` with the original
CDN Host header succeeded with TLS enabled. All 28 wheel hashes were checked
against official HTTPS metadata before offline `--require-hashes` installation.
No third-party mirror downloads or system DNS changes were used. Wheel proof:
`artifacts/dashboard-wheel-verification-v1.json`, manifest
`70a7bfa522d1b47d307a9f286e7dd367f8d6df24dd46ff96c34b791a19db246e`.

Delivery snapshot: `reports/dashboard-snapshot-v2`, manifest
`dded5318528ad4d5e17b4a17c83279f47576d66331f9014d9dedb625456f1648`.
Four runs remain separate: Stage A development/evaluation, main v3, baselines.
There are 176 cells, 31,200 request metadata rows and 1,520 text examples. Stage A
retains one ID-hash-selected repetition-one question per dataset/run across all
conditions; Stage B retains all repetition-one examples. Raw records are linked,
not duplicated in this optional viewing package. Prototype snapshot v1 is not
the delivery artifact and remains preserved locally.

Independent check `artifacts/check-dashboard-snapshot-v2.py` passed: Stage A
saved estimates/timing intervals/counts, original Stage B metrics/source intervals,
all 4,200 main/baseline request links, all 1,520 question/answer records and every
packed source offset, plus all new Stage A vector bar values. Proof:
`artifacts/dashboard-snapshot-verification-v2.json`, manifest
`271babf1861c8587b6d5f43695f99597f6e9153fc7f68adf3b5bb3fe28d444ba`.

Decision 2026-10-14: reuse the existing standard-library SVG/PDF renderer instead
of adding Matplotlib. Twelve verified core publication assets are copied unchanged;
eight Stage A assets are new offline renderings. Output formats, numbers, units,
counts and uncertainty contracts are unchanged. Stage A uses 500 question-cluster
draws with source-dependence limitations labeled; Stage B retains original 2,000
source-cluster draws and matched contrasts. Missing studies remain pending.

Actual verification:

- `PYTHONPATH=src artifacts/dashboard-env/bin/python -m unittest discover -s tests -p 'test_dashboard*.py' -v`: 21 passed, 0.397 s; `artifacts/dashboard-tests-v4.log`.
- Full core unittest discovery with recorded Torch library path: 237 discovered,
  227 passed, 10 optional viewer tests skipped, 14.983 s;
  `artifacts/dashboard-core-regression-v1.log`. All ten skipped viewer tests passed
  in the separate isolated suite above.
- Ruff on changed Python/CLI and three focused test files: passed.
- Isolated `pip check`: passed. Core environment still has no Dash/Plotly.
- Fresh viewer import and actual `/_dash-layout` response: 200; no Torch,
  Transformers, runner or exporter modules loaded.
- Isolated headless Chrome: charts, Stage A filters, source explorer, paired-model
  boundaries, pending views and allowlisted CSV download passed; no JavaScript
  exceptions. `artifacts/dashboard-browser-verification-v2.json`; screenshots
  `dashboard-main-preview-v3.png`, `dashboard-retrieval-preview-v2.png`,
  `dashboard-explorer-preview-v2.png` under `artifacts/`.
- Focused tests cover missing Stage B, incomplete/incompatible runs, writer
  startup/request guards, formula neutralization, unsafe text, tampering,
  traversal/symlinks, linked selections and a real Dash callback HTTP POST.

Local guidance updated: README, PROJECT_DEEP_DIVE, PRD, PLAN and a clearly labeled
current-status appendix to the historical `report.md`. Handoff:
`reports/dashboard-handoff-v1/README.md`. Markdown/tests remain ignored, no files
are staged, and the unrelated `.gitignore` edit is preserved. Standalone archive
verification and extraction checks are the final packaging step; their external
proofs record the actual outcome without rewriting core delivery artifacts.

Packaging outcome (done, 2026-10-15):
`artifacts/archives/ragbench-dashboard-v1.zip` contains 123 inventoried payloads,
30,893,058 bytes, SHA-256
`4ba313b696888fac6365751ff4d38a43fff92f68cc412294f84d1ff2b001b2dc`.
Every payload was verified by the existing archive verifier; external proof is
`artifacts/dashboard-archive-verification-v1.json`. The archived progress file
records the pre-packaging checkpoint; this entry and the external proof record
subsequent completion without rewriting the delivered ZIP.

`PYTHONPATH=src .venv/bin/python artifacts/replay-dashboard-v1.py`: passed after
fresh safe extraction and a new temporary environment. Wheel-only/no-index/hash-
required installation, `pip check`, CLI help, all 21 archived tests, real snapshot
layout/dependencies/CSS/CSV responses and absent model/runner/exporter imports
passed. Proof `artifacts/dashboard-replay-verification-v1.json`, manifest
`4dd04e785d1199b174a13c5417dcf097dc451a27efe625045b51ae56b9346786`.
The replay also rehashed both core delivery ZIPs and confirmed their original
identities. Temporary replay extraction/environment were removed by its context
manager. The verification browser/server are stopped at handoff; the isolated
viewer environment, wheels and snapshot remain available for user startup.

## Completed planning

| Item | Status | Evidence |
| --- | --- | --- |
| Project goals and scope | done | PRD.md |
| Two-stage experimental design | done | PRD.md and PLAN.md |
| Contributor, Git, and writing rules | done | AGENTS.md |
| Task breakdown and phase gates | done | PLAN.md |
| Local ignore template | done | .gitignore in the planning bundle; exclusion patterns checked during document preparation |
| Runtime feasibility | done | Phase 6's measured 40-request paired pilot; original estimates remain separate from reduced-study results |

## Phase status

| Phase | Status | Evidence / next gate |
| --- | --- | --- |
| 0 — scaffold | done | Editable install, configuration checks, local tests, and hardware inventory verified |
| 1 — data | done | Both real pilot preparations pass saved-hash, evidence, and split checks; HotpotQA mirror provenance recorded |
| 2 — chunking and BM25 | done | Six profiles inspected; full-corpus BM25 smoke from both datasets to packed context and evidence metrics |
| 3 — Dense and Hybrid | done | 42 local tests and all five recipes on both bounded real corpora; saved identities, native runtime, and timing verified |
| 4 — Stage A | done | Complete development/evaluation runs, freeze and reports |
| 5 — generation and reranking | done | Integrated adapter/reranker/baselines/scoring; 16 real-model diagnostics and regression checks passed |
| 6 — pilot and freeze | done | 40 paired requests, verified cache controls/resources, prospective scientific study freeze |
| 7 — Stage B | done | Reduced v3 main 3,600/3,600; separate baselines 600/600; archive verified; v1/v2 preserved separately |
| 8 — analysis | done | Paired reports, figures, declared failure review, validity discussion, two-part delivery and fresh-workspace replay verified |

## Decisions

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-10-12 | Prepare Phase 5 in an isolated detached checkout while keeping the benchmark checkout and environment fixed | User requested completion; independent implementation can advance during long offline index builds. Stage A gates still precede integration and model-backed validation |
| 2026-10-12 | Correct the proposed reranker ID from ms-marco-MiniLM-L-6-v2 to the published ms-marco-MiniLM-L6-v2 | The intended six-layer candidate exists under the latter ID; this corrects an identifier typo, not the factorial or Stage A reranking-off setting. Publisher: https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2 |
| 2026-10-12 | Pin the native chat-template date and reject backend/native prompt-count discrepancies | Llama's native template can insert the current date; explicit date avoids prompt changes across days. Token-count mismatch requires review rather than assuming truncation did not occur |
| 2026-10-12 | Phase 5 generation remains diagnostic until Phase 6 cache isolation is verified | Ollama may reuse prompt work; cached counts are recorded when present and missing counts stay unknown. No formal generation latency claim is authorized from these diagnostics |
| 2026-10-12 | Retain the PRD 50 development/100 held-out questions and complete declared source corpora in a separate Stage A study config and preparations | User authorized continuation of Phase 4; the planned split is feasible with default source isolation. Preserve 10/10 pilots and their identities |
| 2026-10-12 | Plan 24 hours of CPU compute, 20 GiB disk, and an 8 GiB process-memory allowance for development screening | Full-corpus profiles and sampled throughput project about 9.8 hours of encoding/chunking/BM25 work and 6.6 GiB payloads; allow overhead and thermal variation. These are estimates/allowances, not full-run measurements or enforced caps |
| 2026-10-12 | Continue using the already pinned HotpotQA mirror as the explicitly declared adapted corpus | Source bytes and corpus identity remain unchanged; official-byte equivalence remains unverified and must be disclosed in selection/report/archive provenance |
| 2026-10-11 | Split P4.3–P4.5 into implementation and real-compute tasks | Synthetic and bounded diagnostics do not establish development selection or held-out findings |
| 2026-10-11 | Final automatic selection requires complete successful first attempts and the PRD 50/100 split | Preserve bad runs/retries and prevent the existing 10/10 pilots from silently redefining the frozen study |
| 2026-10-11 | Report timing uncertainty by resampling whole question clusters; no interval for one question | Repetitions measure the same question and are not independent quality observations |
| 2026-10-11 | Working repo name: ragbench-lab | Describes the evaluation scope; alternatives have not been selected |
| 2026-10-11 | Broad retrieval screening before end-to-end runs | Expands retrieval coverage while controlling generation cost |
| 2026-10-11 | Stage A: 30 configurations per dataset | Five recipes, two chunkers, three sizes |
| 2026-10-11 | Stage B: 12 configurations per dataset/model | Three families, two sizes, reranking off/on |
| 2026-10-11 | Two datasets and two small local generators | Check whether results depend on dataset and generator |
| 2026-10-11 | README, project deep dive, and tests stay out of Git | User's repository policy; local validation remains required |
| 2026-10-11 | PLAN.md owns task checkboxes | Avoid conflicting completion states across documents |
| 2026-10-11 | Use native local JSON with the standard library for Phase 1 | No implemented requirement needs Hugging Face Datasets yet; installation previously failed on PyPI DNS |
| 2026-10-11 | Exclude whole questions with missing, invalid, or ambiguous evidence before sampling; record every exclusion | Prevent partial evidence labels from overstating coverage; do not repair answer offsets |
| 2026-10-11 | Seeded SHA-256 sampling, development first, isolate evidence documents and titles by default | Stable source-order-independent selection; insufficient isolated candidates fail explicitly |
| 2026-10-11 | HotpotQA exact title/sentence duplicates share documents; conflicting variants remain distinct | Preserve source provenance and detect ambiguous supporting titles |
| 2026-10-11 | Split P1.4 and P1.5 into implementation and real-data verification subtasks | Synthetic validation does not establish the complete real-data phase gate |
| 2026-10-11 | Temporarily ignore all Markdown and remove existing Markdown files from the index, preserving local contents | User requested all Markdown stay local for now, with explicit force-add available for selective commits; supersedes the earlier Markdown tracking policy |
| 2026-10-11 | Use HotpotQA mirror revision 7e54db4656209750ff487f6fdf8e39a66dba136b for pilot data preparation | Official host repeatedly timed out; mirror bytes match its published SHA-256. Official byte equivalence is not verified; record this limitation before final study freeze |
| 2026-10-11 | Pin BGE tokenizer revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a and tokenizers 0.22.1 | Accurate offsets and counts without downloading model weights; runtime dependency graph saved in requirements.lock |
| 2026-10-11 | BM25 uses Unicode word/casefold preprocessing, k1 1.5, b 0.75, positive log1p Robertson IDF, and repeated query-term counts | Declare formula and preprocessing before screening; use a small sparse standard-library implementation instead of adding rank_bm25 |
| 2026-10-11 | Sentence boundaries use HotpotQA source sentences or punctuation/paragraph heuristic; overlong sentences fall back to verified fixed-token slices | Deterministic rule without a learned sentence-segmentation dependency; abbreviation handling remains heuristic |
| 2026-10-11 | Include bracketed full chunk IDs and separators in context budget; verify actual concatenated text | Preserve source mapping and exact budget despite non-additive tokenization; only final included chunk is truncated |
| 2026-10-11 | Phase 2 retrieval accepts development IDs only and stores diagnostic JSON records | Avoid premature held-out evaluation; timing repetitions, selection, and formal JSONL runner remain Phase 4 work |
| 2026-10-11 | Phase 3 uses direct Transformers/PyTorch BGE CLS and E5 masked-mean pooling, published prefixes, CPU float32, four threads, and seed 20261011 | Make input-length and pooling behavior explicit; SentenceTransformers is suggested, not required. No accelerator timing or numerical mode is silently substituted |
| 2026-10-11 | Pin E5 revision ffb93f3bd4047442299a41ebb6fa998a38507c52 and preserve the Phase 2 BGE revision | Official model API supplies Git blob identities and weight SHA-256; check files before loading, never download inside retrieval |
| 2026-10-11 | Phase 3 validation uses synthetic fixtures followed by declared source-order bounded corpora | Validate all recipes without launching the full Stage A matrix or inspecting held-out results |
| 2026-10-11 | Replace initial Transformers 4.57.6 pin with 5.0.0 and restore Hub 1.33.0; pin NumPy 2.3.5 | Preserve the existing datasets 5.1.0 dependency and Python 3.11 package support. Runtime lock remains Python 3.14/macOS arm64-specific |
| 2026-10-11 | Use one shared OpenMP library on macOS via CLI startup re-execution with torch/lib first in DYLD_LIBRARY_PATH | Both pip wheels otherwise abort with duplicate OpenMP initialization; do not modify native binaries or suppress the safety check. Record the shared-library hash in model/index identity |

These decisions include original planning history. The measured pilot, selection,
pinned inputs and completed reduced study now exist; their later dated evidence
and current phase table supersede the early scaffold checkpoints.

## Open items

| Item | Current status | Evidence / remaining action |
| --- | --- | --- |
| Hardware, models and package versions | resolved | Inventory, study/assets manifests and lockfiles |
| Dataset hashes, corpus pool and split IDs | resolved | Prepared manifests; mirror equivalence remains unverified |
| Embedder/chunker selection | resolved | Frozen E5 sentence-aware development selection |
| Cache policy and timer boundaries | resolved for pinned backend | Isolation proof, pilot and execution manifests; cold-kernel limits remain |
| Active sample/workload | resolved | 25 IDs/dataset; 3,600 main and 600 separate baseline successes |
| Local archival | resolved | Core and viewer ZIPs with external verification proofs |
| Off-device backup | pending user decision | Local archives exist; external backup confirmation not established |
| Public sharing/licensing/privacy clearance | pending | Review text, paths, terms and permitted audience |
| Supervisor acceptance of reduced scope | unverified | Do not imply approval from software completion |
| Optional model/context/load studies | pending authorization | Separate manifests, development gates and budgets |

No unresolved item here requires automatically launching more core requests.

## Verification record

The following Phase 0 checks are historical, dated 11 October 2026. No model runs
had occurred at that checkpoint; subsequent execution evidence appears below.

| Date | Task | Command / inspection | Result | Artifact |
| --- | --- | --- | --- | --- |
| 2026-10-11 | P0.1 | `python -m pip install -e .` | passed; editable package and CLI installed | `pyproject.toml`, `src/ragbench_lab/` |
| 2026-10-11 | P0.2 | `python -m ragbench_lab validate configs/pilot.toml` | passed; config hash recorded and 30 Stage A conditions confirmed | `configs/pilot.toml` |
| 2026-10-11 | P0.2 | `python -m unittest discover -s tests -v` | passed; 2 tests including invalid candidate-depth rejection | ignored `tests/test_phase0.py` |
| 2026-10-11 | P0.3 | `python -m ragbench_lab hardware --workspace .` plus Windows and `nvidia-smi` inspection | passed; CPU, RAM, GPU, disk, Python, and backend availability recorded | `manifests/hardware.json` |
| 2026-10-11 | P0.1 | `git check-ignore -v README.md PROJECT_DEEP_DIVE.md tests/test_phase0.py` | passed; local docs and tests ignored | `.gitignore` |

For subsequent work, append an entry containing date, task ID, command or inspection, result, and relevant artifact path. Use exact commands only after they exist and have been run.

### Phase 1 verification — 2026-10-11

- `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v`: passed, 12 tests covering Unicode offsets, paragraph reconstruction, supporting sentences, shared-corpus deduplication, same-title variants, explicit exclusions, duplicate IDs, split isolation/determinism, source hashes, CLI preparation, no-overwrite behavior, and saved-artifact corruption. An intermediate run failed two manifest round-trip assertions because tuples became JSON lists; normalized the returned JSON manifest and reran successfully.
- `PYTHONPATH=src .venv/bin/python -m ragbench_lab validate configs/pilot.toml`: passed, existing config hash unchanged and 30 Stage A conditions confirmed.
- `.venv/bin/python -m compileall -q src`: passed.
- Official SQuAD validation download via `curl --fail --location --max-time 60 --output data/raw/squad-dev-v1.1.json https://raw.githubusercontent.com/rajpurkar/SQuAD-explorer/master/dataset/dev-v1.1.json`: passed. `shasum -a 256 data/raw/squad-dev-v1.1.json` returned `95aa6a52d5d6a735563366753ca50492a658031da74f301ac5238b03966972c9`.
- `PYTHONPATH=src .venv/bin/python -m ragbench_lab prepare configs/pilot.toml --dataset squad --source data/raw/squad-dev-v1.1.json --revision squad-dev-v1.1 --sha256 95aa6a52d5d6a735563366753ca50492a658031da74f301ac5238b03966972c9 --output data/prepared/squad-pilot-v1`: passed; 48 reconstructed articles, 10,570 eligible questions, zero exclusions, 10 development and 10 evaluation questions, zero evidence-document/title overlap. These are preparation counts, not retrieval or performance results.
- `PYTHONPATH=src .venv/bin/python -m ragbench_lab inspect-data data/prepared/squad-pilot-v1`: passed; manifest `9893c13ff89d482bac5412ff28cbdd7136a3053bede3abcd685ca81e7951734d`. Read-only sample inspection of development question `57296f85af94a219006aa406` confirmed `Chloroplast` source slice `[26789:26795]` equals annotated answer `starch`.
- HotpotQA official-source connectivity checks with `curl --head --location --max-time 15` against both `https://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json` and its original HTTP URL: both failed with curl exit 28 (15-second connection timeout). No real HotpotQA artifact was created or claimed verified.
- `git check-ignore -v README.md PROJECT_DEEP_DIVE.md tests/test_phase1.py`: passed. `git diff --cached --name-only`: empty; nothing staged or committed. A full `git diff --check` reports the pre-existing trailing blank line in the user's `.gitignore` change; scoped checks of this task's tracked edits passed. Required planning files remain tracked despite existing redundant ignore entries.

The current Mac environment still lacks an editable package installation; the earlier Phase 0 install and Windows hardware checks are historical evidence, not current-machine verification. Current commands above use `PYTHONPATH=src` and the standard-library-only `.venv`. No dependency was added, so no dependency lockfile was created in this task.

## Experiment ledger

Current completed active runs (15 October 2026):

| Run ID | Scope | Successful / planned | Failed attempts | Artifact |
| --- | --- | --- | --- | --- |
| 8aee356a-46ae-4af2-9fc0-496a74d40a64 | A development | 9,000 / 9,000 | 0 | `runs/stage-a-development-v1/` |
| 7b44f0dd-5dac-4553-a442-0f58e197f946 | A held-out retrieval | 18,000 / 18,000 | 0 | `runs/stage-a-evaluation-v1/` |
| 9b893393-897e-43eb-a72a-80b30bc539d6 | B reduced v3 main | 3,600 / 3,600 | 0 | `runs/stage-b-evaluation-v3/` |
| 7122ea5a-5aeb-427b-bbbb-31df30cb9d89 | Separate baselines | 600 / 600 | 0 | `runs/baseline-evaluation-v1/` |

Main/baseline runs reuse the same fifty question units; totals are not independent
sample counts. Historical v1/v2 generation attempts remain separate and excluded.

### Historical launch checkpoint — 12 October 2026

Full Stage A screening began on 2026-10-12. The table below was a launch
observation, not a live completion counter. At that time the planned main
workload was 14,400 and generation had not yet begun.

| Run ID | Stage | Config/manifest | Planned / completed / failed | Artifact location |
| --- | --- | --- | --- | --- |
| 8aee356a-46ae-4af2-9fc0-496a74d40a64 | A development; in_progress | configs/stage-a-study.toml; manifest 2d621cf0c65ef2b18ae7009a24ead7eb8e46cf771b809bd4e1769cec08f182b2 | 9,000 planned / 100 verified successes / 0 failed attempts or setup failures at launch checkpoint | runs/stage-a-development-v1/; indexes/stage-a-study-v1/ |

## Session handoff template

Copy this structure for each meaningful implementation session:

- Date:
- Task IDs and resulting status:
- Changed behavior and files:
- Verification performed and result:
- Decisions or deviations:
- Blockers:
- Next smallest task:

Keep entries short and factual. Only mark tasks done when their completion checks pass. Preserve failed experiment records and describe retries explicitly.

## Session handoff

- Date: 2026-10-11
- Task IDs and resulting status: P0.1, P0.2, and P0.3 done; Phase 0 gate passed.
- Changed behavior and files: added installable package and CLI, strict TOML configuration records, pilot config, hardware probe and inventory; corrected ignore rules so required planning files can be tracked.
- Verification performed and result: editable install, valid config CLI, hardware CLI, compile check, and 2 focused tests passed. Invalid candidate depth raises a clear configuration error.
- Decisions or deviations: TOML and standard-library validation avoid premature runtime dependencies. Dataset/tokenizer revisions remain explicit placeholders until their download phases.
- Blockers: Ollama is not installed or reachable. This does not block Phase 0; model feasibility remains a Phase 6 measurement.
- Next smallest task: P1.1, define typed data and evidence records.

## Phase 1 session handoff — 2026-10-11

- Task status: P1.1, P1.2, P1.3, P1.4a, P1.5a done; P1.4b and P1.5b pending for real HotpotQA. Phase 1 remains in_progress.
- Changed files: `src/ragbench_lab/data/` records, adapters, preparation/inspection; CLI `prepare` and `inspect-data`; `configs/data-smoke.toml`; compact SQuAD pilot provenance in `manifests/squad-data-pilot-v1.json`; tracked contract/checklists/status; ignored README, deep dive, and local tests.
- Verification: 12 tests, CLI smoke, real SQuAD preparation and persisted identity/evidence/split checks passed. No RAG benchmark or model run was executed.
- Artifacts: ignored SQuAD source in `data/raw/`; prepared corpus/questions/full manifest in `data/prepared/squad-pilot-v1/`. This is a 10/10 pilot data selection, not the final 50/100 study freeze.
- Blocker: official HotpotQA host unreachable over both protocols; real-source format and evidence gate remain unverified. Native JSON ingestion is usable offline as soon as a source file is available.
- Next smallest task: P1.4b, acquire and hash the official HotpotQA distractor validation file, then run `prepare` and `inspect-data` before advancing to Phase 2.

## Local README handoff — 2026-10-11

- Updated ignored `README.md` with project purpose, current implementation status, setup, existing-corpus inspection, source-hash preparation examples, pilot sample counts, and local validation guidance. No phase task status changed; next task remains P1.4b.
- Verified `PYTHONPATH=src .venv/bin/python -m ragbench_lab --help`, `validate configs/pilot.toml`, and `inspect-data data/prepared/squad-pilot-v1`: passed. Editable installation remains optional and unverified in this environment; its documented command is not claimed to have succeeded.
- `git check-ignore -v README.md`: confirmed ignored. `git diff --cached --name-only`: empty; no documentation or tests staged, and nothing committed.

## HotpotQA download and Phase 1 gate — 2026-10-11

- P1.4b and P1.5b done. Official HTTPS download retry failed with curl exit 28 after the 15-second connection timeout. Downloaded a 61.1 MB revision-pinned mirror from `https://huggingface.co/datasets/namlh2004/hotpotqa/resolve/7e54db4656209750ff487f6fdf8e39a66dba136b/hotpot_dev_distractor_v1.json` instead; no adapter or sampling changes were needed.
- `shasum -a 256 data/raw/hotpot-mirror-7e54db4.json.part` returned `e3da074df24e8369009918aa5cdbdd254dadcde4c63f7569d36afd6f2268caa8`, matching the pinned mirror's published checksum. Renamed the completed file to `data/raw/hotpot-mirror-7e54db4.json`.
- `PYTHONPATH=src .venv/bin/python -m ragbench_lab prepare configs/pilot.toml --dataset hotpot_qa --source data/raw/hotpot-mirror-7e54db4.json --revision namlh2004/hotpotqa@7e54db4656209750ff487f6fdf8e39a66dba136b --sha256 e3da074df24e8369009918aa5cdbdd254dadcde4c63f7569d36afd6f2268caa8 --output data/prepared/hotpot-pilot-v1`: passed. Pool has 7,405 questions, 66,635 distinct documents, 7,404 eligible questions, 54 same-title variants, and one exclusion. Development/evaluation samples are 10/10 with no question, evidence-document, or title overlap.
- `PYTHONPATH=src .venv/bin/python -m ragbench_lab inspect-data data/prepared/hotpot-pilot-v1`: passed; full manifest identity `1b33f8d785170e3896a6e9563583731c148af1eeaae540ae1723a4c3ee0c18e9`. Development sample `5a83dd2c554299334474609e` has three verified sentence mappings across `Martin Ruhe` and `The American (2010 film)`.
- Excluded question `5ae61bfd5542992663a4f261` has a missing supporting sentence, confirmed against the original mirror row. Its ID/reason are retained in the full manifest and compact provenance; it was not repaired or silently discarded.
- Added compact provenance `manifests/hotpot-data-pilot-v1.json`; updated ignored PLAN, PROGRESS, and README. Raw/prepared data remain ignored. No model run or performance measurement, and no new commit, was made.
- Limitation: the official source remains unreachable, so equivalence to official bytes is unverified. This is pilot data preparation, not a frozen 50/100 study sample or a held-out experiment.
- Next smallest task: P2.1, fixed-token chunking with source offsets.

## Phase 2 session handoff — 2026-10-11

- P2.1–P2.4 done; Phase 2 gate passed. Source modules: `tokenization`, `chunking`, `retrieval`, `context`, `metrics`, and `pipeline`; CLI commands `chunks`, `index`, `retrieve`; validated BM25 settings in config; prepared-data loader reused. Added `configs/bm25-pilot.toml`, `requirements.lock`, and `manifests/reference-tokenizer-v1.json`. Local README/deep dive/plan/status updated and still ignored.
- Dependency setup: `.venv/bin/python -m pip install tokenizers==0.22.1` passed. Resolver changed huggingface-hub from 2.2.0 to 1.33.0 to satisfy tokenizers' supported range; pip check passes. `.venv/bin/python -m pip install --no-deps -e .` passed, refreshing installed package metadata. The previously reported editable-install blocker is now resolved. The lockfile records the runtime dependency closure for Python 3.14/macOS arm64, not a universal cross-platform lock.
- Tokenizer-only download from the pinned BGE source passed; `shasum -a 256 models/bge-small-en-v1.5/tokenizer.json` returned `d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66`. No model weights downloaded; truncation/padding disabled, counts exclude automatically added special tokens.
- `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v`: 27 tests passed, including 15 new tests for fixed/sentence boundaries, fallback, Unicode/WordPiece re-tokenization, all six real-tokenizer profiles, BM25 formula/ties, headers and truncation, evidence union/deduplication, SQuAD alternative locations, HotpotQA all-required scoring, stale index/corruption rejection, tokenizer mismatch, and development-only retrieval.
- `.venv/bin/python -m compileall -q src`, `.venv/bin/python -m pip check`, `.venv/bin/ragbench validate configs/bm25-pilot.toml`, and `git diff --check`: passed. Phase 2 resolved config identity is `4f6064df1fc7cd07870510710bc359129bf9ce99d68347ca4f497f6760af4c34`. New resolved defaults change hashes when old TOML files are reloaded; existing Phase 1 manifests/hashes were preserved and remain verifiable, not rewritten.
- Six-profile diagnostics: `PYTHONPATH=src .venv/bin/python -m ragbench_lab chunks configs/bm25-pilot.toml --data-dir data/prepared/squad-pilot-v1 --output artifacts/phase2-squad-profiles-v1.json` passed on all 48 documents. Fixed-token chunk counts at 64/128/256 were 5,180/2,603/1,314; sentence-aware 7,058/3,045/1,413, with 449/20/1 fallback sentences. Same command for `data/prepared/hotpot-pilot-v1`, with `--document-limit 100 --output artifacts/phase2-hotpot-profiles-100docs-v1.json`, passed on a declared source-order diagnostic prefix. All six observed max token lengths are at or below targets; full HotpotQA six-profile distribution screening remains future work.
- Full-corpus indexes: `index configs/bm25-pilot.toml --data-dir data/prepared/squad-pilot-v1 --method fixed_token --size 128 --output indexes/squad-fixed128-v1` and `index configs/bm25-pilot.toml --data-dir data/prepared/hotpot-pilot-v1 --method sentence_aware --size 128 --output indexes/hotpot-sentence128-v1` (both through `PYTHONPATH=src .venv/bin/python -m ragbench_lab`) passed. Saved 2,603 and 94,110 chunks respectively. Both indexes reference exact source/config/tokenizer identities; postings rebuild during offline load, before online timing starts.
- Real development smoke commands: `retrieve configs/bm25-pilot.toml --data-dir data/prepared/squad-pilot-v1 --index indexes/squad-fixed128-v1 --output runs/phase2-squad-bm25-smoke-v1.json` and equivalent HotpotQA command with `--data-dir data/prepared/hotpot-pilot-v1 --index indexes/hotpot-sentence128-v1 --output runs/phase2-hotpot-bm25-smoke-v1.json` (same Python invocation) passed. Each retrieved 50 chunks and packed exactly 1,024 tokens, truncating only the final included chunk. Development question IDs were `57296f85af94a219006aa406` and `5a83dd2c554299334474609e`.
- Observations, not study conclusions: SQuAD's example had answer-span and supporting-paragraph coverage in packed context; HotpotQA's example had 2/3 supporting sentences in top 50, but zero complete supporting sentences in context. Recorded online paths were about 0.082 s and 0.114 s, without planned warmup/repetitions or uncertainty; do not compare these as benchmark estimates. Full prompts/LLM timing do not exist yet. Raw smoke artifacts retain the results and stage timings.
- Limitations: sentence segmentation is heuristic on SQuAD; blank/control-only source regions are omitted from searchable chunks. Index artifacts store chunks and rebuild BM25 postings during offline initialization. Full formal JSONL run/error/resume machinery, timing repetitions, Dense/Hybrid, and embedding-input truncation detection remain later phases. HotpotQA mirror provenance limitation remains.
- Next smallest task: P3.1. No commit made during Phase 2; ignored documentation/tests/data/indexes/runs are not staged.

## Phase 3 session handoff — 2026-10-11

- P3.1–P3.5 done; Phase 3 gate passed on bounded real corpora. Added `embeddings.py`, `dense.py`, `native.py`, RRF and BM25 postings persistence in `retrieval.py`, recipe-aware indexing/retrieval and stage timings in `pipeline.py`, CLI recipe/model-directory options and `download-embedders`, optional validated embedding config, `configs/retrieval-pilot.toml`, and compact `manifests/embedding-artifacts-v1.json`. Updated runtime dependencies/lock and local ignored guidance/tests.
- `.venv/bin/python -m pip install torch==2.9.1 transformers==4.57.6 faiss-cpu==1.13.2` installed successfully after one interrupted/resumed PyTorch download, but reported a conflict with pre-existing datasets 5.1.0. Resolved with `.venv/bin/python -m pip install transformers==5.0.0 huggingface-hub==1.33.0`; no dataset package was removed. `.venv/bin/python -m pip install numpy==2.3.5` preserves the package's Python 3.11 floor. Installed optional local linter ruff 0.14.0; it is not a runtime dependency. `.venv/bin/python -m pip install --no-deps -e .` passed and refreshed metadata.
- `PYTHONPATH=src .venv/bin/python -m ragbench_lab download-embedders --models-dir models` passed with network permission, and a second offline invocation reused verified files without downloading. Both weight files are 133,466,304 bytes. `shasum -a 256 models/bge-small-en-v1.5/model.safetensors models/e5-small-v2/model.safetensors` returned the published pinned hashes `3c9f31665447c8911517620762200d2245a2518d6e7208acc78cd9db317e21ad` and `45bfa60070649aae2244fbc9d508537779b93b6f353c17b0f95ceccb1c5116c1`; metadata passed pinned Git blob checks. Acquisition provenance contains no private paths.
- Initial `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v` aborted with exit 134 on duplicate OpenMP initialization when FAISS and PyTorch ran together. Import order alone did not solve it. Starting Python with PyTorch's library directory first in `DYLD_LIBRARY_PATH` passed the native tensor/search probe; CLI now re-executes before native imports to share that runtime. Installed binaries remain untouched; unsafe `KMP_DUPLICATE_LIB_OK` is rejected. Runtime identity includes the shared-library SHA-256 and effective PyTorch thread counts.
- Final focused checks: `DYLD_LIBRARY_PATH=/Users/shirinmanzari/Desktop/ragbench-lab/.venv/lib/python3.14/site-packages/torch/lib PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v` passed all 42 tests. Coverage includes exact dot-product agreement, save/load, normalized/nonfinite vectors, cutoff ties (positive/zero/negative), RRF union/formula/dedup/conflicts, prefixes, special-token lengths, padding-aware pooling, saved-posting integrity, all five schemas on both adapters, fresh query encoding on repeated calls, recipe/config/vector corruption rejection, native-runtime guards, and real encoders rejecting 513/515-token inputs before forward passes. Transformers 5 reconstructs the non-trainable position-ID buffer; verified exact equivalence to pinned weights. Missing/mismatched/other unexpected keys fail loading.
- `.venv/bin/ruff check src/ragbench_lab/native.py src/ragbench_lab/embeddings.py src/ragbench_lab/dense.py src/ragbench_lab/retrieval.py src/ragbench_lab/config.py src/ragbench_lab/pipeline.py src/ragbench_lab/cli.py`, `.venv/bin/python -m compileall -q src`, `.venv/bin/python -m pip check`, `.venv/bin/ragbench validate configs/retrieval-pilot.toml`, and `git diff --check` passed. Initial lint errors were line lengths and were corrected. Config identity: `64d173f9c283157749af49a632c2139423428da922c248a89286acc6b7b3c14d`; Phase 2 config hash remains unchanged. Lock records the current Python 3.14/macOS arm64 runtime closure, not a universal lock or a clean-machine verification.
- `PYTHONPATH=src .venv/bin/python tests/phase3_smoke.py` passed ten sequential real CLI conditions: five recipes on SQuAD's first two source documents (115 fixed-128 chunks), then five on HotpotQA's first 100 source documents (140 fixed-128 chunks). Each dataset's five indexes have identical chunk hashes and output schema, 50 unique candidates, dev-only queries, and valid source mappings/context. Dense/Hybrid execute real query encoding in the online timer; Hybrid saves both 50-hit constituent lists and times fusion. Native query encoding observed approximately 0.014–0.016 seconds in these single unwarmed diagnostics; these are not latency estimates or recipe comparisons. Hotpot Dense contexts underfilled to 997/1,016 reference tokens; remaining contexts used 1,024, and underfill is recorded.
- Exact equivalent CLI workflow, for each `RECIPE` in `bm25 dense_bge dense_e5 hybrid_bge hybrid_e5`: `PYTHONPATH=src .venv/bin/python -m ragbench_lab index configs/retrieval-pilot.toml --data-dir data/prepared/squad-pilot-v1 --method fixed_token --size 128 --recipe RECIPE --document-limit 2 --output indexes/phase3-squad-RECIPE-v2`; then `PYTHONPATH=src .venv/bin/python -m ragbench_lab retrieve configs/retrieval-pilot.toml --data-dir data/prepared/squad-pilot-v1 --index indexes/phase3-squad-RECIPE-v2 --output runs/phase3-squad-RECIPE-smoke-v2.json`. Hotpot equivalents use `data/prepared/hotpot-pilot-v1`, limit 100, and `phase3-hotpot-` output prefixes. Normal commands do not depend on the ignored smoke script or synthetic fixtures.
- Raw artifacts: `indexes/phase3-{squad,hotpot}-{recipe}-v2/`, `runs/phase3-{squad,hotpot}-{recipe}-smoke-v2.json`, and aggregate diagnostic `reports/phase3-smoke-v2.json`. Offline records include chunking, model loading, corpus encoding, FAISS/BM25 construction, persistence, and asset bytes. Online records separate query encoding, constituent searches, fusion, packing, and total retrieval path.
- Backward compatibility: `PYTHONPATH=src .venv/bin/python -m ragbench_lab retrieve configs/bm25-pilot.toml --data-dir data/prepared/squad-pilot-v1 --index indexes/squad-fixed128-v1 --output runs/phase3-legacy-bm25-smoke-v1.json` passed using the original Phase 2 artifact. Preliminary `indexes/phase3-squad-dense_bge-v1` is preserved, but predates the loading-report identity check; use the complete v2 smoke set. No prior results were overwritten.
- Limitations: no complete-corpus Dense screening, held-out retrieval, repeated/warmed timing distributions, selected embedder/chunker, or LLM experiment. Formal JSONL failures/retries/resume remain Phase 4 runner work; diagnostic errors here were recorded above. HotpotQA mirror equivalence remains unverified. Direct library/test callers on macOS must set the shared runtime environment before Python starts; the CLI handles it automatically.
- Next smallest task: P4.1, enumerate 30 unique conditions per dataset. No commit made for Phase 3. `git check-ignore -v README.md PROJECT_DEEP_DIVE.md tests/test_phase3.py PLAN.md PROGRESS.md` confirmed local ignores; staged file list remains empty.

## Phase 4 implementation handoff — 2026-10-11

- Status: in_progress. P4.1/P4.2, P4.3a, P4.4a, and P4.5a are done. Full-corpus development screening, final selection freeze, and held-out evaluation remain pending. Phase 3 was subsequently committed as b06a539; this Phase 4 work is not committed.
- Changed source: conditions.py enumerates stable factorial IDs and seeded block order; run_store.py provides exclusive writers, unique run IDs, hashed manifests, fsynced hash-chained JSONL, and strict resume; stage_a.py executes offline setup, distinct warmups, and fresh online queries. pipeline.py now separates loaded sessions from query execution while retaining existing retrieve behavior.
- selection.py records four equal-dataset embedder/chunker candidates and the declared coverage/latency/index-cost rule. Incomplete matrices, failed first attempts, and diagnostic freezes are rejected. Held-out runs require matching final selection/config/data/model/tokenizer and code/environment fingerprints. reporting.py separates first-attempt quality, repeated timings, failures, and retries and gives question-clustered median/p95 uncertainty. configs/stage-a-protocol.json keeps critical commands/invariants tracked without depending on ignored fixtures.
- Verification: `DYLD_LIBRARY_PATH=/Users/shirinmanzari/Desktop/ragbench-lab/.venv/lib/python3.14/site-packages/torch/lib PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v` passed all 50 tests. Eight new Phase 4 tests cover factorial uniqueness/block order, lock/resume/retry integrity, corrupt/partial-tail preservation, full synthetic matrix stop/resume, no duplicate successes, fresh query encoding, selection weights/first-repetition isolation, close-score tie breaks, held-out/diagnostic guards, setup versus online failure separation, report counts, and seeded question-cluster intervals.
- Real-model diagnostic command: `PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-a-run configs/retrieval-pilot.toml --squad-dir data/prepared/squad-pilot-v1 --hotpot-dir data/prepared/hotpot-pilot-v1 --index-root indexes/phase4-diagnostic-v1 --output runs/phase4-diagnostic-v1 --document-limit 2 --question-limit 1 --max-requests 7` passed and stopped at seven successes. Same command without max-requests and with `--resume` completed 180 successes: 60 conditions, three repetitions, one dev question per dataset. Zero request/setup failures and 180 separate warmup events. A subsequent identical resume remained complete with 180 unique successful request keys and no extra events.
- Raw run ID: db662256-9b68-437c-b3c5-1246225d3116. Manifest SHA-256: b5fd3e24efabc42aa828ff67ccc69e46a45f69330a4b22e0d1d0b361ff9cf05a. Assets: ignored indexes/phase4-diagnostic-v1/ and runs/phase4-diagnostic-v1/. `stage-a-select --run-dir runs/phase4-diagnostic-v1 --output reports/phase4-diagnostic-selection-v1.json` and `stage-a-report --run-dir runs/phase4-diagnostic-v1 --output reports/phase4-diagnostic-summary-v1.json` (same source Python invocation) passed.
- These measurements are diagnostics only. Both source-order corpora contain just two documents, and all selection coverage scores were zero; the diagnostic ordering is not a defensible embedder/chunker choice. Single-question intervals are unavailable. Early diagnostic requests overlapped local test execution; do not interpret their timings as study estimates. No held-out questions were run, no final freeze exists, and no prior artifacts were overwritten.
- Final checks: focused `ruff check` on cli.py, pipeline.py, conditions.py, run_store.py, stage_a.py, selection.py, reporting.py passed; `.venv/bin/python -m compileall -q src`, `.venv/bin/python -m pip check`, and `git diff --check` passed. Whole-source Ruff still reports pre-existing formatting errors outside this change (chunking.py, data adapters/preparation, hardware.py); these were not rewritten. Transformers emits the previously documented position-ID-buffer report; buffers remain verified. Tokenizers emitted fork-parallelism warnings during tests, with no failed checks.
- Local README/deep dive updated; `git check-ignore -v README.md PROJECT_DEEP_DIVE.md tests/test_phase4.py PLAN.md PROGRESS.md` passed. Staged diff/file list is empty, so no ignored documents/tests are staged. No dependencies added, downloads performed, or commits made.
- Limitations: history is retained in memory; model/index loading repeats per block; Dense and Hybrid currently construct separate passage indexes. Final-screening compute/storage feasibility must be assessed rather than extrapolated from tiny diagnostics. Hotpot mirror official-byte equivalence remains unverified. Positive final-freeze/held-out integration is still unverified on real 50/100 data.
- Next smallest task: P4.3b. User scope question is pending: use planned 50 development/100 held-out samples with full corpora, or retain a 10/10 pilot without freezing the final study. Then prepare a separate run set and assess full-corpus resource cost before screening.

## Phase 4 scope and capacity handoff — 2026-10-12

- P4.3b done; Phase 4 remains in_progress. Next task is P4.3c. No full development screening, held-out retrieval, selection freeze, or generation was executed in this task.
- Added `configs/stage-a-study.toml` (identity `2d94038ed1ffa0ea93becb277a1136c7addd7341e5d3eb7bb13f83b93421292b`), `src/ragbench_lab/feasibility.py`, compact `manifests/stage-a-study-data-v1.json` and `manifests/stage-a-capacity-v1.json`; updated local ignored README/deep dive/plan/status and added ignored `tests/test_feasibility.py`. No dependency changes or downloads.
- `validate configs/stage-a-study.toml` passed. Both `prepare` commands used the same pinned source revision/SHA-256 as their pilots, new `data/prepared/{squad,hotpot}-study-v1` paths, and the new config. Each saved 50 development/100 evaluation IDs with no evidence-document/title overlap. Corpus hashes and all eligible-question records match the pilots; source bytes and exclusions were preserved. `inspect-data` passed for both new directories. SQuAD manifest: `e1d096f336c3ab6aee6055a366bb68c801fcb82df091da1b8322a6fe7b152e15`; HotpotQA: `69f4d2555d3b12f16a497dc2dded4fb730f2638b2c860988a809810bf365dacb`.
- Actual command: `DYLD_LIBRARY_PATH=/Users/shirinmanzari/Desktop/ragbench-lab/.venv/lib/python3.14/site-packages/torch/lib PYTHONPATH=src .venv/bin/python -m ragbench_lab.feasibility configs/stage-a-study.toml --squad-dir data/prepared/squad-study-v1 --hotpot-dir data/prepared/hotpot-study-v1 --output artifacts/stage-a-preflight-v1`. Passed all 12 full-corpus profiles and both native-tokenizer length checks over 675,234 profile chunk instances. Maximum native passage lengths: BGE 258, E5 260; no overlength passages. Sampled encoding used 64 evenly spaced sorted chunk IDs, one separate batch warmup, and three timed executions per profile/model. Measured peak RSS was 2,003,140,608 bytes. Full diagnostic provenance/timings are in `artifacts/stage-a-preflight-v1/{profiles.jsonl,summary.json}`; this is a capacity diagnostic, not a Stage A selection run.
- Full HotpotQA chunk counts for fixed-token 64/128/256: 153,600/92,290/69,088; sentence-aware: 176,394/94,110/69,139. SQuAD counts remain 5,180/2,603/1,314 and 7,058/3,045/1,413. Separate read-only native-tokenizer checks of only the 50 development queries per dataset passed: maximum lengths BGE/E5 were 35/29 for SQuAD and 46/40 for HotpotQA. No held-out query text was used for throughput or query-length assessment.
- Estimates, not completed full builds: encoding 34,075.89 seconds (9.47 h), chunking/BM25 1,265.88 seconds (0.35 h), and index payload 7,034,265,166 bytes (6.55 GiB). Projection accounts for separate Dense/Hybrid encoding and five chunk/three posting/four vector assets per profile. It excludes model/index loading, persistence/serialization, online requests, raw records, and filesystem overhead. Warmed samples do not establish actual full-run runtime under thermal load.
- Historical 180-request diagnostic records average 72,472 serialized bytes and 134,009 Python-object bytes per request; projected raw logs are 0.61/1.21 GiB and request history 1.12/2.25 GiB for 9,000 development/18,000 held-out requests. Smaller-corpus records may underestimate full record size; preflight peak RSS is not a measured full-run peak. Planning allowances and overrun policy are explicit in the capacity manifest.
- Current hardware: `sysctl -n hw.memsize hw.model` returned 17,179,869,184 bytes and MacBookPro17,1 after sandbox permission was granted. `ragbench hardware --workspace .` reported 8 logical cores and about 72.9 GB free disk. `manifests/hardware.json` remains the historical Windows inventory. Full study identity validation passed with 60 conditions, 50 development IDs per dataset, and no diagnostic limits.
- Verification: `.venv/bin/ruff check src/ragbench_lab/feasibility.py` passed after correcting one initial line-length error; `DYLD_LIBRARY_PATH=/Users/shirinmanzari/Desktop/ragbench-lab/.venv/lib/python3.14/site-packages/torch/lib PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v` passed all 52 tests. Existing Transformers position-buffer and tokenizers fork warnings remain, with no failed checks. `.venv/bin/python -m compileall -q src`, `.venv/bin/python -m pip check`, and `git diff --check` passed. Read-only metadata assertions verified config equality to the pilot except name/sample counts, prepared identities, artifact SHA-256 hashes, and all profile totals. Pip emitted a non-writable cache warning; dependency integrity passed.
- Limitation: the official HotpotQA byte-equivalence question remains unresolved. Full-corpus memory during accumulated runner history and positive real selection-freeze/held-out execution remain unmeasured. Planned commands in the capacity manifest have not been run; no screening run ID exists for these preparations.
- Git handoff: `git check-ignore` confirmed local Markdown/tests/prepared data/preflight artifacts ignored. `git diff --cached --name-only` was empty; nothing staged or committed. Only the new source module, study config, and two compact JSON provenance files appear as untracked source-controlled candidates.

## Phase 4 full development screening launch — 2026-10-12

- P4.3c in_progress. Started the complete unbounded development matrix at 13:46:28 Asia/Shanghai; screening, selection and reporting are not marked done. P4.4b/P4.5b remain pending.
- Run ID `8aee356a-46ae-4af2-9fc0-496a74d40a64`; run manifest identity `2d621cf0c65ef2b18ae7009a24ead7eb8e46cf771b809bd4e1769cec08f182b2`. Provenance pins commit `37b506d232658b1f3145f0b46d6efe90da15f20b`, a clean worktree, all 60 conditions, 50 development questions per dataset and three repetitions. Diagnostic limits are absent; planned requests total 9,000. No held-out execution was launched.
- Actual command launched by the local supervisor: `PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-a-run configs/stage-a-study.toml --squad-dir data/prepared/squad-study-v1 --hotpot-dir data/prepared/hotpot-study-v1 --index-root indexes/stage-a-study-v1 --output runs/stage-a-development-v1`.
- `caffeinate -i .venv/bin/python artifacts/stage-a-operations-v1/launch.py` starts the supervisor and holds an idle-system-sleep assertion. `pmset -g assertions` confirmed the assertion for caffeinate PID 29572. Supervisor PID 29571; benchmark writer PID 29573; tool execution session 20228. These PIDs/session are launch evidence and may become stale.
- Ignored `artifacts/stage-a-operations-v1/launch.py` waits for screening, then invokes `stage-a-report` to `reports/stage-a-development-summary-v1.json` and, only on a successful run/report, `stage-a-select` to `reports/stage-a-selection-v1.json`. It never retries failures or creates a selection freeze. Console output is retained in `artifacts/stage-a-operations-v1/console.log`; fsynced lifecycle events in `events.jsonl`. Future reports remain planned until their files and validations exist.
- Launch checks: config validation passed (same identity); about 72.5 GB free disk; no conflicting target run/index directories. The runner verified prepared-data and model identities before creating its manifest. Its macOS native-runtime startup guard handled the shared OpenMP environment. No package/configuration/source changes or model downloads occurred.
- First checkpoint: `verified_manifest`, `read_records`, `validate_requests`, and `completion` passed on the active run's written prefix: 100 successful request keys, zero request/setup failures, 8,900 remaining, diagnostic false, status incomplete. First two condition blocks (SQuAD Dense-BGE fixed-256 and BM25 fixed-256) produced 50 successes each. No study ranking or latency conclusion is claimed from this prefix.
- Next check: inspect supervisor events and raw records; completion requires 9,000 successful unique requests, no unreviewed failures, and saved candidate scores. A long index build can produce no new request rows until offline construction finishes. Allow roughly 10 hours plus overhead based on the preflight; this is still an estimate. Keep source/config/environment fixed while running or resuming. Do not start a second writer.
- If interrupted, preserve logs and any partial assets. Verify the recorded writer is no longer running before recovering a stale lock; never silently delete a lock or incomplete tail. Resume with the exact screening command plus `--resume` after integrity checks; failed first attempts require explicit review.

## Phase 4 follow-on queue — 2026-10-12

- User authorized the remaining sequence. P4.3c remains in_progress; P4.4b/P4.5b remain pending and are now queued. Phase 5 implementation waits until Stage A measurements finish so code/environment fingerprints remain stable.
- Started `caffeinate -i .venv/bin/python artifacts/stage-a-operations-v1/followup.py` at 13:56:07 Asia/Shanghai. Follow-on PID 29908, tool session 80431. No second development writer was launched. It polls the original supervisor's small lifecycle file every 30 seconds, with a 24-hour review deadline; it does not scan the growing raw log at each poll.
- It requires the exact development manifest `2d621cf0c65ef2b18ae7009a24ead7eb8e46cf771b809bd4e1769cec08f182b2`, a stopped writer, 9,000 successful requests, zero missing/failed/setup requests, a non-diagnostic run, and matching development summary/selection record hashes. Failure events take precedence over completion; failed/incomplete runs remain for review rather than automatic retry.
- After these gates, the existing `stage-a-select` CLI will revalidate the raw hash chain, successful first attempts, all 60 conditions, and the 50/100 split, write `reports/stage-a-selection-frozen-v1.json`, and create `manifests/stage-a-selection-v1.json`. The supervisor verifies that the frozen selection is identical to the already saved development table before launching held-out evaluation. Existing freeze/evaluation paths are preserved and rejected.
- Planned held-out command: `PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-a-run configs/stage-a-study.toml --squad-dir data/prepared/squad-study-v1 --hotpot-dir data/prepared/hotpot-study-v1 --index-root indexes/stage-a-study-v1 --output runs/stage-a-evaluation-v1 --split evaluation --freeze manifests/stage-a-selection-v1.json`. It reuses corpus indexes while recomputing the measured online path. The runner requires matching frozen source/config/model/tokenizer/code/environment identities.
- After held-out execution it invokes `stage-a-report --run-dir runs/stage-a-evaluation-v1 --output reports/stage-a-evaluation-summary-v1.json`. A `stage_a_complete` lifecycle event requires a verified report with 18,000 successes, zero failures/setup failures/missing requests and no diagnostic limits. These files/events do not exist yet and are not claimed complete.
- Follow-on logs: ignored `artifacts/stage-a-operations-v1/followup-console.log` and `followup-events.jsonl`; exclusive `.followup.lock` prevents duplicate supervisors. Exceptions/deadline expiration record `needs_review` without deleting measurements, retrying failures or changing experiment settings.
- Verification: `.venv/bin/python -m unittest discover -s tests -p test_stage_a_followup.py -v` passed three focused local tests for incomplete/failed/diagnostic request gates, failure precedence, and withholding evaluation while development is running. Supervisor startup recorded `waiting_for_development` with the exact expected manifest. No frozen selection or held-out run has been launched yet; development checkpoint remains 200 successes, zero recorded failures as observed before queuing.
- All orchestration files/tests/docs remain ignored. No tracked source/config/dependencies changed, and no commit/push was made. Future freeze creation is an authorized new provenance artifact, not an algorithm change.

## Phase 5 isolated preparation and deferred validation — 2026-10-12

- User requested finishing the active sequence. Phase 4 screening remains in_progress. P5.1–P5.5 preparation started in isolated detached worktree `/private/tmp/ragbench-phase5.qeEN0b` at commit 37b506d; no tasks are marked done. No tracked source/configuration/package changes were made in the active benchmark checkout.
- Draft source: `generation.py` implements pinned local Ollama identity, a native-template/tokenizer path, prompt/output-window guards, an overall HTTP deadline, bounded streaming, partial output/errors, backend/cache counts, abstention/truncation, and client first-visible-output timing. `answering.py` implements a development-only answer command with offline setup, fresh retrieval, optional reranking, exactly one packing pass, generation timing, post-answer evidence/quality evaluation and no-overwrite diagnostic artifacts. `pipeline.py` factors search/fusion into a shared helper; `cli.py` adds `answer` only in the isolated checkout.
- Additional draft modules: `reranking.py` loads locally pinned six-layer MiniLM classifier weights, validates every untruncated query/passage pair before any forward pass, retains the same initial candidates and uses deterministic score/ID ordering. `answer_metrics.py` follows SQuAD v1.1 and HotpotQA normalization/EM/token-F1 conventions. `baselines.py` exposes explicit empty-context and gold-evidence baselines. No-RAG retains the grounding instruction, so its abstention behavior needs that interpretation; gold packs SQuAD supporting paragraphs or HotpotQA supporting sentences under the same source-preserving context budget.
- `generator_assets.py` prepares native tokenizer exports from local Ollama model vocabulary/merges and revision-pinned publisher chat templates. The Llama pre-tokenization rule is explicit and persisted. Backend prompt-count agreement remains mandatory; this conversion is not claimed verified on real models yet. It uses existing Transformers/tokenizers, with no added dependency or download during measured work.
- `configs/generation-protocol.json` in the isolated checkout records diagnostic invariants and runnable command shapes; pinned real model/settings files still await acquisition. Preferred validation models are qwen2.5:3b-instruct-q4_K_M and llama3.2:3b-instruct-q4_K_M, both documented by Ollama. Actual artifacts/digests and server version must be recorded from local acquisition, not inferred from tag names.
- Latest synthetic validation: `PYTHONPATH=src /Users/shirinmanzari/Desktop/ragbench-lab/.venv/bin/python -m unittest discover -s tests -v` from the isolated checkout passed 25 tests. Coverage includes native/backend token mismatch, overflow before generation, incomplete/malformed streams, partial timeouts, HTTP protocol errors, deadline/transport closure, mutable model tags, output caps, abstention, normalization/alternative answers/Hotpot special answers, exact gold provenance/truncation, candidate-set invariance/ties, 512/513 pair limits before forward, reranking before a single packing pass, held-out rejection, and explicit baselines. Intermediate failures were JSON tuple/list round-trip comparisons and lint-only line lengths/imports; the returned JSON is now normalized and relevant checks reran successfully.
- Focused Ruff on the isolated changed modules, `git diff --check`, and `answer --help` passed. `generator_assets.py` passed Ruff and compile checks; native GGUF conversion/model-backed calls remain unverified. The original main-checkout model-backed test suite was not rerun concurrently with benchmark measurements. No LLM/reranker inference or new model downloads have run during Stage A.
- Read-only `ollama --version` reported installed client 0.34.1 and no running default server; no backend version is claimed verified. Benchmark process inspection with approved targeted `ps` showed active CPU encoding at roughly two CPU cores and 2.2 GiB RSS. Most recent raw-record observation: 450 successful development requests, zero recorded request/setup failures. This checkpoint is not a live counter.
- Queued `artifacts/stage-a-operations-v1/phase5_after_stage_a.py` via `caffeinate -i .venv/bin/python ...` with approved model-download/local-server permission. It started at 15:06:39 Asia/Shanghai, PID 31682, tool session 59011, lifecycle state `waiting_for_stage_a`. It requires a successful `stage_a_complete` event and complete 9,000/18,000-request summaries before any model acquisition or server startup.
- The deferred job uses a dedicated loopback port 11435 and a separate `models/phase5-validation-v1` store, pins two Q4_K_M model digests/server version/native tokenizer exports and published reranker files, and attempts 16 development diagnostics across two models, two datasets and four variants (BM25 off/on reranking, No-RAG, gold). It checks paired-model context hashes, preserves failed outputs, writes `runs/phase5-validation-v1/summary.json`, and emits a completion event only on 16 successes. Integration into the main checkout and reconciliation of phase gates still require review after those results exist. No real-model success is claimed yet.
- Deferred logs: `artifacts/stage-a-operations-v1/phase5-events.jsonl`, later `phase5-console.log` and `phase5-server.log`; failures/deadline expiration create `needs_review`. The job never modifies benchmark algorithms mid-run, retries failed diagnostics silently, starts Stage B, or commits/pushes files. It only terminates its own dedicated backend after validation.
- Backup checkpoint v1: ignored `artifacts/stage-a-operations-v1/phase5-preparation-v1.tar.gz` (SHA-256 c8c1bac5f063edf1560a40768949574fd8d327bfb95f1d804efde20561b5c7a1). This predates later transport/asset additions. Checkpoint v2: `phase5-preparation-v2.tar.gz` (SHA-256 7becced44ef421f068751b448ffa437959dcac897bd332ea02229f673dd366bf). The immutable integration packet described below contains the latest reviewed source.

## Completion pipeline and integration guards — 2026-10-12

- Latest isolated checks passed 27 focused tests, focused Ruff, compile checks and git diff checks. Added native-export revision/family/vocabulary guards; no native inference occurred during the benchmark. Two tokenizer-export guard tests do not establish real GGUF conversion correctness; the queued real-model checks remain required.
- `artifacts/stage-a-operations-v1/prepare_integration.py` packaged the reviewed draft into `phase5-integration.patch` and `phase5-integration.json`: eight source files, one protocol JSON and seven ignored local test files. The packet pins each isolated file's new SHA-256 and the corresponding main file's original SHA-256/absence. Unrelated changes or any modified packet/file block integration. No main source was changed by packaging.
- Queued `caffeinate -i .venv/bin/python artifacts/stage-a-operations-v1/finalize_phase5.py`. Current waiting helper PID 32451, tool session 38772; lifecycle log `finalization-events.jsonl` records `waiting_for_model_validation` at 15:35:38 Asia/Shanghai. Three earlier waiting-helper instances were intentionally interrupted/reloaded to update completion documentation and use a persistent apply_patch helper path; their locks were released. The benchmark, held-out follow-on and deferred model-validation processes were not interrupted.
- Finalizer requires a successful 16-diagnostic real-model gate, no mixed diagnostic source identities, unchanged main/isolated file hashes and an intact reviewed patch. It runs isolated and existing regression suites before integration, applies only the reviewed source/config/tests with apply_patch, verifies integrated hashes, then runs the combined suite, focused Ruff and git diff checks. It updates local PLAN/PROGRESS through apply_patch only after those gates pass. It never stages, commits, pushes, retries failed measurements or launches Phase 6/Stage B.
- Finalization logs are preserved in `finalization-events.jsonl` and, once work starts, `finalization-console.log`. A failure emits `needs_review`; completed measurements and draft/packet files remain intact. The persistent local apply_patch symlink resolves to the existing installed coding tool; an empty-patch probe confirmed dispatch without modifying files.
- Most recent approved process inspection showed the benchmark actively encoding at about 208% CPU and 2.14 GiB RSS, with the waiting supervisors idle. Latest observed development checkpoint: 500 successful requests, zero request/setup failures. No selection freeze, held-out result, model-validation result or main integration is claimed complete yet.

## Interrupted screening recovery — 2026-10-12

- User requested the next step. Read-only process inspection proved that the prior writer and all queued supervisors had exited; no alternate benchmark processes were found. Their stale locks remained. The reason for termination is unknown; earlier lifecycle logs do not record a clean stop. Prior chat counters incorrectly included warmup events: the verified checkpoint is 750 successful requests and 15 successful block warmups, with zero failed requests or setup failures.
- `PYTHONPATH=src .venv/bin/python` checks using `verified_manifest`, `read_records`, `validate_requests`, and `implementation_identity` passed: the complete hash chain, request uniqueness and current source/config/package/hardware provenance match the original run. All 15 existing index directories have manifests; no incomplete index directory was found.
- Preserved each confirmed stale lock as its exact `.abandoned-v1` sibling, rather than deleting evidence. Updated only ignored operational scripts: `launch.py` accepts explicit `--resume` and uses a fresh `console-resume-v1.log`; `followup.py` appends to its existing empty console log. Added guarded `recover_v1.py`, which checks exact absent lock owners and refuses recorded failures before launching the previously authorized pipeline detached with sleep prevention.
- At 16:14:52 Asia/Shanghai, `.venv/bin/python artifacts/stage-a-operations-v1/recover_v1.py` resumed the same run ID and manifest, without `--retry-failures` or study changes. Development supervisor PID 33732, writer PID 33740; follow-on supervisor 33733; deferred Phase 5 validation 33734; finalizer 33737. `recovery-v1.jsonl`, `recovery-*.log`, and existing lifecycle files retain startup evidence. Elevated `ps` confirmed all four supervisors alive and the writer using CPU after the launching command returned.
- Git status and staged file list remain empty; `git diff --check` passed. Main source, configuration, dependencies and experiment identity were not modified. No commit or push was made; ignored docs/tests are not staged.
- P4.3c remains in_progress. Next smallest task is P4.4b, pending complete successful development screening; P4.5b and real-model validation are still gated. No held-out run, selection freeze or Phase 5 model-backed result is claimed complete.

## Shorter screening sessions — 2026-10-12

- User authorized pausing after the current block and splitting later work into smaller sessions. At 16:33 Asia/Shanghai, `pause_after_block.py` held the development supervisor and the three waiting follow-on jobs. Process inspection confirmed those four processes exited and their three waiting-job locks were released; writer 33740 continued encoding unchanged. No automatic selection, held-out evaluation, model acquisition or integration will start from those stopped jobs.
- Detached watcher PID 34632 waits for all 50 requests in repetition 1 of condition `33a023e94f1401368e269e93594af0e3b2703daa4babbb45a5c4601ccbfb182e` (HotpotQA Hybrid–E5, fixed-token 128). It reads only appended complete records, sends SIGINT after the block's successes are saved, waits for writer exit, then verifies the hash chain, request identities and writer-lock release. An external interrupt may reach the start of the next block; any extra saved requests remain preserved. There is no force-kill, lock deletion, silent failure retry or signal-based suspension inside a timed request. Interruption output stays in the existing console log; lifecycle evidence is `pause-events-v1.jsonl` and `pause-watcher-v1.log`. A `screening_paused` event is required before claiming the run is stopped; `needs_review` means inspect rather than force recovery.
- Added ignored `run_screening_block.py`. Once paused, `caffeinate -i .venv/bin/python artifacts/stage-a-operations-v1/run_screening_block.py` verifies identity and saved records, then resumes exactly the remaining requests in the next declared block via existing CLI `--resume --max-requests N`. It preserves randomized block order and three repetitions, refuses an existing writer lock or recorded failures, writes a fresh per-session console log and does not start subsequent phases. Request count does not bound offline index time; a large new index still needs one uninterrupted build.
- `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p test_screening_sessions.py -v`: four tests passed (recorded order, partial block, repetitions/warmups, completeness). Focused Ruff passed after correcting an import separator and long line. `git diff --check` passed; Git status/staged lists remain empty. All helpers, tests and documentation are ignored; source/config/dependencies and frozen identities are unchanged.
- Current verified checkpoint remains 750 successful measured requests and 15 warmups, zero failed records. P4.3c remains in_progress with pause requested. Next task is to verify `screening_paused`, then resume the next development block when the user chooses; P4.4b remains pending until the full 9,000-request gate.

## Bounded session to 1,000 requests — 2026-10-12

- The pause watcher emitted `screening_paused` at 16:36:51 Asia/Shanghai: 800 successful measured requests, 16 warmups, zero failed records; record-chain tip `c412f31b1d4dade349cc49e07c3dc2a08ac531fe81dbf09f78457633e250c3c2`. Subsequent process inspection confirmed writer/watcher exited and the writer lock was absent. All index directories have manifests; no partial index required recovery.
- User requested the next session finish 1,000 requests. Interpret this as 1,000 cumulative successes, not 1,000 additional requests. Extended the ignored session helper with `--target-total`: it subtracts only successful request records, excludes warmups, bounds the target by the declared matrix, retains default one-block behavior and does nothing when the target is already reached. Completion verifies the saved chain, request identities, exact target, no failures and lock release before emitting `session_paused`.
- Eight focused session tests passed, including cumulative targets, warmup exclusion, invalid targets and no-op completion. Focused Ruff and `git diff --check` passed; source/config/dependencies remain unchanged and Git status/staged list are empty.
- Initial detached launch was rejected by the provenance guard before any writer or measurement started; its message is preserved in `session-to-1000-v1.log`. A fresh foreground preflight matched the saved provenance, and the unchanged CLI passed its own full resume identity check. No guard was bypassed and no failed measurement was retried.
- At 16:40:55, `PYTHONPATH=src .venv/bin/python artifacts/stage-a-operations-v1/run_screening_block.py --target-total 1000` started supervisor 35818, writer 35822, tool session 97865 with `--resume --max-requests 200`. Sleep prevention PID 35838 watches this writer. Process inspection confirmed active CPU work. Session lifecycle: `screening-session-20261012T084055841921Z.jsonl`; console: `screening-block-20261012T084055841921Z.log`. It will return normally after 200 new attempts; any failure requires review rather than being silently replaced.
- P4.3c remains in_progress. Current measured checkpoint at launch is 800/9,000, not a claimed 1,000 completion. Next smallest task is verifying this session's `session_paused` event and exact 1,000-success checkpoint. Selection/held-out/model-validation jobs remain held and do not restart automatically.

## Next 500 requests — 2026-10-12

- The prior session paused normally at 17:15:24 Asia/Shanghai with 1,000 successful requests, 20 warmups and zero failed records. Saved chain tip: `f7f7cfeced858f693b05cfc31d2c754b675a303004516792700045a28aca5600`. Record-chain/request validation passed, processes exited and writer lock was released. Elapsed session time was 34 minutes 28 seconds for 200 requests plus offline setup; do not extrapolate as a constant per-request rate.
- User authorized 500 additional requests. Preflight reverified the chain, request identities, absent writer lock, zero failures and unchanged provenance. At 17:26:32, `PYTHONPATH=src .venv/bin/python artifacts/stage-a-operations-v1/run_screening_block.py --target-total 1500` launched supervisor 36873 and writer 36877, tool session 11375, using `--resume --max-requests 500`. Sleep prevention watches writer 36877. No retry flag or experimental change was introduced.
- Lifecycle: `artifacts/stage-a-operations-v1/screening-session-20261012T092632210566Z.jsonl`; console: `screening-block-20261012T092632210566Z.log`. Completion must emit `session_paused` with exactly 1,500 successful requests and a released writer lock; failures require review. Selection/held-out/model jobs remain held.
- P4.3c remains in_progress; next task is verifying the 1,500 checkpoint, not claiming it complete at launch. Main source/config/dependencies unchanged, no commit/push; Git status and staged file list empty, `git diff --check` passed.

## Recovery to the 1,500 checkpoint — 2026-10-12

- The prior session exited unexpectedly at 1,350 successful requests and 27 warmups. Its writer/supervisor were absent, no alternative writer was found, and the stale lock named PID 36877. Logs contain no clean session completion or explanation for the interruption. Verified saved chain and request identities, zero failed records, unchanged provenance and no incomplete index directories before recovery.
- User authorized continuing to 1,500. Preserved the stale lock as `runs/stage-a-development-v1/.writer.lock.abandoned-36877`; no records or indexes were deleted. Two detached launch attempts were rejected before any writer started because the launcher resolved `.venv/bin/python` to the system interpreter, changing package provenance. Their diagnostics remain in `session-to-1500-recovery-v1.log` and `-v2.log`. Preserving the virtual-environment executable path corrected the launcher; no identity guard was bypassed, environment modified or measured failure retried.
- At 19:31:44 Asia/Shanghai, detached `caffeinate -i .venv/bin/python artifacts/stage-a-operations-v1/run_screening_block.py --target-total 1500` passed preflight and started supervisor 39870 and writer 39875 with `--resume --max-requests 150`. Elevated process inspection confirmed the supervisor survived launcher return and writer was actively computing. The lifecycle log is `screening-session-20261012T113144341383Z.jsonl`, console `screening-block-20261012T113144341383Z.log`, startup output `session-to-1500-recovery-v3.log`.
- This session remains in_progress; 1,500 completion is not yet claimed. It will stop through the existing request-limit return and verify exact target/chain/lock release before emitting `session_paused`. Follow-on jobs stay held. Source/config/dependencies and study manifest unchanged; Git status/staged list empty and `git diff --check` passed. Next task is verify the 1,500 checkpoint.

## Completion/failure alert — 2026-10-12

- User requested notification when the session finishes or fails. Added ignored `notify_session_1500.py` and launched detached watcher PID 40237. It reads complete lifecycle events, verifies saved chain/request identities/counts and lock release before a success alert, and checks exact writer PID/command for unexpected exits. It never stops, resumes or retries screening. Desktop notification uses `osascript`; actual banner delivery depends on macOS notification permissions. Alert command errors remain in `notification-session-1500-v1.log` rather than claiming delivery.
- Three synthetic notification tests passed (incomplete event handling, shell-free argument passing and notification-error preservation); focused Ruff and `git diff --check` passed. Tests mocked notifications; no successful real alert delivery is claimed. An initial read-only chat monitor was stopped after the notification watcher was verified alive, avoiding duplicate monitors. Screening writer 39875 remains unchanged; no completion/failure is claimed yet.

## Session to 3,000 requests — 2026-10-12

- The recovered session paused cleanly at 20:12:50 Asia/Shanghai with 1,500 successful requests, 30 warmups and zero failed records. Verified chain tip `0a1c5139feb8e39c0672693780e7dc364007dd4ea0e5c6393ada84b8aed6e36d`; writer/supervisor exited and lock released. The desktop alert command returned zero at 20:12:57; this proves successful command execution, not that a banner was visible.
- User authorized continuing to 3,000 cumulative requests. Saved chain/request validation, unchanged provenance, absent writer lock and complete index directories passed. At 20:16:23, detached sleep-protected `run_screening_block.py --target-total 3000` started supervisor 41072, writer 41081, with `--resume --max-requests 1500`. The virtual-environment executable symlink was preserved. Lifecycle: `screening-session-20261012T121623995731Z.jsonl`; console: `screening-block-20261012T121623995731Z.log`; startup: `session-to-3000-v1.log`.
- Extended the ignored notification helper with explicit local events path, writer PID and cumulative target; prior defaults are retained. Started a desktop-alert watcher for this session, log `notification-session-3000-v1.log`. Three focused notification tests and Ruff passed; no actual 3,000 completion or alert delivery is claimed. Follow-on selection/evaluation/model jobs remain held.
- P4.3c remains in_progress. Measured launch checkpoint is 1,500/9,000 with no failures; target 3,000 is planned work. Next task is verifying the session's exact target/chain/lock release. Main source/config/dependencies unchanged, no commit or push; Git status/staged list empty and `git diff --check` passed.

## Session to 6,000 requests — 2026-10-13

- Previous session emitted `session_paused` at 01:58:02 Asia/Shanghai: 3,000 successful requests, 60 warmups and zero failed records, chain tip `6dd94a1164eea1fd5eb7609411a5e083d857a743f53df3ab32b45ce350a992b1`. Before resuming, verified the full record chain, request identities, absent writer lock, unchanged provenance and no incomplete index directories. All first-repetition conditions are complete; later requests reuse existing indexes while performing fresh online retrieval and warmups.
- User authorized the next 3,000 requests, interpreted as 6,000 cumulative successes. At 02:26:04, detached sleep-protected `run_screening_block.py --target-total 6000` launched supervisor 50273 and writer 50290, using `--resume --max-requests 3000`. The first pending block is SQuAD Hybrid–BGE fixed-128, repetition 2. Lifecycle: `screening-session-20261012T182604296435Z.jsonl`; console: `screening-block-20261012T182604296435Z.log`; startup: `session-to-6000-v1.log`.
- Started a completion/failure desktop-alert watcher for this specific session, log `notification-session-6000-v1.log`. Exact 6,000 success, saved chain and writer-lock release are checked before a success alert. Alert banner delivery depends on macOS permissions. Automatic follow-on jobs remain held, and no selection/freeze/evaluation/model validation is launched.
- P4.3c remains in_progress. Launch checkpoint is measured 3,000/9,000 with no failures; 6,000 is not yet claimed complete. Next task is verifying the 6,000 checkpoint. Source/config/dependencies and frozen identities unchanged; no commit or push.

## Final development screening session — 2026-10-13

- The preceding session paused cleanly at 02:43:55 Asia/Shanghai with 6,000 successful measured requests, 120 warmups and zero failed records. Chain tip `06e88b2631a64588e75a2042a965f6d6eaf6306fdb25e2d39a2fcda00a4b08ae`. Its 3,000 additional requests and offline setup took about 17 minutes 52 seconds; this is an observed session duration, not a universal throughput estimate.
- User authorized the next 3,000 requests. Verified full saved chain/request identities, zero failures, absent writer lock and unchanged provenance. At 02:45:02, detached sleep-protected `run_screening_block.py --target-total 9000` started supervisor 51058 and writer 51073 with `--resume --max-requests 3000`. It resumes repetition 3 on existing indexes and performs fresh online retrieval. Lifecycle: `screening-session-20261012T184502341645Z.jsonl`; console: `screening-block-20261012T184502341645Z.log`; startup: `session-to-9000-v1.log`.
- Started the desktop completion/failure watcher for this session, log `notification-session-9000-v1.log`. Success requires exact 9,000 saved successes, valid chain, no failed records and writer-lock release. Banner visibility still depends on macOS permissions. No selection freeze, held-out evaluation, model validation or source integration is automatically launched; those jobs stay held.
- P4.3c remains in_progress until the 9,000 gate is verified. Next task is checking completeness and producing the development summary/selection table; P4.4b remains pending. Main source/config/dependencies and run identity unchanged; no commit/push.

## Development screening and report verified — 2026-10-13

- P4.3c done. Final session emitted `session_paused` at 03:03:16 Asia/Shanghai with exactly 9,000 successful measured requests, 180 successful warmup events, zero failed attempts, zero setup failures and no remaining requests. Run `8aee356a-46ae-4af2-9fc0-496a74d40a64`, manifest `2d621cf0c65ef2b18ae7009a24ead7eb8e46cf771b809bd4e1769cec08f182b2`, chain tip `86d37e33a24441c2f87f55dddec4d9ebd94b569315030180c67e97e583a5fc46`; writer lock absent. Hash-chain and request-schema/identity checks passed; no duplicate success or retry was accepted. Final 3,000-request session took about 18 minutes 14 seconds including setup.
- User requested the next smallest step: verification and development reporting. `PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-a-report --run-dir runs/stage-a-development-v1 --output reports/stage-a-development-summary-v1.json` passed. `stage-a-select --run-dir runs/stage-a-development-v1 --output reports/stage-a-selection-v1.json` under the same Python invocation passed without `--freeze`. These are new ignored artifacts; no earlier report or measurement was overwritten.
- Independently checked report/run manifest alignment, full raw-record file SHA-256 alignment, selection-manifest integrity and declared freeze-rule validation. All 60 conditions have 150 successful first attempts, 50 first-repetition quality observations, zero failed first attempts/retries and 150 timing measurements; repeated measurements are not independent new questions. Selection preserves all four equal-dataset candidates: BGE fixed-token coverage 0.777361; BGE sentence-aware 0.812361; E5 fixed-token 0.790833; E5 sentence-aware 0.828194. The declared rule selects E5 sentence-aware (mean online retrieval 0.182329 seconds across its candidate conditions). These are development retrieval/evidence measurements, not held-out or answer-quality findings.
- `DYLD_LIBRARY_PATH=/Users/shirinmanzari/Desktop/ragbench-lab/.venv/lib/python3.14/site-packages/torch/lib PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p test_phase4.py -v`: eight tests passed, covering enumeration, resume/chain/tail integrity, failures/retries, setup failures, selection ties/held-out guards and timing clusters. Initial attempt to locate tests with ordinary `rg --files` returned none because tests are intentionally ignored; corrected to `rg --files --no-ignore tests`. No validation result was fabricated.
- Report intervals use the existing question-cluster percentile bootstrap, not a source-document-cluster analysis. HotpotQA mirror byte-equivalence limitation and interrupted-build overhead remain disclosed. No frozen selection manifest exists and held-out/model jobs remain held. Phase 4 is still in_progress; P4.4b is next, pending. Main source/config/dependencies untouched; ignored docs/tests/reports absent from staging, no commit or push.

## Frozen selection and held-out launch — 2026-10-13

- P4.4b done. User authorized the next Phase 4 step. `PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-a-select --run-dir runs/stage-a-development-v1 --output reports/stage-a-selection-frozen-v1.json --freeze manifests/stage-a-selection-v1.json` passed. Selection is E5 with sentence-aware chunking, chosen only from development evidence. Frozen manifest identity `0ef5eef4ba57f109f4edd9539243e3f617f735f292576cec2da82ec948614f2b`; verified it matches the earlier candidate table exactly, including all four candidate scores, raw-record hash and development provenance. No held-out result was used or inspected to change selection.
- Added ignored `run_heldout_v1.py`: refuses existing output/report paths, verifies the complete development report and unchanged frozen selection, launches full held-out Stage A, retains return codes/errors and generates the summary after the writer stops. No retries or subsequent phases are launched. At 03:39:36 Asia/Shanghai, detached sleep-protected supervisor 52535 started writer 52537. Run `7b44f0dd-5dac-4553-a442-0f58e197f946`, manifest `56e1fe6f9caf7a54ec825e6b750fe2ee4c2b17868fd3d90e164fdf941395ca4a`. Verified evaluation split, non-diagnostic full 60-condition matrix, 100 questions per dataset and exact freeze identity. Planned 18,000 requests are not claimed complete.
- Results: `runs/stage-a-evaluation-v1/`; lifecycle `heldout-events-v1.jsonl`, console `heldout-console-v1.log`, startup `heldout-startup-v1.log` under `artifacts/stage-a-operations-v1/`. On completion, supervisor writes `reports/stage-a-evaluation-summary-v1.json` and checks exact completeness/zero failures. A command failure preserves results and emits `needs_review`; there is no automatic retry.
- Notification helper now accepts the run directory and allows the supervisor time to validate/report after its writer exits, avoiding a premature failure alert during reporting. Held-out alert watcher PID 52562, log `notification-heldout-v1.log`. Three mocked notification tests and focused Ruff passed; no actual held-out completion/alert delivery is claimed. Elevated process inspection confirmed the writer actively computing with `--split evaluation --freeze manifests/stage-a-selection-v1.json`.
- Source/config/dependencies unchanged. The new compact frozen JSON manifest is untracked and not staged; it contains no private absolute paths. Ignored docs/tests/raw results/reports remain unstaged. No commit or push. P4.5b is in_progress; next task is verify/report held-out completeness. Phase 5 model validation/integration and later phases stay held.

## Phase 4 completion and Phase 5 launch — 2026-10-13 (Asia/Tehran)

- P4.5b and the Phase 4 gate are done. Held-out report completed at 00:32:17 with exactly 18,000 successful requests, 180 successful warmups, no request/setup failures, no remaining work and no writer lock. Verified both Stage A reports against their run manifests and raw-record SHA-256 values. All 60 held-out conditions have 100 first-repetition quality questions and 300 successful first-attempt timing measurements, zero retries. Development freeze remained unchanged.
- User authorized the next stage. Reviewed the isolated Phase 5 implementation and existing guarded integration packet; every isolated new file and main original file matched the packet hashes. `PYTHONPATH=src /Users/shirinmanzari/Desktop/ragbench-lab/.venv/bin/python -m unittest discover -s tests -v` from `/private/tmp/ragbench-phase5.qeEN0b` passed all 27 tests. These are synthetic/transport checks, not real model success. Ollama is installed and about 63 GiB disk is available.
- Updated only the ignored Phase 5 supervisor to use the actual completed `heldout-events-v1.jsonl` gate, replacing the obsolete stopped follow-on log. Actual development/evaluation completeness guards remain required. Fixed existing helper lint/import issues with Ruff formatting; focused Ruff passed. At 09:29:31, detached sleep-protected validation supervisor 56754 started dedicated Ollama server 56756 on loopback 11435 and began asset acquisition. Models/results use fresh `models/phase5-validation-v1` and `runs/phase5-validation-v1` paths. Lifecycle `phase5-events.jsonl`; startup `phase5-startup-v1.log`; server `phase5-server.log`; diagnostics later `phase5-console.log` under `artifacts/stage-a-operations-v1/`.
- Planned gate remains 16 development diagnostics across both preferred 3B Q4_K_M generators, both datasets, BM25 reranking off/on and explicit No-RAG/gold baselines. Model digests/server version/native tokenizers/reranker files are pinned and checked; native/server prompt counts and paired context hashes must agree. Failures and partial outputs are preserved; there is no full Stage B run or silent measurement retry. Generation cache isolation remains unverified until Phase 6.
- Guarded finalizer was adjusted to reconcile current status lines and use Asia/Tehran dates after actual success. It still requires all real-model successes, intact packet/unchanged files and pre/post-integration regression checks before applying source. No integration has occurred yet. The existing frozen selection JSON remains untracked; source/config/dependencies otherwise unchanged and ignored docs/tests/raw artifacts unstaged. No commit/push. Next task is verify acquisition/diagnostics and integrate only after those gates.
- Guarded finalizer PID 56875 is waiting for real-model success; process inspection confirmed validation supervisor 56754, dedicated server 56756 and finalizer alive. About 52 MiB of model assets were present at the first acquisition checkpoint; asset completion is not claimed. Local alert watcher PID 56929 reads validation/finalization lifecycle events and reports completion or review-needed on the Mac; log `notification-phase5-v1.log`. It never changes or retries the run. Notification helper Ruff passed; banner visibility depends on macOS permissions.

## Installed generators and reporting correction — 2026-10-13 (Asia/Tehran)

- Acquisition attempts 1 and 2 failed before any generation diagnostic: Ollama's model storage returned network routing/TLS errors. Attempt 2 reused hash-verified reranker assets and partial downloads, but also failed; both attempts and stopped finalizers are preserved in their original logs. No alternate GGUF was substituted: inspected publisher metadata had a different blob hash. The user downloaded the exact planned tags into their default Ollama store and reported installation complete.
- Verified both local manifests and referenced blobs present: Qwen `qwen2.5:3b-instruct-q4_K_M` manifest digest `357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b`; Llama `llama3.2:3b-instruct-q4_K_M` digest `a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72`. Added ignored `installed_models.py`, which copies only selected artifacts into a fresh isolated project store, checks sizes and SHA-256, retains exact manifest bytes and never modifies the user's store. Three focused tests passed after correcting a test-fixture parent-directory creation bug; corrupt/incomplete models cannot install a manifest. No model weight redownload was needed.
- Attempt 3 used those installed models in `models/phase5-validation-v3` and `runs/phase5-validation-v3`. Qwen's first diagnostic passed, but reranking exposed Transformers 5 loading-report sets that were not JSON serializable. Console preserves `Object of type set is not JSON serializable` and the resulting zero-byte `qwen-squad-rag_on.json`; no success is inferred from that invalid artifact. The supervisor stopped, and integration was withheld. Unreadable diagnostic handling now retains the failed artifact and records the failure instead of losing context to a JSONDecodeError.
- Corrected the isolated reranker loading-report metadata to serialize exact set members in stable order; model weights, reranking scores and candidate membership were not changed. The isolated JSON writer validates/serializes before opening its output so serialization errors cannot create an empty artifact. Added regression tests for set metadata and invalid-output preservation. Full isolated suite: 29 tests passed; focused Ruff passed. One initial patch-context mismatch and subsequent missing-helper import were resolved before the final successful suite. Main source remained untouched.
- Preserved the original integration packet; created a new reviewed 16-file packet in `artifacts/stage-a-operations-v1/packet-2`. At 14:03 Asia/Tehran, fresh attempt 4 began using the exact installed generators and verified reranker. Validation supervisor 60875, finalizer 60946 (explicit corrected packet), local completion/failure watcher using attempt-4 events. Artifacts: `models/phase5-validation-v4`, `runs/phase5-validation-v4`; logs under `artifacts/stage-a-operations-v1/attempt-4`, startup `phase5-startup-v4.log`. Qwen's first three diagnostics passed at the latest checkpoint; full 16 and main integration are not yet claimed complete.
- Previous failures remain separate from this corrected source/run identity; there is no silent retry, measurement replacement, model substitution or Phase 6/Stage B launch. P5 remains in_progress; next task is verify all 16 real-model checks and guarded regression/integration. Frozen Stage A selection and reports are unchanged; no commit/push.

## Explicit backend BOS accounting — 2026-10-13 (Asia/Tehran)

- Attempt 4 completed all 16 diagnostics with eight Qwen successes and eight Llama failures. Llama's backend prompt count exceeded the locally rendered count by exactly one for every diagnostic, including both datasets and all baseline/reranking variants. Failures, partial answers and backend counts are preserved in `runs/phase5-validation-v4`; integration was withheld. No token-count guard was relaxed.
- Installed model metadata explicitly disables auto-BOS for Qwen; Llama metadata omits this setting. The pinned backend's observed Llama behavior adds BOS. The adapter now records this backend policy, omits an existing leading BOS from the transmitted template body when the backend supplies it, and includes that token in the full native count and pre-request context-overflow check. It still requires exact agreement with backend counts for every accepted request. Evidence text, instructions, models, quantization, seeds and limits are unchanged; this corrects duplicated prompt framing before any generation study freeze.
- Added focused BOS/nonduplication and overflow regression tests. Isolated suite passed all 31 tests; focused Ruff passed after correcting a test import order. Preserved packets 1/2 and created corrected packet 3 for guarded integration. Official Ollama source on main documents leading-BOS normalization (`https://github.com/ollama/ollama/blob/main/llm/llama_server.go`); attempted retrieval of a v0.34.1-tagged file returned 404, so actual pinned-backend observations and new real-model validation are the acceptance evidence, not an assertion that main exactly matches the installed binary.
- Fresh attempt 5 launched using installed artifacts only, logs under `artifacts/stage-a-operations-v1/attempt-5`, results `runs/phase5-validation-v5`. Acquisition failures 1/2, serialization failure 3 and token mismatches 4 remain intact and are not mixed with this source/run identity. Main integration still waits for actual 16-success verification and full regression gates. Phase 6/Stage B are not launched and no commit/push is authorized.


## Verified Phase 4/5 completion — 2026-10-13

- P4.3c/P4.4b/P4.5b and P5.1–P5.5 done after actual completion gates. The development/evaluation summaries contain 9,000/18,000 successes with no failures; the development-only selection freeze precedes held-out execution.
- `runs/phase5-validation-v5/summary.json` verifies 16 successful model-backed development diagnostics across both preferred 3B models, both datasets, reranking off/on, and explicit No-RAG/gold baselines. Paired contexts match.
- Reviewed source/config/tests integrated using the guarded apply_patch packet; pre-integration isolated and original regression suites and post-integration local suite passed. Focused Ruff and git diff checks passed. Exact console evidence: artifacts/stage-a-operations-v1/finalization-console.log.
- Raw prompts, contexts, mappings, token counts, cache observations, timings and model/tokenizer/reranker provenance remain in the diagnostic artifacts. These are bounded integration checks, not formal generation findings.
- Generation cache isolation remains unverified and must be checked in Phase 6. No Phase 6 pilot, study freeze, Stage B requests or commits/pushes were launched.
- Next smallest task: P6.1, the declared feasibility pilot.

## Final Phase 5 reconciliation — 2026-10-13 (Asia/Tehran)

- Attempt 5 passed all 16 real-model diagnostics at 14:15:32, and guarded integration completed at 14:16:22. Independently verified all 16 saved JSON records have success status, one shared isolated source identity `ec50df949e9887dc07dfa6feab7821ae4269d976904931b9c68c7ed10762003e`, and exact native/backend prompt counts. Paired context hashes were checked by the supervisor. Real reranking/generation used installed planned model digests; native tokenizer/revision/quantization provenance remains in `models/phase5-validation-v5` and results in `runs/phase5-validation-v5`.
- Integration evidence `artifacts/stage-a-operations-v1/attempt-5/finalization-console.log`: isolated 31 tests passed, original-main regression 69 tests passed against isolated code, and combined post-integration 100 tests passed. Focused source Ruff and `git diff --check` passed. The reviewed packet applied six new modules, updated pipeline/CLI, diagnostic protocol JSON and seven ignored test files. User changes were not overwritten; source/config file hashes were verified before/after integration.
- Updated protocol metadata to reflect verified integration and explicit backend BOS accounting. Earlier acquisition, serialization and Llama framing failures are preserved separately; the 16 successful corrected diagnostics are not described as zero failures across all historical attempts. Main generation adapter reports unknown/unverified cache behavior rather than claiming formal timing validity.
- Alert command returned zero after Phase 5 completion; actual banner delivery remains dependent on macOS permissions. No server on the user's default port was terminated; the supervisor stopped only its own dedicated server. Phase 6 pilot/cache/residency/resource verification is next; no Stage B request or automatic study freeze was launched. No commit or push; ignored documentation/tests/results/reports remain absent from staging. Source/config changes and the frozen selection manifest are ready for review, not staged.

## Requested commit and push — 2026-10-13 (Asia/Tehran)

- User explicitly requested commit/push. Reviewed changed source, protocol and compact freeze, checked for private paths/credentials, confirmed no tracked Markdown/tests and staged only explicit approved paths. Frozen selection committed separately as `9b189cf` (`freeze retrieval selection`); source/protocol committed as `3cd4b6d` (`add local answer diagnostics`). Staged source hashes matched the tested packet; staged diff/name list and whitespace checks passed. Focused Ruff and protocol JSON validation passed; prior 16 real-model checks and 100-test regression evidence remain linked above.
- `git push origin main` passed, updating `37b506d..3cd4b6d`. Local HEAD and origin/main both resolve to `3cd4b6d3eb28300d4f77631ee7c403e640d92656`; Git worktree/staged lists are clean. Ignored Markdown, tests, model stores and raw study artifacts were not committed. Phase 6 pilot remains the next pending task; no experiment was launched by this Git operation.

## Phase 6 cache controls and pilot — 2026-10-13 (Asia/Tehran)

- User authorized Phase 6, not Stage B. First read the current specifications/status and pipeline. Baseline repeated identical-prompt probes on the dedicated server showed cached counts 59/60 for Qwen and 81/82 for Llama; leaving a model loaded would bypass prompt work. Artifacts `artifacts/phase6-cache-probe-v1/` preserve all six observations and resident-model metadata. Official generate API defines `prompt_eval_cached_count`; older shift/cache coupling was changed upstream, so no undocumented flag was assumed to disable reuse.
- Implemented explicit model unload followed by an empty-prompt weight preload, requiring an empty dedicated residency list after unload and exactly the pinned model/context resident after preload. Repeated isolated probes passed six requests with cached counts zero and full native/backend count agreement; artifacts `artifacts/phase6-cache-isolation-v1/`. Model weights are loaded before timing, while fresh decoder state may still affect kernel warmth. This limitation and isolation wall cost are recorded, not hidden. Scientific settings remain unchanged except explicitly pinning generator host threads to four before the generation study freeze.
- Added small source modules `serving.py`, `resources.py`, `pilot.py`; `pilot` CLI and separate `configs/generation-pilot.json`; optional offline retrieval/reranker warmup for answer diagnostics; macOS RAM inventory. No dependency or lockfile changes. Pilot selects ten deterministic development IDs per dataset, assigns six representative profiles across BM25/Dense/Hybrid, both sizes and reranking states, then pairs both models. Model-group question/configuration order is deterministic randomized; no cached query results bypass timed retrieval.
- Per-request checks enforce zero cached prompt tokens (missing/boolean counts rejected), exact token counts, one pinned resident model and identical paired contexts. Sampled summed RSS covers caller and dedicated-server descendants; runtime device allocation is recorded separately to avoid adding overlapping unified-memory counters. All attempts and exceptions go to hash-chained pilot records and answer artifacts; no automatic retries.
- Declared planning gates: 40 successes, 20 independent questions, complete representative strata, valid memory samples with peak RSS under 12 GiB and projected online+isolation+block-setup runtime with 1.5x headroom under 48 hours. Estimates extrapolate six profiles rather than all twelve interactions. Passing gates produces a prospective frozen generation study plan with 100 held-out questions, two preferred 3B Q4_K_M models and 14,400 main requests; Phase 7 execution-code provenance is still pending and no generation evaluation is started.
- Full local suite passed 107 tests; focused Ruff, pilot CLI help, JSON and whitespace checks passed. The first focused run caught pre-existing hardware line lengths and import order; formatting corrected them. Source checks include deterministic development sampling, full 12-profile enumeration, missing-cache/failure freeze guards, model unload/preload/residency and process-tree filtering. Config and source remain uncommitted; docs/tests are ignored and unstaged.
- Launched the dedicated pilot through `artifacts/phase6-launch.py`, startup `artifacts/phase6-startup-v1.log`. Lifecycle/console/server logs live in `artifacts/phase6-operations-v1`; results in `runs/phase6-pilot-v1`; optional prospective freeze in `manifests/stage-b-study-v1.json`. P6.1b is in_progress: neither 40-request completion nor freeze is claimed yet. Next task is verify pilot completeness, runtime/memory and all cache/residency gates.

## Phase 6 verified handoff — 2026-10-13 (Asia/Tehran)

- P6.1–P6.4 done. Pilot `c4686f55-6779-4127-87c6-1e1465095e8f`, manifest `3faa45435037d104300a61a35184c3b4c812c6fe974331c665dd2b1e1c5ac5f3`, completed at 15:38:11 with 40 successes, zero failures and exactly 20 independent development questions paired across both models. Independently verified chain/request integrity, exact native/backend tokens, all cached counts integer zero, matching context hashes for every pair, current/pilot provenance alignment and absent writer lock. The wrapper reported return code zero and completed study-plan gates; no Stage B request was launched.
- Measured sampled RSS peak 5.223 GiB on the 16 GiB Mac; largest separately reported device allocation about 2.373 GiB (do not add to RSS on unified memory). All requests had valid process-memory samples without sampler errors and exactly the pinned resident model/context before/after generation. Per-model equal-stratum online+isolation means: Qwen 6.9304 s, Llama 6.5251 s. These are pilot observations, not held-out performance findings.
- Estimated main 14,400-request online+isolation workload 26.911 hours, projected block setup 0.752 hours, total 27.663 hours. Applying declared 1.5x headroom yields 41.494 hours, below the 48-hour planning allowance. Six representative profiles do not measure all interactions, and headroom is not a confidence interval. Separate baselines, reports, archiving and analysis are additional work; no measured full-study duration is claimed.
- Prospective scientific study freeze `manifests/stage-b-study-v1.json`, identity `ca0b183f7dd84cfe3ea43c27ec425493f82736850fb2e7d68feac95f5a1e7fe6`, passed integrity/raw-record linkage checks. Retains preferred model digests, Q4_K_M, pinned templates/date/instruction/reranker/reference tokenizer, four generator host threads, selected E5 sentence-aware, 100 held-out questions per dataset, all twelve pipelines/48 dataset-model conditions and three timing repetitions (14,400 main requests). Cache-isolation policy and fresh-decoder limitation are explicit.
- Decision: freeze the scientific study plan in Phase 6, then pin actual execution runner revision/fingerprint in Phase 7 after its missing orchestration is implemented. This resolves the phase ordering without pretending a Stage B run manifest/runner already exists. Any scientific-setting change creates a new manifest/run set; no frozen retrieval or pilot record was rewritten. Tracked `configs/phase6-protocol.json` records validation commands and critical invariants for local ignored tests.
- Full local suite passed 107 tests before pilot; focused source Ruff, help/JSON and diff checks passed. Models and dependencies were reused, with no lockfile changes, downloads, commits or pushes. Read-only post-run `ps` inspection hit an automatic approval-review timeout (not a safety denial); completion/lock/provenance evidence is independently verified, and the wrapper's dedicated-server shutdown is part of its recorded lifecycle. Ignored docs/tests/raw artifacts remain unstaged. Next smallest task: P7.1; Phase 7 is pending, not running.
- The permitted single retry of `ps -p 62836,62840,62847` returned only its header with no matching processes: pilot, supervisor and dedicated server are confirmed exited. The desktop alert command returned zero after success. No default user Ollama server was stopped.

## Phase 6 commit and blocked push — 2026-10-13

- User requested commit and push. Reviewed and explicitly staged ten Phase 6 source/config/study-plan files; ignored documentation, tests, models and raw outputs remained unstaged. Re-ran the full local suite: 107 tests passed; focused Ruff and staged whitespace checks passed.
- Committed `6f38375` (`add pilot and freeze generation study`). Worktree is clean. Cached origin/main already matches HEAD, but a successful remote push was not independently confirmed in this turn.
- Auto-review rejected `git push origin main` before execution because the GitHub destination was not explicitly trusted for project/study-plan data egress. No workaround or retry was attempted. Push awaits user approval of the specific remote `https://github.com/shirin-manzari/ragbench-lab`; Phase 7 remains pending.

- User subsequently approved the specific GitHub destination. `git push origin main` succeeded with `Everything up-to-date`; independent `git ls-remote origin refs/heads/main` confirmed remote main and local HEAD both equal `6f383754a349c1f1967456f050b41c39fd4ee3d2`. Worktree is clean; ignored documentation/tests/raw results remain local. Phase 7 has not started.

## Project progress report — 2026-10-13

- User requested `report.md`. Created a local report covering Phases 0–6, scientific controls, completed Stage A counts and candidate scores, model integration fixes and preserved failures, measured pilot resources, runtime projections, Git status, artifact locations, limitations, and pending Phases 7–8.
- Reconciled historical documentation with the current implementation and saved development/evaluation, Phase 5, and Phase 6 summaries. The report distinguishes measured observations from projections and does not claim Stage B execution or final answer-quality conclusions. No experiment or phase implementation was launched, and existing measurements were not edited.
- Markdown remains ignored under the user's override. No commit/push is requested for this report; next implementation task remains P7.1.
- Report validation passed: referenced repository artifact paths exist, saved completion totals agree, Stage B remains pending, and there is no trailing whitespace. Initial path-check logic incorrectly treated model identifiers as filesystem paths; restricting it to repository path prefixes resolved the checker error without changing report facts. Git worktree and staging remain clean because the report and progress log are ignored.

## Phase 7 planning gate — 2026-10-13

- User authorized the next phase. Split the larger execution task into P7.2a runner/resume, P7.2b tiny development model-backed verification, and P7.2c bounded held-out sessions. Completed only the first independently reviewable slice, P7.1; no generator/server was started and no held-out request executed.
- Added `src/ragbench_lab/stage_b.py`, CLI `stage-b-plan`, and `configs/stage-b-protocol.json`. The planner verifies the study and nested development-selection hashes, resolved config, exact factorial profiles, unique disjoint frozen 50/100 split IDs, pinned prompt/cache/generator controls, and passing linked pilot. It emits stable condition/index identities, seeded model-group blocks, shared paired question order, and request/pair keys. Baselines remain separate; first repetition remains the quality observation.
- Actual CLI: `PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-b-plan configs/stage-a-study.toml --study manifests/stage-b-study-v1.json --output artifacts/phase7-plan-v1.json` passed. Plan identity `ef449c7e4412c229bb77b75414ed7cfd11fb6bf35636d9233984175d42a35691`; 12 pipelines, 48 conditions, 144 blocks, 14,400 unique request keys, and 7,200 two-model pair keys. Independently checked all twelve expected existing retrieval index manifest paths. Presence is not a substitute for the runner's future asset/content validation.
- Ten new local tests cover exact enumeration, shared initial retrieval identities, held-out-only questions, deterministic orders, malformed/duplicate profiles and IDs, manifest/config/pilot/control rejection, and CLI no-overwrite behavior. Focused suite passed 10 tests; full local suite passed 117 in 13.291 seconds. Ruff on changed source/tests, CLI help, and `git diff --check` passed. The full suite includes an expected mocked notification permission-error record; overall result is OK.
- Frozen study hash remains `ca0b183f7dd84cfe3ea43c27ec425493f82736850fb2e7d68feac95f5a1e7fe6`. No dependencies, model downloads, frozen-manifest changes, commits, or pushes. The user's pre-existing `.gitignore` addition for `report.md` was preserved. Ignored docs/tests/plan output remain unstaged.
- Limitation: this prospective plan is not an execution manifest and does not verify actual server residency or run model-backed checks. P7.2a is next, followed by a separate tiny development diagnostic before any main matrix launch. Phase 7 is in_progress, not complete.

## Phase 7 planner commit and push — 2026-10-13

- User requested commit/push. Staged only `src/ragbench_lab/stage_b.py`, `src/ragbench_lab/cli.py`, and `configs/stage-b-protocol.json`; reviewed staged names/statistics and whitespace. Focused ten-test planner suite and changed-source Ruff passed again; earlier full suite passed 117 tests.
- Committed `e6413cc` (`add frozen generation study planning`) and successfully pushed `6f38375..e6413cc` to the explicitly approved origin/main. Local HEAD and origin/main both equal `e6413ccbe8d2ec035b37328d283001a29958e9c8`; staging is empty.
- The user's pre-existing `.gitignore` edit remains uncommitted and untouched. Ignored Markdown/tests/raw outputs remain local. No experiment was launched; P7.2a remains next.

## Optional extension planning — 2026-10-13

- User explicitly requested planning only for SmolLM3-3B, context budgets, and a Dash + Plotly dashboard. Read project instructions/specifications/plan/history, current planner/config/packing/generation/reporting implementation, and the frozen study. Only this planning update is done; no extension implementation, support verification, acquisition, pilot, or experiment is claimed.
- Updated PLAN.md with stable pending XG.1–XG.8, XC.0–XC.8, and XD.1–XD.9 tasks, dependencies, XS/S effort estimates, and observable gates. Preserved completed tasks and the core P7.2a next step. Added scope/workload/reuse gates and corrected the plan's stale opening status against verified current evidence, without deleting historical records.
- PRD.md now records the separate optional requirements and corrects its stale implementation status. AGENTS.md adds the narrowly scoped optional dashboard exception to the no-UI preference and reinforces scientific boundaries. No README/deep-dive update is needed because implemented behavior did not change. All Markdown remains local and ignored.
- Decision: v1 stays Qwen/Llama, twelve pipelines, 48 conditions and 14,400 main requests. SmolLM replication adds 7,200 requests (21,600 combined, 72 conditions). Independent two-model context study has eighteen profiles/72 conditions/21,600 requests; three models would have 108 conditions/32,400 requests. Pilots/baselines/retries are additional, and extension runtime allowances remain unresolved until measured pilots. These counts are not runtime measurements.
- SmolLM's pinned-backend support, `no_think` switch, Q4_K_M artifact and framing are unverified gates, not assumed capabilities. Backend changes require Qwen/Llama regressions in separate run identities. Context predeclaration must precede inspection of held-out answer-quality findings; 1,024-budget overlap permits no automatic measurement reuse. Dashboard starts with saved Stage A snapshots, remains read-only/offline during timing, and shows missing later results honestly.
- No source, configuration, dependencies, frozen manifest, measurements, downloads, experiments, commits or pushes were changed/launched. The user's existing `.gitignore` edit is preserved. Next smallest core implementation task remains P7.2a; the first extension task, if separately authorized, is XG.1 (backend/mode support review).
- Planning validation passed: all 26 new extension task IDs are unique and pending, all 40 completed core checkboxes are preserved in order, workload/overlap arithmetic agrees, and SHA-256 snapshots of 60 source/config/dependency/manifest/summary/ignore files are unchanged. Changed Markdown has no trailing whitespace; ignore checks confirm all four documents stay local, staging is empty, and Git reports only the pre-existing `.gitignore` edit. No model-backed tests were necessary or run for this documentation-only update.

## Bounded Stage B runner — 2026-10-13

- User authorized the next core phase task. P7.2a done: added `execution.py` for a fresh measured query-to-answer path and `stage_b_runner.py` for block setup/warmup, immutable execution provenance, strict resume, bounded attempts, preserved failures, and pairing checks. Added CLI `stage-b-run`; updated tracked protocol metadata. No dependency/lock change, download, generator/server launch, held-out run, or extension implementation occurred.
- Default diagnostic mode uses one frozen development ID per dataset and all 48 conditions/three repetitions, yielding 144 requests and two independent questions. Held-out mode retains all 14,400 requests and requires a stopped, complete, failure-free, compatible full diagnostic run. Both modes require an explicit positive `--max-requests`; question limits are forbidden in held-out mode. Source/environment/settings/asset/index manifest identities are pinned in each new run; actual index contents are checked on block load.
- Measured work includes fresh embedding/search/fusion, reranking on unchanged initial candidates, one shared-budget pack, and generation. Evidence/answer scoring, serialization, cache isolation and setup remain outside online latency. Full raw prompt/context/output/backend metadata are embedded in append-only records. Cache isolation cost, residency and sampled caller/server memory are recorded separately. Missing/positive cache counts, mismatched counts/contexts/candidates, or invalid memory fail the attempt and stop the session.
- Resume validates chains and prior request schema, checks paired contexts and candidate hashes across models/repetitions, skips successes and retains original failed attempts. Retries require explicit `--resume --retry-failures`. Caught keyboard interrupts preserve an interrupted failed attempt, unload only the selected model and release the writer lock. Abrupt process death may still leave a stale lock/incomplete tail requiring explicit reviewed recovery; it is not silently repaired. Unload failures are recorded and included in the returned failure summary.
- Decision: pin offline generation and full retrieval/reranker warmup per condition block in the execution identity, followed by the already verified decoder isolation for each measured request. Scientific settings/v1 remain unchanged; extra block overhead must be measured in P7.2b rather than claimed covered by the earlier projection. No current generator is claimed newly validated from synthetic tests.
- Fifteen new focused tests cover bounded resume, duplicate prevention, setup failure vs online attempts, failure preservation/explicit retry, no implicit retries, identity/tail corruption rejection, keyboard interruption, cache/memory and pairing guards, unload-error visibility, preflight modes/counts, scoring, and complete/incomplete diagnostic gates. Intermediate checks exposed test import/lint issues and a missing-dataset guard; corrected before the focused suite passed. Full-suite verification and final local preflight are recorded below.
- Real local identity preflight passed for both prepared corpora, frozen native tokenizer/reranker/embedder hashes, reference tokenizer, and twelve existing index manifests. First snapshot `artifacts/phase7-runner-preflight-v1.json` predates explicit execution warmup metadata; retained unchanged. It checks local identities only, not actual runtime/cache/residency or index content load. The next task is P7.2b model-backed development verification, not launching the full matrix.
- No commit/push. The user's `.gitignore` edit remains untouched. Ignored docs/tests/preflight artifacts are not staged; SmolLM, context-budget and dashboard tasks remain pending.
- Final verification: `DYLD_LIBRARY_PATH=/Users/shirinmanzari/Desktop/ragbench-lab/.venv/lib/python3.14/site-packages/torch/lib PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -q` passed 132 tests in 12.150 seconds; log `/private/tmp/ragbench-phase7-runner-tests-final.log`. Focused runner suite passed fifteen tests; changed-source/test Ruff, `stage-b-run --help`, protocol JSON validation and `git diff --check` passed. Expected mocked notification permission errors in the suite are not test failures.
- Final local identity preflight `artifacts/phase7-runner-preflight-v2.json` includes the execution warmup metadata and passed 144 diagnostic/14,400 held-out count checks. It made no backend requests or model forward passes. Frozen study identity remains `ca0b183f7dd84cfe3ea43c27ec425493f82736850fb2e7d68feac95f5a1e7fe6`. Source is uncommitted; no run-store experiment has been created by this preflight. Normal model-backed validation must use a new stopped execution identity, with code/environment kept fixed across resume and its later evaluation gate.

## Runner commit and push — 2026-10-13

- User requested commit/push. Reviewed and explicitly staged only the runner's four source/protocol files; staged name list/diff/whitespace passed. Re-ran changed-source Ruff and fifteen focused runner tests successfully; the previous full suite passed 132 tests. Ignored Markdown/tests/preflight artifacts were excluded, and the user's existing `.gitignore` edit remains local and untouched.
- Committed `c75f541` (`add resumable generation benchmark runner`) and successfully pushed `e6413cc..c75f541` to the approved origin/main. Local HEAD and origin/main both resolve to `c75f54187443c6b9d8a315f3ca4ec1aafdadd9bc`; staging is empty. No benchmark request was launched. P7.2b model-backed development verification remains next; its execution identity must use the current committed code, not the historical pre-commit preflight provenance.

## Model-backed runner validation launch — 2026-10-13

- User authorized P7.2b. Started only the bounded development diagnostic, using the committed runner and unchanged v1 study/settings. Planned 144 requests across 48 conditions/three repetitions on two independent development questions. Session 1 stops after four successes for chain/schema/lock checks; session 2 resumes the remaining 140 only if the checkpoint is failure-free. There is no retry, held-out launch, baseline execution or extension work in this supervisor.
- Added ignored `artifacts/phase7-validate.py`, reusing verified installed model copies and dedicated port 11436. Ruff and whitespace checks passed after import-order/line-length fixes. The helper saves lifecycle, startup, server and session logs, checks exact diagnostic counts, independently validates each row, attempts a local desktop terminal-status alert, and terminates only its owned backend. Alert delivery depends on macOS permissions. No assets or dependencies were downloaded/changed.
- Dedicated backend started at 17:03:11 Asia/Tehran (13:33:11 UTC); supervisor 67597, server 67599, first writer 67602. Elevated process inspection confirmed all alive with diagnostic arguments. Results `runs/phase7-validation-v1`; logs `artifacts/phase7-operations-v1/{events.jsonl,server.log,session-1.log,session-2.log}` (second session log only exists after resume); startup `artifacts/phase7-startup-v1.log`.
- Run ID `121b8c41-a532-44a5-8dcf-ba9dee530470`, manifest `0cbee77e2776db16260a025a80a6cad85d53a1409be98221bfb9cc01aa109d2f`. First verified checkpoint: one successful request, zero request/setup failures, 143 remaining, valid saved chain, writer lock present as expected while active. This is launch/progress evidence, not completed validation or an end-to-end research finding.
- P7.2b remains in_progress; completion requires all 144 requests, native/cache/residency/resource and paired-evidence/candidate checks, verified pause/resume, final gate, and released lock. Source/config/frozen study remain unchanged; user's `.gitignore` edit is preserved, staging empty, no commit/push. No main Stage B request has started.
- The first session stopped cleanly at 17:04:32 with four successes and no failures. The supervisor verified chain/request schema and released lock, then started the explicitly planned `--resume --max-requests 140` session, writer 67733, without changing its manifest. Latest saved-prefix count is seven successes, zero request/setup failures and 137 remaining. Pause/resume is observed; full completion is still pending.
- User requested the next step while validation was active. Independently verified the saved prefix at fifteen successes, zero request/setup failures and 129 remaining, including native counts, cache/residency/resources and pairing checks. Elevated inspection confirmed supervisor 67597, dedicated server 67599 and resumed writer 67733 alive. No second run, source/config change or held-out execution was started; the prerequisite gate remains in_progress.

## Verified runner gate and first held-out session preparation — 2026-10-13

- P7.2b done. Development diagnostic finished at 17:39:41 Asia/Tehran with 144 successful requests, zero request/setup failures, no retries, intact chain and released lock. Independently revalidated all rows: native/backend counts, integer zero cache counts, model/context residency, resources, shared paired contexts and initial candidates across models/repetitions. Real four-request pause/resume was recorded. Run/manifest remain `121b8c41-a532-44a5-8dcf-ba9dee530470` / `0cbee77e2776db16260a025a80a6cad85d53a1409be98221bfb9cc01aa109d2f`.
- Diagnostic peak sampled RSS 5,665,800,192 bytes (about 5.28 GiB), maximum block setup 20.164 seconds. Two independent development questions validate integration, not a new general feasibility/answer-quality ranking. Dedicated server shutdown and local notification command return zero are recorded; notification visibility is not guaranteed.
- User requested next. Preparing only the first 100 new held-out requests under the full frozen 14,400-request matrix, followed by a checked pause. No automatic follow-on, retries, source/config/model changes or extension experiment. New run/output paths preserve every previous diagnostic artifact.
- Before any held-out generation/quality inspection, completed XC.0's planning-only predeclaration in PLAN.md: fixed matrix, primary/secondary paired contrasts/outcomes, first-attempt quality/repetition policy, source-dependent paired bootstrap and sensitivity analysis, failures/overflow handling, independent-run budget assumption and strict reuse audit. This fulfills the existing planning dependency without implementing the context extension or changing v1. Subsequent held-out-informed changes must be exploratory or use new data.
- At 17:45:29 Asia/Tehran, new ignored `artifacts/stage-b-first-session.py` passed the stopped diagnostic/current-code gate and launched dedicated server 71456, supervisor 71451 and writer 71461. Uses `--mode evaluation --validation-run runs/phase7-validation-v1 --max-requests 100`; no question/condition limit, retries or automatic follow-on. Helper Ruff and whitespace checks passed. Logs `artifacts/stage-b-operations-v1/{events.jsonl,server.log,session-1.log}`; startup `artifacts/stage-b-startup-v1.log`; results `runs/stage-b-evaluation-v1`.
- Held-out run ID `2365956d-7f73-438e-89c6-04cebfb977bb`, manifest `0e55c4313bceda076a151b9db60510707db5e6cb53bdd3c59b29221ca2ca78c8`. Independently verified first two successes, no request/setup failures, diagnostic false and 14,398 remaining under the unchanged 14,400-request plan; writer lock present while active. Row checks passed on that saved prefix. No held-out answer-quality values were used to change settings or predeclaration.
- Completion is not claimed: the session must pause at exactly 100 successes, revalidate chain/schema/paired controls, release its lock, save the checkpoint and stop only its owned server. Any error retains artifacts and needs review, without retry. Source/config/dependencies/frozen manifest unchanged; staging empty, user's `.gitignore` edit preserved, no commit/push. Full Stage B conclusions, baselines, archive and extension work remain pending.

## Held-out session to 200 — 2026-10-13

- First session paused cleanly at 17:56:43 Asia/Tehran with 100 successes, zero request/setup failures, intact chain and released lock; checkpoint `artifacts/stage-b-operations-v1/checkpoint-100.json`. Its dedicated server shutdown is recorded. The session lasted about eleven minutes thirteen seconds including local preparation/setup; this is an observation, not a full-study duration estimate.
- User requested next. Independently checked stopped-run rows/controls, the unchanged execution manifest and current source/environment gate before resuming. Added ignored `artifacts/stage-b-resume-session.py`, which executes one explicitly bounded session, preserves existing records, refuses failures/active locks or changed provenance, and never automatically retries or launches a follow-on. Ruff and whitespace checks passed.
- At 18:00:27 Asia/Tehran, supervisor 73570 started dedicated server 73575 and writer 73580 with `--resume --max-requests 100`, targeting 200 cumulative successes. Session `20261013T143027308499Z`; console `artifacts/stage-b-operations-v1/session-20261013T143027308499Z.log`; server log with matching timestamp; startup `artifacts/stage-b-resume-to-200-v1.log`; shared lifecycle `events.jsonl`.
- Latest verified saved prefix: 102 successes, no request/setup failures, writer lock present during execution. Run `2365956d-7f73-438e-89c6-04cebfb977bb` and manifest `0e55c4313bceda076a151b9db60510707db5e6cb53bdd3c59b29221ca2ca78c8` remain unchanged; 14,298 of the full plan remain. No held-out quality result changed settings. Full 200 checkpoint and full study completion remain pending; no source/config/dependency/freeze change, commit or push. User's `.gitignore` edit remains untouched.

## Held-out session to 300 — 2026-10-13

- Previous session paused cleanly at 18:10:26 Asia/Tehran with 200 successes, zero request/setup failures and a released writer lock. Independently verified all saved row/chain/paired controls; checkpoint `artifacts/stage-b-operations-v1/checkpoint-200.json`. Dedicated-server shutdown and notification command return zero are recorded. Overall study remains incomplete, with 14,200 requests remaining at that checkpoint.
- User requested next. Reused the bounded resume helper after unchanged-source/environment and compatible diagnostic gates. At 18:12:23, supervisor 75450 started dedicated server 75455 and writer 75458 with `--resume --max-requests 100`, targeting 300 successes. Session `20261013T144223633617Z`; console `artifacts/stage-b-operations-v1/session-20261013T144223633617Z.log`; startup `artifacts/stage-b-resume-to-300-v1.log`. Existing run and manifest identities remain unchanged.
- No retries, automatic follow-on, source/config/dependency/frozen-manifest changes, commits or pushes. Full 300 checkpoint is pending. User's `.gitignore` edit remains untouched; all operations/logs/docs stay ignored and unstaged. Scientific settings and extension predeclaration remain fixed.

## Requested 500-request session to 800 — 2026-10-13

- Previous session paused cleanly at 18:21:56 Asia/Tehran with 300 successes, no request/setup failures and a released lock. Saved `checkpoint-300.json`; dedicated-server shutdown and notification command return zero are recorded. Independently checked the stopped record chain and every saved request/pairing/control before resuming. Observed first three 100-request session durations: 11.22, 9.97 and 9.52 minutes; only Llama conditions had been measured so far. These do not establish full-model/full-study throughput.
- User explicitly requested 500 new requests. At 19:08:58 Asia/Tehran, existing helper passed unchanged-provenance and compatible-diagnostic gates, then started supervisor 77856, dedicated server 77872 and writer 77875 with `--resume --max-requests 500`. Target is 800 cumulative successes, not 500 cumulative. Session `20261013T153858577194Z`; console `artifacts/stage-b-operations-v1/session-20261013T153858577194Z.log`; startup `artifacts/stage-b-resume-to-800-v1.log`; shared lifecycle `events.jsonl`.
- Initial checkpoint remains 300 successes, zero failures and 14,100 remaining; writer lock is present during setup as expected. No 800 completion is claimed. The session stops at the requested bound or the first failure, preserves all records, and does not retry or launch a follow-on. Run/manifest/frozen scientific settings/source/config/dependencies are unchanged; no commit/push, and user's `.gitignore` edit remains untouched. P7.2c remains in_progress.

## Next 500-request session to 1,300 — 2026-10-13

- Previous session paused cleanly at 19:58:34 Asia/Tehran with 800 successes, zero request/setup failures and a released writer lock. Checkpoint `artifacts/stage-b-operations-v1/checkpoint-800.json`; dedicated-server shutdown recorded. Observed 500-request CLI session lasted about 49 minutes 34 seconds; this is measured session wall time, not a guarantee for later configurations.
- User requested another 500. Independently verified every saved row/chain/paired control and the stopped checkpoint before resuming. At 20:55:13 Asia/Tehran, supervisor 86275 started dedicated server 86292 and writer 86295 with `--resume --max-requests 500`, targeting 1,300 cumulative successes. Session `20261013T172513257293Z`; console `artifacts/stage-b-operations-v1/session-20261013T172513257293Z.log`; startup `artifacts/stage-b-resume-to-1300-v1.log`.
- Unchanged-provenance and diagnostic gates passed. Existing run/manifest and frozen study are preserved; no source/config/dependency/model changes, automatic retry/follow-on, commit or push. Initial completion remains 800/14,400 with 13,600 remaining; full 1,300 checkpoint is pending. User's `.gitignore` edit is untouched; P7.2c remains in_progress.

## Session toward 1,800 stopped on a recorded failure — 2026-10-13

- Prior session paused cleanly at 21:45:54 Asia/Tehran with 1,300 successful requests, zero failures and released lock; `checkpoint-1300.json` and dedicated-server shutdown are recorded. User explicitly requested the next 500. Independently verified all saved rows and paired controls before starting the bounded resume helper; unchanged-provenance/diagnostic gates passed and manifest stayed unchanged.
- New supervisor 95314 began session `20261013T182128796805Z` with `--resume --max-requests 500`, targeting 1,800. Startup `artifacts/stage-b-resume-to-1800-v1.log`; console `artifacts/stage-b-operations-v1/session-20261013T182128796805Z.log`. It completed 105 new successful requests, then recorded a failure on new attempt 106 and stopped with CLI return code one. At 22:02:57, lifecycle reports `needs_review` and owned-server shutdown. Writer lock is absent.
- Verified totals: 1,405 successful requests, one failed attempt, zero setup failures, 12,995 unfinished request slots. All saved chain/request/pairing checks passed. The failed first-attempt key is SQuAD `56dde3aa9a695914005b9662`, repetition one, Llama, Hybrid–E5 sentence-aware size 256, reranking on; condition `d374b61310d7060e67ce3aadda54a31497c25b7912f8c85b97b3317fb153c515`.
- Recorded failure: locally counted full prompt has 1,112 native tokens; backend reports 1,110 prompt tokens, zero cached tokens, fourteen output tokens and stop completion. The exact-count guard rejected this result; raw prompt/context, partial output and backend metadata remain preserved. This is a detected discrepancy, not yet a diagnosed root cause. No truncation/cache explanation is assumed and no guard was relaxed.
- No automatic retry, follow-on, source/config/dependency/model/frozen-manifest change, commit or push. The 1,800 target is not complete. Continuation needs discrepancy diagnosis and an explicit decision consistent with the frozen study; corrected scientific/protocol settings must not silently mix into the current run. User's `.gitignore` edit remains untouched.

## Tokenizer mismatch diagnosis verified — 2026-10-13

- User authorized diagnosis. P7.2d1 done; no production fix or benchmark retry. Read saved failed prompt, frozen tokenizer/export code and local Transformers converter. The Llama JSON contains BPE `ignore_merges=False`; toggling that one property only in memory gives 1,110 full prompt tokens instead of 1,112. Differential analysis isolates ` daleko`: original IDs split into three tokens, candidate recognizes its existing whole-vocabulary token. The non-ASCII characters in the prompt were inspected but were not the differing segment.
- Audited all 1,405 successful saved prompts: original and candidate token ID sequences are exactly identical, not merely equal in count. This supports compatibility investigation, not automatic authorization to relabel or merge results into a changed study. Original failed first attempt and all measurements remain preserved.
- Added ignored `artifacts/diagnose-llama-count.py`, lint passed. Ran four isolated probes using the pinned local Ollama/Llama model and explicit unload/empty-preload. Minimal example: original 78 native vs 76 backend tokens rejected; candidate 76/76 accepted. Exact saved prompt: original 1,112/1,110 rejected again; candidate 1,110/1,110 accepted. Both variants transmit identical prompt hashes per case, including exact agreement with the saved failing prompt, and all backend cached counts are zero. Owned diagnostic backend stopped on script completion.
- Evidence: `artifacts/llama-count-diagnosis-v1/{offline-audit.json,minimal-False.json,minimal-True.json,saved_failure-False.json,saved_failure-True.json,summary.json,server.log}`. Candidate changes existed only in memory and are explicitly labeled as differing from frozen tokenizer identity. All raw probe failures/outputs are preserved outside the benchmark run; no diagnostic is counted as a held-out retry/success.
- Independent summary/hash checks passed: four expected probe outcomes, matching prompt hashes, zero cache, exact candidate counts, no changed prior token sequences, and SHA-256 equality of original run manifest/records, frozen study and all frozen Llama tokenizer files before/after. `git diff --check` passed; staging empty; Git reports only user's existing `.gitignore` change. No download/dependency/source/config/manifest mutation, commit or push.
- Primary source corroboration: upstream llama.cpp sets ignore_merges for llama3/llama-bpe (`https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/llama-vocab.cpp`); Transformers v5.0.0's tiktoken converter sets it explicitly (`https://raw.githubusercontent.com/huggingface/transformers/v5.0.0/src/transformers/convert_slow_tokenizer.py`). Installed GGUF Llama conversion constructs BPE without that setting, and our export overrides the split regex but not merge policy. Upstream main is not claimed to equal the installed binary; actual four-probe results on pinned 0.34.1 are the acceptance evidence. Fetching the gated native tokenizer source was unavailable; no model/template substitution followed.
- Next: obtain direction for P7.2d2–P7.2d4, export correction/regressions and a separate corrected identity with explicit reuse/lineage decision, followed by development revalidation. v1 remains stopped at 1,405 successes and one failed attempt. Exact-count guard will not be weakened, and a changed native tokenizer hash cannot silently resume v1.

## Corrected export, v2 identity, and real asset regressions — 2026-10-13

- User delegated the correction/recovery decision. P7.2d2/P7.2d3 done. Added `configure_llama_bpe` to set the published split rule and `ignore_merges=True` only on supported BPE Llama exports. Added `correct_llama_export` to verify pinned original inputs and create fresh assets/provenance, changing exactly one semantic field while preserving vocabulary/template/files. Unsupported models, corrupt/unpinned inputs and existing output paths fail without overwriting old assets. Exact-count generation guard is unchanged.
- Five new synthetic regressions cover the whole-vocabulary token lookup, serialization/vocabulary preservation, unsupported tokenizer types, separate/no-overwrite correction and corrupt input rejection. Focused asset suite passed seven tests; full local suite passed 137 tests in 12.330 seconds (`/private/tmp/ragbench-tokenizer-correction-tests.log`). Changed-source/tests/operation-helper Ruff and whitespace checks passed after correcting a helper line length. No dependencies or model weight downloads were added.
- Ignored `artifacts/prepare-stage-b-v2.py` created `models/stage-b-corrected-v2`, copying verified unchanged Qwen native inputs/reranker and producing corrected Llama inputs/settings plus provenance. Independent parsed JSON comparison verified the only semantic tokenizer change is `model.ignore_merges: false -> true`; model digests, native template/date, instruction, datasets, selected retrieval settings, reference budgeting and matrix remain unchanged.
- Separate study `manifests/stage-b-study-v2.json`, hash `243b356e2c5e9b20d65be484458fda00e88b8c8a1dfb38e99b1f5ef73fca9bb1`, records v1 parent/failed-run lineage, correction reason/source provenance and legacy feasibility estimates. It is a prospective plan, not an executed v2 experiment. V1 study hash remains `ca0b183f7dd84cfe3ea43c27ec425493f82736850fb2e7d68feac95f5a1e7fe6` and old raw manifest/records/native assets are SHA-256 unchanged. New plan `artifacts/stage-b-v2-plan.json` enumerates the unchanged 48-condition/14,400-slot design under new condition identities.
- Decision: `artifacts/stage-b-v2-compatibility-audit.json` preserves per-request raw record/prompt lineage for all 1,405 prior successes, with identical token sequences. Nevertheless, native counting work occurs inside the measured generation path, so output/token equality does not prove equal implementation cost. Do not import or pool v1/v2 timing or quality aggregates. Preserve every old success/failure as separate historical evidence; v2 will execute a fresh 14,400-request matrix after its diagnostic gate. This costs additional compute but avoids an undeclared mixed-protocol result set. No old measurement was deleted or relabeled.
- Actual corrected-file smoke through `artifacts/check-corrected-assets.py` passed four isolated probes: Llama synthetic 76/76 tokens and known failing context 1,110/1,110; Qwen synthetic 54/54 and same context 1,202/1,202. All cached counts integer zero; backend/model/context residency checked, Llama's original failing prompt hash preserved, and v1 run/manifest hashes unchanged. Results `artifacts/corrected-assets-smoke-v2`; owned backend stopped. These probes are labeled technical regression/diagnosis, not held-out study observations or a complete runner diagnostic.
- Tracked `configs/tokenizer-correction-protocol.json` documents invariants, normal CLI checks and local test commands. Corrected local runner preflight checks both real corpora/asset hashes and twelve existing index manifests, with 144 development slots and 14,400 new held-out slots; artifact `artifacts/stage-b-v2-local-preflight.json`. No index rebuild or query/model forward work is performed by this preflight.
- P7.2d4 remains pending: stabilize source revision, then execute a fresh 144-request corrected development diagnostic with pause/resume before any new held-out run. Source correction/config/v2 manifest are uncommitted; no automatic commit/push or full benchmark launch. Keeping revision/environment unchanged avoids invalidating resume/validation identity. User's `.gitignore` edit remains untouched; ignored docs/tests/assets/probes/preflight remain unstaged. SmolLM/context/dashboard implementation and extension experiments remain pending.

## Tokenizer correction committed — 2026-10-13

- User requested the fix commit. Created `2a83c4a` (`fix llama native token counting`) with only `src/ragbench_lab/generator_assets.py`, `configs/tokenizer-correction-protocol.json`, and `manifests/stage-b-study-v2.json`. Reviewed staged paths/stat and whitespace checks; ignored Markdown/tests/artifacts were absent. The unrelated user `.gitignore` edit remains local and untouched.
- Rechecked focused generator asset regressions: seven tests passed. Ruff for the changed source and `git diff --check` passed. No push or benchmark execution was requested or performed. Next task remains P7.2d4: fresh 144-request corrected development validation under this stable committed source before any new held-out run.

## Corrected validation and authorized 1,000-request session started — 2026-10-13

- User requested a 1,000-request session. Started ignored `artifacts/stage-b-v2-session.py` under committed source `2a83c4a`, with full corrected development validation first (four-request pause, then 140-request resume), and only on a successful compatible gate a fresh 1,000-attempt held-out session. Stops on any failure, without retries, imports from v1, or follow-on sessions. Helper Ruff and whitespace checks passed.
- At 23:37:16 Asia/Tehran, supervisor 99024 started dedicated backend 99031 and validation writer 99034. Backend uses original pinned private weights on port 11436, corrected v2 native assets, and unchanged twelve retrieval indexes. Startup `artifacts/stage-b-v2-startup.log`; lifecycle/server/validation logs `artifacts/stage-b-authorized-1000-v2/`; evaluation log will be `evaluation-1000.log` only after the gate passes.
- Validation run `6d294e82-dba7-4355-8d99-618032fb795a`, execution manifest `c26982b3936b0791aefa584c35932d023bd84a58baa4005ddae16e60b5d4569c`, output `runs/phase7-validation-v2`. Independently verified initial saved chain/schema: zero successes/failures/setup failures, writer lock present during setup. Full validation is not yet complete and held-out v2 has not yet started. Its separate output will be `runs/stage-b-evaluation-v2`, capped at 1,000 attempts of the unchanged full 14,400-slot matrix.
- P7.2d4 is in_progress. V1 remains unchanged at 1,405 successes and one failure. No push, source/config/manifest mutation or new commit; user `.gitignore` edit remains untouched, and all operational scripts/docs/results stay ignored.

## Corrected validation passed; user stopped held-out session — 2026-10-14

- Corrected diagnostic completed 144/144 with zero request/setup failures and verified pause/resume; supervisor checked compatible provenance and full validation gate before starting evaluation. P7.2d4 done. Diagnostic execution manifest remains `c26982b3936b0791aefa584c35932d023bd84a58baa4005ddae16e60b5d4569c`.
- User asked about reducing scope, then explicitly requested stopping the current session. Sent SIGINT only to verified evaluation writer 3114. Runner preserved its interrupted attempt, released its lock, and supervisor stopped its owned backend 99031 at 00:24:38 Asia/Tehran. Process inspection confirmed writer, supervisor and dedicated backend all absent. No automatic resume or retry.
- Independently verified complete saved chain, row and paired-context/candidate checks: 103 successful held-out requests, one failed attempt explicitly labeled `KeyboardInterrupt`, zero setup failures. Run `daee8e81-f598-4631-a654-98301dea1ac7`, output `runs/stage-b-evaluation-v2`. Original 14,400-slot plan remains immutable and incomplete; 14,297 unfinished slots. V1 remains separate and unchanged.
- Proposed smaller 25-question-per-dataset/3,600-request main study is not approved or implemented. No config, source or manifest change, deletion, commit or push. Wait for scope decision before further compute; all saved results remain preserved.

## Reduced scope approved and frozen — 2026-10-14

- User approved the reduction and requested Markdown updates. P7.R1/P7.R2 done. Active main target is 25 questions per dataset × 12 pipelines × two datasets × two models × three repetitions = 3,600 requests, preserving every factorial comparison and the original Stage A selection/corpora. Baselines use the same 25 IDs: No-RAG and gold × two datasets × two models × three repetitions = 600 separate requests. Total planned measurements 4,200, excluding fresh 144-request development diagnostics, setup/warmups and explicitly authorized retries. Optional extensions remain deferred.
- Separate manifest `manifests/stage-b-study-v3-reduced.json`, SHA `60c8fcb5bae6c6a6ea71ca040e491bdbfe44a0863a5a5d61019dc9866022f71c`, freezes exact IDs selected by ID-only digest ranking (`stage-b-reduced-25-v1`, seed 20261011, dataset, question ID). No answer, quality, latency or completion-order values select the sample. Original 100-ID source pools and frozen nested selection remain unchanged. Parent lineage labels the reduction as a compute-budget amendment after partial execution, not a wholly pre-execution protocol; supervisor approval is not claimed.
- `src/ragbench_lab/stage_b.py` supports only the explicit 25-ID rule or the original full 100-ID plan, rejecting malformed/manual subsets. It enumerates 48 conditions, 144 timing blocks and 3,600 unique request keys, 75 per condition, with paired model questions. `stage_b_runner.py` preflight/execution use the same frozen reduced IDs; development diagnostic still uses separate development questions and 144 slots. Strict new-identity validation/resume remains required.
- Reuse decision: zero prior requests imported or aggregates pooled, because subset support changes source/execution provenance. Preserve v1's 1,405 successes/tokenizer failure and v2's 103 successes/user interruption in their original run sets. Ignored preparation helper verified chain/pairing of stopped v2 and original file hashes before/after; audit `artifacts/stage-b-reduction-preservation.json`. No measurements, assets or old manifests were deleted or rewritten.
- Validation: full local suite passed 140 tests in 12.513 seconds (`/private/tmp/ragbench-reduced-study-tests.log`). Three new planning regressions cover balanced/unique paired reduced requests, invalid/manual sample rejection, and source-order independence; runner regression covers 3,600 evaluation vs 144 development slots and exact selected IDs. Original 14,400 tests continue passing. Changed source/tests/helper Ruff and `git diff --check` passed; helper line-length/import issues were corrected before final checks. CLI reduced plan and actual local runner preflight verify pinned native/reranker/embedder inputs, both full prepared corpora and all twelve existing index manifests without starting backend/model-forward work. Artifacts `artifacts/stage-b-v3-reduced-{plan,preflight}.json`.
- Updated local AGENTS, PRD, PLAN, PROGRESS, README, PROJECT_DEEP_DIVE and report with the active target, historical v1/v2 status, preservation, no reuse, uncertainty and next gate. All Markdown/tests remain ignored; user's `.gitignore` edit is untouched. Tracked `configs/reduced-study-protocol.json` records validation commands and invariants so normal operation never depends on ignored tests. No commit, push or experiment launch. Next P7.R3; baseline orchestration, reduced execution, archive and analysis are pending.

## Reduced study committed — 2026-10-14

- User requested committing the changes. Created `9d48ed8` (`add reduced generation study`) with only the two Stage B source modules, `configs/reduced-study-protocol.json`, and `manifests/stage-b-study-v3-reduced.json`. Reviewed staged paths/stat/whitespace; ignored Markdown/tests/artifacts were absent and user `.gitignore` edit remains untouched.
- Rechecked 28 focused Stage B tests: passed in 0.421 seconds. Changed-source Ruff, manifest integrity and `git diff --check` passed. No push or experiment launch. Reduced model-backed validation remains pending under this stable source revision; P7.R3 is not complete.

## Reduced validation and first 1,000 main requests authorized — 2026-10-14

- User requested continuation to 1,000. Started a fresh reduced v3 workflow, not a resume or import of stopped v2. Ignored helper `artifacts/stage-b-v3-session.py` uses the reduced manifest and unchanged corrected v2 assets/indexes. Requires 144 development diagnostics with four-request pause/resume before a compatible gate can launch exactly 1,000 new main attempts. No baseline launch, retries, follow-on session or optional extension. Helper Ruff/whitespace passed.
- At 00:34:23 Asia/Tehran, supervisor 5708 started dedicated backend 5714 and validation writer 5717 under source `9d48ed8`. Logs `artifacts/stage-b-authorized-1000-v3/{events.jsonl,server.log,validation-1.log,validation-2.log}`; startup `artifacts/stage-b-v3-startup.log`. New diagnostic `runs/phase7-validation-v3`; later gated main output `runs/stage-b-evaluation-v3` and console `evaluation-1000.log`. Completion is not claimed; held-out v3 has not yet started.
- All v1/v2 measurements remain separate and untouched. No source/config/manifest mutation, commit or push; user `.gitignore` edit remains untouched. P7.R3 in_progress, P7.R4 pending the gate, baseline orchestration pending.

## User changed stop boundary to validation only — 2026-10-14

- User requested stopping at 144 and continuing later. Verified original supervisor 5708, dedicated backend 5714 and diagnostic writer 5853. Paused only supervisor 5708 with SIGSTOP to block any automatic held-out launch while the diagnostic writer continued unchanged.
- Ignored validation-only cleanup `artifacts/stop-after-v3-validation.py` passed Ruff; launched cleanup 8817. It verified the paused supervisor identity, cancelled that launcher with SIGTERM/SIGCONT, and waits for existing diagnostic writer to finish naturally. It then checks the complete 144-request gate, preserves a summary and stops only backend 5714. No retries or held-out launch. Cancellation events recorded at 01:08:21 Asia/Tehran; console `artifacts/stop-after-v3-validation.log`.
- Latest saved count 130/144 successes, zero request/setup failures, 14 remaining. `runs/stage-b-evaluation-v3` does not exist. P7.R3 remains in_progress until actual completion; P7.R4 requires renewed user authorization. Source/manifest unchanged; no commit/push or deletion.

## Reduced diagnostic verified; first 500 main requests started — 2026-10-14

- P7.R3 done: reduced development diagnostic completed 144/144 with zero request/setup failures, verified chain/paired controls and released lock. Summary saved; dedicated backend stopped at 01:11:40 Asia/Tehran as requested. Run `8e72ca27-6e46-45c9-bfd8-ea0effd00231`, manifest `af8ff13bbec4f48a2e1733cda859337a020ae066bc2ca4236ce836922d5d8474`. No main requests started during that previous workflow.
- User now requested 500 requests. Independently revalidated complete diagnostic gate and current implementation/environment equality, and confirmed fresh main output. New ignored helper `artifacts/stage-b-first-500-v3.py` passed Ruff and whitespace checks. It executes only `--max-requests 500` under the full reduced 3,600-slot plan, verifies the checkpoint/lock/controls, then stops its dedicated backend. No retries, baseline launch or automatic follow-on.
- At 08:39:51 Asia/Tehran, supervisor 10850 started dedicated backend 10855 and writer 10859. Output `runs/stage-b-evaluation-v3`; logs `artifacts/stage-b-operations-v3/{events.jsonl,server.log,session-1.log}`; startup `artifacts/stage-b-first-500-v3-startup.log`. Writer initially performs local pinned-input preflight/setup. P7.R4 in_progress; 500 completion is not claimed.
- Source/config/study/assets unchanged; v1/v2 preserved separately. No commit/push; user `.gitignore` edit untouched and docs/helpers/results remain ignored. Baseline orchestration, remaining reduced main requests and final analysis stay pending.

## Next 500 reduced main requests authorized — 2026-10-14

- First session paused cleanly at 09:32:07 Asia/Tehran with 500/3,600 successes, zero request/setup failures and released lock. Checkpoint `artifacts/stage-b-operations-v3/checkpoint-500.json`; dedicated backend shutdown recorded. Run `9b893393-897e-43eb-a72a-80b30bc539d6`, manifest `b1c9677ba496c32351522e3981c55b085e28420e37437e2631d1bbd79da4d71b`. Independently verified every saved chain/request/paired control and compatible diagnostic/current-source gate before resuming.
- User requested next 500. New ignored `artifacts/stage-b-resume-v3.py` preserves immutable execution identity, refuses existing failures/active locks/provenance changes, and runs only `--resume --max-requests 500`, targeting 1,000 cumulative successes. Helper Ruff and whitespace checks passed. Supervisor 20744 started; startup `artifacts/stage-b-resume-to-1000-v3.log`, timestamped console/backend/lifecycle under `artifacts/stage-b-operations-v3/`.
- P7.R4 remains in_progress; 1,000 checkpoint not yet complete. No automatic retries/follow-on, baseline requests, source/config/study/asset changes, commit or push. User `.gitignore` edit remains untouched. V1/v2 stay separate and preserved.

## Reduced session toward 1,500 — 2026-10-14

- Previous session paused cleanly at 10:35:16 Asia/Tehran with 1,000 successes, zero request/setup failures, intact chain and released writer lock; checkpoint `artifacts/stage-b-operations-v3/checkpoint-1000.json`, dedicated-backend shutdown recorded. Independently checked all saved request/paired controls, unchanged current provenance and compatible diagnostic before resuming.
- User requested next 500. Reused bounded resume helper after Ruff passed; supervisor 30156 launched with `--resume --max-requests 500`, targeting 1,500 cumulative successes. Startup `artifacts/stage-b-resume-to-1500-v3.log`; timestamped lifecycle/console/backend logs remain under `artifacts/stage-b-operations-v3/`. Existing run/manifest remain unchanged.
- Full target checkpoint not yet complete. No retry/follow-on, baseline work, source/config/study/asset mutation, commit or push. P7.R4 in_progress; original 3,600-slot main matrix and separate 600-baseline plan remain fixed. User `.gitignore` edit untouched.

## Reduced session toward 2,000 — 2026-10-14

- Previous session paused cleanly at 11:44:41 Asia/Tehran with 1,500/3,600 successes, zero request/setup failures and released lock. Checkpoint `artifacts/stage-b-operations-v3/checkpoint-1500.json`; dedicated backend shutdown recorded. Independently verified all saved chain/request/paired controls, compatible validation and unchanged runtime provenance.
- User requested next 500. Launched the same bounded resume helper with `--resume --max-requests 500`, targeting 2,000 cumulative successes. Startup `artifacts/stage-b-resume-to-2000-v3.log`; lifecycle/console/backend logs in `artifacts/stage-b-operations-v3/`. Existing run/manifest/settings unchanged; target checkpoint pending.
- No automatic retry/follow-on, baseline work, source/config/model/study changes, commit or push. User `.gitignore` edit remains untouched. P7.R4 in_progress; separate 600 baseline requests and analysis remain pending.

## Reduced session toward 2,500 — 2026-10-14

- Previous session paused cleanly at 13:27:30 Asia/Tehran with 2,000 successes, zero request/setup failures and released lock. Checkpoint `artifacts/stage-b-operations-v3/checkpoint-2000.json`, dedicated-backend shutdown recorded. Independently revalidated every saved chain/request/paired control, unchanged runtime provenance and compatible development gate.
- User requested next 500. Supervisor 49851 launched existing bounded resume helper with `--resume --max-requests 500`, targeting 2,500 cumulative successes. Startup `artifacts/stage-b-resume-to-2500-v3.log`; lifecycle/console/backend logs in `artifacts/stage-b-operations-v3/`. Existing run/manifest unchanged; full checkpoint pending.
- No automatic retry/follow-on, baseline work, source/config/assets/study changes, commit or push. P7.R4 in_progress; user `.gitignore` edit remains untouched. Main matrix still 3,600 slots, baselines 600 separately.

## Reduced session toward 3,000 — 2026-10-14

- Previous session paused cleanly at 14:47:31 Asia/Tehran with 2,500 successes, zero request/setup failures, intact chain and released lock. Checkpoint `artifacts/stage-b-operations-v3/checkpoint-2500.json`; dedicated backend shutdown recorded. Independently checked every saved request/pairing control and unchanged source/environment/compatible diagnostic gate.
- User requested next 500. Launched existing bounded resume helper with `--resume --max-requests 500`, targeting 3,000 cumulative successes. Startup `artifacts/stage-b-resume-to-3000-v3.log`; lifecycle/timestamped console/backend logs under `artifacts/stage-b-operations-v3/`. Run/manifest unchanged; target checkpoint pending.
- No automatic retries/follow-on, baseline work, source/config/assets/study mutation, commit or push. User `.gitignore` edit untouched. P7.R4 in_progress; main target 3,600 and separate baseline target 600 remain fixed.

## Final 600 reduced main requests started — 2026-10-14

- Previous session paused cleanly at 16:09:05 Asia/Tehran with 3,000 successes, zero request/setup failures, intact chain and released lock. Checkpoint `artifacts/stage-b-operations-v3/checkpoint-3000.json`; dedicated backend shutdown recorded. Independently verified all saved request/pairing controls, unchanged runtime provenance and compatible development gate; exactly 600 main slots remain.
- User requested next 600. Supervisor 67596 launched the bounded resume helper with `--resume --max-requests 600`, targeting the complete 3,600-slot main matrix. Startup `artifacts/stage-b-resume-to-3600-v3.log`; timestamped console/backend/lifecycle under `artifacts/stage-b-operations-v3/`. Existing run/manifest unchanged; completion not yet claimed.
- No retry/follow-on or baseline launch. The separately planned 600 baselines still require orchestration and authorization after main verification. No source/config/study/asset changes, commit or push; user `.gitignore` edit untouched. P7.R4 in_progress; archive/analysis pending.

## Reduced main study complete; baseline vertical slice implemented — 2026-10-14

- P7.R4/P7.2c done for the approved reduced target. Final session ended at 17:45:37 Asia/Tehran; checkpoint verified at 17:45:43 and dedicated backend stopped at 17:45:44. Independently verified 3,600 unique successful slots across 48 conditions/three repetitions, zero request/setup failures, all raw chain/request/pairing/native/cache/residency/resource checks, released lock and `checkpoint-3600.json`. Run `9b893393-897e-43eb-a72a-80b30bc539d6`, execution manifest `b1c9677ba496c32351522e3981c55b085e28420e37437e2631d1bbd79da4d71b`. No baseline was automatically launched; archive and conclusions remain pending.
- User requested next phase. Implemented P7.R5a as a reviewable vertical slice: `baseline_runner.py` plans, preflights and executes separate No-RAG/gold records with bounded safe resume, explicit failures/retries, cache isolation, native count/residency/resource checks, offline synthetic warmups and unload cleanup. Shared `run_blocks` gains only a keyword row-check callback; main validation remains its unchanged default. CLI adds `baseline-plan` and `baseline-run`; no models/dependencies/index downloads or rebuilds.
- Frozen `manifests/stage-b-baselines-v1.json`, hash `11b45a49ef9a983899c35414e005ea6ce4ab30398e1a1b4007ecfff9c0f3c0d1`, pins completed parent manifest and records SHA `1e5d18150427b1187b5fa124a8071c97a51024c92df64eaef310fb3b18c06d9a`. Main measurements/settings are not rewritten or pooled. Eight baseline/dataset/model conditions × 25 IDs × three repetitions = 600 requests (300 per baseline). Default baseline diagnostic uses one separate development ID per dataset: 24 additional requests across all eight conditions and repetitions. Its compatible stopped failure-free gate is required; the main 144-request gate is not substituted.
- No-RAG sends exactly empty evidence with the original grounding/abstention instruction, making it an abstention/control diagnostic rather than an unrestricted parametric-knowledge test. Gold uses existing SQuAD diagnostic paragraphs and Hotpot supporting sentences, not bare answer strings. Same reference budget/identifiers/offset rules apply, including final truncation. Each timed request constructs fresh baseline candidates, packs once and generates; scores afterward. Preflight expected inputs only validate measured work. No retrieval/reranker is loaded. Different online paths and baseline implementation fingerprints must be disclosed in comparisons; do not treat them as pooled timing samples or gold as a guaranteed upper bound.
- Eleven new focused synthetic tests pass: balanced/unique 600-slot enumeration and pairing, development isolation/plan guards, exact empty and paragraph gold inputs, truncated offsets, 3-request pause/21-request resume and own gate, corrupt context/cache/count/retrieval rejection, strict changed-provenance resume, preserved keyboard interruption/released lock, fresh evidence construction/scoring and CLI no-overwrite. Testing caught a tuple/list serialization mismatch on resume, now canonicalized; fixture token-field and repeated-unit assumptions were corrected. Full suite passed 151 tests in 12.993 seconds (`/private/tmp/ragbench-baseline-tests.log`); changed-source/tests Ruff and whitespace checks passed. Expected mocked notification permission errors and intentional tokenizer overlength warnings are not test failures.
- Actual CLI plan creation passed, as did `baseline-run --help`. Real local baseline preflight verifies both prepared corpora, exact corrected native asset inputs, reference identity, completed parent and selected questions/contexts, with 24 diagnostic vs 600 evaluation slots; artifact `artifacts/baseline-local-preflight-v1.json`. No model forward, server startup or baseline measurement occurred. Tracked `configs/baseline-protocol.json` records critical normal commands/invariants independent of ignored tests.
- Updated local PRD/PLAN/PROGRESS/README/PROJECT_DEEP_DIVE/report. Markdown/tests/artifacts remain ignored and staging empty; user's `.gitignore` edit is preserved. No commit/push or benchmark launch. Next P7.R5b: stable commit then 24-request model-backed development diagnostic; 600 baseline execution, archive and analysis remain pending.

## Baseline runner committed and pushed — 2026-10-14

- User requested commit and push. Created `239734b` (`add separate baseline runner`) with only `baseline_runner.py`, CLI/scheduler integration, `configs/baseline-protocol.json` and `manifests/stage-b-baselines-v1.json`. Explicit staged-file/stat/whitespace review passed; Markdown/tests/artifacts absent. User `.gitignore` edit remains local and untouched.
- Rechecked eleven focused baseline tests (passed in 0.209 seconds), changed-source Ruff and whitespace. Push to `https://github.com/shirin-manzari/ragbench-lab` succeeded; local HEAD and `origin/main` both `239734b337649e06f55d57dbf42e60735d4a82e9`. The previously local tokenizer-fix and reduction commits were included in the normal fast-forward push.
- No model-backed validation or benchmark was launched. P7.R5b remains pending its 24-request diagnostic under stable committed source; 600 held-out baseline requests, archive and final analysis remain pending. Main raw records and frozen study remain unchanged.

## Baseline development validation started — 2026-10-14

- User requested running the next step. Started only the 24-request baseline development diagnostic: four-request checked pause then twenty-request resume, all eight baseline/dataset/model conditions and three repetitions on one development question per dataset. No held-out baseline launch, retry or follow-on. Ignored helper `artifacts/validate-baselines.py` passed Ruff and whitespace after import formatting.
- At 18:09:17 Asia/Tehran, supervisor 80735 started dedicated backend 80737 and first diagnostic writer 80741 under committed source `239734b`. Corrected pinned v2 native assets and original private Ollama store on port 11436 are reused without mutation. CLI verifies completed parent main and frozen baseline plan before measuring. Fresh output `runs/baseline-validation-v1`; startup `artifacts/baseline-validation-startup-v1.log`; lifecycle/console/backend `artifacts/baseline-validation-operations-v1/`.
- P7.R5b in_progress; completion is not claimed. Existing main/v1/v2 measurements are preserved separately. No source/config/study change, commit or push; user `.gitignore` edit untouched. Baseline held-out 600, archive and analysis remain pending.

## Baseline gate verified; 600 held-out requests started — 2026-10-14

- P7.R5b done: baseline development validation completed 24/24 with zero request/setup failures, verified four-request pause/resume, preserved chain/paired contexts/exact gold or empty inputs, released writer lock and stopped its dedicated backend at 18:11:10 Asia/Tehran. Run `7404557b-95c0-4d40-9e28-26a4c539c2e3`, manifest `8fbdbc555bd6a69b23b4edbd594d906f64069338518b734df4e62a1ffed7b0c6`; peak sampled RSS 4,207,804,416 bytes, maximum block setup 4.803 seconds. Two development questions are integration evidence, not feasibility/quality generalization.
- User authorized all 600 baselines after a planning estimate of 25–40 minutes. Diagnostic measured mean request wall 1.857 seconds; with recorded setup this projects 19.38 minutes for 600, not a guarantee across held-out contexts. Independently rechecked complete baseline gate/current-source equality before starting; previous main remains unchanged.
- At 20:24:55 Asia/Tehran, ignored helper `artifacts/run-baseline-600-v1.py` started supervisor 81952, dedicated backend 81956 and writer 81959 with `--mode evaluation --validation-run runs/baseline-validation-v1 --max-requests 600`. Fresh results `runs/baseline-evaluation-v1`; lifecycle/server/console `artifacts/baseline-operations-v1/{events.jsonl,server.log,session-1.log}`; startup `artifacts/baseline-600-startup-v1.log`. An operational-helper line-length lint issue was corrected; final Ruff passed without runtime/scientific changes.
- Stops at 600 or first failure, preserves records without automatic retry/follow-on and stops only its owned backend. P7.R5c in_progress; completion not yet claimed. Source/config/plan/assets unchanged; no commit/push, user `.gitignore` edit untouched. Archive/analysis remain pending.

## Baseline study complete; raw archive gate started — 2026-10-14

- Baseline evaluation finished 600/600 with zero request/setup failures; run `7122ea5a-5aeb-427b-bbbb-31df30cb9d89`, manifest `a1f104d11305852be95d5482797379731e25b82f7d8ad18a7490daafc2f3cb19`. Checkpoint `artifacts/baseline-operations-v1/checkpoint-600.json`; writer lock released and owned backend stopped at 20:45:54 Asia/Tehran. Observed session duration about 20 minutes 58 seconds, not a promise for other workloads. P7.R5/P7.R5c/P7.3 done; no new generation is needed for the archive step.
- User requested next. P7.4 in_progress: added streaming `iter_records` with the same complete chain/sequence/attempt invariants, preserving eager `read_records` for existing callers. New `archiving.py` audits exact slot sets, repetitions, failures/retries, source/native/cache/pairing/resource controls and validation links, then exports explicitly scoped files to a fresh ZIP and verifies each member SHA-256. CLI adds `study-archive` and `archive-verify`; no dependencies, downloads or model/server calls.
- `configs/archive-protocol.json` declares active/historical raw run scope, prepared corpora, source snapshots and explicit exclusions. Archived historical v1/v2 remain visibly incomplete with their failures, not pooled. All ten recorded source revision fingerprints were independently checked against their Git snapshots; matching snapshots will be included. The local archive includes raw prompts/docs/provenance and requires privacy review before external sharing. Weight files, index arrays and native raw downloads are excluded; prepared data and recorded pins are included, so this supports offline analysis but is not a self-contained model rerun.
- Eleven new archive tests passed, including streaming/eager equivalence, complete-tail rejection, exact matrix/repetition audit, visible incomplete/failed history, writer lock refusal, traversal/symlink protection, ZIP checksum roundtrip/corruption rejection, no overwrite and source fingerprint checks. Full suite passed 162 tests in 13.052 seconds (`/private/tmp/ragbench-archive-tests.log`). A temporary-directory test exposed standard macOS ancestor symlinks; scope checks now reject symlinks inside the selected project root while allowing resolved system ancestors. Changed-source/tests Ruff and whitespace checks passed before archive execution. Archive creation/checksum completion is not yet claimed.

## Phase 7 archive gate verified — 2026-10-14

- P7.4 done. Actual `study-archive` command completed successfully and verified every member: `artifacts/archives/ragbench-core-v1.zip`, 1,455,438,610 bytes (about 1.36 GiB), 477 files and 4,130,394,208 uncompressed bytes. Archive inventory manifest SHA `85401bc357dd7800dead16895fd497af938bdd715d220afa723e5403664438d6`; ZIP SHA `d1709c0bee5ef98fb44b469b313641d7f8a5ee9e0ec1c1d2c58fd6d20e488999`. Creation/audit log `artifacts/study-archive-v1.log`.
- Streaming audit verified Stage A development 9,000/9,000 and evaluation 18,000/18,000, main v3 3,600/3,600, baselines 600/600, main validation 144/144 and baseline validation 24/24, all with zero request/setup failures, zero retries and exact declared matrices/repetitions. Main/baseline question pairs, frozen selection and validation/parent links match. Historical v1's 1,405 successes/one tokenizer failure and v2's 103 successes/one interruption remain visibly incomplete in separate archived run sets; no imported or pooled rows.
- Five core measurement Git revisions are archived and reproduce the source-tree fingerprints for all ten audited run sets. Prepared corpus/questions, scientific plans, raw prompts/results, native/reference tokenizer inputs, selected pilot/probe/operation evidence and local docs are included. Supplementary pilot evidence is retained with its provenance; only explicitly audited core run revisions have source snapshots. Exclusions remain explicit: weight blobs, index arrays, original downloaded native JSON and unlisted unrelated artifacts. This is a local offline-analysis archive, not a self-contained model rerun or publication-cleared package; P8.5 final delivery still pending.
- Independent fresh-process `archive-verify` passed all 477 member checksums; proof `artifacts/archive-verification-v1.json` has the same ZIP/inventory hashes. Additional independent checks compared each archived audited run manifest to its unchanged local manifest and all corrected native/reference tokenizer file hashes to scientific pins; passed. Focused archive tests rechecked eleven cases after metadata guards, passed in 0.047 seconds; final Ruff/whitespace clean. Existing eager-reader behavior is retained and validated by the full 162-test suite.
- Updated local docs/phase checkboxes. No model/backend launched, quality-based setting changes, source data deletion, commit or push. All docs/tests/artifacts remain ignored, staging empty and user `.gitignore` edit untouched. New archiver/CLI/stream-reader/protocol changes remain uncommitted. Phase 7 complete; next P8.1 paired analysis, not additional compute. Do not describe archive completeness as completed analysis or conclusions.

## Archive tools committed — 2026-10-14

- User requested commit only. Created `4f8dc91` (`add verified study archives`) with only `archiving.py`, CLI integration, the streaming record reader and `configs/archive-protocol.json`. Explicit staged-name/stat/whitespace review passed; ignored Markdown/tests/artifacts and unrelated user `.gitignore` edit were not staged.
- Rechecked eleven focused archive tests (passed in 0.044 seconds), changed-source Ruff and whitespace. Permission review timed out once for staging and once for commit; each allowed retry succeeded. Final worktree contains only the untouched user `.gitignore` edit. No push, model requests or archive overwrite. Next P8.1 remains pending.

## Phase 8 paired analysis started — 2026-10-14

- User requested next. Split P8.1 into protocol/statistical validation (P8.1a done) and archived-input report execution (P8.1b in_progress). Before aggregate score inspection, recorded `configs/analysis-protocol.json`: first attempt/repetition-one quality, three within-question timing measurements, 2,000 seeded whole-source-cluster paired percentile bootstrap resamples, equal-dataset stratified macro estimates and question-cluster sensitivity. All declared contrasts are retained, with descriptive unadjusted intervals and no significance-based winner/tuning rule. This detailed plan is finalized after data collection, not described as prospective preregistration.
- Source units: SQuAD reconstructed article document ID; Hotpot connected components of selected questions sharing supporting document IDs or casefolded titles, conservatively including passage variants. Source intervals unavailable with fewer than two clusters; distinct question IDs are counted separately from independent source units. Dataset-stratum random streams are independent, while comparison sides share each resample's weights. Median/p95 resampling retains all three repeated timing observations per question.
- New `paired_statistics.py` and `analysis.py`, CLI `stage-b-report`: validate the saved archive/proof and exact input bytes, fully stream run chains/control checks, reject diagnostics/failures/retry substitutions, recompute answer/evidence scores and abstention/truncation flags from raw output/packed intervals. Planned exports: 56 cells, 220 per-dataset paired contrasts, 28 equal-dataset macro cells, 110 macro contrasts, compact raw-record-linked observations and CSV/JSON reports. No output-completion claim until real generation/validation finishes.
- Fourteen focused synthetic tests passed in 1.386 seconds. Checks cover exact weighted percentile equivalence, paired shift intervals, whole-cluster weights, one-source interval withholding, dataset macro weighting, quality repetition selection, malformed pairs/nonfinite values, SQuAD/Hotpot transitive/title clustering, all contrast directions/counts, ordering determinism and recomputed score rejection. Ruff/whitespace passed; full suite running. No dependency additions, model calls, scientific-setting changes, historical imports, commit or push; user `.gitignore` edit untouched.

## Paired report and independent verification complete — 2026-10-14

- P8.1/P8.1b done. Actual `stage-b-report` command completed: `reports/stage-b-analysis-v1/` contains 56 condition cells, 220 per-dataset paired contrasts, 28 equal-dataset macro cells and 110 macro contrasts. It consumes 4,200 verified main/baseline measurements on 50 distinct questions. Report manifest SHA `b3d2746c4707876db83ef25a27f5aecb01f25ebe1a7b14ba5428bc793658e775`; log `artifacts/stage-b-analysis-v1.log`. Exact archived input bytes and record chains match, and all stored answer/evidence/abstention/truncation values passed recomputation checks.
- Source structure is measured: 12 SQuAD article clusters and 25 Hotpot supporting-document/title components across 25 questions per dataset. All cell source intervals are available; the generic estimator still withholds them below two clusters. Repetition-one quality and within-question repeated timing are kept separate. Macro percentile results are equal-dataset averages of dataset-specific percentiles, not pooled percentiles. All intervals are descriptive/unadjusted; no significance-based winner or new experimental setting is selected.
- Exports: `report.json`, `analysis-plan.json`, `source-clusters.json`, 4,200 compact raw-record-linked `observations.jsonl`, `cells.csv` (448 metric rows) and `contrasts.csv` (1,760 metric rows). Added a concise local `SUMMARY.md` explaining measured reference points, units, source dependence and limitations; this human summary is separate from the six numerical exports.
- Measured equal-dataset gold token F1: Llama 44.26%, Qwen 45.15%; No-RAG 4.29% and 0%. Gold mean online latency 1.478/1.648 seconds; No-RAG .603/.482 seconds. Qwen No-RAG first-repetition abstention is 100% under the unchanged grounding instruction, not evidence of general inability to answer from model knowledge. Main model/pipeline macro F1 ranges 20.45–40.72%, descriptively; token F1 is not accuracy, and these values do not establish a statistically selected winner or gold upper bound.
- Independent standard-library point check `artifacts/check-analysis-v1.py` recomputed every cell mean/median/p95, all paired/macro point differences, interval shape and all CSV estimates, and checked raw record hashes and analysis source/environment provenance. Passed; proof `artifacts/stage-b-analysis-verification-v1.json`, manifest SHA `78161758050e89b572e5afc01841c07b78c94d488f3e809f5a83e59927da89f6`. Proof hashes the six numerical exports; later human summary is not part of that numerical inventory. Helper line-length formatting was corrected and final Ruff passed.
- Full suite passed 176 tests in 14.545 seconds (`/private/tmp/ragbench-analysis-tests.log`), fourteen newly focused analysis tests; final source/tests/helper Ruff and whitespace clean. No dependencies, downloads, model requests, run/manifest/ZIP changes, historical pooling, commit or push. Docs/tests/reports/helpers remain ignored and staging empty; user `.gitignore` edit untouched. P8.2 charts is next; P8.3/P8.4/P8.5 remain pending. The original raw archive is not overwritten to add analysis; final analysis delivery remains P8.5.

## Paired analysis committed — 2026-10-14

- User requested commit only. Created `ad9f335` (`add paired benchmark analysis`) with `analysis.py`, `paired_statistics.py`, CLI integration and `configs/analysis-protocol.json`. Explicit staged-name/stat/whitespace review passed; ignored Markdown/tests/reports/artifacts absent. User `.gitignore` edit remains local and untouched.
- Rechecked fourteen focused analysis tests (passed in 1.308 seconds), changed-source Ruff and whitespace. No push, model requests, report regeneration or archive overwrite. Saved analysis retains its original pre-commit provenance; the committed implementation has the same source-tree content. Next P8.2 remains pending.

## Offline charts and stage breakdowns complete — 2026-10-14

- User requested next; P8.2 done. Added `figures.py`, the small standard-library `vector_export.py`, CLI `stage-b-figures` and `configs/figure-protocol.json`. No model loading, benchmark execution or new study settings. Attempted Matplotlib installation failed on `files.pythonhosted.org` DNS; it exited without installation. Dependency files remain unchanged; SVG/PDF export needs no new package.
- Exported `reports/stage-b-figures-v1/`: six four-facet figures in both SVG/PDF (12 vector files), `stage-times.csv` and `stage-evidence.json` for 56 conditions. Figures cover main quality/latency, packed evidence/quality, separate baseline quality/latency, main/baseline stage costs and post-reranking top-5/10/50 versus packed coverage. All factor levels retained, paired-report source intervals reused without recomputation or winner selection. Scatter labels occupy a separate rail after visual inspection found the first version crowded.
- Read-only export checks the independent numerical proof and six file hashes, raw run bindings/hash chains and exact 4,200 observation-record identities. First attempts only; no historical v1/v2 mixing, failed/retry substitutions, or record omissions. Repetition-one evidence means use 25 questions per cell; all 75 timing measurements contribute to stage means. Packed coverage and online total means match the verified analysis. Disjoint timer sums plus measured unattributed remainder reconstruct online time; invalid/overlapping timers are rejected. Setup, model isolation and scoring are excluded from these online bars. Baseline preparation is separate, and baseline/main implementation differences remain explicit.
- Figure manifest SHA `4ca403fd90a63f4a5d71625190ee218cb25ce2ecdab0f79fec4b0aac83138575`. Independent helper `artifacts/check-figures-v1.py` recomputed all raw stage/evidence means and CSV values, checked output hashes, all SVG facets/profile counts and PDF cross-reference offsets. Proof `artifacts/stage-b-figures-verification-v1.json`, SHA `2d80bb5a59ee7c52d0b46ed1a2421c289789bbeff78d1a67d4b3901b57af5dcb`. Quick Look rendered all six final chart families across SVG/PDF; previews visually inspected. First-pass generated figures preserved in `artifacts/stage-b-figures-first-pass-v1/`; no measured run or original analysis/archive overwritten.
- Fifteen focused tests passed (0.037 seconds): timer reconstruction/negative/overlap/nonfinite checks, baseline isolation, all-factor labels, rep-one evidence, raw omission/mismatch rejection, complete proof requirements, stage mean mismatch, SVG escaping/PDF object offsets, protocol rejection and no-overwrite. Full suite passed 191 tests in 14.515 seconds (`/private/tmp/ragbench-figure-tests-final.log`). Source Ruff/whitespace passed; helper line-length issue corrected and rechecked. README, deep dive, report and planning docs updated locally, including stale top-level Phase 7/8 status rows. No commit/push; ignored docs/tests/artifacts remain unstaged and user `.gitignore` edit preserved. Next P8.3 deterministic declared failure-case review; optional extensions remain pending.

## Declared exploratory failure review complete — 2026-10-14

- User requested next; P8.3 done. Recorded `configs/failure-review-protocol.json` before selected-case text inspection: one paired question/pipeline per dataset/stratum, three mutually exclusive strata (candidate top-50 annotation coverage incomplete, top-50 complete but packed incomplete, packed complete with at least one non-exact answer), repetition one only. Hash rank uses declared salt/seed/dataset/stratum/question/pipeline; question deduplication runs in declared stratum order. Empty strata are reported without substitute criteria. This is a post-collection, post-aggregate exploratory review, not prospective preregistration or held-out tuning.
- Added `failure_review.py` and CLI `failure-review`; reused the independent analysis proof/raw-chain audit, checked all paired generator candidate IDs/order/context identities, and persisted `selection.json` before loading selected question/answer/context text. Prepared source hashes match the measured source manifests; each exported packed segment matches source and context offsets, and saved answer/evidence scores recompute exactly. Both models are retained even if only one fails; all same-question gold/no-RAG repetition-one controls remain separate. No dependency/model/server call or measurement changes.
- Output `reports/stage-b-failure-review-v1/`: six units, twelve main responses and twenty-four matching baseline responses, with exact contexts, source annotations, answer strings/scores, raw request keys/record hashes. `selection.json` includes all six eligibility inventories and exact selected IDs. Selected SQuAD IDs: `57274f67708984140094dbf6`, `56f8ae099e9bad19000a02ec`, `56de4a89cffd8e1900b4b7be`; Hotpot IDs: `5a901e5c55429933b8a2047c`, `5a83e98e5542992ef85e2387`, `5a7741775542994aec3b724f`. Case manifest SHA `eeb2d9cf53b81ba520b4e2587dc2256141dd6d493c5056e126103488f5b3e455`; selection SHA `e8cd50e782b0f7bf876946c8b1f145ca60a3f98fbd1a0bead7a3486fe1313561`. Saved/current source fingerprints match after final formatting.
- Inspected all six packed contexts, twelve main answers, twenty-four baseline answers and the relevant gold contexts. Added agent-authored `review-notes.json` and `REVIEW.md`, explicitly not independent human adjudication. Cases show unrelated candidate evidence, missing multi-hop links, offset loss despite alternative entity mentions, semantically appropriate verbose answers penalized by concise references, free-form insufficiency missed by exact-sentinel abstention, distractor/entity conflation with output truncation, and gold sentence extraction lacking coreference context. Frozen scores/settings are unchanged. Six selected failure-enriched units cannot estimate prevalence or isolate causal mechanisms; annotated coverage is not semantic sufficiency and gold is not a guaranteed upper bound.
- Independent `artifacts/check-failure-review-v1.py` reconstructs candidate eligibility, seeded ranking, distinct-question selection and all inventory counts without importing the sampler, checks current raw hashes/chains and all 36 selected exported answers/scores/contexts, plus output/notes hashes. Passed; proof `artifacts/stage-b-failure-review-verification-v1.json`, SHA `ee7cea1edb4cf62d1cebf25ad99282ca76934315705b453ed0154ed9261ff2c2`. This proves selection/export integrity, not the qualitative interpretations.
- Eight focused tests passed (0.003 seconds), covering all strata, one-sided errors, complete/matching pairs, input-order invariance, cross-stratum question deduplication, empty strata, duplicate rejection, protocol changes, no overwrite and source/context offsets. Full suite passed 199 tests in 14.632 seconds (`/private/tmp/ragbench-failure-review-tests.log`); changed source/tests/helper Ruff and whitespace passed. Initial lint-only line/import formatting corrected before final checks. Local docs updated; no commit/push. Existing uncommitted P8.2 source and unrelated user `.gitignore` edit preserved; ignored docs/tests/reports remain unstaged. P8.4 dataset/model dependence and validity synthesis is next; P8.5 final bundle remains pending.

## Dataset/model synthesis and validity discussion complete — 2026-10-14

- User requested next; P8.4 done. Added `synthesis.py`, CLI `study-synthesis`, and `configs/synthesis-protocol.json`. Offline inputs are the existing independently checked analysis, figure and failure-review outputs. Proof identities, numerical file inventories, stage/evidence exports and authored case notes are hash-checked and must link to the same paired analysis. No model/backend startup, dependency changes, raw-run changes, historical imports, study tuning or new inferential procedure.
- Actual output `reports/study-synthesis-v1/`: `facts.json`, `TABLES.md`, generated manifest and separately authored `DISCUSSION.md`. Four dataset/model groups retain all twelve profiles each; 22 main contrast groups summarize all six contrast families and retain all 120 original paired details/intervals. All 48 main-cell intervals and eight separate baseline cells remain intact. Min/max across profiles are explicitly not confidence intervals; sign counts are descriptive, not significance counts. No pooled baseline/main timing, newly averaged effect or significance-selected winner.
- Measured main token-F1 ranges: SQuAD Llama 37.36–58.69%, Qwen 30.24–50.64%; Hotpot Llama 9.38–23.02%, Qwen 10.65–20.06%. Llama exceeds Qwen's SQuAD point estimates in all twelve matched profiles; Hotpot Qwen-minus-Llama varies from −5.18 to +7.37 points. Qwen mean online latency is higher in all matched main cells. Reranking increases online mean latency in all 24 paired comparisons (about 0.33–1.03 seconds), while answer-score changes have both signs. Generation-call mean/online-total mean ranges 79.27–96.22% across main cells, not per-request-ratio averaging or total session cost.
- Discussion covers all factor families, paired-evidence controls, shared-budget size interpretation, and fixed illustrative BM25/128 source intervals. SQuAD Qwen-minus-Llama F1 −5.82 points has source interval −18.51 to +4.40; Hotpot +1.72 has −6.34 to +8.73. SQuAD Llama reranking example source interval crosses zero although its question-only sensitivity interval does not: source dependence must not be replaced by a more favorable analysis. No superiority conclusion is inferred from point signs or multiple unadjusted intervals.
- Validity limits include 50 dependent question units/12 SQuAD sources/25 Hotpot components, repeated timing and fragile tails, post-start sample amendment and post-collection analysis choices, no verified supervisor acceptance, format-sensitive EM/F1, exact-sentinel abstention, annotation versus semantic sufficiency, output caps, gold coreference omissions, sequential/resumed single-host timing, backend-specific cache isolation, excluded setup/isolation/scoring, resource sampling/counter scope, adapted corpora/mirror equivalence, pinned model/hardware limits and publication/privacy review. Six-case notes remain agent-authored illustrations, not prevalence estimates or causal adjudication. P8.5 delivery is explicitly not claimed complete.
- Independent helper `artifacts/check-synthesis-v1.py` recomputed every group min/max/sign/count, exact original interval retention, 48 stage ratios, table ranges and fixed example intervals without importing the synthesis module. Passed; output `artifacts/study-synthesis-verification-v1.json`, SHA `b6b6ad6ba09910c76b15d7d8e7fc4ef6631cdf7e3cab14a131722a89a6faef8b`. Generated manifest SHA `dc8096304e876058efea8433b0c068cf74a986282fa818f3167f57a4dbd4b61f`; proof additionally hashes the authored discussion. First-pass generated files retained at `artifacts/study-synthesis-first-pass-v1/` after lint-only source wrapping; final source fingerprint matches saved export provenance.
- Nine focused tests passed (0.004 seconds): finite/sign ranges, unchanged intervals, correct ratio-of-means, stage scope/total mismatch, duplicate/baseline-mixing rejection, changed protocols, table units/no overwrite, proof/input corruption and fresh-output gate. Full suite passed 208 tests in 14.456 seconds (`/private/tmp/ragbench-synthesis-tests.log`). Source/tests/helper Ruff and whitespace passed after initial line/import formatting correction. README/deep dive/report/planning docs updated locally. No commit/push; prior uncommitted charts/review and user `.gitignore` edit preserved; ignored docs/tests/artifacts remain unstaged. Next P8.5 final guidance and reproducibility packaging, without additional benchmark requests.

## Final offline-analysis delivery gate complete — 2026-10-14

- User requested next; P8.5 done for the approved reduced core. Added `delivery.py`, CLI `delivery-bundle`/`delivery-verify` and `configs/delivery-protocol.json`. Delivery has two parts: unchanged `artifacts/archives/ragbench-core-v1.zip` and separate `artifacts/archives/ragbench-analysis-v1.zip`. It deep-verifies the raw archive against the original proof, checks analysis/figure/review/synthesis proof inventories and shared report/raw-run bindings, then hashes every explicitly scoped current source/config/manifest/report/doc/test/checker file before exclusive ZIP copy and member verification. No weights/index arrays/Git internals/venv or user `.gitignore` edit are packaged in the analysis overlay. Raw original and all previous reports remain unchanged.
- Refreshed ignored README/deep dive into current concise guides rather than leaving Phase 6/7 pending claims at the top. Updated local report/planning status and added `reports/final-delivery-v1/START_HERE.md`, `VALIDATION.md` and actual `replay-verification.json`. Guides explain raw-first/analysis-second extraction into a fresh checkout with a valid Git HEAD, old measurement snapshots versus current source, source/dirty provenance, numerical equality versus report identity, separate original proofs and authored prose, dependency/platform caveats and privacy/license review. No claim of model rerun, new installation, cross-platform validation or public sharing clearance.
- Eight focused delivery tests passed in 0.034 seconds: companion identity, member corruption, archive kind, no overwrite/suffix rejection, scoped export, traversal/symlink rejection and cross-analysis mixing. Full suite passed 216 tests in 15.253 seconds (`/private/tmp/ragbench-delivery-tests.log`). Ruff/whitespace passed after helper line wrapping. No models, backend, measurements, dependencies, scientific settings, commit or push.
- Fresh-checkout rehearsal v1 verified archives and ran the four export commands, then failed two analysis tests because a transitive ignored helper was missing. Preserved `artifacts/archives/ragbench-analysis-rehearsal-v1.zip` and `artifacts/final-delivery-replay-v1.log`; failure is not counted as success. Explicit package scope now includes `test_answering.py`, `test_baselines_reranking.py`, `test_generation.py` and `test_stage_b_runner.py`, in addition to the six selected test modules. A new rehearsal ZIP/run was used rather than overwriting the failed evidence.
- Successful rehearsal `artifacts/archives/ragbench-analysis-rehearsal-v2.zip` has 137 members, SHA `00c04ad1a58b821ff2b8d1a7932b58a14d90f26984fa15b83aa7c7d108c0512c`. Ignored helper `artifacts/replay-delivery-v1.py` created a new local no-checkout Git clone, verified/extracted raw then overlay, and ran `stage-b-report`, `stage-b-figures`, `failure-review` and `study-synthesis` using only the existing installed environment. All 65 focused packaged tests passed. Twenty-three numerical/vector/selection files match byte-for-byte; all paired report fields match except newly recorded provenance/manifest identity, and extracted/current source fingerprints match. Replayed report SHA `7a1b2ce76052fa76bec714a53529358166912c6389661f0acf40871bb983d756`; replay proof SHA `f2fe702d2da3816173a6751ac75ebec805813c00af302303107017d8b9a19b32`; detailed log `artifacts/final-delivery-replay-v2.log`. Authored notes/discussion are preserved rather than regenerated.
- Final release adds the successful replay proof and refreshed completion guidance to the same tested source/numerical payload. Its final archive hashes/member count are recorded externally in `artifacts/final-delivery-verification-v1.json` after fresh-process verification; the ZIP does not attempt to contain its own checksum proof. No additional benchmark requests are required. Optional extensions remain unstarted; external sharing and Git commit/push still need the user's direction. Prior uncommitted charts/review/synthesis changes and unrelated `.gitignore` edit remain preserved; docs/tests/artifacts stay ignored and staging empty.

## Final release verification — 2026-10-14

- `artifacts/archives/ragbench-analysis-v1.zip` completed with 139 inventoried payload files, 1,505,610 bytes, archive SHA `36e3512c419870c815b26bac651dd735c3f6d3ffb38f78ac7b89e00a36ee7455` and inventory SHA `9ca6c1b122f9272c9161bb5d6f94f0bfef80e6dd5c516a5991d4b12edcd3334c`. Build log `artifacts/final-delivery-build-v1.log`; fresh-process `delivery-verify` passed every analysis/raw member and exact companion link, writing `artifacts/final-delivery-verification-v1.json`. Raw companion remains 477 inventoried files with the original SHA `d1709c0bee5ef98fb44b469b313641d7f8a5ee9e0ec1c1d2c58fd6d20e488999`.
- Independent inventory comparison confirmed final source/configs/manifests/tests/reports match the successful rehearsal; only six completion documents changed and two replay/validation evidence files were added. Final inventory provenance matches current source and successful extracted-source fingerprint `5ffe97463568fa13d96fea45fe649dc91049c4d8e49ce0d069e6f687d7ef5830`. The external proof and this post-release log entry are deliberately outside the immutable ZIP; archived guidance points to the external proof.
- Removed only the two explicitly verified temporary replay checkouts (about 3.9 GiB each). These were disposable clones/extracted copies reproducible from the retained archives; all original measurements, final archives, failure/rehearsal ZIPs, logs and proofs remain saved. No Git commit/push; staged diff empty, ignored documentation/tests absent and unrelated user `.gitignore` edit untouched. Approved reduced core complete; no further requests required.

## Final source committed and pushed — 2026-10-14

- User requested commit and push. Created `abb714d` (`finish offline study delivery`) with exactly ten reviewed source/config files: CLI, figure/vector export, failure review, synthesis, delivery and four protocol specifications. All ten match the verified delivery snapshot. Staged names/stat/whitespace were reviewed; ignored Markdown/tests/reports/archives and unrelated `.gitignore` edit were excluded.
- Rechecked the full local suite: 216 tests passed in 15.389 seconds (`/private/tmp/ragbench-precommit-tests.log`); changed-source Ruff and whitespace passed. Normal fast-forward push to the existing `https://github.com/shirin-manzari/ragbench-lab` succeeded from `239734b` through `abb714d`, also including earlier local `4f8dc91` archive and `ad9f335` paired-analysis commits. Local HEAD and origin/main agree at `abb714d0b3810b832a2cf8c6373f7d1ec4d6dfc9`.
- Only the preserved user `.gitignore` edit remains visible in the worktree; staging is empty. No model requests, output regeneration, dependency changes or archive rewrites. Saved report/delivery provenance intentionally retains its original pre-commit identity; source contents match the committed files. Documentation, tests and both archive files remain local and were not pushed. Core complete; next practical handoff is backup/review of the two verified archives before any external sharing.

## Dashboard motion polish — 2026-10-15

- Added a restrained dashboard motion layer: visible view panels and the page header enter with a short fade/slide, the search field gets a calm focus transition, and Reset filters has a small press response alongside its existing hover. Existing tab-slider motion was preserved without adding hover lift, bounce, or shake.
- Added `prefers-reduced-motion` coverage for the new transitions and animations. No data, benchmark, report, export, or experiment behavior changed.
- Focused dashboard tests passed: 45 tests in 0.691 seconds. `git diff --check` passed. No commit/push; ignored docs/tests remain local.

## Comparison heading cleanup — 2026-10-15

- Removed repeated `Left`/`Right` prefixes from the lower comparison metric and saved-response headings. The selector labels, side-by-side column order, and comparison table still identify direction where it matters.
- Focused dashboard tests and whitespace checks remain the validation target; no benchmark data or scientific records changed.

## Sidebar polish — 2026-10-15

- Modernized the existing sidebar without changing its controls: added a restrained dark gradient, rounded filter surface, clearer control spacing, softer dropdown borders, accessible focus rings, and a small elevation treatment for Reset filters.
- Kept the sidebar content, filter logic, responsive behavior, and read-only scope unchanged.

## Sidebar polish reverted — 2026-10-15

- Reverted the previous sidebar visual changes at the user's request. The earlier dashboard animation and comparison-heading cleanup remain in place.

## Evidence overflow fix — 2026-10-15

- Fixed long source document identifiers in saved evidence cards so they wrap within their comparison column instead of widening the page. Evidence content and identifiers are unchanged.
- Added a minimum-width guard for evidence cards and verified with the focused dashboard suite: 45 tests passed; `git diff --check` passed.

## Dashboard title — 2026-10-15

- Changed the visible dashboard title from `RAGBench` to `RAGBench Lab`. No behavior or study data changed.
