# Contributing

## New apps

New apps go to the **[Modc App Store](https://github.com/MyOwnDataCenter/Modc-app-store)** first:
[submit one with a short form](https://github.com/MyOwnDataCenter/Modc-app-store/issues/new?template=submit-app.yml),
or follow [its guide](https://github.com/MyOwnDataCenter/Modc-app-store/blob/main/CONTRIBUTING.md) to open a pull
request. Apps that do well there move here, with the submitter credited.

## Fixes to apps here

Pull requests that fix an app in this store are welcome: a newer image version, a port or folder that changed
upstream, a better description, a broken icon.

1. Change the app's folder (`<id>/docker-compose.yml` and `<id>/omarchy-app.yml`). Keep the `id` and the `port`
   the same: servers that already installed the app rely on them.
2. Pin images to a version (`:1.4.2`), not `latest`, where the project publishes versions.
3. Run `npm ci`, then `npm run validate`. It must say `0 errors`.
4. Install the changed app on My Own Data Center to check it: push to your fork, then **App Store › Stores › Add by
   link** with your fork's address. Remove it again afterwards.
5. Open the pull request and say what changed and how you tested it.

The listing format is described in the
[Modc guide](https://github.com/MyOwnDataCenter/Modc-app-store/blob/main/CONTRIBUTING.md#3-omarchy-appyml); it's
the same here.
