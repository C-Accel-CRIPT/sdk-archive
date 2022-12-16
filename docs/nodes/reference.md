# Reference

## Definition
The reference node contains the metadata for a literature publication, book, or anything external
to CRIPT. The reference node does not contain the base attributes. 

The reference node is always used inside the citation sub-object to enable users to 
specify the context of the reference.

!!! warning "Reference will always be public"
    Reference node is meant to always be public and static to allow globally link data to the reference

## Can be added to:
* [citation](../subobjects/citation.md)

## Attributes


| Attribute | Type      | Example                                                                                                                                      | Description                                   | Required    |
|-----------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|-------------|
| url       | str       | [https://criptapp.org/reference/99dde595-2bf3-4ff6-9658-8dfa9ae0e7ef/](https://criptapp.org/reference/99dde595-2bf3-4ff6-9658-8dfa9ae0e7ef/) | CRIPT’s unique ID of the node                 | True        |
| type      | str       | "journal_article"                                                                                                                            | type of literature                            | True        |
| title     | str       | "Living Polymers"                                                                                                                            | title of publication                          | True        |
| authors   | list[str] | "Michael Szwarc",                                                                                                                            | list of authors                               |             |
| journal   | str       | "Nature"                                                                                                                                     | journal of the publication                    |             |
| publisher | str       | "Springer"                                                                                                                                   | publisher of publication                      |             |
| year      | int       | 1956                                                                                                                                         | year of publication                           |             |
| volume    | int       | 178                                                                                                                                          | volume of publication                         |             |
| issue     | int       | 0                                                                                                                                            | issue of publication                          |             |
| pages     | list[int] | [1168, 1169]                                                                                                                                 | page range of publication                     |             |
| doi       | str       | "10.1038/1781168a0"                                                                                                                          | DOI: digital object identifier                | Conditional |
| issn      | str       | "1476-4687"                                                                                                                                  | ISSN: international standard serial number    | Conditional |
| arxiv_id  | str       | "1501"                                                                                                                                       | arXiv identifier                              |             |
| pmid      | int       | ########                                                                                                                                     | PMID: PubMed ID                               |             |
| website   | str       | "[https://www.nahttp://www.nature.com/artic](https://www.nahttp://www.nature.com/artic)"                                                     | website where the publication can be accessed |             |


!!! note "Conditional"
    Some attributes can be required depending on the [reference type](https://criptapp.org/keys)
    
    **Example:** journal articles require DOI




## Reference Object
```json
{
    "url": "https://criptapp.org/api/reference/99dde595-2bf3-4ff6-9658-8dfa9ae0e7ef/",
    "uid": "99dde595-2bf3-4ff6-9658-8dfa9ae0e7ef",
    "group": "https://criptapp.org/api/group/665f3ae5-0880-46cb-b8ff-62d03bc8f0d2/",
    "title": "Ref1",
    "authors": [
        "Brad"
    ],
    "journal": "journal",
    "publisher": "o'reilly media",
    "year": 2022,
    "volume": 11,
    "issue": 943,
    "pages": [],
    "doi": "doi:/1",
    "issn": "test",
    "arxiv_id": "test",
    "pmid": 1,
    "website": "https://www.google.com/",
    "notes": null,
    "public": false,
    "created_at": "2022-09-20T22:49:09.167420Z",
    "updated_at": "2022-10-06T19:43:18.450721Z"
}
```

## Create
```python

```
## Save
```python

```

!!! warning
    **Reference nodes cannot be deleted once they are saved**

    Please be sure everything with the node is fine before saving them

## Get
```python

```
