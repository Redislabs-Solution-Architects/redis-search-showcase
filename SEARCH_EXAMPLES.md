# Redis Search Examples

Copy and paste these examples into the search prompt when running `python3 src/search.py`

## Basic Text Search

Search for movies by title or plot content:
```
idx:movies "star wars"
idx:movies "space adventure"
idx:movies "love story"
idx:movies "batman"
```

## Field-Specific Search

Search within specific fields using @ syntax:
```
idx:movies @title:"future"
idx:movies @plot:"time travel"
idx:movies @genre:{Action}
idx:movies @genre:{Comedy}
```

## Numeric Range Queries

Filter by ratings and years:
```
idx:movies @rating:[8 10]
idx:movies @rating:[9 10]
idx:movies @release_year:[2010 2020]
idx:movies @release_year:[1990 2000]
```

## Combined Queries

Mix text search with filters (note: combined queries need proper syntax):
```
idx:movies "superhero @rating:[7 10]"
idx:movies "@genre:{Action} @rating:[8 10]"
idx:movies "@genre:{Drama} @release_year:[2000 2020]"
idx:movies "war @release_year:[1990 2000] @rating:[8 10]"
```

## Sorting Results

Sort by rating or year:
```
idx:movies @genre:{Action} SORTBY rating DESC
idx:movies @genre:{Comedy} SORTBY rating DESC LIMIT 0 10
idx:movies "*" SORTBY release_year DESC LIMIT 0 20
idx:movies @rating:[8 10] SORTBY release_year ASC
```

## Wildcard and All Documents

Get all movies or use wildcards:
```
idx:movies "*" LIMIT 0 5
idx:movies "star*"
idx:movies "@title:star*"
idx:movies "@title:the*"
```

## Fuzzy Search (if supported)

Note: Fuzzy syntax varies by module. Try these variations:
```
idx:actors "%ryan%"
idx:actors "ryan~1"
idx:movies "%interstellar%"
```

## Complex Queries

Advanced search combinations:
```
idx:movies "@genre:{Action|Adventure} @rating:[7 10]"
idx:movies "james bond @release_year:[1990 2020]" SORTBY rating DESC
idx:movies "@genre:{Drama} -war @rating:[8 10]"
```

## Actor Searches

Search the actors index:
```
idx:actors "harrison"
idx:actors "tom"
idx:actors @last_name:"ford"
idx:actors @first_name:"brad"
idx:actors "*" LIMIT 0 10
idx:actors @date_of_birth:[1960 1980] SORTBY date_of_birth DESC
```

## Return Specific Fields

Limit which fields are returned:
```
idx:movies "star wars" RETURN 3 title rating release_year
idx:movies @genre:{Action} RETURN 2 title rating LIMIT 0 5
idx:actors "harrison" RETURN 2 first_name last_name
```

## Count Only

Get just the count without results:
```
idx:movies "*" LIMIT 0 0
idx:movies @genre:{Action} LIMIT 0 0
idx:movies @rating:[9 10] LIMIT 0 0
```