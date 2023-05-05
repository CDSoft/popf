#!/usr/bin/env python
#coding: Latin1

"""
PopF - A Spam Filter for POP3 Email Clients
Copyright (C) 2002-2008 Christophe Delord

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

For further information about PopF you can visit
http://christophe.delord.free.fr/popf

"""

try:
    import psyco
    psyco.profile()
except ImportError:
    pass

__version__ = "4.3.8"
__date__ = "2008-08-19"
__url__ = "http://christophe.delord.free.fr/popf"
__author__ = "Christophe Delord"

__python_version__ = 2, 3, 0

USAGE = r"""
Usage: popf [option]
    -changelog      : differences between versions
    -check          : check the current database
    -clean          : clean and forward POP3 accounts
    -efficiency     : compute the actual efficiency
    -gen            : generate statistics for the filter
    -help           : short help message
    -kill           : kill the local POP3 proxy if running
    -license        : show the GNU General Public License
    -proxy          : launch the local POP3 proxy
    -purge          : purge the spam corpus
    -version        : show the version
    -setup [method] <exhaustion>
                    : configure PopF (method can be "Graham",
                      "Robinson" or "Robinson-Fisher").
                      Use training to exhaustion learning method
                      if the <exhaustion> argument is given.
    -test <files>   : test files
    -sha            : show the SHA digest of the script to check
                      the integrity of the file

popf -proxy install the POP3 proxy at localhost:50110.
You must configure your email client like this:
    POP3 server  : localhost
    POP3 port    : 50110
    POP3 account : <your.pop3.identifier>@<the.pop3.server.of.your.isp>
    POP3 password: <your.pop3.password>

For further information:
    PopF home page:
        http://christophe.delord.free.fr/popf
    PopF's quicktopic discussion forum:
        http://www.quicktopic.com/22/H/kHFUf8uZXEw
    A Plan for Spam (Paul Graham):
        http://www.paulgraham.com/spam.html
    Spam Detection (Gary Robinson):
        http://radio.weblogs.com/0101454/stories/2002/09/16/spamDetection.html

"""

CHANGE_LOG = r"""
4.3.8 / 2008-08-19 Christophe Delord <christophe.delord@free.fr>

    * Minor bug fix
        Removes X-PopF-* and X-Spam flags before computing the spam
        probability (X-Spam was not removed)

4.3.7 / 2008-07-26 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Efficiency now calculated on a given duration.

4.3.6 / 2008-07-14 Christophe Delord <christophe.delord@free.fr>

    * Bug fix
        Date parser more robust.

4.3.5 / 2008-07-08 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Domain list update.
        Change purge option. A float value forces a spam/ham ratio.

4.3.4 / 2008-07-04 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Minor changes to recognize Claws mailboxes.

    * Bug fix
        -check option now works (wrong exclude parameter).

4.3.3 / 2008-03-27 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Minor changes to recognize Evolution mailboxes.

4.3.2 / 2007-09-29 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Uses USERPROFILE when HOME is not defined

4.3.1 / 2007-09-08 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Minor changes to recognize Thunderbird mailboxes.

    * Bug fix
        Fix token generation on Windows.
		Ignore SPAM directories inside HAM directories.

4.3.0 / 2007-05-01 Christophe Delord <christophe.delord@free.fr>

    * Changes
        PopF can forward (filtered) email to other accounts.

4.2.1 / 2006-03-02 Christophe Delord <christophe.delord@free.fr>

    * Bug fix
        Disable BYPASS when calling "popf -test" and "popf -gen".

4.2.0 / 2006-02-12 Christophe Delord <christophe.delord@free.fr>

    * Changes
        PopF can filter only headers to be faster (and maybe not to
        be fooled by non significative words in spams, to be used
        carefully). See HEADER_FILTER and BODY_FILTER options.
        BYPASS option defines messages not to be filtered.

4.1.3 / 2005-11-20 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Changed HTML comment recognition (<!--...--> instead of <!...>).

4.1.2 / 2005-10-04 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Some spams contain more than one Subject header. Popf now
        tags all the matching headers, not only the first.

4.1.1 / 2005-04-12 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Only "popf -proxy" and "popf -kill" can now stop the proxy.
        The user has to launch the proxy before using "popf -clean"
        for instance.  This way it is easier to have several popf
        processes running together (proxy, clean, normal email
        client, ...).
        The proxy is executed again when a socket error occurs.

4.1.0 / 2005-03-25 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Added a "X-Spam-Flag: YES" header for gnubiff support (and
        other mail client using this tag).

4.0.10 / 2005-02-14 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Some spams have base64 encoded objects that in fact are text
        objects. Now when a base64 object can not be decoded, PopF
        considers it as text.

    * Bug fixes
        Missing import traceback (ie can not decode badly encoded data)

4.0.9 / 2004-05-11 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Minor bug in -efficiency report (bad token number)

4.0.8 / 2004-10-27 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        When PopF was launched and tried to kill other PopF servers it
        sometimes failed because it didn't wait for the old servers to
        terminate. No need to execute it twice now.

4.0.7 / 2004-10-10 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Improve the identification of attachment names (recognize the name
        and filename tags) and HTML tag arguments (better "unsplitting" of
        tokens).

4.0.6 / 2004-10-03 Christophe Delord <christophe.delord@free.fr>

    * Changes
        PopF recognizes attachment file names (this should help in filtering
        viruses when PopF is used without an antivirus software).

    * Bug fixes
        Delete the old token file before generating it with Window$ (this OS
        can not rename a file if the new name already exists).

4.0.5 / 2004-09-06 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Training to exhaustion is not experimental any more. It has now
        be proven to be more efficient than the basic method (it's not
        the default method because it needs a huge amount of memory).
        It is so efficient that the antiviruses are useless ;-)

4.0.4 / 2004-06-23 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Try different sorts for the training to exhaustion learning method,
        the most efficient (ie which produces the smallest database) seems
        to be the chronological ordering.

4.0.3 / 2004-06-17 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Better interlace the list of spams and hams in the training
        to exhaustion learning method.

    * Bug fixes
        Minor bug fixes in regular expressions

4.0.2 / 2004-06-11 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Minor bug fixes in regular expressions
        Add the --mbox in the parameters of clamscan

4.0.1 / 2004-06-03 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Change the default parameters.
        The default UNCERTAIN value has been raised to 0.15.

    * Bug fixes
        In version 4.0.0 the whitelist was not correctly loaded.

4.0.0 / 2004-06-01 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Training to Exaustion as described by Gary Robinson (option
        TRAINING_TO_EXHAUSTION = True or False). The learning stage is
        slower but generate an incrediblely smaller database (and seems to
        be more efficient too).
        Complete rewriting to improve readability of the source.
        Remove the DNSBL usage since it broke the structure of the
        software (and I don't want to use external sources to filter
        spams).
        Default calculation method is Robinson-Fisher because it seems to
        work better with the training to exhaustion algorithm (the Robinson
        method takes a long time to converge or doesn't converge at all).
        Require Python 2.3.

    * Bug fixes
        Some spams have broken headers, PopF now tries to "unbreak" them.

3.1.5 / 2004-04-25 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Improve valid and invalid HTML tags detection, improve tag attribute
        detection (tags such as <S�R> are now invalid).
        Invalid tags and HTML comments are now considered as a special HTML
        tag (since they are good spam indicators).

    * Bug fixes
        Only the first antivirus was used. PopF now tries all antiviruses
        until one of them finds a virus.

3.1.4 / 2004-03-14 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Clean the whitelist when it is loaded (bug introduced in version
        3.1.2)

3.1.3 / 2004-02-26 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Use Psyco if it is available (mainly to load the database
        faster).

3.1.2 / 2004-02-15 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Reloads the database and the whitelist when they are generated.
        This feature is enabled by the AUTORELOAD option.

3.1.1 / 2004-02-08 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Run antivirus only on non spam messages to fasten the process
        (enabled by the FAST_ANTIVIRUS option).
        Can use many antiviruses. Warning: the ANTIVIRUS option replaces
        ANTIVIRUS_PROGRAM and ANTIVIRUS_VIRUS_REGEX options.

    * Bug fixes
        Scan stdout and also stderr when running antiviruses programs.

3.1.0 / 2004-01-22 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Added a fake threading emulation for Python distributions built
        without the thread support (thanks to Andreas Heijdendael for
        reporting the bug).

3.0.10 / 2004-01-18 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        HTML_COMMENT_RE expression sometimes loops for a long time. The
        expression has been simplified (undo 3.0.5 change).
        Some spelling errors fixed in the web documentation (thanks to
        Kevin Rowanet).

3.0.9 / 2004-01-07 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Store DNSBL in lower case in the database.
        Better compatibility with Python 2.2.1 : SIGNIFICANT=None now
        works with Python 2.2.1 (thanks to Nicolas Di Pietro for reporting
        the bug).

3.0.8 / 2003-11-18 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        When the POP3 identification failed, PopF entered an infinite loop
        and waisted most of CPU ressources (thanks to Jesper Nee for his
        comments and his help on this bug).

3.0.7 / 2003-11-02 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Changed some regular expressions but not really bugs.

3.0.6 / 2003-10-28 Christophe Delord <christophe.delord@free.fr>

    * Changes
        The default UNCERTAIN value has been lowered to 0.05.

    * Bug fixes
        Converts HTML characters *before* searching HTML tags.
        Finds more HTML characters (&#\d+; instead of &#\d\d\d;)

3.0.5 / 2003-10-24 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Removes <RNDMX[8]> tags (and more generally <...> tags) in HTML
        comments that split significant words (this may be a bug of
        spammer tools, spammers are not very intelligent).

3.0.4 / 2003-10-13 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Fake HTML tag detection improved (now fake tags can contain fake
        parameters).
        Added a html* token type for HTML tags to analyse tags appart from
        the rest of the message (and then to unsplit splitted words)

3.0.3 / 2003-10-09 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Minor bug fixed (on mutual exclusion of the filter)

3.0.2 / 2003-09-09 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Reload the database before each cleaning (see popf -clean)

3.0.1 / 2003-08-26 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Only check IP addresses when using DNSBLs

3.0.0 / 2003-08-25 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Added the DNSBL support as described by Jon Seymour (when a
        server is known by a DNSBL, the DNSBL is added to the list of
        tokens of the message, if the DNSBL is good enough it will help
        in separating spams and non spams).
        Added DNSBL efficiency testing in -efficiency
        Added filtering in the TOP command.
        Remove useless headers (messages id for example) before extracting
        tokens to have a smaller database.
        Better URLs, IPs and emails analysis.

    * Bug fixes
        Better split multipart messages.
        Some spams have two \r to break headers so added headers are
        ignored. Multiple \r are now reduced to a single \r.

2.2.2 / 2003-08-03 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Added the -efficiency to compute the real efficiency of PopF

    * Bug fixes
        Removes '\r' in incoming messages (otherwise attachments may not
        be decoded and some spams passed throught even if popf -test reports
        them as spam).

2.2.1 / 2003-07-29 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Better lexical analyse for URL and emails (store partial addresses).
        Thanks to Jon Seymour for the idea.
        Jon Seymour has also created a quicktopic discussion forum for PopF.

    * Bug fixes
        The '-' char was not escaped in the default TOKEN regular expression.
        Minor bug in popf -clean

2.2.0 / 2003-07-23 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Add the -clean option to clean POP3 servers.
        Add timeout support in socket IO (using Python 2.3 sockets)
        Python 2.3 is required for timeout sockets but PopF should works
        fine with Python 2.2.2 without the timeout feature.
        Add the -purge option to purge the spam corpus (ie to remove
        oldest spams).
        Add the DEBUG parameter to print debug information.
        Add a registration page on PopF's web.

    * Bug fixes
        Try to fix badly base64 encoded attachments (thanks to Axel
        Vandevenne for reporting and analysing the bug). Not really
        a bug but PopF is now more robust (but less efficient when
        those attachments can not be fixed).

2.1.4 / 2003-07-03 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Try to decode strange Micro$oft encoding (non mime encoding)

    * Bug fixes
        Avoid zero division on empty files (ie no token in file). Thanks
        to Francois Garnier for reporting the bug.

2.1.3 / 2003-06-24 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Add a VIRUS_TAG in the subject when a virus is detected.
        (Thanks to Bruno Tanqueray for the suggestion).
        Don't scan files that don't contain messages (At this time only
        Sylpheed, KMail, Netscape and Evolution are known, please report
        file names to be ignored for others email clients to help me update
        the default values of the IGNORED_EXTENSIONS parameter).
        Default calculation method is Robinson (Robinson-Fisher is less
        robust because of overflow)

    * Bug fixes
        Better split multipart documents (smaller and faster data base).
        Change html_comment_re to avoid RuntimeError (Thanks to Neo KoD
        for reporting the bug).
        Correctly save the \ separator of window$ path names in popfrc.
        Don't get stuck on a UIDL command with a message number (may now
        work better with Evolution).

2.1.2 / 2003-05-28 Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Empty corpus doesn't raise a ZeroDivisionError anymore.

2.1.1 / 2003-05-19 Christophe Delord <christophe.delord@free.fr>

    * Changes
        Consider any unknown HTML tag as HTML comment (stronger
        than 1.7 feature).
        Change HTML comments from <!--.*?--> to <!.*?>
        HTML comments can be multiline.

    * Bug fixes
        Empty POP3 command is ignored instead of raising an error

2.1 / 2003-03-31    Christophe Delord <christophe.delord@free.fr>

    * Changes
        Added the popf -license command.
        popf.py renamed shorter as popf.
        Statistic generator included into popf. Some changes to the
        PopF home page too.

    * Bug fixes
        Uppercase emails now work well in the whitelist.

2.0.5   Christophe Delord <christophe.delord@free.fr>

    * Changes
        Non significative words are ignored (words which probability is close
        to 0.5).
        Predefined configurations have been tuned for an improved efficiency.
        Listing of the probabilities of all messages.
        Multithreading support for probability loading and request handling so
        as not to block connexions and authorise simultaneous connections.

    * Bug fixes
        Window$ and Mac messages can contain \r characters and are now
        correctly decoded (Thanks to Jon Seymour).

2.0.4   Christophe Delord <christophe.delord@free.fr>

    * Changes
        Added a default configuration file (C:\popf.conf for Window$ and
        /etc/popf.conf for Linux/Unix/Others) (Thanks to Antoine Tissier).

    * Bug fixes
        Uses a fake socket before the connection is established because some
        mail clients send command (eg CAPA) before identification (Thanks to
        Antoine Tissier).

2.0.3   Christophe Delord <christophe.delord@free.fr>

    * Changes
        Implements the improvement described by Gary Robinson in "A
        Statistical Approach to the Spam Problem".
        Treat rare words smoother (using f(w) calculation and
        RARE_WORD_STRENGH parameter).
        Doesn't tag uncertain messages (see UNCERTAIN parameter).
        Added the Robinson-Fisher method (uses a Chi-2 distribution)
        (Thanks to Gary Robinson for his help)

2.0.2   Christophe Delord <christophe.delord@free.fr>

    * Changes
        Integrity check (SHA method) to detect bad downloads.

    * Bug fixes
        Minor bug in case of bad identification on the POP3 server.

2.0.1   Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        HTML characters which code is greater than 256 are not converted.
        Fixed the FakeSocket.recv prototype (crashes when the connection
        fails).
        Allows POP3 identifiers to contain '@'.
        Fixed a bug when the result of a LIST is empty.
        (Thanks to Nicolas Vivier)

2.0     Christophe Delord <christophe.delord@free.fr>

    * Changes
        PopF can be connected to an antivirus (works well with f-prot).
        Messages containing viruses are added a X-PopF-Virus header.
        (I also wanted to automatically warn the sender that he/she is
        infected but viruses may change the From header and I don't want PopF
        to be a spammer ;-)

1.8     Christophe Delord <christophe.delord@free.fr>

    * Changes
        If TAG == "", subject is not tagged
        Added a X-PopF-Spam header containing the spam probability.
        (Thanks to Florian Kleinmanns)

    * Bug fixes
        Correctly tag the subject when this header is not in the message.
        (Thanks to Florian Kleinmanns)

1.7.4   Christophe Delord <christophe.delord@free.fr>

    * Changes
        CAPA command support.

1.7.3   Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Better Window$ support (socket.socket is a class on Linux and a
        function on Window$). This bug was introduced in 1.6.
        (Thanks to Hayward Cho)

1.7.2   Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Fixed a bug in message decoding introduced in 1.7.1

1.7.1   Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Fixed a bug in message decoding (mime type converted to lower case)

1.7     Christophe Delord <christophe.delord@free.fr>

    * Changes
        Added the METHOD parameter (Graham or Robinson).
        URL are considered as a single token (symbolic address and IP) by the
        lexer.
        The euro sign is know by the lexer.
        Removes unknown HTML tags (some spams use them to split relevant
        spammy words). These tags are seen as HTML comment and are recognized
        as <[a-zA-Z]{6,}>.
        I did some testing with WINDOW > 1 but new spams are not all filtered
        so WINDOW remains inactive.
        Special HTML characters are handled (&...;) by the lexer.
        Hexadecimal coded caracters are handled (=XX) by the lexer.

    * Bug fixes
        Messages were decoded twice. PopF should now be faster.

1.6     Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Fixed a bug in POP3 data interpretation that make PopF incorrectly tag
        spams.

1.5     Christophe Delord <christophe.delord@free.fr>

    * Changes
        Added some comment in the source code.
        Made some speed improvments.

1.4     Christophe Delord <christophe.delord@free.fr>

    * Changes
        Removes non printable chararacters (some spams contains ^H, ^A, ^N in
        the subject header)
        Added the log support (if LOG == TRUE) in ~/.popf/popf.log.
        Removes the user email address from the whitelist since spammers often
        uses the user email as the sender email.

1.3     Christophe Delord <christophe.delord@free.fr>

    * Changes
        Removes HTML comments before the message is analysed.

1.2     Christophe Delord <christophe.delord@free.fr>

    * Changes
        Makes no difference between upper case and lower case emails.

    * Bug fixes
        Desactivation of the WINDOW parameter because of false positive when
        WINDOW > 1

1.1     Christophe Delord <christophe.delord@free.fr>

    * Bug fixes
        Fixed some bugs in message decoding.

1.0     Christophe Delord <christophe.delord@free.fr>

    * First release.
"""

