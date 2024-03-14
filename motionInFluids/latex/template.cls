\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

%--------------------------------------------------------------------------------------
%	PACKAGES
%--------------------------------------------------------------------------------------

\usepackage{listings}
\usepackage{float}
\usepackage{siunitx}
\usepackage{physics}
\usepackage{amsmath}
\usepackage{enumitem} % Required for list customization
\usepackage{subfigure}
\usepackage[font=small,labelfont=bf]{caption}
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=black,
  citecolor=black
}

\setlist{partopsep=0pt, topsep=0pt} % Customize spacing around and inside lists

\setlength{\parindent}{0pt} % Suppress paragraph indentation

\usepackage{graphicx} % Required for including images
\graphicspath{{../figures}{./}} % Specifies where to look for included images (trailing slash required)


%--------------------------------------------------------------------------------------
%	MARGINS
%--------------------------------------------------------------------------------------

\usepackage[
	top=4.25cm, % Top margin
	bottom=4cm, % Bottom margin
	left=3cm, % Left margin
	right=3cm, % Right margin
	% showframe % Uncomment to show frames around the margins for debugging purposes
]{geometry}

%--------------------------------------------------------------------------------------
%	FONTS
%--------------------------------------------------------------------------------------

\usepackage[T1]{fontenc} % Output font encoding for international characters
\usepackage[utf8]{inputenc} % Required for inputting international characters

\usepackage[scale=0.96]{XCharter} % Use the XCharter text font
\usepackage[xcharter]{newtxmath} % Set the math font


% -- Defining colors:
\usepackage[dvipsnames]{xcolor}
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{python}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codepurple},
    keywordstyle=\color{NavyBlue},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize\bfseries,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=t,
    keepspaces=true,
    numbers=left,
    numbersep=5pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2
}

\lstset{style=python}
\renewcommand{\lstlistingname}{Function}