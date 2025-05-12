# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# import os

# sentry_sdk.init(
#     dsn = f"https://{os.environ.get("SENTRY_DSN")}",
#     # Add data like request headers and IP for users,
#     # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info

#     # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing.
#     traces_sample_rate=1.0,
#     # Set profile_session_sample_rate to 1.0 to profile 100% of profile sessions.
#     profile_session_sample_rate=1.0,

#     # Set profile_lifecycle to "trace" to automatically run the profiler on when there is an active transaction
#     profile_lifecycle="trace",

#     send_default_pii=True,

#     integrations=[
#         DjangoIntegration(),
#     ],
# )