ABOUT_POPF = """\
PopF version %s, Copyright (C) 2002-%s %s
PopF comes with ABSOLUTELY NO WARRANTY; for details type `popf -help'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `popf -license' for details.
"""%(__version__, __date__.split('-')[0], __author__)

LICENSE = r"""
                    GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc.
 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The licenses for most software are designed to take away your
freedom to share and change it.  By contrast, the GNU General Public
License is intended to guarantee your freedom to share and change free
software--to make sure the software is free for all its users.  This
General Public License applies to most of the Free Software
Foundation's software and to any other program whose authors commit to
using it.  (Some other Free Software Foundation software is covered by
the GNU Library General Public License instead.)  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
this service if you wish), that you receive source code or can get it
if you want it, that you can change the software or use pieces of it
in new free programs; and that you know you can do these things.

  To protect your rights, we need to make restrictions that forbid
anyone to deny you these rights or to ask you to surrender the rights.
These restrictions translate to certain responsibilities for you if you
distribute copies of the software, or if you modify it.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must give the recipients all the rights that
you have.  You must make sure that they, too, receive or can get the
source code.  And you must show them these terms so they know their
rights.

  We protect your rights with two steps: (1) copyright the software, and
(2) offer you this license which gives you legal permission to copy,
distribute and/or modify the software.

  Also, for each author's protection and ours, we want to make certain
that everyone understands that there is no warranty for this free
software.  If the software is modified by someone else and passed on, we
want its recipients to know that what they have is not the original, so
that any problems introduced by others will not reflect on the original
authors' reputations.

  Finally, any free program is threatened constantly by software
patents.  We wish to avoid the danger that redistributors of a free
program will individually obtain patent licenses, in effect making the
program proprietary.  To prevent this, we have made it clear that any
patent must be licensed for everyone's free use or not licensed at all.

  The precise terms and conditions for copying, distribution and
modification follow.

                    GNU GENERAL PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. This License applies to any program or other work which contains
a notice placed by the copyright holder saying it may be distributed
under the terms of this General Public License.  The "Program", below,
refers to any such program or work, and a "work based on the Program"
means either the Program or any derivative work under copyright law:
that is to say, a work containing the Program or a portion of it,
either verbatim or with modifications and/or translated into another
language.  (Hereinafter, translation is included without limitation in
the term "modification".)  Each licensee is addressed as "you".

Activities other than copying, distribution and modification are not
covered by this License; they are outside its scope.  The act of
running the Program is not restricted, and the output from the Program
is covered only if its contents constitute a work based on the
Program (independent of having been made by running the Program).
Whether that is true depends on what the Program does.

  1. You may copy and distribute verbatim copies of the Program's
source code as you receive it, in any medium, provided that you
conspicuously and appropriately publish on each copy an appropriate
copyright notice and disclaimer of warranty; keep intact all the
notices that refer to this License and to the absence of any warranty;
and give any other recipients of the Program a copy of this License
along with the Program.

You may charge a fee for the physical act of transferring a copy, and
you may at your option offer warranty protection in exchange for a fee.

  2. You may modify your copy or copies of the Program or any portion
of it, thus forming a work based on the Program, and copy and
distribute such modifications or work under the terms of Section 1
above, provided that you also meet all of these conditions:

    a) You must cause the modified files to carry prominent notices
    stating that you changed the files and the date of any change.

    b) You must cause any work that you distribute or publish, that in
    whole or in part contains or is derived from the Program or any
    part thereof, to be licensed as a whole at no charge to all third
    parties under the terms of this License.

    c) If the modified program normally reads commands interactively
    when run, you must cause it, when started running for such
    interactive use in the most ordinary way, to print or display an
    announcement including an appropriate copyright notice and a
    notice that there is no warranty (or else, saying that you provide
    a warranty) and that users may redistribute the program under
    these conditions, and telling the user how to view a copy of this
    License.  (Exception: if the Program itself is interactive but
    does not normally print such an announcement, your work based on
    the Program is not required to print an announcement.)

These requirements apply to the modified work as a whole.  If
identifiable sections of that work are not derived from the Program,
and can be reasonably considered independent and separate works in
themselves, then this License, and its terms, do not apply to those
sections when you distribute them as separate works.  But when you
distribute the same sections as part of a whole which is a work based
on the Program, the distribution of the whole must be on the terms of
this License, whose permissions for other licensees extend to the
entire whole, and thus to each and every part regardless of who wrote it.

Thus, it is not the intent of this section to claim rights or contest
your rights to work written entirely by you; rather, the intent is to
exercise the right to control the distribution of derivative or
collective works based on the Program.

In addition, mere aggregation of another work not based on the Program
with the Program (or with a work based on the Program) on a volume of
a storage or distribution medium does not bring the other work under
the scope of this License.

  3. You may copy and distribute the Program (or a work based on it,
under Section 2) in object code or executable form under the terms of
Sections 1 and 2 above provided that you also do one of the following:

    a) Accompany it with the complete corresponding machine-readable
    source code, which must be distributed under the terms of Sections
    1 and 2 above on a medium customarily used for software interchange; or,

    b) Accompany it with a written offer, valid for at least three
    years, to give any third party, for a charge no more than your
    cost of physically performing source distribution, a complete
    machine-readable copy of the corresponding source code, to be
    distributed under the terms of Sections 1 and 2 above on a medium
    customarily used for software interchange; or,

    c) Accompany it with the information you received as to the offer
    to distribute corresponding source code.  (This alternative is
    allowed only for noncommercial distribution and only if you
    received the program in object code or executable form with such
    an offer, in accord with Subsection b above.)

The source code for a work means the preferred form of the work for
making modifications to it.  For an executable work, complete source
code means all the source code for all modules it contains, plus any
associated interface definition files, plus the scripts used to
control compilation and installation of the executable.  However, as a
special exception, the source code distributed need not include
anything that is normally distributed (in either source or binary
form) with the major components (compiler, kernel, and so on) of the
operating system on which the executable runs, unless that component
itself accompanies the executable.

If distribution of executable or object code is made by offering
access to copy from a designated place, then offering equivalent
access to copy the source code from the same place counts as
distribution of the source code, even though third parties are not
compelled to copy the source along with the object code.

  4. You may not copy, modify, sublicense, or distribute the Program
except as expressly provided under this License.  Any attempt
otherwise to copy, modify, sublicense or distribute the Program is
void, and will automatically terminate your rights under this License.
However, parties who have received copies, or rights, from you under
this License will not have their licenses terminated so long as such
parties remain in full compliance.

  5. You are not required to accept this License, since you have not
signed it.  However, nothing else grants you permission to modify or
distribute the Program or its derivative works.  These actions are
prohibited by law if you do not accept this License.  Therefore, by
modifying or distributing the Program (or any work based on the
Program), you indicate your acceptance of this License to do so, and
all its terms and conditions for copying, distributing or modifying
the Program or works based on it.

  6. Each time you redistribute the Program (or any work based on the
Program), the recipient automatically receives a license from the
original licensor to copy, distribute or modify the Program subject to
these terms and conditions.  You may not impose any further
restrictions on the recipients' exercise of the rights granted herein.
You are not responsible for enforcing compliance by third parties to
this License.

  7. If, as a consequence of a court judgment or allegation of patent
infringement or for any other reason (not limited to patent issues),
conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot
distribute so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you
may not distribute the Program at all.  For example, if a patent
license would not permit royalty-free redistribution of the Program by
all those who receive copies directly or indirectly through you, then
the only way you could satisfy both it and this License would be to
refrain entirely from distribution of the Program.

If any portion of this section is held invalid or unenforceable under
any particular circumstance, the balance of the section is intended to
apply and the section as a whole is intended to apply in other
circumstances.

It is not the purpose of this section to induce you to infringe any
patents or other property right claims or to contest validity of any
such claims; this section has the sole purpose of protecting the
integrity of the free software distribution system, which is
implemented by public license practices.  Many people have made
generous contributions to the wide range of software distributed
through that system in reliance on consistent application of that
system; it is up to the author/donor to decide if he or she is willing
to distribute software through any other system and a licensee cannot
impose that choice.

This section is intended to make thoroughly clear what is believed to
be a consequence of the rest of this License.

  8. If the distribution and/or use of the Program is restricted in
certain countries either by patents or by copyrighted interfaces, the
original copyright holder who places the Program under this License
may add an explicit geographical distribution limitation excluding
those countries, so that distribution is permitted only in or among
countries not thus excluded.  In such case, this License incorporates
the limitation as if written in the body of this License.

  9. The Free Software Foundation may publish revised and/or new versions
of the General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

Each version is given a distinguishing version number.  If the Program
specifies a version number of this License which applies to it and "any
later version", you have the option of following the terms and conditions
either of that version or of any later version published by the Free
Software Foundation.  If the Program does not specify a version number of
this License, you may choose any version ever published by the Free Software
Foundation.

  10. If you wish to incorporate parts of the Program into other free
programs whose distribution conditions are different, write to the author
to ask for permission.  For software which is copyrighted by the Free
Software Foundation, write to the Free Software Foundation; we sometimes
make exceptions for this.  Our decision will be guided by the two goals
of preserving the free status of all derivatives of our free software and
of promoting the sharing and reuse of software generally.

                            NO WARRANTY

  11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.

  12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES.

                     END OF TERMS AND CONDITIONS
"""

import glob
import locale
import math
import operator
import os
import re
import rfc822
import sha
import smtplib
import socket
import StringIO
import sys
import tempfile
import time
import traceback

from itertools import chain

####################################################################
#
# Various functions
#
####################################################################

first = lambda seq: seq[0]
second = lambda seq: seq[1]

firsts = lambda seq: map(first, seq)
seconds = lambda seq: map(second, seq)

lower = lambda st: st.strip().lower()
lowers = lambda seq: map(lower, seq)

def robust(function, *args):
    try:
        return function(*args)
    except Exception:
        if DEBUG_LEVEL > 0:
            traceback.print_exc()
        return None

def uniq(iterable):
    seen = {}
    for item in iterable:
        if item not in seen:
            seen[item] = True
            yield item

####################################################################
#
# Error messages
#
####################################################################

DEBUG_LEVEL = 0

def warning(msg):
    print >>sys.stderr, "WARNING -", msg

def error(msg):
    print >>sys.stderr, "ERROR -", msg
    sys.exit(-1)

def debug(level, msg):
    if level <= DEBUG_LEVEL:
        print >>sys.stderr, "DEBUG -", msg

class Tee:
    def __init__(self, out1, out2):
        self.out1 = out1
        self.out2 = out2
    def write(self, s):
        self.out1.write(s)
        self.out2.write(s)
        self.out1.flush()
        self.out2.flush()

def start_log():
    if config['LOG']:
        log = file(config['LOG_FILE'], 'a')
        sys.stdout = Tee(sys.stdout, log)
        sys.stderr = Tee(sys.stderr, log)

####################################################################
#
# Version check
#
####################################################################

if sys.version_info[:3] < __python_version__:
    error("PopF %s requires at least Python %s"%(__version__, ".".join(map(str, __python_version__))))

expected_sha = 0x54921EDF1904BB92A1D14EC8F9A8B0C278D9DA60

def compute_sha():
    code = file(sys.argv[0], "rb").read()
    code = re.sub(r'expected_sha = 0x[0-9a-fA-Z]+', '', code)
    return long(sha.new(code).hexdigest(), 16)
computed_sha = compute_sha()

if computed_sha != expected_sha:
    warning("Integrity check failed, you are using an unofficial modified PopF")

def popf_sha():
    print ABOUT_POPF
    if computed_sha == expected_sha:
        print "Integrity check passed"
    else:
        print "Integrity check failed"
    print
    print "SHA Digest: 0x%X"%computed_sha

####################################################################
#
# Threading emulation (if not enabled)
#
####################################################################

try:
    import threading
except ImportError:
    warning("The threading support has been disabled in your Python")
    warning("distribution. You can use PopF anyway but you must wait")
    warning("PopF to be ready before sending the first request.")

    class threading:

        class Thread:
            def __init__(self, *args, **kwargs): pass
            def start(self): return self.run()
            def getName(self): return "no thread"

        class Lock:
            def acquire(self, *args, **kwargs): pass
            def release(self, *args, **kwargs): pass

