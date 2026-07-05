from manim import *
import numpy as np
import random
import re


config.background_color = "#05070D"

CURVE = "#00B7FF"
SECANT = "#FF2D95"
P_COLOR = "#FFD43B"
Q_COLOR = "#FF4B4B"
R_COLOR = "#9D4EDD"
SECRET = "#00F5D4"
GOOD = "#27FF8A"
ALERT = "#FF2E2E"
GRID = "#2A3246"
MUTED = "#7D879C"
FOG = "#AAB3C5"
ALICE = "#74C0FC"
BOB = "#FF922B"

MATH_COLOR_MAP = {
    "P": P_COLOR,
    "Q": Q_COLOR,
    "R": R_COLOR,
    "S": SECRET,
    "A": ALICE,
    "B": BOB,
    "a": ALICE,
    "b": BOB,
    "r": R_COLOR,
    "s": SECRET,
    "k": P_COLOR,
    "p": GOOD,
    "x": R_COLOR,
    "y": CURVE,
    "E": CURVE,
    "\\Delta": ALERT,
    "\\mathcal{O}": R_COLOR,
    "\\rho": SECANT,
}

TEXT_TOKEN_COLORS = {
    "P": P_COLOR,
    "Q": Q_COLOR,
    "R": R_COLOR,
    "S": SECRET,
    "A": ALICE,
    "B": BOB,
    "Alice": ALICE,
    "Bob": BOB,
    "ECDLP": ALERT,
    "Frobenius": ALERT,
    "Vulnerabilidad": ALERT,
    "Critica": ALERT,
    "Secreto": SECRET,
    "secreto": SECRET,
    "Pairing": SECRET,
    "Pairings": SECRET,
    "isogenia": SECANT,
    "isogenias": SECANT,
    "mapa": SECANT,
    "curvas": CURVE,
    "curva": CURVE,
    "2022": ALERT,
}


def _math_color_map(tex):
    if "\\" in tex or "_" in tex:
        return {k: v for k, v in MATH_COLOR_MAP.items() if len(k) > 1 or k.startswith("\\")}
    return MATH_COLOR_MAP


def _split_text_tokens(text):
    tokens = sorted(TEXT_TOKEN_COLORS, key=len, reverse=True)
    pattern = r"(?<![A-Za-z])(" + "|".join(re.escape(t) for t in tokens) + r")(?![A-Za-z])"
    pieces = []
    last = 0
    for match in re.finditer(pattern, text):
        if match.start() > last:
            pieces.append(text[last:match.start()])
        pieces.append(match.group(0))
        last = match.end()
    if last < len(text):
        pieces.append(text[last:])
    return [p for p in pieces if p]


def add_halo(mob, width=5):
    mob.set_stroke(BLACK, width=width, background=True)
    return mob


def mtex(tex, scale=0.58, color=WHITE):
    mob = MathTex(tex, tex_to_color_map=_math_color_map(tex), color=color)
    return add_halo(mob.scale(scale), width=4)


def ttex(text, scale=0.48, color=WHITE):
    pieces = _split_text_tokens(text)
    mob = Tex(*pieces, color=color)
    for part in mob:
        key = part.get_tex_string()
        if key in TEXT_TOKEN_COLORS:
            part.set_color(TEXT_TOKEN_COLORS[key])
    return add_halo(mob.scale(scale), width=4)


def floating_label(text, anchor, direction=UP, scale=0.46, color=WHITE, buff=0.22):
    label = ttex(text, scale=scale, color=color)
    label.next_to(anchor, direction, buff=buff)
    label.set_z_index(30)
    return label


def formula_bubble(tex, point, scale=0.58):
    formula = mtex(tex, scale=scale)
    formula.move_to(point)
    formula.set_z_index(40)
    return formula


def glow_dot(point, color, radius=0.075, z=10):
    dot = Dot(point, radius=radius, color=color).set_z_index(z + 1)
    halo = Circle(radius=radius * 2.8, color=color, stroke_width=2)
    halo.set_fill(color, opacity=0.16)
    halo.move_to(point).set_z_index(z)
    return VGroup(halo, dot)


def new_axes(x_range=(-3.5, 4.0, 1), y_range=(-4.0, 4.0, 1), x_length=8.2, y_length=6.0):
    axes = Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "include_tip": False,
            "stroke_color": GRID,
            "stroke_width": 2,
        },
    )
    return axes


