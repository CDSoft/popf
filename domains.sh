# #!/bin/bash

RFC1591="http://www.frameip.com/rfc/rfc1591.php"
ISO3166="http://www.iso.org/iso/fr/list-en1-semic-3.txt"

#rm $ISO3166
#wget $ISO3166
(   cat $(basename $ISO3166) |
        grep -v "(;)"        |
        grep ";"             |
        sed 's/.*; *//'

    echo "co ac com edu org net"
    echo "gov mil int aero biz cat coop"
    echo "info jobs mobi museum name pro"
    echo "travel eu"

    echo "ac ad ae aero af ag ai al am an ao aq ar arpa as at au aw az ba bb bd"
    echo "be bf bg bh bi biz bj bm bn bo br bs bt bv bw by bz ca cc cd cf cg ch"
    echo "ci ck cl cm cn co com coop cr cu cv cx cy cz de dj dk dm do dz ec edu"
    echo "ee eg eh er es et fi fj fk fm fo fr ga gb gd ge gf gg gh gi gl gm gn"
    echo "gov gp gq gr gs gt gu gw gy hk hm hn hr ht hu id ie il im in info int"
    echo "io iq ir is it je jm jo jp ke kg kh ki km kn kp kr kw ky kz la lb lc"
    echo "li lk lr ls lt lu lv ly ma mc md mg mh mil mk ml mm mn mo mp mq mr ms"
    echo "mt mu museum mv mw mx my mz na name nc ne net nf ng ni nl no np nr nu"
    echo "nz om org pa pe pf pg ph pk pl pm pn pr pro ps pt pw py qa re ro ru rw"
    echo "sa sb sc sd se sg sh si sj sk sl sm sn so sr st su sv sy sz tc td tf"
    echo "tg th tj tk tm tn to tp tr tt tv tw tz ua ug uk um us uy uz va vc ve"
    echo "vg vi vn vu wf ws ye yt yu za zm zw"

) | tr A-Z a-z |
tr " " "\n" | sort -u | tr "\n" " " |
sed "s/\(.\{60\}\) /\1;/g" | tr ";" "\n"