####################################################################
#
# Miscellaneous help functions
#
####################################################################

def popf_help():
    print ABOUT_POPF
    print "--"
    print "PopF & Python", sys.version
    print "--"
    print USAGE
    print __doc__.strip()

def popf_changelog():
    print ABOUT_POPF
    print CHANGE_LOG

def popf_license():
    print LICENSE

def popf_version():
    print "PopF v%s"%__version__

####################################################################
#
# Configuration
#
####################################################################

class Config(dict):
    """ Dictionnary holding PopF parameters
    """

    COMMON = {
        # Proxy parameters
            'HOST': 'localhost',
            'PORT': 50110,
            'TIMEOUT': None,
        # Save POP3 dialog if LOG is True
            'LOG': False,
        # Print debug information up to a level
            'DEBUG': None,

        # Lexical analyser
            'LOCALE': None,
            # accepts letters, digits, _, ', $, -, euro
            'TOKEN': r"[\w\'$\-\200]+",
            # rejects numbers and one or two letter words
            'NONTOKEN': r"\d+|.{,2}",
            # filters headers and bodies
            'HEADER_FILTER': True,
            'BODY_FILTER': True,

        # Pathes to bad and good corpora
            'GOOD_CORPUS': (),
            'BAD_CORPUS': (),
        # Files to be ignored
            'IGNORED_EXTENSIONS': (
                                                            # Sylpheed (no file to ignore)
                                                            # KMail (no file to ignore)
                '.snm', '.dat',                             # Netscape
                '.xml', '.ev-summary', '.index', '.data',   # Evolution
                '.cmeta', '.ev-summary-meta',               # Evolution 
                '.msf',                                     # Thunderbird
                                                            # Claws mail (no file to ignore)
            ),

        # Learning method
            'TRAINING_TO_EXHAUSTION': False,
            'TRAINING_TO_EXHAUSTION_GOOD_LIMIT': 0.1,
            'TRAINING_TO_EXHAUSTION_BAD_LIMIT': 0.8,
            'TRAINING_TO_EXHAUSTION_MAX_ITERATION': 20,

        # User emails used to build the white list
            'WHITELIST': (),

        # Autoreload the database when it is generated
            'AUTORELOAD': False,

        # Tag added at the beginning of the subjet of spam messages
            'TAG': "[S P A M]",

        # Default antivirus interface is inactive
            'ANTIVIRUS': (),
            'VIRUS_TAG': "[V I R U S]",
            'FAST_ANTIVIRUS': False,

        # Bypass regular expressions
            'BYPASS': (),

        # Cleaner options
            'CLEANER_ACCOUNTS': (),
            'CLEANER_DIRECTORY': "",
            'CLEANER_PERIOD': None,
            'CLEANER_FORWARDS': (),
            'CLEANER_SMTP': "localhost",

        # Purge options
            'PURGE': None,              # number of monthes before purging a message
                                        # or spam/ham ratio
            'PURGE_DIRECTORY': None,    # directory where purged messages are saved
    }

    DEFAULT = {
        "Graham": {
            "METHOD": "Graham",
            "FREQUENCY_THRESHOLD": 5,
            "GOOD_BIAS": 2.0,
            "BAD_BIAS": 1.0,
            "GOOD_PROB": 0.0001,
            "BAD_PROB": 0.9999,
            "UNKNOWN_PROB": 0.4,
            "RARE_WORD_STRENGTH": 0.0,
            "SIGNIFICANT": 15,
            "BAD_THRESHOLD": 0.9,
            "UNCERTAIN": 0.0,
            "PROBABILITY_THRESHOLD": 0.1,
            'TRAINING_TO_EXHAUSTION': False,
        },
        "Robinson": {
            "METHOD": "Robinson",
            "FREQUENCY_THRESHOLD": 0,
            "GOOD_BIAS": 1.0,
            "BAD_BIAS": 1.0,
            "GOOD_PROB": 0.0001,
            "BAD_PROB": 0.9999,
            "UNKNOWN_PROB": 0.45,
            "RARE_WORD_STRENGTH": 0.0,
            "SIGNIFICANT": None,
            "BAD_THRESHOLD": 0.5,
            "UNCERTAIN": 0.15,
            "PROBABILITY_THRESHOLD": 0.1,
            'TRAINING_TO_EXHAUSTION': False,
        },
        "Robinson-Fisher": {
            "METHOD": "Robinson-Fisher",
            "FREQUENCY_THRESHOLD": 0,
            "GOOD_BIAS": 1.0,
            "BAD_BIAS": 1.0,
            "GOOD_PROB": 0.0001,
            "BAD_PROB": 0.9999,
            "UNKNOWN_PROB": 0.45,
            "RARE_WORD_STRENGTH": 0.0,
            "SIGNIFICANT": None,
            "BAD_THRESHOLD": 0.5,
            "UNCERTAIN": 0.15,
            "PROBABILITY_THRESHOLD": 0.1,
            'TRAINING_TO_EXHAUSTION': False,
        },
        "Graham-exhaustion": {
            "METHOD": "Graham",
            "FREQUENCY_THRESHOLD": 5,
            "GOOD_BIAS": 2.0,
            "BAD_BIAS": 1.0,
            "GOOD_PROB": 0.0001,
            "BAD_PROB": 0.9999,
            "UNKNOWN_PROB": 0.4,
            "RARE_WORD_STRENGTH": 0.0,
            "SIGNIFICANT": 15,
            "BAD_THRESHOLD": 0.9,
            "UNCERTAIN": 0.0,
            "PROBABILITY_THRESHOLD": 0.1,
            'TRAINING_TO_EXHAUSTION': True,
            'TRAINING_TO_EXHAUSTION_GOOD_LIMIT': 0.1,
            'TRAINING_TO_EXHAUSTION_BAD_LIMIT': 0.9,
        },
        "Robinson-exhaustion": {
            "METHOD": "Robinson",
            "FREQUENCY_THRESHOLD": 5,
            "GOOD_BIAS": 1.0,
            "BAD_BIAS": 1.0,
            "GOOD_PROB": 0.0001,
            "BAD_PROB": 0.9999,
            "UNKNOWN_PROB": 0.45,
            "RARE_WORD_STRENGTH": 0.0,
            "SIGNIFICANT": None,
            "BAD_THRESHOLD": 0.5,
            "UNCERTAIN": 0.15,
            "PROBABILITY_THRESHOLD": 0.1,
            'TRAINING_TO_EXHAUSTION': True,
            'TRAINING_TO_EXHAUSTION_GOOD_LIMIT': 0.2,
            'TRAINING_TO_EXHAUSTION_BAD_LIMIT': 0.7,
        },
        "Robinson-Fisher-exhaustion": {
            "METHOD": "Robinson-Fisher",
            "FREQUENCY_THRESHOLD": 5,
            "GOOD_BIAS": 1.0,
            "BAD_BIAS": 1.0,
            "GOOD_PROB": 0.0001,
            "BAD_PROB": 0.9999,
            "UNKNOWN_PROB": 0.45,
            "RARE_WORD_STRENGTH": 0.0,
            "SIGNIFICANT": None,
            "BAD_THRESHOLD": 0.5,
            "UNCERTAIN": 0.15,
            "PROBABILITY_THRESHOLD": 0.1,
            'TRAINING_TO_EXHAUSTION': True,
            'TRAINING_TO_EXHAUSTION_GOOD_LIMIT': 0.1,
            'TRAINING_TO_EXHAUSTION_BAD_LIMIT': 0.8,
        },
    }

    def default(self, method="Robinson-Fisher", exhaustion=False):
        if exhaustion: method += '-exhaustion'
        try:
            default_config = Config.DEFAULT[method]
        except KeyError:
            error("No predefined parameters for this method (%s)"%method)
        self.update(default_config)

    def __init__(self):
        dict.__init__(self)
        # Default builtin configuration
        self.update(Config.COMMON)
        self.default()
        # Defaut/common configuration
        if sys.platform.startswith("win"):
            self['POPFCONF'] = os.path.join("C:", "popf.conf")
        else:
            self['POPFCONF'] = os.path.join(os.sep, "etc", "popf.conf")
        if os.path.isfile(self['POPFCONF']): execfile(self['POPFCONF'], self)
        # User's configuration
        if 'HOME' in os.environ:
            home = os.environ['HOME']
        elif 'USERPROFILE' in os.environ:
            home = os.environ['USERPROFILE']
        elif 'HOME' in self:
            home = self['HOME']
        else:
            error("Environment variable HOME or USERPROFILE not defined\nHOME not defined in %s"%self['POPFCONF'])
        home = os.path.join(home, ".popf")
        self.update({
            # HOME : path where .popf directory resides
            'HOME': home,
            # POPFRC : name of the config file
            'POPFRC': os.path.join(home, "popfrc"),
            # TOKEN : name of the probability file
            'TOKEN_FILE': os.path.join(home, "tokens"),
            # WHITELIST : name of the whitelist file
            'WHITELIST_FILE': os.path.join(home, "whitelist"),
            # LOG_FILE : name of the log file (if enabled)
            'LOG_FILE': os.path.join(home, "popf.log"),
        })

        # Creates .popf if first execution
        if not os.path.isdir(self['HOME']): os.mkdir(self['HOME'])

        # Load user configuration
        if os.path.isfile(self['POPFRC']): execfile(self['POPFRC'], self)

        # Lexical analyser initialisation
        if self['LOCALE'] is not None: locale.setlocale(locale.LC_ALL, self['LOCALE'])
        self['TOKEN_RE'] = re.compile(self['TOKEN'], re.LOCALE)
        self['NONTOKEN_RE'] = re.compile(r"^(%s)$"%self['NONTOKEN'], re.LOCALE)

        # whitelist and corpora must be lists of strings
        if isinstance(self['GOOD_CORPUS'], str): self['GOOD_CORPUS'] = [self['GOOD_CORPUS']]
        if isinstance(self['BAD_CORPUS'], str): self['BAD_CORPUS'] = [self['BAD_CORPUS']]
        if isinstance(self['WHITELIST'], str): self['WHITELIST'] = [self['WHITELIST']]

        # cleaner's account list must be a list of strings
        if isinstance(self['CLEANER_ACCOUNTS'], str): self['CLEANER_ACCOUNTS'] = [self['CLEANER_ACCOUNTS']]
        if isinstance(self['CLEANER_FORWARDS'], str): self['CLEANER_FORWARDS'] = [self['CLEANER_FORWARDS']]

        # bypass must be a list of strings
        if isinstance(self['BYPASS'], str): self['BYPASS'] = [self['BYPASS']]
        self['BYPASS_RE'] = [re.compile(b, re.MULTILINE|re.DOTALL) for b in self['BYPASS']]

        # Set the global DEBUG flag
        global DEBUG_LEVEL
        DEBUG_LEVEL = self['DEBUG'] or 0
        debug(1, "Activating debug information (level %s)"%DEBUG_LEVEL)

    def save(self):
        config = StringIO.StringIO()

        def title(msg):
            print >>config, "#"*60
            print >>config, "#", msg
            print >>config, "#"*60
            print >>config

        def help(msg):
            print >>config, "#", msg

        def var(name, value):
            print >>config, name, "=", value

        def nl():
            print >>config

        title("PopF settings")
        map(help, ABOUT_POPF.splitlines())
        nl()

        title("POPF's HOME")
        help("If PopF is launched during startup, before HOME is set")
        help("you can copy this file to %s and set HOME"%self['POPFCONF'])
        if sys.platform.startswith("win"):
            help("HOME = 'C:'")
        else:
            help("HOME = '/home/someone'")
        nl()

        title("POP3 proxy")
        var("HOST", "'%s'"%self['HOST'])
        var("PORT", self['PORT'])
        var("TIMEOUT", self['TIMEOUT'])
        nl()
        help("Log POP3 traffic to popf.log?")
        var("LOG", bool(self['LOG']))
        nl()
        help("Save debug information (detail level between 0 and 3)")
        var("DEBUG", self['DEBUG'] or None)
        nl()

        title("Locale settings")
        var("LOCALE", self['LOCALE'] and "'%s'"%self['LOCALE'] or None)
        nl()

        title("Tokenizer settings")
        help("Regular expression used to split messages into tokens")
        nl()
        help("Regular tokens")
        var("TOKEN", "r'%s'"%self['TOKEN'])
        nl()
        help("Regular expression used to discard non significative tokens")
        var("NONTOKEN", "r'%s'"%self['NONTOKEN'])
        nl()
        help("Header filter flag")
        var("HEADER_FILTER", bool(self['HEADER_FILTER']))
        nl()
        help("Body filter flag")
        var("BODY_FILTER", bool(self['BODY_FILTER']))
        nl()

        title("Corpuses settings")
        help("Files or directories containing non spam messages")
        var("GOOD_CORPUS", ", ".join(["'%s'"%c.replace('\\', '\\\\') for c in self['GOOD_CORPUS']]) or ())
        nl()
        help("Files or directories containing spam messages")
        var("BAD_CORPUS", ", ".join(["'%s'"%c.replace('\\', '\\\\') for c in self['BAD_CORPUS']]) or ())
        nl()
        help("Files to be ignored while scanning corpora")
        var("IGNORED_EXTENSIONS", ", ".join(["'%s'"%e for e in self['IGNORED_EXTENSIONS']]) or ())
        nl()
        help("Your emails (to build the white list from people you write to)")
        var("WHITELIST", ", ".join(["'%s'"%a for a in self['WHITELIST']]) or ())
        nl()
        help("Autoreload the database when it is generated")
        var("AUTORELOAD", bool(self['AUTORELOAD']))
        nl()

        title("Filter settings")
        help("Learning method")
        var("TRAINING_TO_EXHAUSTION", bool(self['TRAINING_TO_EXHAUSTION']))
        var("TRAINING_TO_EXHAUSTION_GOOD_LIMIT", self['TRAINING_TO_EXHAUSTION_GOOD_LIMIT'])
        var("TRAINING_TO_EXHAUSTION_BAD_LIMIT", self['TRAINING_TO_EXHAUSTION_BAD_LIMIT'])
        var("TRAINING_TO_EXHAUSTION_MAX_ITERATION", self['TRAINING_TO_EXHAUSTION_MAX_ITERATION'])
        nl()
        help("Computation method (Graham, Robinson or Robinson-Fisher)")
        var("METHOD", "'%s'"%self['METHOD'])
        nl()
        help("Number of times a word should be received to be stored in the filter")
        var("FREQUENCY_THRESHOLD", self['FREQUENCY_THRESHOLD'])
        nl()
        help("Ignore words which probability p verifies |p-0.5| < PROBABILITY_THRESHOLD")
        var("PROBABILITY_THRESHOLD", self['PROBABILITY_THRESHOLD'])
        nl()
        help("Bias for nonspam words")
        var("GOOD_BIAS", self['GOOD_BIAS'])
        nl()
        help("Bias for spam words")
        var("BAD_BIAS", self['BAD_BIAS'])
        nl()
        help("Probability of nonspam messages")
        var("GOOD_PROB", self['GOOD_PROB'])
        nl()
        help("Probability of spam messages")
        var("BAD_PROB", self['BAD_PROB'])
        nl()
        help("Probability of unknown words")
        var("UNKNOWN_PROB", self['UNKNOWN_PROB'])
        nl()
        help("Strength of the background information (rare words)")
        var("RARE_WORD_STRENGTH", self['RARE_WORD_STRENGTH'])
        nl()
        help("Number of the most significant words to be used by the filter")
        var("SIGNIFICANT", self['SIGNIFICANT'])
        nl()
        help("Threshold for spam messages")
        var("BAD_THRESHOLD", self['BAD_THRESHOLD'])
        nl()
        help("Width of the uncertain band")
        var("UNCERTAIN", self['UNCERTAIN'])
        nl()
        help("Tag added to the subject of spam messages")
        var("TAG", "'%s'"%self['TAG'])
        nl()
        title("Antivirus settings")
        help("Antivirus programs (complete command lines and regular expressions for virus names)")
        var("ANTIVIRUS", "%s # eg ('f-prot', 'Infection:(.*)', 'clamscan --mbox --disable-summary', ': (.*) FOUND')"%(", ".join(["'%s'"%a for a in self['ANTIVIRUS']]) or "()"))
        nl()
        help("Tag added to the subject of messages containing viruses")
        var("VIRUS_TAG", "'%s'"%self['VIRUS_TAG'])
        nl()
        help("FAST_ANTIVIRUS = True to scan only non spam messages")
        var("FAST_ANTIVIRUS", bool(self['FAST_ANTIVIRUS']))
        nl()
        title("Bypass definition")
        help("Regular expression that let messages in without being filtered")
        var("BYPASS", ", ".join(["r'%s'"%b for b in self['BYPASS']]) or "()")
        nl()
        title("PopF Cleaner")
        help("PopF cleaner connect to POP3 servers and move spams to a local directory")
        help("The cleaner can also optionally forward non spams")
        nl()
        help("Accounts to be cleaned")
        var("CLEANER_ACCOUNTS", ", ".join(["'%s'"%e for e in self['CLEANER_ACCOUNTS']]) or ())
        nl()
        help("Emails to transfer non-spam")
        var("CLEANER_FORWARDS", ", ".join(["'%s'"%e for e in self['CLEANER_FORWARDS']]) or ())
        var("CLEANER_SMTP", "'%s'"%self['CLEANER_SMTP'])
        nl()
        help("Directory where spams are moved to")
        var("CLEANER_DIRECTORY", "'%s'"%self['CLEANER_DIRECTORY'].replace('\\', '\\\\'))
        nl()
        help("Cleaner period in hours")
        var("CLEANER_PERIOD", self['CLEANER_PERIOD'])
        nl()
        title("PopF purge")
        help("PopF purge removes older spams")
        nl()
        help("Purge method")
        help("PURGE = integer: Number of monthes a spam is kept before being purged")
        help("PURGE = float  : spam/ham ratio to keep")
        help("PURGE = None   : no purge")
        var("PURGE", self['PURGE'])
        nl()
        help("Directory where purged spams are saved (if not None)")
        var("PURGE_DIRECTORY", self['PURGE_DIRECTORY'] and "'%s'"%self['PURGE_DIRECTORY'].replace('\\', '\\\\') or None)
        nl()

        config.seek(0)
        return config.read()
