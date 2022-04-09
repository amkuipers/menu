# menu
Python menu experiment

## code

This is less than 100 lines of code, including the rules.

## interactive

User input can match the regex of a rule, and the statements for Windows or Linux are executed.

## rules

It is a yaml structure. It has a list of rules (names) that are just a handle. Per rule it defines `match`, `desc`, `Windows_NT` and `Linux`. User input is compared per rule if it matches the `match`. If so it executes the `Windows_NT` or `Linux` statements. And `desc` is just a description.
A `match` can include parameters, like an IP address. 

## example rules

When the user input is `pwd`, then on Windows, the `cd` and on Linux, the `pwd` is executed.

    pwd:
        match: ^pwd$
        desc: Print Working Directory
        Windows_NT: cd
        Linux: pwd

When the user input is `info` then it executes multiple statements, and these don't need to be the same.

    info:
        match: ^info$
        desc: Info on the system
        Windows_NT: |
            cd
            whoami
            dir .
        Linux: |
            pwd
            whoami
            id
            ls -al

This `id` rule includes a comment.

    id:
        match: ^id$
        desc: Id of user
        Windows_NT: whoami  # for windows
        Linux: id

    ls:
        match: ^ls$
        desc: Dir
        Windows_NT: dir
        Linux: ls -al

Here a ping to localhost shows a difference in an script argument on two operating systems.

    ping:
        match: ^ping$
        desc: Ping
        Windows_NT: ping -n 1 127.0.0.1
        Linux: ping -c 1 127.0.0.1
        
This rule has a regex that can take a parameter that is then used in the scripts. In this case after a `ping ` it accepts a pattern like `127.0.0.1` and names it `ip`, using `?P<ip>` as named capturing group. That parameter is then used in the script as `{ip}`.

    pingip:
        match: ^ping (?P<ip>[.0-9]*)$
        desc: Ping address
        Windows_NT: ping -n 1 {ip}
        Linux: ping -c 1 {ip}
        
