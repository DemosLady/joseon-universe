joseon-universe.com
===================

Everything in this zip goes in the root of your site folder, keeping
the folder structure exactly as it is here.

    D:\AI\CODE\learning-curve-auto\JOSEON\


WHAT IS IN HERE
---------------

    index.html                  Korean home
    story.html                  Korean summary
    characters.html             14 characters
    timeline.html               17 events, six hundred years
    ledger.html                 the paper through nine hands
    search.html                 all 2,012 lines, searchable
    tistory_ch1..ch6.html       chapters 1 to 6
    chapter7/8/9.html           chapters 7 to 9
    lyrics-ch1..ch9.html        all 36 songs, Korean and English

    en/                         the same 15 pages in English

    book/
      joseon-stories.pdf        English edition, 147 pages
      joseon-stories-kr.pdf     Korean edition, 93 pages

    sitemap.xml                 41 urls, both books included
    robots.txt                  Google, Naver Yeti, Daum
    .nojekyll                   stops hosts stripping folders


WHAT IS NOT IN HERE
-------------------

The images. They only exist on your machine, so copy these folders
into the same place, untouched:

    art/
      hero.jpg                  the panorama behind every page
      mark.png                  the seal, and the favicon

    covers/
      ch1.jpg ... ch9.jpg       nine album covers

    portraits/
      king.png        yeoni.png       yunje.png
      talswe.png      jeongan.png     buni.png
      buni_young.png  sugyeom.png     baeswe.png
      gapsu.png       oki.png         smith.png
      soldier.png     farmer.png      granddaughter.png

Fifteen portraits, nine covers, two art files. If one is missing the
page still works — you just get an empty box where the picture was.


AFTER YOU PUBLISH
-----------------

    joseon-universe.com/book/joseon-stories-kr.pdf     should download
    joseon-universe.com/book/joseon-stories.pdf        should download
    joseon-universe.com/robots.txt                     should show text
    joseon-universe.com/sitemap.xml                    should show xml

Then resubmit the sitemap in Google Search Console and in Naver
Search Advisor — it has two new urls in it.


ONE THING TO CHECK IN .gitignore
--------------------------------

If it contains a blanket rule for pdf files, the books will not be
published. Add an exception:

    !book/*.pdf