config = Config()

def popf_setup(method=None, exhaustion=False):
    if method is not None:
        config.default(method, exhaustion)
    config_data = config.save()
    print config_data
    f = file(config['POPFRC'], 'wt')
    f.write(config_data)
    f.close()
    print "%s created"%config['POPFRC']
    print "You can edit %s if you whish."%config['POPFRC']
    print "Don't forget to run \"%s -gen\" to update your database."%sys.argv[0]
    print

####################################################################
#
# Messages
#
####################################################################

class FileExtractor:
    """ Extracts file names
    """

    def __init__(self, *names):
        self.ignore_extensions = config['IGNORED_EXTENSIONS']
        self.names = names

    def __iter__(self):
        """ recursively generates the file names in a set of directories or files
        """
        stack = list(self.names)
        while stack:
            pattern = stack.pop(0)
            for name in glob.glob(pattern):
                if os.path.isdir(name):
                    stack.append(os.path.join(name, '*'))
                else:
                    # filter non message files
                    file_name, file_ext = os.path.splitext(os.path.basename(name))
                    file_name = file_name.lower()
                    file_ext = file_ext.lower()
                    if file_ext in self.ignore_extensions: continue
                    if file_name.startswith("."): continue

                    yield name

class MessageExtractor:
    """ Extracts messages in files or directories
    """

    def __init__(self, names, excludes=(), age=None):
        self.excludes = excludes
        self.files = FileExtractor(*names)
        self.limit = age and (time.time() - age*24*60*60) or 0

    def __iter__(self):
        """ recursively generates the data of the messages in the files in a set of directories or files
        """

        for name in self.files:
        
            exclude = False
            for exc in self.excludes:
                if name.startswith(exc):
                    exclude = True
            if exclude: continue
            if self.limit and os.stat(name).st_mtime <= self.limit: continue

            f = file(name, 'rt')
            content = f.read().replace("\r", "")
            f.close()

            # Unix mailbox
            if content.startswith("From "):
                msgs = iter(content.split("\n\nFrom "))
                yield msgs.next()
                for msg in msgs:
                    yield "From "+msg

            # MH mailbox
            else:
                yield content

class Message(dict):

    def __init__(self, data):
        dict.__init__(self)

        data = data.replace('\r', '')
        data = unbreak_header(data)
        msg = rfc822.Message(StringIO.StringIO(data))
        self.senders = lowers(seconds(msg.getaddrlist('from') + msg.getaddrlist('reply-to') + msg.getaddrlist('sender')))
        self.recipients = lowers(seconds(msg.getaddrlist('to') + msg.getaddrlist('cc') + msg.getaddrlist('cci') + msg.getaddrlist('bcc')))
        self.subject = msg.getheader('subject')
        self._time = _time(msg.getheader('Received') or msg.getheader('Date'))
        if config['HEADER_FILTER']:
            header = clean_header(data[:msg.startofbody])
            self.update(tokenize(header, header=True))
        if config['BODY_FILTER']:
            body = data[msg.startofbody:]
            content_type = msg.getheader('Content-Type')
            content_transfer_encoding = msg.getheader('Content-Transfer-Encoding')
            encoding = msg.getheader('Encoding')
            self.update(tokenize(body, content_type, content_transfer_encoding, encoding))

    def update(self, tokens):
        for token, n in tokens:
            self[token] = self.get(token, 0) + n

    def __cmp__(self, other):
        return cmp(self._time, other._time)     # test older messages first

VALID_HEADERS = """
    Return-Path
    Delivered-To
    Received
    Message-ID
    From
    Reply-To
    To
    Subject
    Date
    MIME-Version
    Content-Type
    Content-Transfer-Encoding
""".split()
FAKE_HEADER_END_RE = re.compile(r'(\r?\n)+(?=(%s):)'%('|'.join(VALID_HEADERS)), re.IGNORECASE)

def unbreak_header(data):
    while True:
        end_header_match = end_header_re.search(data)
        if not end_header_match: break
        fake_end_match = FAKE_HEADER_END_RE.match(data, end_header_match.start())
        if not fake_end_match: break
        data = data[:fake_end_match.start()] + data[fake_end_match.end():]
    return data

RECEIVED_DATE_RE = re.compile(r"""
    \b
    (?P<day> \d{1,2} )
    \s+
    (?P<month> Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec )
    \s+
    (?P<year> \d{4} )
    \s+
    (?P<hour> \d+ ) : (?P<minute> \d+ ) : (?P<second> \d+ )
    \b
""", re.VERBOSE+re.IGNORECASE)

