#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# based on answer by scanny on Jul 16, 2019 at 18:00
# in https://stackoverflow.com/questions/57057474/read-in-powerpoint-theme-colours-in-python-pptx
# 
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn  # ---makes qualified name---

# ---access the theme part---
prs = Presentation("Presentation1.pptx") # based on "PPT figtree 240110.potx"
presentation_part = prs.part
theme_part = presentation_part.part_related_by(RT.THEME)

# ---access theme XML from part---
theme_xml = theme_part.blob
print(theme_xml) # ---should look like example above, just longer---

# ---parse XML---
theme_element = parse_xml(theme_xml)

# ---find color elements---
# color_elements = theme_element.xpath(".//%s/child::*" % qn("a:clrScheme"))
color_elements = theme_element.xpath(".//a:clrScheme/child::*")
print(len(color_elements)  # ---should be 12, of which you care about 6---
for e in color_elements:
    print(e.tag)
    print(e[0].get("val"))
      