def add_grid(axes, opacity=0.16):
    lines = VGroup()
    x_min, x_max, x_step = axes.x_range
    y_min, y_max, y_step = axes.y_range
    for x in np.arange(x_min, x_max + 0.01, x_step):
        lines.add(Line(axes.c2p(x, y_min), axes.c2p(x, y_max), stroke_width=1, color=GRID, stroke_opacity=opacity))
    for y in np.arange(y_min, y_max + 0.01, y_step):
        lines.add(Line(axes.c2p(x_min, y), axes.c2p(x_max, y), stroke_width=1, color=GRID, stroke_opacity=opacity))
    lines.set_z_index(-5)
    return lines


def curve_implicit(axes, a=-1, b=1, color=CURVE, width=4):
    curve = axes.plot_implicit_curve(
        lambda x, y: y**2 - x**3 - a * x - b,
        color=color,
        stroke_width=width,
    )
    curve.set_z_index(2)
    return curve


def curve_point(axes, point, label=None, color=P_COLOR, direction=UP, radius=0.085):
    dot = glow_dot(axes.c2p(*point), color, radius=radius)
    if label is None:
        return dot
    lab = mtex(label, scale=0.5).next_to(dot, direction, buff=0.08)
    return VGroup(dot, lab)


def curve_y(a, b, x, branch=1):
    value = x**3 + a * x + b
    return branch * np.sqrt(max(0, value))


def third_intersection(a, p, q):
    x1, y1 = p
    x2, y2 = q
    if abs(x1 - x2) < 1e-7 and abs(y1 - y2) < 1e-7:
        slope = (3 * x1**2 + a) / (2 * y1)
    else:
        slope = (y2 - y1) / (x2 - x1)
    x3 = slope**2 - x1 - x2
    y3 = slope * (x3 - x1) + y1
    return (x3, y3), (x3, -y3), slope


def secant_on_axes(axes, point, slope, x_left=-3.6, x_right=4.0, color=SECANT, width=4):
    x0, y0 = point
    return Line(
        axes.c2p(x_left, slope * (x_left - x0) + y0),
        axes.c2p(x_right, slope * (x_right - x0) + y0),
        color=color,
        stroke_width=width,
    ).set_z_index(4)


def vertical_line_on_axes(axes, x, y1, y2, color=R_COLOR):
    return DashedLine(
        axes.c2p(x, y1),
        axes.c2p(x, y2),
        color=color,
        stroke_width=3,
        dash_length=0.12,
    ).set_z_index(3)


def finite_field_points(p=17, a=2, b=2):
    pts = []
    for x in range(p):
        rhs = (x**3 + a * x + b) % p
        for y in range(p):
            if (y * y - rhs) % p == 0:
                pts.append((x, y))
    return pts


def inv_mod(n, p):
    return pow(n % p, -1, p)