MONTH_NUMBER = {
    'Jan':  1, 'Feb':  2, 'Mar':  3, 'Apr':  4,
    'May':  5, 'Jun':  6, 'Jul':  7, 'Aug':  8,
    'Sep':  9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

def limits(n, n0, n1): return max(min(n, n1), n0)

def _time(st):
    if st is None:
        return 0 # maybe an attachment
    date = RECEIVED_DATE_RE.search(st)
    if date:
        return time.mktime(
            (   limits(int(date.group('year')), 2000, 2037),
                limits(MONTH_NUMBER[date.group('month')], 1, 12),
                limits(int(date.group('day')), 1, 31),
                limits(int(date.group('hour')), 0, 23),
                limits(int(date.group('minute')), 0, 59),
                limits(int(date.group('second')), 0, 59),
                -1, -1, -1
            )
        )
    return 0

hexa_text_re = re.compile(r"(\?(?:iso-[\d-]*|us-ascii)\?Q\?(.*?)\?=)")
hexa_char_re = re.compile(r"=[0-9a-fA-F]{2}")
X_PopF_re = re.compile(r"^(?:X-PopF|X-Spam).*", re.MULTILINE)
useless_headers = """
Content-ID
Date
In-Reply-To
Message-ID
Posted-Date
References
Sent
Thread-Index
X-UIDL
""".split()
useless_header_re = re.compile(r"^(%s):.*(\n .*)*"%("|".join(useless_headers)), re.IGNORECASE+re.MULTILINE)

# Regexp for multipart boundaries
boundary_re = re.compile(r"""boundary\s*=\s*["']?([^"';\n]+)["']?;?""", re.IGNORECASE)

def clean_header(header):
    """ removes useless information in headers
    """

    # Removes X-PopF-* headers
    header = X_PopF_re.sub("", header)

    # Removes useless headers
    header = useless_header_re.sub("", header)

    # Removes multipart boundaries
    for boundary in boundary_re.findall(header):
        header = header.replace(boundary, "")

    # Cleans hexa chars in header
    for hexatext, text in hexa_text_re.findall(header):
        for c in hexa_char_re.findall(text):
            text = text.replace(c, chr(int(c[1:], 16)))
        text = text.replace("_", " ")
        header = header.replace(hexatext, text)

    return header

def tokenize(data, content_type=None, content_transfer_encoding=None, encoding=None, header=False):
    content_type_lower = lower(content_type or "text/")
    content_transfer_encoding_lower = lower(content_transfer_encoding or "")

    # Decode data

    if encoding:
        # Try to decode that strange Micro$oft encoding
        lines = data.splitlines()
        data = []
        for format in encoding.split(','):
            nb, typ = format.split()
            nb = int(nb)
            typ = typ.lower()
            if typ.startswith('text'):
                piece = lines[:nb]
            else:
                piece = []
            del lines[:nb+1]
            data.extend(piece)
        data = "".join(["%s\n"%line for line in lines])
        for token in _tokenize(data, header=header):
            yield token

    else:

        # Text format:
        #   decodes base64 and quoted-printable messages
        #   removes HTML comments
        if content_type_lower.startswith('text/'):
            if content_transfer_encoding_lower.startswith('base64'):
                data = filter_base64(data)
            elif content_transfer_encoding_lower.startswith('quoted-printable'):
                data = data.decode('quopri')
            if content_type_lower.startswith('text/html'):
                data = clean_html(data)
            for token in _tokenize(data, header=header):
                yield token

        # RFC822 format:
        #   decodes base64 and quoted-printable messages
        #   analyses the decoded message
        elif content_type_lower.startswith('message/rfc822'):
            if content_transfer_encoding_lower.startswith('base64'):
                data = filter_base64(data)
            elif content_transfer_encoding_lower.startswith('quoted-printable'):
                data = data.decode('quopri')
            for token, n in Message(data).iteritems():
                yield token, n

        # Multipart format :
        #   decodes base64 and quoted-printable messages
        #   splits and analyses each part
        elif content_type_lower.startswith('multipart/'):
            if content_transfer_encoding_lower.startswith('base64'):
                data = filter_base64(data)
            elif content_transfer_encoding_lower.startswith('quoted-printable'):
                data = data.decode('quopri')
            boundary = boundary_re.search(content_type)
            if boundary:
                boundary = boundary.group(1).strip()
                boundary = re.compile(r"^-*%s-*$"%re.escape(boundary), re.MULTILINE)
                for msg in boundary.split(data):
                    for token, n in Message(msg.strip()).iteritems():
                        yield token, n

        # Other formats are ignored
        else:
            pass

# Regexp for HTML comments
#HTML_COMMENT_RE = re.compile(r"""<![^>]*>""", re.DOTALL)
HTML_COMMENT_RE = re.compile(r"""<!--.*?-->""", re.DOTALL)
#HTML_COMMENT_RE = re.compile(r"""<!(?:<[^>]+>?|[^<>]+)*>""", re.DOTALL) # also removes <RNDMX[8]> tags in comments
HTML_TAG_RE = re.compile(r"""<\s*/?\s*\w+[^>]*>|<!--.*?-->""", re.DOTALL)       # tag or comment
HTML_TAGS = """
A ABBR ACRONYM ADDRESS APPLET AREA B BASE BASEFONT BDO BIG BLOCKQUOTE BODY BR BUTTON
CAPTION CENTER CITE CODE COL COLGROUP DD DEL DFN DIR DIV DL DT EM FIELDSET FONT FORM FRAME FRAMESET
H1 H2 H3 H4 H5 H6 HEAD HR HTML I IFRAME IMG INPUT INS ISINDEX KBD LABEL LEGEND LI LINK
MAP MENU META NOFRAMES NOSCRIPT OBJECT OL OPTGROUP OPTION P PARAM PRE Q
S SAMP SCRIPT SELECT SMALL SPAN STRIKE STRONG STYLE SUB SUP
TABLE TBODY TD TEXTAREA TFOOT TH THEAD TITLE TR TT U UL VAR
""".split()
#HTML_VALID_TAG_RE = re.compile(r"""<\s*/?\s*(?P<tag>%s)(?P<args>(?:\s+[^>]*)?)>"""%("|".join(HTML_TAGS)), re.IGNORECASE)
HTML_VALID_TAG_RE = re.compile(r"""                 # Adapted from HTMLParser.py
    < \s* /? (?P<tag>%s)                            # tag name
    (?P<args>
        (?: \s+
            (?: [a-zA-Z_][-.:a-zA-Z0-9_]*           # attribute name
                (?: \s* = \s*                       # value indicator
                    (?:     '[^']*'                 # LITA-enclosed value
                    |       "[^"]*"                 # LIT-enclosed value
                    |       [^'">\s]+               # bare value
                    )
                )?
            )
        )*
    )
    \s* >
"""%("|".join(HTML_TAGS)), re.VERBOSE+re.IGNORECASE)

# HTML special characters
HTML_CHARS_RE = re.compile(r"""&[a-zA-Z]+;""")
HTML_CHARS = {
    "&nbsp;":       " ",
    "&cent;":       "�",
    "&pound;":      "�",
    "&yen;":        "�",
    "&acute;":      "�",
    "&Agrave;":     "�",
    "&Aacute;":     "�",
    "&Acirc;":      "�",
    "&Atilde;":     "�",
    "&Auml;":       "�",
    "&Aring;":      "�",
    "&AElig;":      "�",
    "&Ccedil;":     "�",
    "&Egrave;":     "�",
    "&Eacute;":     "�",
    "&Ecirc;":      "�",
    "&Euml;":       "�",
    "&Igrave;":     "�",
    "&Iacute;":     "�",
    "&Icirc;":      "�",
    "&Iuml;":       "�",
    "&Ntilde;":     "�",
    "&Ograve;":     "�",
    "&Oacute;":     "�",
    "&Ocirc;":      "�",
    "&Otilde;":     "�",
    "&Ouml;":       "�",
    "&Oslash;":     "�",
    "&Ugrave;":     "�",
    "&Uacute;":     "�",
    "&Ucirc;":      "�",
    "&Uuml;":       "�",
    "&Yacute;":     "�",
    "&szlig;":      "�",
    "&agrave;":     "�",
    "&aacute;":     "�",
    "&acirc;":      "�",
    "&atilde;":     "�",
    "&auml;":       "�",
    "&aring;":      "�",
    "&aelig;":      "�",
    "&ccedil;":     "�",
    "&egrave;":     "�",
    "&eacute;":     "�",
    "&ecirc;":      "�",
    "&euml;":       "�",
    "&igrave;":     "�",
    "&iacute;":     "�",
    "&icirc;":      "�",
    "&iuml;":       "�",
    "&ntilde;":     "�",
    "&ograve;":     "�",
    "&oacute;":     "�",
    "&ocirc;":      "�",
    "&otilde;":     "�",
    "&ouml;":       "�",
    "&oslash;":     "�",
    "&ugrave;":     "�",
    "&uacute;":     "�",
    "&ucirc;":      "�",
    "&uuml;":       "�",
    "&yacute;":     "�",
    "&yuml;":       "�",
}
HTML_CHARCODES_RE = re.compile(r"""&#\d+;""")

base64_valid_line_re = re.compile(r"^\s*[A-Za-z0-9\+\/]+\s*$")
base64_last_line_re =  re.compile(r"^\s*[A-Za-z0-9\+\/]+=+\s*$")

def filter_base64(data):
    lines = []
    it_lines = iter(data.splitlines())
    # ignoring non base64 lines
    for line in it_lines:
        if not base64_valid_line_re.match(line):
            continue
        lines.append(line+"\n")
        break
    # storing base64 lines
    for line in it_lines:
        if base64_valid_line_re.match(line):
            lines.append(line+"\n")
            continue
        if base64_last_line_re.match(line):
            lines.append(line+"\n")
            break
        break
    base64_data = "".join(lines)
    # if decode fails it can be caused by a fake base64 enconding containing simple text
    return robust(base64_data.decode, 'base64') or data

def clean_html(data):
    """ finds HTML comments and fake tags
    """
    #data = HTML_COMMENT_RE.sub("<html*comment>", data)
    for c in uniq(HTML_CHARS_RE.findall(data)):
        data = data.replace(c, HTML_CHARS.get(c, c))
    for c in uniq(HTML_CHARCODES_RE.findall(data)):
        asc = int(c[2:-1])
        if asc < 256:
            data = data.replace(c, chr(asc))
    for tag in uniq(HTML_TAG_RE.findall(data)):
        match = HTML_VALID_TAG_RE.match(tag)
        if match is None:                   # Invalid tag or comment
            repl = HTML_COMMENT_RE.match(tag) and "comment" or "invalid_tag"
            data = data.replace(tag, "<html*%s>"%repl)
        else:
            tag_name = match.group('tag')
            args = match.group('args')
            data = data.replace(tag, "<html*%s %s>"%(tag_name, args))
    return data

# Domains found here:
# http://www.iso.org/iso/fr/country_codes/iso_3166_code_lists.htm
# http://www.frameip.com/rfc/rfc1591.php
# and Python sources.

domains = """
ac ad ae aero af ag ai al am an ao aq ar arpa as at au aw az
ba bb bd be bf bg bh bi biz bj bm bn bo br bs bt bv bw by bz
ca cat cc cd cf cg ch ci ck cl cm cn co com coop cr cu cv cx
cy cz de dj dk dm do dz ec edu ee eg eh er es et eu fi fj fk
fm fo fr ga gb gd ge gf gg gh gi gl gm gn gov gp gq gr gs gt
gu gw gy hk hm hn hr ht hu id ie il im in info int io iq ir is
it je jm jo jobs jp ke kg kh ki km kn kp kr kw ky kz la lb lc
li lk lr ls lt lu lv ly ma mc md mg mh mil mk ml mm mn mo mobi
mp mq mr ms mt mu museum mv mw mx my mz na name nc ne net nf
ng ni nl no np nr nu nz om org pa pe pf pg ph pk pl pm pn pr
pro ps pt pw py qa re ro ru rw sa sb sc sd se sg sh si sj sk
sl sm sn so sr st su sv sy sz tc td tf tg th tj tk tm tn to tp
tr travel tt tv tw tz ua ug uk um us uy uz va vc ve vg vi vn
vu wf ws ye yt yu za zm zw 
""".split()

_IP = r"\.".join([r"(?: [1-9][0-9]{,2} | 0 )"]*4)
_SERVER = r"""
    (?: (?: [\w\-]+ \. )+ (?:%s)\b      # Server in a valid domain
    |   %s                              # IP
    )
    (?! \. )                            # server name ends here (no more dot)
"""%("|".join(domains), _IP)

URL_RE = re.compile(r"""
    (?P<url>
        (?: \w+:// )?
        (?P<server>
            %s
        )
        (?P<path>
            (?: / [\w\.\-]+ )*
        )
    )
"""%(_SERVER), re.VERBOSE+re.IGNORECASE)

IP_RE = re.compile(r"^%s$"%_IP, re.VERBOSE)

EMAIL_RE = re.compile(r"""
    (?P<email>
        (?P<name>
            [\w\-\@]+ (?: \. [\w\-\@]+ )*
        )
        @
        (?P<server>
            %s
        )
    )
"""%(_SERVER), re.VERBOSE+re.IGNORECASE)

PREPRO_HTML_RE = re.compile(r"<html\*(\w+)([^>]*)>")   # HTML tags preprocessed by clean_html

FILE_RE = re.compile(r"(?:(?:file)?name\s*=\s*)(\"[^\"]*\"|\'[^\']*\'|[\w\.]*\b)")

def _tokenize(data, header=False):
    """ split a string into tokens
    """

    data = lower(data)

    # Extracts emails and URLs

    if header:
        data_files = FILE_RE.findall(data)  # il faut extraire les fichiers avant les URL
        data = FILE_RE.sub(" ", data)       # pour �viter que les fichiers .com soient vus comme des adresses
    else:
        data_files = ()

    data_emails = firsts(EMAIL_RE.findall(data))
    data = EMAIL_RE.sub(" ", data)

    data_urls = firsts(URL_RE.findall(data))
    data = URL_RE.sub(" ", data)

    data_html = PREPRO_HTML_RE.findall(data)
    data = PREPRO_HTML_RE.sub("", data)  # no space because tags are used to split words !

    # Tokens
    return chain(
        _tokens(data),
        _urls(data_urls),
        _emails(data_emails),
        _html_tags(data_html),
        _files(data_files),
    )

TOKEN_RE = config['TOKEN_RE']
NONTOKEN_RE = config['NONTOKEN_RE']

def _tokens(data):
    """ yields each single word from a message
    """
    for token in TOKEN_RE.findall(data):
        if not NONTOKEN_RE.match(token):
            yield (token,), 1

def _urls(data_url):
    """ yields each URL from a message
    URLs yield several tokens (partial path and partial server name)
    URLs are stored in the tokens file prefixed with "url*"
    """
    tag = "url*"
    for url in map(URL_RE.match, data_url):
        server = url.group('server')
        path = url.group('path')

        # Complete URL
        tokens = [tag+server+path]

        # Complete server + partial path
        words = [server] + filter(None, path.split('/'))
        for i in range(len(words)-1, 0, -1):
            tokens.append(tag+"/".join(words[:i]))

        if IP_RE.match(server):

            # The server looks like an IP address
            # Partial server (right truncated)
            words = server.split('.')
            for i in range(len(words)-1, 0, -1):
                tokens.append(tag+".".join(words[:i])+".")

        else:

            # The server is not an IP address
            # Partial server (left truncated)
            words = server.split('.')
            for i in range(1, len(words)):
                tokens.append(tag+"."+".".join(words[i:]))

        # yield the current token set
        yield tuple(tokens), 1

def _emails(data_email):
    """ yields each email from a message
    emails yield several tokens (partial server name)
    emails are stored in the tokens file prefixed with "email*"
    """
    tag = "email*"
    for email in map(EMAIL_RE.match, data_email):
        name = email.group('name')
        server = email.group('server')

        # Complete email
        tokens = [tag+name+"@"+server]

        # Complete server
        tokens.append(tag+"@"+server)

        if IP_RE.match(server):

            # The server looks like an IP address
            # Partial server (right truncated)
            words = server.split('.')
            for i in range(len(words)-1, 0, -1):
                tokens.append(tag+"@"+".".join(words[:i])+".")

        else:

            # The server is not an IP address
            # Partial server (left truncated)
            words = server.split('.')
            for i in range(1, len(words)):
                tokens.append(tag+"@"+"."+".".join(words[i:]))

        # User name
        tokens.append(tag+name+"@")

        # Yield the current token set
        yield tuple(tokens), 1

def _html_tags(data_html):
    """ yields each preprocessed HTML tag from a message
    """
    tag = "html*"
    for html_tag, args in data_html:
        yield (tag+html_tag,), 1
        for token, n in _tokenize(args):
            yield token, n

MULTIPLE_SPACES_RE = re.compile(r'\s{2,}')

def _files(data_files):
    """ yields the file names and extensions from a message
    """
    tag = "file*"
    for name in data_files:
        if name[0] in "\"\'" and name[0] == name[-1]:
            name = name[1:-1]
        name = MULTIPLE_SPACES_RE.sub(' ', name)
        root, ext = os.path.splitext(name)
        if ext:
            yield (tag+name, tag+ext, tag+root+'.'), 1
        else:
            yield (tag+name,), 1

# Regexp to search the end of headers in messages
end_header_re = re.compile(r"^\r?\n", re.MULTILINE)

def tag_header(data, field, value, prepend=False):
    """ add or update a header
    """

    data = unbreak_header(data)
    end_header_match = end_header_re.search(data)

    header = data[:end_header_match.start()]
    body = data[end_header_match.start():]

    # update an existing header
    if prepend:

        field_re = re.compile(r"^(%s):"%field, re.IGNORECASE+re.MULTILINE)
        new_header = field_re.sub(r"\1: %s"%value, header)
        if new_header != header:
            # one or more fields found => return the prepended tags
            return new_header + body
        else:
            # field not found => add a new header
            pass

    # add a new header
    if end_header_match:
        return header + "%s: %s\r\n"%(field, value) + body

    # can not add the header (should not happend)
    debug(1, "Can't add the '%s' header ???"%field)
    return data

####################################################################
#
# Spam filter
#
####################################################################

class Whitelist(dict):

    def __init__(self):
        dict.__init__(self)
        self.roots = lowers(config['WHITELIST'])

    def store(self, msg):
        for x in msg.senders:
            if x in self.roots:
                for y in msg.recipients:
                    self[y] = True
                break

    def clean(self):
        for email in self.roots:
            if email in self:
                del self[email]

    def load(self):
        try:
            debug(1, "Loading white list...")
            f = file(config['WHITELIST_FILE'])
        except (OSError, IOError):
            debug(1, "Can not load the white list")
        else:
            for email in f:
                self[lower(email)] = True
            self.clean()
            debug(1, "Whitelist loaded")

    def save(self):
        if self.roots:
            self.clean()
            emails = self.keys()
            emails.sort()
            f = file(config['WHITELIST_FILE'], 'wt')
            for email in emails:
                print >>f, email
            f.close()

class NullWhitelist(dict):
    def store(self, msg): pass
    def clean(self): pass
    def load(self): pass
    def save(self): pass

class Corpus(dict):

    def __init__(self, whitelist=None):
        dict.__init__(self)
        self.nb = 0
        if whitelist is None:
            whitelist = NullWhitelist()
        self.whitelist = whitelist

    def update(self, msg):
        self.whitelist.store(msg)
        for tokens, freq in msg.iteritems():
            for token in tokens:
                self[token] = self.get(token, 0) + freq
        self.nb += 1

class Computation:
    """ Generic probability computation object
    """

    def __init__(self, filter):
        self.significant = config['SIGNIFICANT'] or sys.maxint
        self.loading = filter.loading
        self.filter = filter

    def __call__(self, msg):
        probs = []
        self.loading.acquire()
        for tokens in msg:
            for token in tokens:
                try:
                    probs.append(self.filter[token])
                    break # only use the first known token (for multiple tokens)
                except KeyError:
                    pass
        self.loading.release()
        probs.sort(lambda x,y: cmp(abs(y-0.5),abs(x-0.5)) or cmp(x,y))
        return self.compute(probs[:self.significant] or [0.5])

class Graham_Computation(Computation):

    def compute(self, probs):
        """ computes the probability of a message being spam (Graham's method)
            P = prod(1-p)
            Q = prod(p)
            S = Q / (P + Q)
        """
        P = reduce(operator.mul, map(lambda p: 1.0-p, probs), 1.0)
        Q = reduce(operator.mul, probs, 1.0)
        return Q / (P + Q)

class Robinson_Computation(Computation):

    def compute(self, probs):
        """ computes the probability of a message being spam (Robinson's method)
            P = 1 - prod(1-p)^(1/n)
            Q = 1 - prod(p)^(1/n)
            S = (1 + (P-Q)/(P+Q)) / 2 = P / (P+Q)
        """
        nth = 1./len(probs)
        P = 1.0 - reduce(operator.mul, map(lambda p: 1.0-p, probs), 1.0) ** nth
        Q = 1.0 - reduce(operator.mul, probs, 1.0) ** nth
        return P / (P + Q)

class Robinson_Fisher_Computation(Computation):

    def compute(self, probs):
        """ computes the probability of a message being spam (Robinson-Fisher's method)
            H = C-1( -2.ln(prod(p)), 2*n )
            S = C-1( -2.ln(prod(1-p)), 2*n )
            I = (1 + H - S) / 2
        """
        n = len(probs)
        try: H = chi2P(-2.0 * math.log(reduce(operator.mul, probs, 1.0)), 2*n)
        except (OverflowError, ValueError): H = 0.0
        try: S = chi2P(-2.0 * math.log(reduce(operator.mul, map(lambda p: 1.0-p, probs), 1.0)), 2*n)
        except (OverflowError, ValueError): S = 0.0
        return (1 + H - S) / 2

def chi2P(chi, df):
    """ return P(chisq >= chi, with df degre of freedom)

    df must be even
    """
    assert df & 1 == 0
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df/2):
        term *= m/i
        sum += term
    return min(sum, 1.0)

multiple_slash_r = re.compile(r"\r\r+")

