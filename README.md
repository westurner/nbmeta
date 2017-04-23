
"""

Check these off when there are tests:

- [ ] Node
  - [ ] ``@type=Union[URI, List[URI]]``  # JSONLD
  - [ ] type()
  - [ ] types() -> types_expanded()
  - [ ] children=[]
  - [ ] _repr_html_
  - [ ] __repr__
  - [ ] __unicode__
  - [ ] __iter__
    yield node; yield node.children

- [ ] Thing(Node)
  - [ ] name
  - [ ] description
  - [ ] url
- [ ] CreativeWork(Thing)
  - [ ] author
- [ ] ScholarlyArticle(CreativeWork)
- [ ] JupyterNotebook(CreativeWork, [ScholarlyArticle?]  )
- [ ] CodeBlock(Node)
- [ ] Include(Node)('../README.rst')
- [ ] Figure(Node)(obj=plot, data=data, meta={author:, title:})

- [ ] Environment(
- [ ] SoftwareEnvironment "SE" ( https://schema.org/SoftwareApplication Software- )
- [ ] PipRequirements(SE)(txt='../requirements-2.txt'))
- [ ] PipFreeze(SE)(PipRequirements)
- [ ] Pipfile(SE)(pipfile='../Pipfile')
- [ ] PipfileLock(SE)(?='../Pipfile.lock')

- [ ] CondaEnvironment(yml='../environment.yml')

```
this_notebook = TODO_GET_HERE()
base URI
 XHTML
 HTML5
https://schema.org/mainEntityOfPage
<>
```
