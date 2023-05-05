# PopF - Antispam filter

Abstract
========

> There was a discussion on comp.lang.python about a spam filter based
> on probabilities. This theory is described by [Paul
> Graham](http://www.paulgraham.com/index.html) in his article [A Plan
> for Spam](http://www.paulgraham.com/spam.html) and partially includes
> the improvement described by Gary Robinson in [Spam
> Detection](http://radio.weblogs.com/0101454/stories/2002/09/16/spamDetection.html).
>
> If you read this article, you will see that this method is very
> attractive and the results given by the author are very interesting.
> So I decided to write such a filter. This filter should propose the
> following features:
>
> Probabilistic analysis
> :   Each word or word group is associated to a probability which is
>     computed from real emails received by the user. From the
>     individual probability of each word, we compute the probability of
>     a message being a spam. Messages which probability is high are
>     tagged (a tag is added to the subject). The mail reader can sort
>     the incoming messages given this mark.
>
> Separate analysis
> :   For sake of performance, the creation of the database containing
>     each individual probability is independent of the real-time
>     filtering.
>
> White list
> :   To reduce the risk of false positive (which is already nul in my
>     case), people you sent messages to are put in a white list. Then
>     their messages will be accepted without being filtered. It also
>     speeds up the process.
>
> POP3 Proxy
> :   To filter incoming messages, transparently for the user, PopF is a
>     POP3 proxy that link your software to your POP3 server. This
>     system is very simple to use and can be adapted to any software
>     (conforming to the POP3 protocol).
>
> Decoding
> :   Headers, text and other attachments - text, base64 or
>     quoted-printable encoding - are decoded before being filtered.
>     Other formats are ignored (pictures, executable files, ...).
>
> Antivirus
> :   PopF can be connected to an antivirus (not released with PopF).
>
> Training to exhaustion
> :   Iterative learning algorithm using only misclassified messages
>     (smaller database and more selective filter).
>
> PopF is written in [Python](http://www.python.org) and should work on
> any platform accepting Python. I have tested it on Linux only and I am
> very interested in any try on other operating systems.

They speak about PopF
=====================

They speak about PopF on the Internet:

Paul Graham
:   <http://www.paulgraham.com/filters.html>

Gary Robinson
:   <http://www.transpose.com/grobinson.html>
    <http://www.transpose.com/technology.html>

And in the newspaper industry:

Linux Loader
:   The synopsis of number 17 is
    [there](http://www.linuxfrench.net/article.php?id_article=1224). The
    article describes the installation of PopF.

Download
========

PopF Python script is contained in a single file: [popf.py](popf.py)

Efficiency
==========

This table is the result of the `popf.py -check` command. It shows how
efficient PopF is on known spams by testing all messages against the
current database. The efficiency should be close to 100%.

This table is the result of the `popf -efficiency` command. It shows
real results of PopF by checking the X-PopF-Spam header. It better show
the efficiency of PopF at the time a new (and maybe unknown) spam. Be
aware that the efficiency may be very low at the beginning (with few
known spams).

Usage
=====

`popf.py -proxy`
:   starts the POP3 proxy.

`popf.py -kill`
:   kills the proxy.

`popf.py -gen`
:   builds the database.

`popf.py -test files ...`
:   tests files with the current database.

`popf.py -setup`
:   makes a default configuration file. To create a predefined configuration file:
    :   `popf.py -setup Graham [exhaustion]`\
        `popf.py -setup Robinson [exhaustion]`\
        `popf.py -setup Robinson-Fisher [exhaustion]`

`popf.py -clean`
:   cleans POP3 accounts. Spams are kept for the generation of the
    database. Wanted messages can be forwarded to other emails.

`popf.py -purge`
:   purges the most ancient spams.

`popf.py -version`
:   prints PopF version.

`popf.py -check`
:   computes the efficiency of the filter on the messages of the user.

`popf.py -efficiency`
:   computes the actual efficiency of the filter on the messages of the
    user.

Installation
============

The installation described here is for Linux. If you use it with other
operating systems (especially Window\$), do not hesitate to share your
experience ;-)

Python
------

[Python](http://www.python.org) should be installed. I have tested PopF
with version 2.3.4 but should works with version 2.3 or greater.

PopF can also benefit from [Psyco](http://psyco.sourceforge.net/) when
it is installed.

PopF
----

Then you need [popf.py](popf.py). Put it anywhere, in an accessible path
(/usr/bin for example). The script should be executable
(`chmod +x popf.py`).

> **Warning**
>
> To download PopF, you have to use the "Download this link" function
> (or a similar function in your browser). If you copy and paste the
> source directly from the browser, you may get an erroneous popf file.

Configuring PopF
----------------

To configure PopF, run `popf -setup`. It is also possible to use
predefined configurations:

`popf.py -setup Graham`
:   Method described by Paul Graham

`popf.py -setup Robinson`
:   Method described by Gary Robinson

`popf.py -setup Robinson-Fisher`
:   Method described by Gary Robinson, based on Fisher's calculation

This creates \~/.popf/popfrc containing the following parameters:

HOME
:   PopF can be executed before the HOME environment variable is
    defined. To do so, just copy the popfrc configuration file to
    `/etc/popf.conf` (Linux/Unix) or `C:\popf.conf` (Window\$) and
    define the HOME variable in this file. Then the `$HOME/.popf/popfrc`
    file will be read to replace or complete the parameters defined in
    popf.conf. This variable has no effect in the popfrc file.

    On Windows, the USERPROFILE variable is used if HOME is not defined.

HOST, PORT, TIMEOUT
:   Host name and port number of the proxy. HOST should be 'localhost'
    since PopF may run on your machine. PORT default value is 50110. It
    can be 110 (the default value for POP3) if you run PopF as root.
    Default values are recommanded.

    The TIMEOUT parameter is the longuest delay in seconds. After such a
    period of inactivity, the connection is aborted. If TIMEOUT is None,
    there is no limit. This feature only works with Python 2.3. Anyway
    PopF can work without timeout with Python 2.2.

LOG
:   Saving POP3 commands in `~/.popf/popf.log` (LOG = True or False)

LOCALE
:   Definition of the characters in a word. The default value (None)
    doesn't accept accent for example. To know the list of known names,
    run `locale -a`. With a German configuration, we may use
    `LOCALE = 'German'`.

    > **WARNING:**
    >
    > this option works well under Linux/Unix. I don't think so about
    > Window\$.

TOKEN, NONTOKEN
:   TOKEN is a regular expression defining a word. NONTOKEN is a regular
    expression used to ignore some words recognized by TOKEN (for
    example words with only digits or shorter than 3 characters).
    Default values are recommended.

HEADER\_FILTER, BODY\_FILTER
:   If HEADER\_FILTER is True, the filter uses headers. If BODY\_FILTER
    is True, the filter uses the body of the message. By default both
    parameters are active.

GOOD\_CORPUS, BAD\_CORPUS
:   GOOD\_CORPUS is a (set of) file or directory containing non spam
    emails.

    BAD\_CORPUS is a (set of) file or directory containing spam emails.

    These files must be RFC822 complient (Unix format with many messages
    per file or MH format with one file per message). The filter may
    work with other formats but it hasn't been tested.

    You absolutely need to change these values. For example:

        GOOD_CORPUS = '/home/foo/Mail/Archives', '/home/foo/Mail/outbox'
        BAD_CORPUS = '/home/foo/Mail/SPAM'

    GOOD\_CORPUS must not be a subdirectory of BAD\_CORPUS and
    vice-versa.

IGNORED\_EXTENSIONS
:   IGNORED\_EXTENSIONS is the list of the extensions of the files to be
    ignored while learning. These files are those that don't contain
    messages. The default value can be used with some popular softwares.

WHITELIST
:   WHITELIST is the list of addresses of the user. The white list is
    the set of addresses the user has sent emails. It is then useless to
    build it from scratch. For example:

        WHITELIST = 'my.first.email@free.fr', 'my.second.email@free.fr'

TRAINING\_TO\_EXHAUSTION
:   Training to exhaustion learning method. By default this method is
    disabled because it can consume a huge amount of memory. When this
    parameter is True, the following parameters must be defined:

    TRAINING\_TO\_EXHAUSTION\_GOOD\_LIMIT
    :   Maximal probability that non spams should not be above of

    TRAINING\_TO\_EXHAUSTION\_BAD\_LIMIT
    :   Minimal probability that spams should not be below

    TRAINING\_TO\_EXHAUSTION\_MAX\_ITERATION
    :   Maximal number of iterations

METHOD
:   Probability computation for messages (Graham, Robinson or
    Robinson-Fisher).

FREQUENCY\_THRESHOLD
:   Number of occurrences of words needed to be stored in the data base.
    Rare words are not stored. Default values are recommended.

GOOD\_BIAS, BAD\_BIAS, GOOD\_PROB, BAD\_PROB, UNKNOWN\_PROB
:   Bias and probabilities of spam, nonspam and unknown words. Default
    values are recommended.

RARE\_WORD\_STRENGTH
:   Strength given to "rare" words". Default values are recommended.

SIGNIFICANT
:   Number of words to take in account in a message to be filtered.
    Default values are recommended.

BAD\_THRESHOLD
:   Threshold from which the message is considered as spam. Default
    values are recommended (0.9 if METHOD == "Graham", 0.5 if METHOD ==
    "Robinson").

UNCERTAIN
:   Width of the uncertainty band around BAD\_THRESHOLD. Default values
    are recommended.

TAG
:   Tag to insert in the subject of spams.

    To avoid tagging the subject, just use an empty TAG (`TAG = ""`).
    When the tag is empty it is still possible to filter messages using
    the X-PopF-Spam header that is always added to spams. The 4.1.0
    version of PopF also adds a "X-Spam-Flag: YES" tag to be used with
    [gnubiff](http://gnubiff.sourceforge.net/).

    > **Warning**
    >
    > it's better to filter messages using the "X-PopF-Spam" because
    > some spams have more than one "Subject" header and PopF only tags
    > one (will be fixed in a future verion).

AUTORELOAD
:   AUTORELOAD tells PopF to reload the probabilities when they are
    generated.

ANTIVIRUS, VIRUS\_TAG, FAST\_ANTIVIRUS
:   ANTIVIRUS is the list of antivirus to use with the filter. This list
    contains the names (and options) of antiviruses and regular
    expressions that match the names of the detected viruses. For
    instance to use f-prot and clamav:

        ANTIVIRUS = 'f-prot', 'Infection: (.*)', 'clamscan -r --disable-summary', ': (.*) FOUND'

    FAST\_ANTIVIRUS only checks spam messages for viruses to fasten the
    process (FAST\_ANTIVIRUS = True). The default value is
    FAST\_ANTIVIRUS = False.

    VIRUS\_TAG is the tag to insert in the subject of infected messages.

    When a virus is found, the X-PopF-Virus header is added to the
    message. This header holds the name of the virus.

    To avoid tagging the subject, just use an empty VIRUS\_TAG
    (VIRUS\_TAG = "").

BYPASS
:   BYPASS is the list of regular expressions that define the messages
    not to be filtered.

CLEANER\_ACCOUNTS, CLEANER\_DIRECTORY, CLEANER\_PERIOD, CLEANER\_FORWARDS, CLEANER\_SMTP
:   The -cleaner option downloads spams and stores them in a local
    directory (referenced in BAD\_CORPUS). This is useful to clean a
    mailbox and leave wanted messages on the server. This option can
    also forward wanted messages to other emails.

    CLEANER\_ACCOUNTS is the list of accounts to be cleaned. Each item
    of the list looks like `user:password@host:port`

    `:port` is optionnal.

    CLEANER\_DIRECTORY is the directory where spams will be stored. This
    directory should be a sub directory of BAD\_CORPUS or be referenced
    by BAD\_CORPUS.

    CLEANER\_PERIOD is the period in hours between two cleanings. If
    CLEANER\_PERIOD is None, only one cleaning will be done.

    CLEANER\_FORWARDS is the list of emails to which messages are
    forwarded.

    CLEANER\_SMTP is the SMTP server used to forward messages.

PURGE, PURGE\_DIRECTORY
:   The -purge option moves or removes the oldest spams so as not to
    overload the data base and to be more representative of recent spams
    instead of older spams. This also seems to avoid false positives
    that appear when the data base contains old spams (maybe because
    such a data base is too heterogeneous).

    PURGE can have several values:

    `PURGE = integer value`
    :   PURGE is the number of monthes after which spams must be removed

    `PURGE = floating point value`
    :   PURGE is the ham/spam ratio (e.g. if PURGE=1.0, PopF will keep
        spam repository as big as the ham repository)

    `PURGE = None`
    :   the option is disabled

    PURGE\_DIR is the directory to which oldest spams are moved. If
    PURGE\_DIR is None then the spams are deleted.

Generating probability database
-------------------------------

To build the database: `popf.py -gen`

A little patience...

You need to rebuild the database sometimes to maintain its efficiency.

Email reader configuration
--------------------------

To use PopF, you need to configure your software as follows:

Protocol
:   `POP3`

Server
:   `localhost`

User name
:   `your.user.name@your.pop.server`

Password
:   `your password on your.pop.server`

POP3 Port
:   `50110`

For example, my user name is `christophe.delord` on a POP3 server
(`pop.example.com`), my user name for PopF is then
`christophe.delord@pop.example.com` (though PopF knows it will connect to
`pop.example.com` and we can have different POP3 servers for different
accounts).

Starting PopF
=============

To start PopF: `popf.py -proxy`

You can start PopF automatically with your mail reader using a shell
script for instance.

Links
=====

-   [Python](http://www.python.org)
-   [Paul Graham](http://www.paulgraham.com/index.html)
-   [Gary Robinson](http://radio.weblogs.com/0101454/stories/2002/09/16/spamDetection.html)
-   [anti.spam.free.fr](http://anti.spam.free.fr/)
-   [caspam.org](http://caspam.org/)