class Filter(dict):
    """ filters messages
    self.whitelist : whitelist associated to the filter
    self.good_corpus : pathes of the messages accepted by the user
    self.bad_corpus : pathes of the messages rejected by the user
    """

    COMPUTATION = {
        "Graham": Graham_Computation,
        "Robinson": Robinson_Computation,
        "Robinson-Fisher": Robinson_Fisher_Computation,
    }

    def __init__(self):
        dict.__init__(self)
        self.loading = threading.Lock()
        self.last_load = None
        self.whitelist = Whitelist()
        self.good_corpus = Corpus(self.whitelist)
        self.bad_corpus = Corpus()
        try:
            computation_class = self.COMPUTATION[config['METHOD']]
        except KeyError:
            methods = self.COMPUTATION.keys()
            methods.sort()
            error("METHOD is incorrect. Accepted values are: %s"%", ".join(methods))
        self.computation = computation_class(self)

    def update_probabilities(self, msg=None):
        """ merges good and bad corpora and computes probabilities
        """
        freq_thr = config['FREQUENCY_THRESHOLD']
        s = config['RARE_WORD_STRENGTH']
        x = config['UNKNOWN_PROB']
        prob_thr = config['PROBABILITY_THRESHOLD']
        good_bias = config['GOOD_BIAS']
        bad_bias = config['BAD_BIAS']
        good_prob = config['GOOD_PROB']
        bad_prob = config['BAD_PROB']
        ngood = self.good_corpus.nb
        nbad = self.bad_corpus.nb
        if ngood > 0 and nbad > 0:
            if msg is None:
                tokens = chain(self.good_corpus, self.bad_corpus)
            else:
                tokens = chain(*msg.iterkeys())
            for token in tokens:
                g = good_bias * self.good_corpus.get(token, 0)
                b = bad_bias * self.bad_corpus.get(token, 0)
                n = g + b
                if n >= freq_thr:
                    goodMetric = min(1.0, g/ngood)
                    badMetric = min(1.0, b/nbad)
                    p = badMetric / (goodMetric + badMetric)
                    f = (s*x + n*p) / (s + n)
                    if abs(f-0.5) >= prob_thr:
                        self[token] = max(good_prob, min(bad_prob, f))

    def clear_probabilities(self, msg):
        for token in chain(*msg.iterkeys()):
            try:
                del self[token]
            except KeyError:
                pass

    def save(self):
        token_file = config['TOKEN_FILE']
        pairs = [ (prob, token) for (token, prob) in self.iteritems() ]
        pairs.sort()
        tmp = "%s.tmp"%token_file
        f = file(tmp, 'wt')
        for prob, token in pairs:
            print >>f, prob, token
        f.close()
        self.whitelist.save()
        if sys.platform.startswith('win'):
            try:
                os.remove(token_file)
            except WindowsError:
                pass
        os.rename(tmp, token_file)

    class Loader(threading.Thread):
        """ Probability loader
        works in background
        """

        def __init__(self, parent):
            threading.Thread.__init__(self, name="Probability Loader")
            self.parent = parent

        def run(self):
            """ load precomputed probabilities
            """
            try:
                debug(1, "Loading probabilities...")
                f = file(config['TOKEN_FILE'], 'rt')
            except IOError:
                debug(1, "Can not load probabilities")
            else:
                self.parent.clear()
                for l in f:
                    prob, token = l.strip().split(" ", 1)
                    self.parent[token] = float(prob)
                f.close()
                debug(1, "Probabilities loaded")
                self.parent.whitelist.load()
            self.parent.loading.release()

    def load(self):
        self.loading.acquire()
        try:
            current = os.stat(config['TOKEN_FILE']).st_mtime
        except OSError:
            self.loading.release()
        else:
            if current > self.last_load:
                self.last_load = current
                Filter.Loader(self).start()
            else:
                self.loading.release()

    def reload(self):
        if config['AUTORELOAD']:
            self.load()

    def compute(self, msg):
        return self.computation(msg)

    def __call__(self, data):
        """ analyses messages and tags spams.
        Returns the tagged (or not) message.
        """

        bad_thr = config['BAD_THRESHOLD']
        uncertain = config['UNCERTAIN']
        tag = config['TAG']

        # some spams have two \r to break headers so added headers are
        # ignored (X-PopF-Spam for example).
        data = multiple_slash_r.sub('\r', data)

        msg = Message(data)

        # get the spam probability
        prob = self.compute(msg)

        # if the sender is in the white list, PopF accepts the message
        for email in msg.senders:
            if email in self.whitelist:
                print "ok   (%s is in the white list)"%email, msg.subject
                return data

        # if bypass matches the message, PopF also accepts it
        for bypass_re in config['BYPASS_RE']:
            if bypass_re.search(data):
                print "ok   (bypass)", msg.subject
                return data

        # the sender is unknown
        if prob > bad_thr + uncertain:
            print "SPAM (%5.3f)"%prob, msg.subject

            # It's a spam! We add a X-PopF-Spam tag.
            data = tag_header(data, 'X-PopF-Spam', 'Spam Level %5.3f'%prob)

            # and a X-Spam-Flag tag for gnubiff
            data = tag_header(data, 'X-Spam-Flag', 'YES')

            # We also tag the subject.
            if tag:
                data = tag_header(data, 'Subject', tag, prepend=True)

        elif prob >= bad_thr - uncertain:
            # Uncertain for this message. We don't touch the message
            # TODO: should we tag this message? How?
            print "ok ? (%5.3f)"%prob, msg.subject

        else:
            # It's no spam. We don't touch the message
            print "ok   (%5.3f)"%prob, msg.subject

        return data

def popf_gen():
    print ABOUT_POPF
    _gen()

def _gen():
    print "Generatig statistics"

    start = time.time()

    class SmallMessage:
        """ hold the same information as Message but reduce memory usage
        """

        cache = {}      # cache for objects that are equal

        def __init__(self, data):
            msg = Message(data)
            self.senders = msg.senders
            self.recipients = msg.recipients
            self._time = msg._time
            # keep only one instance of each token
            # to reduce the memory usage
            tokens = []
            for ts, f in msg.items():
                try:
                    ts = SmallMessage.cache[ts]
                except KeyError:
                    SmallMessage.cache[ts] = ts
                tokens.append((ts, f))
            # Tokens are stored as a tuple of pairs instead of a dictionnary
            self.tokens = tuple(tokens)

        def __iter__(self):
            for tokens, freq in self.tokens:
                yield tokens
        def iteritems(self):
            for tokens, freq in self.tokens:
                yield tokens, freq
        def iterkeys(self):
            for tokens, freq in self.tokens:
                yield tokens
        def __cmp__(self, other):
            return cmp(self._time, other._time)     # test older messages first

    def mem():
        for l in file('/proc/%s/status'%os.getpid()):
            if l.startswith('VmData:'):
                return l.split(':', 1)[1].strip()
        else:
            return "Memory usage unknown"

    if config['TRAINING_TO_EXHAUSTION']:

        f = Filter()

        def messages(corpus, is_spam, exclude, info):
            msgs = []
            for data in MessageExtractor(corpus, exclude):
                msg = SmallMessage(data)
                if not is_spam:
                    f.good_corpus.whitelist.store(msg)
                msg.is_spam = is_spam
                del msg.senders
                del msg.recipients
                msgs.append(msg)
                print info%len(msgs), '\r',
                sys.stdout.flush()
            print
            return msgs

        def mix(L1, L2):
            L = []
            n1 = n2 = 0
            N1, N2 = len(L1), len(L2)
            while n1 < N1 and n2 < N2:
                if (2*n1+1)*N2 <= (2*n2+1)*N1:
                    L.append(L1[n1])
                    n1 += 1
                else:
                    L.append(L2[n2])
                    n2 += 1
            L.extend(L1[n1:])
            L.extend(L2[n2:])
            return L


        ham  = messages(config['GOOD_CORPUS'], False, config['BAD_CORPUS'], "Reading good corpus: %6d messages")
        spam = messages(config['BAD_CORPUS'],  True,  (),                   "Reading bad corpus : %6d messages")
        SmallMessage.cache.clear()

        nb_ham = len(ham)
        nb_spam = len(spam)
        nb_messages = nb_ham + nb_spam

        #ham.sort()
        #spam.sort()
        #msgs = mix(ham, spam)
        msgs=ham+spam
        msgs.sort()
        del ham
        del spam

        f.good_corpus.whitelist = NullWhitelist()
        f.bad_corpus.whitelist = NullWhitelist()

        config['BYPASS'] = config['BYPASS_RE'] = () # learn without bypass

        ham_limit = config['TRAINING_TO_EXHAUSTION_GOOD_LIMIT']
        spam_limit = config['TRAINING_TO_EXHAUSTION_BAD_LIMIT']

        total_err = 0
        min_err = sys.maxint
        min_errors = []
        best_f = {}

        # Taille du process
        if DEBUG_LEVEL>=1: debug(1, "Memory usage: %s"%mem())

        for iteration in xrange(1, config['TRAINING_TO_EXHAUSTION_MAX_ITERATION'] or sys.maxint):
            info = "Iteration %d: %%d/%d messages / %%d errors"%(iteration, len(msgs))

            nb_err = 0
            errors = []

            for i, msg in enumerate(msgs):
                p = f.compute(msg)

                if msg.is_spam:
                    if p <= spam_limit:
                        nb_err += 1
                        errors.append(i)
                        f.clear_probabilities(msg)
                        f.bad_corpus.update(msg)
                        f.update_probabilities(msg)
                else:
                    if p >= ham_limit:
                        nb_err += 1
                        errors.append(i)
                        f.clear_probabilities(msg)
                        f.good_corpus.update(msg)
                        f.update_probabilities(msg)

                print info%(i+1, nb_err), "\r",
                sys.stdout.flush()

            total_err += nb_err

            print

            if nb_err < min_err:

                # Found a better filter
                best_f.clear()
                best_f.update(f)
                min_err = nb_err
                min_errors = errors

                if nb_err == 0:
                    # It won't be better!
                    break

#            #elif nb_err == min_err:
            elif errors == min_errors:
                # The filter seems to be stable now, go back to the previous filter
                break

        # Save the best filter found
        if nb_err > 0:
            f.clear()
            f.update(best_f)

        # Taille du process
        if DEBUG_LEVEL>=1: debug(1, "Memory usage: %s"%mem())

        print "Done in %d iterations (%d/%d messages used)"%(iteration, total_err, nb_messages)
        for i in xrange(len(msgs)):
            del msgs[0]

        # Taille du process
        if DEBUG_LEVEL>=1: debug(1, "Memory usage: %s"%mem())

    else:

        f = Filter()
        for ham in MessageExtractor(config['GOOD_CORPUS'], config['BAD_CORPUS']):
            f.good_corpus.update(Message(ham))
            print "Reading good corpus: %6d messages\r"%f.good_corpus.nb,
            sys.stdout.flush()
        print
        for spam in MessageExtractor(config['BAD_CORPUS']):
            f.bad_corpus.update(Message(spam))
            print "Reading bad corpus : %6d messages\r"%f.bad_corpus.nb,
            sys.stdout.flush()
        print

        # Taille du process
        if DEBUG_LEVEL>=1: debug(1, "Memory usage: %s"%mem())

        print "Computing probabilities"
        f.update_probabilities()
        nb_messages = f.good_corpus.nb + f.bad_corpus.nb

        # Taille du process
        if DEBUG_LEVEL>=1: debug(1, "Memory usage: %s"%mem())

    print "Saving %d tokens"%len(f)
    f.save()

    stop = time.time()
    print "Speed: %d messages/hour"%(nb_messages/(stop-start)*60*60)

    # Taille du process
    if DEBUG_LEVEL>=1: debug(1, "Memory usage: %s"%mem())

#####################################################################
#
# Virus scanner
#
#####################################################################

class AntiVirus:
    """ Interface to a virus scanner
    """

##    WARNING = r"""
##Hello
##
##This message is automatically generated by PopF (a spam filter) to
##warn you that a virus has been sent from your computer. It may be
##wiser to use an antivirus software to protect you.
##
##Date: %(date)s
##Virus sent: %(virus)s
##
##Best regards,
##PopF
##
##===========================================================
##
##Bonjour
##
##Ce message a �t� g�n�r� automatiquement par PopF (filtre de spam)
##pour vous avertir qu'un virus a �t� envoy� depuis votre ordinateur.
##Il serait plus sage d'utiliser un logiciel antivirus pour vous
##prot�ger.
##
##Date : %(date)s
##Virus envoy� : %(virus)s
##
##Cordialement,
##PopF
##
##"""

    def __init__(self):
        programs = config['ANTIVIRUS']
        self.programs = []
        for program, virus_re in [programs[i:i+2] for i in range(0, len(programs), 2)]:
            self.programs.append((program, re.compile(virus_re, re.MULTILINE)))
        self.tag = config['VIRUS_TAG']
        self.fast_antivirus = config['FAST_ANTIVIRUS']
##        self.smtp_server = self['ANTIVIRUS_SMTP_SERVER']
##        self.smtp_user = self['ANTIVIRUS_SMTP_USER']
##        self.smtp_password = self['ANTIVIRUS_SMTP_PASSWORD']

    def scan(self, data):
        """ Scans a message and returns the names of the virus
        found in the message.
        """
        for program, virus_re in self.programs:
            tmp = tempfile.mktemp('-popf')
            f = file(tmp, "w")
            f.write(data)
            f.close()
            _in, _out, _err = os.popen3("%s %s"%(program, tmp))
            _in.close()
            result = _out.read()+"\n"+_err.read()
            _out.close()
            _err.close()
            os.remove(tmp)
            virus_found = [v.strip() for v in virus_re.findall(result)]
            if virus_found:
                return ", ".join(uniq(virus_found))
        return ""

    def __call__(self, data):
        if self.fast_antivirus and is_spam_re.search(data):
            return data
        virus = self.scan(data)
        if virus:
            print "Virus found: %s"%virus
            data = tag_header(data, 'X-PopF-Virus', virus)
            if self.tag:
                data = tag_header(data, 'Subject', self.tag, prepend=True)
##            # Send a warning to the sender
##            if self.smtp_server:
##                msg = Message(data)
##                senders = msg.senders
##                recipients = msg.recipients
##                date = msg.getheader('date')
##                server = smtplib.SMTP(self.smtp_server)
##                if self.smtp_user or self.smtp_password:
##                    server.login(self.smtp_user, self.smtp_password)
##                print "Sending a warning from %s to %s"%(", ".join(recipients), ", ".join(senders))
##                server.sendmail(", ".join(recipients), senders, self.WARNING%{'virus':virus, 'date':date})
##                server.quit()
        return data

#####################################################################
#
# POP3 proxy
#
#####################################################################

CRLF = '\r\n'
CRLF_DOT_CRLF = CRLF + '.' + CRLF

# reject chars < 32 (except \r and \n)
illegal_char_re = re.compile(r"[\000-\011\013\014\016-\037]")

class Reply:
    """ POP3 reply (+OK or -ERR)
    ok : True or False
    comment : optional list of strings
    """

    def __init__(self, ok, *comment):
        self.ok = operator.truth(ok)
        self.err = not self.ok
        self.comment = comment

    def __str__(self):
        return (self.ok and "+OK %s" or "-ERR %s")%" ".join(map(str, self.comment))

