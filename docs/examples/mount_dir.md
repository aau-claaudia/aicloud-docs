# Mounting a directory from AI Cloud on your local computer

If you wish to mount a folder in AI Cloud on your local computer
(using Linux) for easier access, you can also do this using `sshfs`
(Linux command line example executed on your local computer):

???+ example

    ```console
    mkdir aicloud-home
    sshfs <aau email>@ai-pilot.srv.aau.dk:/user/<DOMAIN>/<ID> aicloud-home
    ```

where `<DOMAIN>` is 'department.aau.dk' and `<ID>` is 'ab34ef' for
user 'ab34ef@department.aau.dk'. Please note here that `<ID>` for most
users is *not* the same as the name part of your email address.
