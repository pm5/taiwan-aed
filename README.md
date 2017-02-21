
衛生福利部公共場所 AED 急救資訊網
=================================

<http://tw-aed.mohw.gov.tw/SearchPlace.jsp?Action=Search&City=&Area=&Type=&PlaceType=&Key=&intPage=260>

Usage
-----

```
$ bin/get-html      # saves HTML in tmp/
$ bin/get-data      # extracts JSON in data/
$ bin/publish-data  # publish JSON in data/ to remote data branch
```

Notes
-----

* items that return error:
  - 2610 at [page 105](http://tw-aed.mohw.gov.tw/SearchPlace.jsp?Action=Search&City=&Area=&Type=&PlaceType=&Key=&intPage=105)
  - 2790 at [page 113](http://tw-aed.mohw.gov.tw/SearchPlace.jsp?Action=Search&City=&Area=&Type=&PlaceType=&Key=&intPage=113)
  - 5924 at [page 252](http://tw-aed.mohw.gov.tw/SearchPlace.jsp?Action=Search&City=&Area=&Type=&PlaceType=&Key=&intPage=252)
  - 7643 at [page 324](http://tw-aed.mohw.gov.tw/SearchPlace.jsp?Action=Search&City=&Area=&Type=&PlaceType=&Key=&intPage=252)
  - 8500 at [page 360](http://tw-aed.mohw.gov.tw/SearchPlace.jsp?Action=Search&City=&Area=&Type=&PlaceType=&Key=&intPage=360)
* obviously wrong:
  - [680](http://tw-aed.mohw.gov.tw/ShowPlace.jsp?PlaceID=680) location

To do
-----

* Define a better JSON format and generate `data.json` containing all items.