class Socket:
    """ POP3 socket
    """

    class FakeSocket:
        """ Simulate a not connected socket

        Does nothing and always replies with an error.
        """
        def send(self, *args): pass
        def sendall(self, *args): pass
        def recv(self, *args): return "-ERR PopF Socket Error"
        def close(self): pass

    class BufferedSocket:
        """ Put the POP3 data following the first line in a buffer
        """

        def __init__(self, family, type):
            self.socket = socket.socket(family, type)
            self.data_buffer = ""
            self.connect = self.socket.connect
            self.send = self.socket.send
            self.sendall = self.socket.sendall
            self.close = self.socket.close

        def settimeout(self, timeout):
            if hasattr(self.socket, "settimeout"):
                self.socket.settimeout(timeout)

        def recv(self, size=1024):
            data = self.socket.recv(size)
            data = illegal_char_re.sub(" ", data)
            try:
                data_pos = data.index('\n')
            except ValueError:
                self.data_buffer = ""
                return data
            else:
                self.data_buffer = data[data_pos+1:]
                return data[:data_pos].strip()

        def recv_data(self, size=4096):
            data = [self.data_buffer]
            end = (CRLF + self.data_buffer)[-5:]
            self.data_buffer = ""
            while end != CRLF_DOT_CRLF:
                r = self.socket.recv(size)
                r = illegal_char_re.sub(" ", r)
                data.append(r)
                end = (end+r[-5:])[-5:]
            return "".join(data)

    def __init__(self, socket=None):
        if socket is None: socket = Socket.FakeSocket()
        self.s = socket
        self.settimeout(config['TIMEOUT'])

    def __del__(self):
        self.close()

    def settimeout(self, timeout):
        if hasattr(self.s, "settimeout"):
            self.s.settimeout(timeout)

    def connect(self, host, port):
        """ connects to host:port

        If connection fails, uses a FakeSocket
        """
        self.s = Socket.BufferedSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.settimeout(config['TIMEOUT'])
        try: self.s.connect((host, port))
        except socket.error:
            self.s = Socket.FakeSocket()
            return Reply(False, "Connection error")
        return self.get_reply()

    def close(self):
        if self.s is not None:
            self.s.close()
            self.s = Socket.FakeSocket()

    def send(self, cmd, *args):
        """ sends a POP3 command
        """
        args = " ".join(map(str, args))
        if args:
            self.s.sendall("%s %s%s"%(cmd, args, CRLF))
        else:
            self.s.sendall("%s%s"%(cmd, CRLF))

    def send_data(self, data):
        """ sends POP3 data """
        self.s.sendall(data)

    def recv(self):
        """ receives a POP3 reply
        """
        data = self.s.recv(1024)
        if data.endswith(CRLF): data = data[:-len(CRLF)]
        return data

    def recv_data(self):
        """ receives the data following a POP3 reply """
        return self.s.recv_data()

    def get_reply(self):
        """ receives and parses a POP3 reply
        """
        r = self.recv()
        try: res, arg = r.split(' ', 1)
        except ValueError: res, arg = r, ''
        return Reply(res.upper()=='+OK', arg)

    def reply(self, r, data=None):
        """ sends a POP3 reply
        """
        self.send(str(r))
        if data is not None: self.send_data(data)

    def cmd_user(self, name):
        """ POP3 "USER name" command """
        self.send("USER", name)
        return self.get_reply()

    def cmd_pass(self, pass_):
        """ POP3 "PASS password" command """
        self.send("PASS", pass_)
        return self.get_reply()

    def cmd_quit(self):
        """ POP3 "QUIT" command """
        self.send("QUIT")
        return self.get_reply()

    def cmd_stat(self):
        """ POP3 "STAT" command """
        self.send("STAT")
        return self.get_reply()

    def cmd_list(self, msg):
        """ POP3 "LIST [msg]" command """
        self.send("LIST", msg)
        reply = self.get_reply()
        data = None
        if reply.ok and not msg: data = self.recv_data()
        return reply, data

    def cmd_retr(self, msg):
        """ POP3 "RETR [msg]" command """
        self.send("RETR", msg)
        reply = self.get_reply()
        data = None
        if reply.ok: data = self.recv_data()
        return reply, data

    def cmd_dele(self, msg):
        """ POP3 "DELE" command """
        self.send("DELE", msg)
        return self.get_reply()

    def cmd_noop(self):
        """ POP3 "NOOP" command """
        self.send("NOOP")
        return self.get_reply()

    def cmd_rset(self):
        """ POP3 "RSET" command """
        self.send("RSET")
        return self.get_reply()

    def cmd_top(self, msg):
        """ POP3 "TOP msg" command """
        self.send("TOP", msg)
        reply = self.get_reply()
        data = None
        if reply.ok: data = self.recv_data()
        return reply, data

    def cmd_uidl(self, msg):
        """ POP3 "UIDL [msg]" command """
        self.send("UIDL", msg)
        reply = self.get_reply()
        data = None
        if reply.ok and not msg: data = self.recv_data()
        return reply, data

    def cmd_capa(self):
        """ POP3 "CAPA" command """
        self.send("CAPA")
        reply = self.get_reply()
        data = None
        if reply.ok: data = self.recv_data()
        return reply, data

class CloseConnectionException(Exception):
    """ Thrown when the connection is closed """
    pass

# Regexp for PASS POP3 command
password_re = re.compile(r"^PASS .*", re.IGNORECASE)

class Session(threading.Thread):
    """ POP3 session

    Intercepts POP3 commands from an email client and filters incomming messages from the server.
    """

    log_lock = threading.Lock()

    def __init__(self, proxy, client, addr, spam_filter, virus_scanner):
        threading.Thread.__init__(self)
        self.proxy = proxy
        self.name = self.getName()
        self.spam_filter = spam_filter
        self.virus_scanner = virus_scanner
        self.server = Socket()
        self.client = Socket(client)
        self.log("#"*30)
        self.log("###", time.asctime())
        self.log("#"*30)
        self.log("Connection from", addr)
        self.client.reply(Reply(True, "PopF ready"))
        self.spam_filter.reload()

    def log(self, *args):
        Session.log_lock.acquire()
        msg = " ".join(map(str, args))
        for line in msg.splitlines():
            print "%s: %s"%(self.name, line)
        Session.log_lock.release()

    def run(self):
        pop3_cmd = {
            'USER': self.cmd_user,
            'PASS': self.cmd_pass,
            'QUIT': self.cmd_quit,
            'STAT': self.cmd_stat,
            'LIST': self.cmd_list,
            'RETR': self.cmd_retr,
            'DELE': self.cmd_dele,
            'NOOP': self.cmd_noop,
            'RSET': self.cmd_rset,
            'TOP' : self.cmd_top,
            'UIDL': self.cmd_uidl,
            'CAPA': self.cmd_capa,
            'KILL': self.cmd_kill,
        }
        try:
            void_cmd = 0
            while True:
                try:
                    cmd = self.client.recv()
                except socket.timeout:
                    # The client doesn't send commands
                    self.log("< Client timeout")
                    raise
                cmd = cmd.strip()
                if cmd:
                    void_cmd = 0
                else:
                    void_cmd += 1
                    if void_cmd < 100:
                        continue
                    else:
                        self.log("Socket seems to be closed (identification problem?)")
                        raise socket.error
                self.log("<", password_re.sub("PASS ...", cmd))     # hide the password in the log file
                try: cmd, arg = cmd.split(' ', 1)
                except ValueError: arg = ''
                try: cmd = pop3_cmd[cmd.upper()]
                except KeyError:
                    r = Reply(False, "Unimplemented command:", cmd)
                    self.log(">", r)
                    try:
                        self.client.reply(r)
                    except socket.timeout:
                        # The client isn't waiting for this reply ???
                        self.log("> Client timeout")
                        raise
                else:
                    try:
                        cmd(arg)
                    except socket.timeout:
                        # The server (or less likely the client) doesn't reply
                        self.log("<> Server or client timeout")
                        raise
        except (CloseConnectionException, socket.error), e:
            self.server.close()
            self.client.close()

        self.log("Connection closed")

    identification_re = re.compile(r"^(?P<user>.+)@(?P<host>.+)(:(?P<port>\d+))?$")

    def cmd_user(self, name):
        """ USER name@host[:port]
        """
        identification = Session.identification_re.match(name)
        if identification:
            name = identification.group('user')
            host = identification.group('host')
            port = int(identification.group('port') or 110)
            self.server = Socket()
            r = self.server.connect(host, port)         # we know the POP3 server and connect to it
            if r.ok:                                    # connection OK
                r = self.server.cmd_user(name)              # we send the USER command
        else:
            r = Reply(False, "Erreur d'identification POP3 (%s)"%name)
        self.log(">", r)
        self.client.reply(r)

    def cmd_pass(self, pass_):
        """ PASS password """
        r = self.server.cmd_pass(pass_)
        self.log(">", r)
        self.client.reply(r)

    def cmd_quit(self, nu):
        """ QUIT """
        r = self.server.cmd_quit()
        self.log(">", r)
        self.client.reply(r)
        raise CloseConnectionException()            # tells PopF to stop the session

    def cmd_stat(self, nu):
        """ STAT """
        r = self.server.cmd_stat()
        self.log(">", r)
        self.client.reply(r)

    def cmd_list(self, msg):
        """ LIST msg """
        r, d = self.server.cmd_list(msg)
        self.log(">", r)
        if d is not None: self.log(d)
        self.client.reply(r, d)

    def cmd_retr(self, msg):
        """ RETR msg """
        r, d = self.server.cmd_retr(msg)
        self.log(">", r)
        if r.ok:

###            if DEBUG_LEVEL >= 1:
###                # On sauve le mail pour pouvoir le comparer avec
###                # le mail enregistre par le client
###                tmp_dir = '/tmp/popf_debug'
###                try: os.mkdir(tmp_dir)
###                except OSError: pass
###                tmp = 1
###                for x in os.listdir(tmp_dir):
###                    try:
###                        tmp = max(tmp, int(x)+1)
###                    except ValueError:
###                        pass
###                tmp = os.path.join(tmp_dir, str(tmp))
###                debug(1, "Message saved in %s"%tmp)
###                f = file(tmp, "w")
###                f.write(d)
###                f.close()

            d = self.spam_filter(d)         # filter the message
            d = self.virus_scanner(d)       # scan for viruses

        self.client.reply(r, d)

    def cmd_dele(self, msg):
        """ DELE msg """
        r = self.server.cmd_dele(msg)
        self.log(">", r)
        self.client.reply(r)

    def cmd_noop(self, nu):
        """ NOOP """
        r = self.server.cmd_noop()
        self.log(">", r)
        self.client.reply(r)

    def cmd_rset(self, nu):
        """ RSET """
        r = self.server.cmd_rset()
        self.log(">", r)
        self.client.reply(r)

    def cmd_top(self, msg):
        """ TOP msg """
        r, d = self.server.cmd_top(msg)
        self.log(">", r)
        if r.ok:
            d = self.spam_filter(d)         # filter the message
        self.client.reply(r, d)

    def cmd_uidl(self, msg):
        """ UIDL [msg] """
        r, d = self.server.cmd_uidl(msg)
        self.log(">", r)
        if d is not None: self.log(d)
        self.client.reply(r, d)

    def cmd_capa(self, nu):
        """ CAPA """
        r, d = self.server.cmd_capa()
        self.log(">", r)
        self.client.reply(r, d)

    def cmd_kill(self, nu):
        """ KILL (this command is PopF specific) """
        self.proxy.socket.close()
        while True: os.kill(os.getpid(), 9)     # should not return

class Proxy:
    """ POP3 proxy

    Intercepts POP3 connection requests and launch a POP3 session in a thread
    """

    def __init__(self):
        self.host = config['HOST']
        self.port = config['PORT']
        self.socket = Socket()

    def __del__(self):
        self.socket.close()

    def serve(self):
        """ serves POP3 connection requests """

        print "Starting PopF proxy"

        spam_filter = Filter()
        spam_filter.load()
        virus_scanner = AntiVirus()

        print "Waiting for connections"

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        while True:
            client, addr = self.socket.accept()
            session = Session(self, client, addr, spam_filter, virus_scanner)
            session.start()

def popf_proxy():
    """ run the POP3 proxy """
    print ABOUT_POPF
    start_log()
    while True:
        try:
            if _kill_proxy():
                print "Running PopF proxy killed"
            proxy = Proxy()
            proxy.serve()
        except socket.error:
            traceback.print_exc()
        print "Proxy has been closed, waiting 10 seconds..."
        time.sleep(10)

#def _kill_proxy():
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    try:
#        s.connect((config['HOST'], config['PORT']))
#    except socket.error:
#        return False
#    else:
#        s.sendall("KILL%s"%CRLF)
#        s.close()
#        return True