def ec_add(p1, p2, prime=17, a=2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % prime == 0:
        return None
    if p1 == p2:
        lam = ((3 * x1 * x1 + a) * inv_mod(2 * y1, prime)) % prime
    else:
        lam = ((y2 - y1) * inv_mod(x2 - x1, prime)) % prime
    x3 = (lam * lam - x1 - x2) % prime
    y3 = (lam * (x1 - x3) - y1) % prime
    return (x3, y3)


def ec_mul(k, point, prime=17, a=2):
    result = None
    addend = point
    while k:
        if k & 1:
            result = ec_add(result, addend, prime, a)
        addend = ec_add(addend, addend, prime, a)
        k >>= 1
    return result


def field_to_plane(pt, prime=17, scale=0.34, offset=ORIGIN):
    x, y = pt
    return np.array([(x - (prime - 1) / 2) * scale, (y - (prime - 1) / 2) * scale, 0]) + offset


def finite_grid(prime=17, scale=0.34, offset=ORIGIN, width=1.0):
    half = (prime - 1) / 2
    lines = VGroup()
    for i in range(prime):
        x = (i - half) * scale
        y = (i - half) * scale
        lines.add(Line(np.array([x, -half * scale, 0]) + offset, np.array([x, half * scale, 0]) + offset))
        lines.add(Line(np.array([-half * scale, y, 0]) + offset, np.array([half * scale, y, 0]) + offset))
    lines.set_color(GRID).set_stroke(width=width, opacity=0.34)
    return lines


def point_cloud(points, prime=17, scale=0.34, offset=ORIGIN, color=CURVE, radius=0.045):
    return VGroup(
        *[
            Dot(field_to_plane(pt, prime, scale, offset), radius=radius, color=color)
            for pt in points
        ]
    ).set_z_index(5)


def finite_point(pt, prime=17, scale=0.34, offset=ORIGIN, color=P_COLOR, radius=0.095):
    return glow_dot(field_to_plane(pt, prime, scale, offset), color, radius=radius)


def path_from_points(points, prime=17, scale=0.34, offset=ORIGIN, color=SECANT, width=4):
    path = VMobject(color=color, stroke_width=width)
    if len(points) == 1:
        path.set_points_as_corners([field_to_plane(points[0], prime, scale, offset)])
    else:
        path.set_points_as_corners([field_to_plane(pt, prime, scale, offset) for pt in points])
    return path


def curved_arrow_between(a, b, color=SECANT, angle=TAU / 8):
    return CurvedArrow(a, b, angle=angle, color=color, stroke_width=3, tip_length=0.18)


def random_network(rows=16, cols=25, spacing=0.9, jitter=0.18, seed=4):
    rng = random.Random(seed)
    pts = []
    for r in range(rows):
        for c in range(cols):
            pts.append(
                np.array(
                    [
                        (c - cols / 2) * spacing + rng.uniform(-jitter, jitter),
                        (r - rows / 2) * spacing + rng.uniform(-jitter, jitter),
                        0,
                    ]
                )
            )
    edges = []
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if c + 1 < cols:
                edges.append((idx, idx + 1))
            if r + 1 < rows:
                edges.append((idx, idx + cols))
            if c + 1 < cols and r + 1 < rows and rng.random() < 0.22:
                edges.append((idx, idx + cols + 1))
    return pts, edges


def make_network(pts, edges, dot_radius=0.025):
    lines = VGroup(*[Line(pts[i], pts[j], color=GRID, stroke_width=1, stroke_opacity=0.34) for i, j in edges])
    dots = VGroup(*[Dot(p, radius=dot_radius, color=MUTED) for p in pts])
    return lines, dots


def wait_read(scene, seconds=2):
    scene.wait(seconds)


def frame_height(width):
    return width * config.frame_height / config.frame_width


def fit_width_for(mobject, min_width=5.6, max_width=10.0, pad=1.35):
    width = max(mobject.width * pad, mobject.height * pad * config.frame_width / config.frame_height, min_width)
    return min(width, max_width)


def focus_on(scene, *mobjects, min_width=5.6, max_width=10.0, pad=1.35, run_time=1.15, shift=ORIGIN):
    group = VGroup(*mobjects)
    width = fit_width_for(group, min_width=min_width, max_width=max_width, pad=pad)
    scene.play(
        scene.camera.frame.animate.move_to(group.get_center() + shift).set(width=width),
        run_time=run_time,
        rate_func=smooth,
    )


def camera_to(scene, point, width=6.0, run_time=1.2):
    scene.play(scene.camera.frame.animate.move_to(point).set(width=width), run_time=run_time, rate_func=smooth)


def keep_near_camera(scene, mob, margin=0.35):
    frame = scene.camera.frame
    center = frame.get_center()
    width = frame.width
    height = frame_height(width)
    left = center[0] - width / 2 + margin
    right = center[0] + width / 2 - margin
    bottom = center[1] - height / 2 + margin
    top = center[1] + height / 2 - margin
    dx = 0
    dy = 0
    if mob.get_left()[0] < left:
        dx = left - mob.get_left()[0]
    if mob.get_right()[0] > right:
        dx = right - mob.get_right()[0]
    if mob.get_bottom()[1] < bottom:
        dy = bottom - mob.get_bottom()[1]
    if mob.get_top()[1] > top:
        dy = top - mob.get_top()[1]
    mob.shift(RIGHT * dx + UP * dy)
    return mob


def callout(scene, text, anchor, direction=UP, scale=0.46, color=WHITE, wait=1.4, fade=True):
    label = floating_label(text, anchor, direction=direction, scale=scale, color=color)
    keep_near_camera(scene, label)
    scene.play(Write(label), run_time=0.65)
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(label), run_time=0.45)
    return label


def replace_formula(scene, old, new_tex, scale=None, run_time=0.9):
    new = mtex(new_tex, scale=scale or 0.58).move_to(old)
    scene.play(ReplacementTransform(old, new), run_time=run_time)
    return new


def show_title(scene, text, scale=0.56):
    title = ttex(text, scale=scale)
    title.move_to(scene.camera.frame.get_center() + UP * frame_height(scene.camera.frame.width) * 0.34)
    keep_near_camera(scene, title)
    scene.play(Write(title), run_time=0.8)
    scene.wait(1.0)
    scene.play(FadeOut(title), run_time=0.45)
    return title


def finite_scene(prime=17, a=2, b=2, scale=0.3, offset=ORIGIN):
    pts = finite_field_points(prime, a, b)
    return finite_grid(prime, scale, offset), point_cloud(pts, prime, scale, offset, CURVE, radius=0.035)


def safe_line(start, end, color=SECANT, width=4):
    return Line(start, end, color=color, stroke_width=width).set_z_index(4)
