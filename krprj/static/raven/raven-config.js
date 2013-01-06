Raven.config({
  "publicKey": "027612096bae442c8661fca98a84acdf",
  "servers": ["https://sentry.thelabmill.de/"],
  "projectId": "8",
  "logger": "javascript"
});
window.onerror = Raven.process;