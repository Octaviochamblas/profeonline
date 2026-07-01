import os
import re

for p in range(1, 14):
    file_path = f"C:\\Users\\PC\\Documents\\Proyectos\\Web\\profeonline\\scratch\\b0309_pair_{p}.py"
    if not os.path.exists(file_path): continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace LaTeX commands with double backslashes to avoid python unicode/escape errors
    # We replace \\ with \\\\ first? No, just replace known ones.
    latex_cmds = [
        "infty", "le", "leq", "ge", "geq", "cup", "cap", "in", "subset", "subseteq", "supset", "supseteq",
        "mathbb", "mathcal", "mathrm", "mathbf", "mathit", "mathsf", "mathtt", "mathfrak",
        "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta", "vartheta",
        "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "varpi", "rho", "varrho", "sigma", "varsigma",
        "tau", "upsilon", "phi", "varphi", "chi", "psi", "omega",
        "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Upsilon", "Phi", "Psi", "Omega",
        "sum", "prod", "int", "oint", "sqrt", "frac", "lim", "to", "rightarrow", "leftarrow", "Rightarrow", "Leftarrow",
        "cdot", "times", "div", "pm", "mp", "neq", "equiv", "approx", "sim", "cong",
        "forall", "exists", "nexists", "emptyset", "nabla", "partial", "circ", "angle", "triangle",
        "sin", "cos", "tan", "csc", "sec", "cot", "arcsin", "arccos", "arctan",
        "log", "ln", "exp", "max", "min", "sup", "inf", "det", "dim", "ker", "deg", "arg",
        "hat", "bar", "vec", "dot", "ddot", "tilde", "breve", "check", "acute", "grave",
        "lbrace", "rbrace", "langle", "rangle", "lfloor", "rfloor", "lceil", "rceil",
        "|", "!", ",", ":", ";", " ", "quad", "qquad"
    ]

    for cmd in latex_cmds:
        # replace \[cmd] but not \\[cmd]
        content = re.sub(r'(?<!\\)\\' + cmd + r'\b', r'\\\\' + cmd, content)
        content = re.sub(r'(?<!\\)\\' + cmd + r'(?=[^a-zA-Z])', r'\\\\' + cmd, content)

    # Also replace \$ with \\$
    content = content.replace(r'\$', r'\\$')

    # Also replace \c with \\c (for \cdot if not caught)
    content = content.replace(r'\c', r'\\c')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
