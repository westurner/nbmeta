###########
nbmeta
###########
| Src: https://github.com/westurner/nbmeta/


Features
===========
- [ ] Add metadata with schema.org classes and properties: Thing(name=, author=, url=)
- [ ] Add metadata about the whole JupyterNotebook to be displayed at the top (as RDFa HTML and/or JSON-LD)
- [ ] Add metadata by emitting structured data nodes from a notebook cell (as RDFa HTML and/or JSON-LD)


Project
==========

- Issue #1:
  https://github.com/westurner/nbmeta/issues/1

- Initial API:
 
  https://github.com/westurner/nbmeta/blob/develop/nb/nbmeta-00-01__exploration.py

  https://github.com/westurner/nbmeta/blob/develop/nb/nbmeta-00-01__exploration.ipynb
  
  https://nbviewer.jupyter.org/github/westurner/nbmeta/blob/develop/nb/nbmeta-00-01__exploration.ipynb
  
  
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

Design Requirements
======================
- Define ``class Meta()`` such that the schema can be passed through to/as:

  - [ ] CSVW
  - Data Libraries:
  
    - [ ] SQLAlchemy
    - [ ] tablib
    - [ ] numpy
    - [ ] Pandas
    - [ ] xray
    - [ ] arrow
    
  - Data Validation, HTML/JS Forms:
  
    - [ ] JSONSchema: http://json-schema.org/documentation.html
    - [ ] SHACL: https://www.w3.org/TR/shacl
    - [ ] colander: https://github.com/Pylons/colander
    - [ ] marshmallow: https://github.com/marshmallow-code/marshmallow
    - [ ] {...}
    - [ ] strypes: https://github.com/westurner/strypes
    


