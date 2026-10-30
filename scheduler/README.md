# Everyday Cart free scheduler

Publishes posts to the Everyday Cart Facebook Page and Instagram through Meta's Graph API.

- `queue.json`: posts to publish (`time` in Dhaka time, `type` = image, carousel or reel, `media` = repo paths).
- `state.json`: written by the workflow; shows what was published, with links and any errors.
- `.github/workflows/publish.yml`: runs every 15 minutes, publishes at most one due post per run,
  skips anything more than 12 hours overdue, retries failures up to 3 times.

Needs one repository secret: `META_PAGE_TOKEN` (a non-expiring Facebook Page access token).
