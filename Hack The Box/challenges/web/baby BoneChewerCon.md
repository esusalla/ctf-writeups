- the challenge description mentions the app is running in production but still has the debugger enabled
- entering a name in the registration field that include a restricted character (e.g. "'") allows you to view the full debugger output which includes all the environment variables
- one of the environment variables is the `APP_KEY` which contains the flag