def _kill_proxy():
    """ try to kill other PopF servers

    up to 10 tries.
    """
    killed = False
    for i in range(10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((config['HOST'], config['PORT']))
        except socket.error:
            # no (more) active PopF server
            break
        else:
            s.sendall("KILL%s"%CRLF)
            s.close()
            time.sleep(1)
            # we've kill one PopF server
            killed = True
    else:
        # Impossible to kill running servers ???
        killed = False
    return killed

def popf_kill():
    """ kills the running POP3 proxy """
    print ABOUT_POPF
    print "Killing PopF proxy"
    if _kill_proxy():
        print "PopF proxy killed"
    else:
        print "PopF proxy is not running"

####################################################################
#
# Testing
#
####################################################################

def popf_test(*names):
    """ tests the filter against files """
    print ABOUT_POPF
    if not names: names = ['.']
    spam_filter = Filter()
    spam_filter.load()
    spam_filter.whitelist = NullWhitelist()     # test with an empty whitelist
    config['BYPASS'] = config['BYPASS_RE'] = () # test without bypass
    for data in MessageExtractor(names):
        spam_filter(data)

#####################################################################
#
# Purge
#
#####################################################################

def popf_purge():
    """ purges BAD_CORPUS """

    print ABOUT_POPF

    purge = config['PURGE']
    if not purge:
        error("Option disabled.")

    purge_dir = config['PURGE_DIRECTORY']
    if purge_dir and not os.path.isdir(purge_dir):
        error("PURGE_DIRECTORY (%s) is not a valid directory."%purge_dir)

    if purge_dir:
        storage_name = 1
        for x in os.listdir(purge_dir):
            try:
                storage_name = max(storage_name, int(x)+1)
            except ValueError:
                pass

    if type(purge) == int:

        # select spams older than PURGE monthes
        limit = time.time() - purge * 365.2422/12. * 24 * 60 * 60
        spams = list(FileExtractor(*config['BAD_CORPUS']))
        old_spams = [name for name in spams if os.stat(name).st_mtime < limit]

    elif type(purge) == float:

        # select oldest spams such that the spam/ham ratio is at most PURGE
        hams = list(FileExtractor(*config['GOOD_CORPUS']))
        spams = list(FileExtractor(*config['BAD_CORPUS']))
        old_spams = sorted(spams, key=lambda name: os.stat(name).st_mtime)
        old_spams = old_spams[:-int(purge*len(hams))]

    else:
        error("PURGE must be an integer or a floating point value.")

    if purge_dir:
        for name in old_spams:
            dest_name = os.path.join(purge_dir, str(storage_name))
            print "Moving %s to %s "%(name, dest_name)
            os.rename(name, os.path.join(purge_dir, dest_name))
            storage_name += 1
    else:
        for name in old_spams:
            print "Deleting %s"%name
            os.remove(name)

    print "Data base contained %s files"%(len(spams))
    if purge_dir:
        print "%s old files have been moved to %s"%(len(old_spams), purge_dir)
    else:
        print "%s old files have been removed"%len(old_spams)
    print "%s files have been kept"%(len(spams)-len(old_spams))

#####################################################################
#
# Check
#
#####################################################################

def _check_config(filter):
    cfg = """\
METHOD                           : %(METHOD)s
BAD_THRESHOLD                    : %(BAD_THRESHOLD)8s   UNCERTAIN                           : %(UNCERTAIN)8s
GOOD_PROB                        : %(GOOD_PROB)8s   GOOD_BIAS                           : %(GOOD_BIAS)8s
BAD_PROB                         : %(BAD_PROB)8s   BAD_BIAS                            : %(BAD_BIAS)8s
PROBABILITY_THRESHOLD            : %(PROBABILITY_THRESHOLD)8s   FREQUENCY_THRESHOLD                 : %(FREQUENCY_THRESHOLD)8s
UNKNOWN_PROB                     : %(UNKNOWN_PROB)8s   RARE_WORD_STRENGTH                  : %(RARE_WORD_STRENGTH)8s
SIGNIFICANT                      : %(SIGNIFICANT)8s
"""%config
    if config['TRAINING_TO_EXHAUSTION']:
        cfg += """\
TRAINING_TO_EXHAUSTION           : %(TRAINING_TO_EXHAUSTION)8s   TRAINING_TO_EXHAUSTION_MAX_ITERATION: %(TRAINING_TO_EXHAUSTION_MAX_ITERATION)8s
TRAINING_TO_EXHAUSTION_GOOD_LIMIT: %(TRAINING_TO_EXHAUSTION_GOOD_LIMIT)8s   TRAINING_TO_EXHAUSTION_BAD_LIMIT    : %(TRAINING_TO_EXHAUSTION_BAD_LIMIT)8s
"""%config
    filter.loading.acquire()
    if filter:
        cfg += """\
Tokens in the database           : %8s
"""%(len(filter))
    filter.loading.release()
    return cfg

def _check_table(tab):
    table = ""
    cols = [max(map(len, c))+2 for c in zip(*filter(None, tab))]
    width = sum(cols) + len(cols) + 1
    for l in tab:
        if l is None:
            table += "-"*width + "\n"
        else:
            table += "|%s|"%"|".join([x.center(w) for (x,w) in zip(l,cols)]) + "\n"
    return table

def _check(listing=None):
    """ checks good and bad corpora """

    bad_thr = config['BAD_THRESHOLD']
    uncertain = config['UNCERTAIN']
    good_corpus = config['GOOD_CORPUS']
    bad_corpus = config['BAD_CORPUS']

    spam_filter = Filter()
    spam_filter.load()
    spam_filter.whitelist = NullWhitelist()     # test with an empty whitelist

    def check_corpus(name, corpus, info):
        total = OK = ok = ko = KO = 0
        for data in MessageExtractor(corpus, name=="HAM" and config['BAD_CORPUS'] or ()):
            msg = Message(data)
            prob = spam_filter.compute(msg)

            if name=="SPAM" and prob < bad_thr - uncertain:
                debug(2, "################ False negative ###################################")
                debug(2, data)
                debug(2, "###################################################################")
            if bad_thr - uncertain <= prob <= bad_thr + uncertain:
                debug(2, "################ Uncertain ########################################")
                debug(2, data)
                debug(2, "###################################################################")
            if name=="HAM" and prob > bad_thr + uncertain:
                debug(2, "################ False positive ###################################")
                debug(2, data)
                debug(2, "###################################################################")

            total += 1
            if uncertain == 0:
                if prob <= bad_thr: OK += 1
                else: KO += 1
            else:
                if prob < bad_thr - uncertain: OK += 1
                elif prob <= bad_thr: ok += 1
                elif prob <= bad_thr + uncertain: ko += 1
                else: KO += 1
            if listing is not None:
                stats.append((prob, name, msg.senders, msg.subject))

            print info%total, "\r",
            sys.stdout.flush()

        print

        l1 = [name, str(total)]
        l2 = ["", ""]
        for n in uncertain==0 and (OK+ok, KO+ko) or (OK, ok, ko, KO):
            if n:
                l1.append(str(n))
                l2.append("%6.2f %%"%(100.*n/total))
            else:
                l1.append("")
                l2.append("")
        if name == 'SPAM':
            efficiency = 100. * (KO) / total
        else:
            efficiency = 100. * (OK+ok+ko) / total
        l2[0] = "==> %6.2f %%"%efficiency
        return [l1, l2]

    def clean(st):
        st = illegal_char_re.sub(" ", repr(st))
        for ch in '\n\r,\'\"':
            st = st.replace(ch, '')
        return st

    stats = []
    tab = []
    tab.append(None)
    b, B, t = bad_thr-uncertain, bad_thr+uncertain, bad_thr
    if uncertain > 0:
        tab.append(["PopF v%s"%__version__, "Total", "[0.000, %5.3f["%b, "[%5.3f, %5.3f]"%(b, t), "]%5.3f, %5.3f]"%(t, B), "]%5.3f, 1.000["%B])
    else:
        tab.append(["PopF v%s"%__version__, "Total", "[0.000, %5.3f]"%t, "]%5.3f, 1.000["%t])
    tab.append(None)
    # good corpus
    tab.extend(check_corpus("HAM", good_corpus, "Checking good corpus: %6d messages"))
    tab.append(None)
    # bas corpus
    tab.extend(check_corpus("SPAM", bad_corpus, "Checking bad corpus : %6d messages"))
    tab.append(None)

    # Listing
    if listing is not None:
        stats.sort()
        lst = StringIO.StringIO()
        for prob, spam, senders, subject in stats:
            print >>lst, ",".join([repr(prob), spam, clean("; ".join(senders)), clean(subject)])
        lst.seek(0)
        lst = lst.read()
    else:
        lst = ""

    # Global statistics
    return _check_table(tab)+_check_config(spam_filter), lst

def popf_check(listing=None):
    """ checks good and bad corpora """

    print ABOUT_POPF

    tab, lst = _check(listing=listing)

    if listing is not None:
        print "Saving listing to", listing
        f = file(listing, 'wt')
        f.write(lst)
        f.close()

    print tab

def _efficiency(age=None):
    nb_ham = {None: 0}
    nb_tagged_ham = {None: 0}
    nb_spam = {None: 0}
    nb_tagged_spam = {None: 0}

    for nb, nb_tagged, corpus, exclude in ( (nb_ham,  nb_tagged_ham,  config['GOOD_CORPUS'], config['BAD_CORPUS']),
                                            (nb_spam, nb_tagged_spam, config['BAD_CORPUS'],  ()),
                                          ):
        for msg in MessageExtractor(corpus, exclude, age=age):
            end_header = end_header_re.search(msg)
            if end_header:
                header = msg[:end_header.start()]
            else:
                header = msg
            nb[None] += 1
            if is_spam_re.search(header):
                nb_tagged[None] += 1

    def eff(n, N):
        try:
            e = 100.*n/N
        except ZeroDivisionError:
            e = 0.0
        return "%4.2f%%"%e

    tab = [None]

    tab.append(["HAM", "Hams received", "Hams not tagged", "Hams tagged", "Actual efficiency"])
    tab.append(None)
    tab.append(["PopF's filter", str(nb_ham[None]),
                                 str(nb_ham[None]-nb_tagged_ham[None]),
                                 str(nb_tagged_ham[None]),
                                 eff(nb_ham[None]-nb_tagged_ham[None], nb_ham[None]) ])
    tab.append(None)

    tab.append(["SPAM", "Spams received", "Spams not tagged", "Spams tagged", "Actual efficiency"])
    tab.append(None)
    tab.append(["PopF's filter", str(nb_spam[None]),
                                 str(nb_spam[None]-nb_tagged_spam[None]),
                                 str(nb_tagged_spam[None]),
                                 eff(nb_tagged_spam[None], nb_spam[None]) ])
    tab.append(None)

    spam_filter = Filter()
    spam_filter.load()

    stats = age and "During the last %d days:\n"%age or ""
    stats += _check_table(tab)+_check_config(spam_filter)
    return stats

def popf_efficiency(age=None):
    """ counts the number of tagged spams in the bad corpus

    This is a better measure of the "real" efficiency of the filter
    """

    print ABOUT_POPF

    tab = _efficiency(age and float(age))

    print tab

####################################################################
#
# Statistics
#
####################################################################

def popf_stat(output=None):

    global config

    print ABOUT_POPF

    # Temporary PopF's home
    tmp_home = tempfile.mktemp('-popf')
    try: os.mkdir(tmp_home)
    except OSError: pass

    methods = Config.DEFAULT.keys()
    methods.sort()
    for method in methods:
        config = Config()
        config.default(method)
        config['HOME'] = os.path.join(tmp_home)
        config['POPFRC'] = os.path.join(tmp_home, 'popfrc')
        config['TOKEN_FILE'] = os.path.join(tmp_home, 'tokens')
        config['WHITELIST_FILE'] = os.path.join(tmp_home, 'whitelist')
        config['WHITELIST'] = ()
        _gen()
        tab, lst = _check()
        print tab
        if output is not None:
            output_name = output
            output_name = output_name.replace('%m', config['METHOD'])
            output_name = output_name.replace('%e', str(config['TRAINING_TO_EXHAUSTION']))
            f = file(output_name, 'wt')
            f.write(tab)
            f.close()
        #os.remove(config['POPFRC'])
        os.remove(config['TOKEN_FILE'])
        #os.remove(config['WHITELIST_FILE'])

    os.removedirs(tmp_home)

    # Actual efficiency
    config = Config()
    tab = _efficiency()
    print tab
    if output is not None:
        output_name = output
        output_name = output_name.replace('%m', 'actual')
        output_name = output_name.replace('%e', str(config['TRAINING_TO_EXHAUSTION']))
        f = file(output_name, 'wt')
        f.write(tab)
        f.close()

#####################################################################
#
# Cleaner
#
#####################################################################

account_re = re.compile(r"^(?P<user>.+?):(?P<password>.+)@(?P<host>.+)(:(?P<port>\d+))?$")
uidl_re = re.compile(r"(\d+)\s+(.+)")
is_spam_re = re.compile(r"^X-PopF-Spam: ", re.MULTILINE)
is_virus_re = re.compile(r"^X-PopF-Virus: ", re.MULTILINE)

def popf_clean():
    """ removes spams from POP3 accounts and forwards non spam"""

    print ABOUT_POPF

    cleaner_dir = config['CLEANER_DIRECTORY']
    if not os.path.isdir(cleaner_dir):
        error("CLEANER_DIRECTORY is no valid directory ('%s')"%cleaner_dir)

    accounts = config['CLEANER_ACCOUNTS']
    if not accounts:
        error("CLEANER_ACCOUNTS is empty")

    forwards = config['CLEANER_FORWARDS']

    spam_filter = Filter()
    virus_filter = AntiVirus()

    #_kill_proxy()
    start_log()

    _seen = {}
    _seen_file = os.path.join(config['HOME'], 'popf.seen')

    def see(id):
        _seen[id] = True
        f = file(_seen_file, "wt")
        f.write(repr(_seen))
        f.close()

    def seen(id):
        return id in _seen

    while True:

        print "#"*30
        print "###", time.asctime()
        print "#"*30

        try:
            _seen = eval(file(_seen_file).read())
        except IOError:
            pass

        spam_filter.load()

        for account in accounts:

            acc = account_re.match(account)
            if acc is None:
                error("Syntax error in CLEANER_ACCOUNTS (%s)"%account)
            user = acc.group('user')
            password = acc.group('password')
            host = acc.group('host')
            port = int(acc.group('port') or 110)

            print "Cleaning %s on %s"%(user, host)

            try:

                print "Connecting..."
                s = Socket()
                r = s.connect(host, port)
                print ">", r
                if not r.ok:
                    print "Cannot connect to %s:%s"%(host, port)
                    break

                print "< USER %s"%user
                r = s.cmd_user(user)
                print ">", r
                if not r.ok:
                    s.cmd_quit()
                    break

                print "< PASS ..."
                r = s.cmd_pass(password)
                print ">", r
                if not r.ok:
                    s.cmd_quit()
                    break

                print "< UIDL"
                r, d = s.cmd_uidl("")
                print ">", r
                if not r.ok:
                    s.cmd_quit()
                    break
                print d

                for n, id in uidl_re.findall(d):
                    if seen(id): continue

                    print "< RETR", n
                    r, d = s.cmd_retr(n)
                    print ">", r
                    if not r.ok:
                        continue

                    d = spam_filter(d)
                    d = virus_filter(d)

                    end_header = end_header_re.search(d)
                    if end_header:
                        h = d[:end_header.start()]
                    else:
                        h = d

                    if is_spam_re.search(h) or is_virus_re.search(h):

                        storage_name = 1
                        for x in os.listdir(cleaner_dir):
                            try:
                                storage_name = max(storage_name, int(x)+1)
                            except ValueError:
                                pass
                        storage_name = os.path.join(cleaner_dir, str(storage_name))

                        print "Moving to", storage_name
                        f = file(storage_name, "w")
                        f.write(d)
                        f.close()

                        print "< DELE", n
                        r = s.cmd_dele(n)
                        print ">", r

                    else: # not a spam => to be forwarded
                    
                        if forwards:
                            print "Forwarding"
                            try:
                                smtp = smtplib.SMTP(config['CLEANER_SMTP'])
                            except socket.error, e:
                                print "Error", e
                            else:
                                try:
                                    errors = smtp.sendmail("PopF", forwards, d)
                                    if not errors:
                                        see(id)
                                except smtplib.Error, e:
                                    print "Error", e
                                smtp.quit()
                        else:
                            see(id)

                print "< QUIT"
                r = s.cmd_quit()
                print ">", r

            except socket.timeout:

                print "Timeout error. Closing connection"

            s.close()

        period = config['CLEANER_PERIOD']
        if period:
            print "waiting %s hour%s before next cleaning..."%(period, period>1 and "s" or "")
            try:
                time.sleep(period*60*60)
            except KeyboardInterrupt:
                print "Cleaner aborted"
                break
        else:
            # No period => cleaner just run once
            break

####################################################################
#
# Main
#
####################################################################

if __name__ == "__main__":
    available_functions = {
        '-help'         : (0, 0,    popf_help),
        '-changelog'    : (0, 0,    popf_changelog),
        '-license'      : (0, 0,    popf_license),
        '-version'      : (0, 0,    popf_version),
        '-sha'          : (0, 0,    popf_sha),
        '-setup'        : (0, 2,    popf_setup),
        '-gen'          : (0, 0,    popf_gen),
        '-test'         : (0, None, popf_test),
        '-check'        : (0, 1,    popf_check),
        '-proxy'        : (0, 0,    popf_proxy),
        '-kill'         : (0, 0,    popf_kill),
        '-stat'         : (0, 1,    popf_stat),
        '-clean'        : (0, 0,    popf_clean),
        '-purge'        : (0, 0,    popf_purge),
        '-efficiency'   : (0, 1,    popf_efficiency),
    }
    class PopFArgumentError(Exception): pass
    try:
        args = sys.argv[1:]
        try:
            cmd = args.pop(0)
            m, M, f = available_functions[cmd]
        except (IndexError, KeyError):
            raise PopFArgumentError
        if m is not None and len(args) < m: raise PopFArgumentError
        if M is not None and len(args) > M: raise PopFArgumentError
        command_line = args
        args = []
        kw = {}
        for arg in command_line:
            if '=' in arg:
                name, value = arg.split('=', 1)
                kw[name] = value
            else:
                args.append(arg)
        f(*args, **kw)
    except PopFArgumentError:
        popf_help()

