###########
nbmeta
###########

- Issue #1:
  https://github.com/westurner/nbmeta/issues/1

- Initial API:
  https://github.com/westurner/nbmeta/blob/develop/nb/nbmeta-00-01__exploration.ipynb
  
API
=====

- [x] Meta
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
- [x] CodeBlock(Node)
- [ ] Include(Node)('../README.rst')
- [ ] Figure(Node)(obj=plot, data=data, meta={author:, title:})
- [ ] Environment(
- [ ] SoftwareEnvironment "SE" ( https://schema.org/SoftwareApplication Software- )
- [ ] PipRequirements(SE)(txt='../requirements-2.txt'))
- [ ] PipFreeze(SE)(PipRequirements)
- [ ] Pipfile(SE)(pipfile='../Pipfile')
- [ ] PipfileLock(SE)(?='../Pipfile.lock')
- [ ] CondaEnvironment(yml='../environment.yml')
