# Nijatva Suite — architecture

Local-first. Zero tracking. No Google Play Services.

The suite is four foundation modules and 24 Android apps. Everything below is the
agreed structure as of the Phase 0 / Phase 1 build.

## 1. Layers

```
                    +--------------------------------------+
                    |      F4  nijatva-suite  (meta)       |
                    |  app index, releases, F-Droid style  |
                    +--------------------------------------+
                                    |
     +------------------------------+------------------------------+
     |                              |                              |
+-----------------+      +-------------------+      +------------------+
| F1 nijatva-core |      | F2 no-gms-check   |      | F3 nijatva-design|
| Compose UI, SAF |      | Gradle plugin     |      | icons, templates |
| helpers, backup |      | + CI action       |      | README template  |
+-----------------+      +-------------------+      +------------------+
     |                              |                              |
     +------------------------------+------------------------------+
                                    |
     +------------------------------+------------------------------+
     |                              |                              |
  Phase 1                     Phase 2 and 3                  Phase 4
  core utility                media and phone roles          flagship
  Calc, Clock,                Gallery, Music, PDF,           Keyboard,
  Notes, QR, Files            Dialer, SMS, Camera,           Launcher,
                              Vault, Tasks, RSS              Browser,
                                                             App Manager
```

F1, F2 and F3 are not optional decoration. If `nijatva-core` lands late, twenty
apps grow twenty copies of the same SAF helper. If `no-gms-check` lands late,
the no-GMS claim becomes a promise instead of a build failure.

## 2. Standard app screen

Every app uses one Compose skeleton, so a user who learns one app knows all 24.

```
+-------------------------------------------------------------------------+
| [Top bar]  <- Nijatva Notes                        [ Offline mode ]     |
+-------------------------------------------------------------------------+
| [Permission and storage banner]  (only when applicable)                 |
|   SAF folder access: granted      INTERNET: not requested               |
+-------------------------------------------------------------------------+
| [Main content]                                                          |
|                                                                         |
|   the primary surface: Markdown editor, media grid, dialpad, reader     |
|                                                                         |
+-------------------------------------------------------------------------+
| [Bottom actions]   [ Home ]      [ Vault / Local ]      [ Settings ]    |
+-------------------------------------------------------------------------+
```

Two rules are visible in the skeleton itself:

- **The privacy state is on screen, not buried in settings.** A banner states
  whether storage access is granted and whether the app holds INTERNET. For the
  keyboard and calculator the honest answer is "not requested", and saying it
  out loud is the product.
- **The middle bar is `Vault / Local`, not `Cloud`.** There is no sync target to
  put there.

## 3. Roadmap and real status

| Phase | Scope | Repos | Apps | Target | Status |
|---|---|---|---|---|---|
| 0 | Foundation base | 4 | nijatva-core, no-gms-check, nijatva-design, nijatva-suite | 2-3 weeks | Repos created, README only |
| 1 | Small apps | 5 | Calc, Clock, Notes, QR Scanner, Files | 4-6 weeks | 4 of 5 repos created |
| 2 | Media and utility | 6 | Gallery, Music, Recorder, PDF Viewer, Device Info, Weather | 6-8 weeks | Not started |
| 3 | Phone roles | 9 | Dialer, Contacts, SMS, Calendar, Camera, Expenses, Tasks, RSS, Vault | 8-10 weeks | Not started |
| 4 | Flagship | 4 | Keyboard, Launcher, Browser, App Manager | 10-12 weeks | Browser built, 182 files |

Totals: 24 apps, 4 foundation repos, 28 repositories. 7 easy, 12 medium,
5 hard. Timeline assumes part-time work and is a floor, not a promise.

## 4. No-GMS / BharOS compliance

| Component | Never | Nijatva replacement | Note |
|---|---|---|---|
| Push notifications | Firebase Cloud Messaging | UnifiedPush / ntfy / foreground WebSocket | Most apps here need no push at all |
| Storage access | MANAGE_EXTERNAL_STORAGE | Storage Access Framework, Photo Picker | A revoked grant shows an empty state, not a crash |
| Maps and location | Google Maps SDK, FusedLocationProvider | osmdroid / MapLibre + OSM; LocationManager | Manual city entry is the primary path |
| On-device ML | ML Kit (Play Services variant) | Bundled TFLite / whisper.cpp / Vosk | Model ships in the APK, runs locally |
| Ads | AdMob | Nothing | An ad SDK is a tracking SDK |
| Crash and analytics | Crashlytics, Firebase Analytics | Nothing, or self-hosted Sentry; local log export | Default is nothing |
| Accounts | Google Sign-In | No account at all | This is the entire pitch |
| App updates | Play Core in-app updates | Own F-Droid style index on Pages | `nijatva-suite` does this |
| Distribution | Play Store | APK repository, F-Droid, sideload | Signing key never in the repo |

## 5. Corrections to the first draft

Recorded so the same two mistakes do not come back:

- **`nijatva-core` does not sync anything.** The draft listed "Compose UI + SAF +
  Sync". There is no sync in a local-first suite. Core carries the design system,
  SAF helpers, a TTS wrapper, encrypted preferences, and local backup/restore.
- **AdMob is advertising, not analytics.** The draft grouped "AdMob /
  Crashlytics" under one heading. They are two separate bans: no ad SDK and no
  analytics SDK, and the second is the one people forget when they add a "crash
  reporter" that ships telemetry with it.

## 6. Naming

- Repository: `nijatva-<app>`, lowercase and hyphenated.
- Package: `in.nijatva.<app>` (fallback `com.devira.<app>`). Locked before the
  first release; changing it later breaks update paths.
- Display name: `Nijatva <App>`.

---

Nijatva is a DEVIRA project. Contact: Vasudev.work@rediffmail.com
