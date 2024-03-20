---
title: Introduction to AI Cloud 
subtitle: Slurm and Singularity Training
date: March 2023
theme: AAUsimple
aspectratio: 169
header-includes: |
  ```{=latex}
  \author[TARI]{Thomas Arildsen}

  \institute[CLAAUDIA]{CLAAUDIA, Aalborg University}

  \usepackage{hyperref}
  \hypersetup{
    colorlinks = true,
    % menucolor = false,
    % backref=true,
    % pagebackref=true,
    % hyperindex=true,
    % breaklinks=true,
    linkcolor=,
    urlcolor=blue,
    bookmarks=true,
    bookmarksopen=false
  }
  % add bookmark level 2 for PDF
  % from https://tex.stackexchange.com/questions/17230/beamer-how-to-make-each-frame-appear-in-the-pdf-toc
  \usepackage{graphicx}
  \usepackage{amsmath}
  \usepackage{minted}
  % \usepackage[dvipsnames]{xcolor}  
  \AtBeginSection{\begin{frame}{\ }\tableofcontents[currentsection]\end{frame}}
  
  \usepackage{bookmark}
  \usepackage{etoolbox}
  \makeatletter
  % save the current definition of \beamer@@frametitle
  \let\nobookmarkbeamer@@frametitle\beamer@@frametitle
  % then patch it to do the bookmarks and/or TOC entries
  % \apptocmd{\beamer@@frametitle}{%
  \apptocmd{\beamer@@frametitle}{%
  \only<1>{\bookmark[page=\the\c@page,level=3]{#1}}
  }%
  {\message{** patching of \string\beamer@@frametitle succeeded **}}%
  {\message{** patching of \string\beamer@@frametitle failed **}}%

  \pretocmd{\beamer@checknoslide}{%
    % ensure the bookmark is not created if the slide is filtered out
    \let\beamer@@frametitle\nobookmarkbeamer@@frametitle
    }%
    {\message{** patching of \string\beamer@checknoslide succeeded **}}%
    {\errmessage{** patching of \string\beamer@checknoslide failed **}}%
  
  \makeatother
  ```
output:
  beamer_presentation
---

## Outline

\tableofcontents
