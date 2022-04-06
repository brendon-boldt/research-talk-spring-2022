import random

prefix = r"""
\begin{tikzpicture}
  \begin{axis}[
    ybar stacked,
    % ybar interval=0.7,
    % grid=x,
    width=9cm, height=6cm,
    xtick=data,
    ytick distance=2,
    ymajorgrids=true,
    yminorgrids=true,
    minor y tick num=1,
    ymin=0,
    ymax=10,
    axis on top,
    grid style={draw=white,line width=0.5mm},
    ]
"""

postfix = r"""
  \end{axis}
\end{tikzpicture}
"""


def make_coords(l):
    s = ""
    for i in range(len(l)):
        s += f"({i},{l[i]})"

    return s + f"({len(l)},0)"


def get_idx_crp(i, alpha, l):
    r = random.random() * (i + alpha)
    idx = 0
    l.append(alpha)
    if not l:
        return 0
    while True:
        r -= l[idx]
        if r < 0:
            l.pop()
            return idx
        else:
            idx += 1


def get_idx_filex(i, alpha, l):
    r = random.random() * (i + alpha * len(l))
    l = [x + alpha for x in l]
    idx = 0
    while True:
        r -= l[idx]
        if r < 0:
            return idx
        idx += 1


def make_plot_command(slide, color, coords):
    return rf"\only<{slide}>{{\addplot[draw={color},fill={color}] coordinates {{{coords}}};}}"


def make_crp(n_iters):
    with open("assets/crp.tex", "w") as fp:
        fp.write(prefix)
        l = []
        alpha = 2
        idx = -1
        for i in range(n_iters):
            coords = make_coords(l)
            fp.write(make_plot_command(i + 1, "blue", coords))
            fp.write("\n")

            coords = (
                "".join(f"({i}, 0)" for i in range(len(l))) + f"({len(l)}, {alpha})"
            )
            fp.write(make_plot_command(i + 1, "green", coords))
            fp.write("\n")

            idx = get_idx_crp(i, alpha, l)
            if idx == len(l):
                l.append(1)
            else:
                l[idx] += 1
        fp.write(postfix)


def make_filex(n_iters):
    with open("assets/filex.tex", "w") as fp:
        fp.write(prefix)
        alpha = 1
        n_params = 5
        l = [0] * n_params

        coords = "".join(f"({i},{alpha})" for i in range(n_params))
        fp.write(make_plot_command("1-", "green", coords))
        fp.write("\n")

        for i in range(0, n_iters + 1):
            idx = get_idx_filex(i, alpha, l)
            l[idx] += 1

            coords = "".join(f"({i}, {l[i]})" for i in range(n_params))
            fp.write(make_plot_command(i + 2, "blue", coords))
            fp.write("\n")

        fp.write(postfix)


def main():
    make_crp(11)
    make_filex(10)


if __name__ == "__main__":
    main()
