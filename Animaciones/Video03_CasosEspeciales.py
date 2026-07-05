from manim import *
import numpy as np


class CasosEspeciales(Scene):
    def construct(self):
        # Curva base: y^2 = x^3 - x + 1
        a = -1
        b = 1

        title = Text("Casos especiales de la suma", font="Cambria").scale(0.48).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-4, 5, 1],
            y_range=[-6, 6, 1],
            x_length=8.5,
            y_length=5.5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.2)

        curve = axes.plot_implicit_curve(
            lambda x, y: y**2 - x**3 - a * x - b,
            color=BLUE,
            stroke_width=3,
        )

        self.play(Create(axes), Create(curve), run_time=2)

        def curve_y(x):
            return np.sqrt(x**3 + a * x + b)

        def add_point(point, label, color, direction, scale=0.42):
            dot = Dot(axes.c2p(*point), color=color, radius=0.08)
            text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
            text.next_to(dot, direction, buff=0.1)
            return VGroup(dot, text)

        def make_formula(parts, colors, scale=0.58):
            formula = VGroup(
                *[
                    Text(part, font="Cambria Math", slant=ITALIC if part not in ["+", "=", "(", ")"] else NORMAL, color=color)
                    for part, color in zip(parts, colors)
                ]
            )
            formula.arrange(RIGHT, buff=0.16).scale(scale)
            formula.move_to(DOWN * 3.32 + LEFT * 0.25)
            return formula

        # ACTO 1: doblar un punto
        p_x = -0.8
        p = (p_x, curve_y(p_x))
        qx = ValueTracker(0.8)

        def get_q():
            x = qx.get_value()
            return (x, curve_y(x))

        def tangent_slope(point):
            x, y = point
            return (3 * x**2 + a) / (2 * y)

        def secant_slope(point_1, point_2):
            x1, y1 = point_1
            x2, y2 = point_2
            if abs(x2 - x1) < 0.035:
                return tangent_slope(point_1)
            return (y2 - y1) / (x2 - x1)

        def line_from_slope(point, slope, color=GREEN):
            x_left, x_right = -3.6, 4.6
            return Line(
                axes.c2p(x_left, slope * (x_left - point[0]) + point[1]),
                axes.c2p(x_right, slope * (x_right - point[0]) + point[1]),
                color=color,
                stroke_width=4,
            )

        p_obj = add_point(p, "P", YELLOW, UP + LEFT)
        q_dot = always_redraw(lambda: Dot(axes.c2p(*get_q()), color=RED, radius=0.08))
        q_label = always_redraw(
            lambda: Text("Q", font="Cambria Math", slant=ITALIC, color=RED)
            .scale(0.42)
            .next_to(q_dot, UP + RIGHT, buff=0.1)
        )
        secant = always_redraw(lambda: line_from_slope(p, secant_slope(p, get_q()), GREEN))

        narrative_1 = Text(
            "El primer caso especial aparece cuando queremos sumar un punto consigo mismo.",
            font="Cambria",
        ).scale(0.39).to_edge(UP)
        self.play(Transform(title, narrative_1))
        self.play(FadeIn(p_obj), FadeIn(q_dot), FadeIn(q_label), Create(secant), run_time=1.0)
        self.wait(0.8)

        narrative_2 = Text(
            "Hacemos que Q se acerque a P: la secante se convierte en la tangente.",
            font="Cambria",
        ).scale(0.40).to_edge(UP)
        self.play(Transform(title, narrative_2))
        self.play(qx.animate.set_value(p_x + 0.02), run_time=3.0, rate_func=smooth)
        same_point_label = Text("P = Q", font="Cambria Math", color=WHITE).scale(0.38)
        same_point_label.next_to(p_obj[0], DOWN + LEFT, buff=0.16)
        self.play(Write(same_point_label), run_time=0.6)
        self.wait(0.4)

        tangent = line_from_slope(p, tangent_slope(p), GREEN)
        self.play(FadeOut(q_dot), FadeOut(q_label), FadeOut(same_point_label), ReplacementTransform(secant, tangent), run_time=0.7)

        narrative_3 = Text(
            "Para calcular P + P usamos esa tangente como recta límite.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_3))

        slope = tangent_slope(p)
        hit_x = slope**2 - 2 * p[0]
        hit_y = p[1] + slope * (hit_x - p[0])
        hit = (hit_x, hit_y)
        double = (hit_x, -hit_y)

        hit_obj = add_point(hit, "-2P", ORANGE, UP + LEFT, scale=0.39)
        hit_obj[1].shift(RIGHT * 0.05 + UP * 0.05)
        self.play(FadeIn(hit_obj), Flash(axes.c2p(*hit), color=ORANGE, flash_radius=0.55), run_time=1.0)

        narrative_4 = Text(
            "La tangente vuelve a cortar la curva en -2P.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_4))
        self.wait(0.8)

        vertical = DashedLine(
            axes.c2p(hit[0], hit[1]),
            axes.c2p(double[0], double[1]),
            color=PURPLE,
            stroke_width=3,
            dash_length=0.12,
        )
        double_obj = add_point(double, "2P", PURPLE, DOWN + RIGHT)
        double_obj[1].shift(UP * 0.3 + LEFT * 0.04)

        formula_double = make_formula(
            ["P", "+", "P", "=", "2P"],
            [YELLOW, WHITE, YELLOW, WHITE, PURPLE],
        )

        narrative_5 = Text(
            "Reflejamos ese punto respecto del eje X y obtenemos 2P.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_5))
        self.play(Create(vertical), run_time=0.8)
        self.play(TransformFromCopy(hit_obj[0], double_obj[0]), Write(double_obj[1]), run_time=1.0)
        self.play(Write(formula_double), Flash(axes.c2p(*double), color=PURPLE, flash_radius=0.55), run_time=1.0)

        narrative_6 = Text(
            "Geométricamente, este procedimiento es el doblado de puntos.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_6))
        self.play(Indicate(formula_double, color=PURPLE, scale_factor=1.05), run_time=1.0)
        self.wait(1.0)

        # ACTO 2: puntos opuestos y el punto al infinito
        self.play(
            FadeOut(p_obj),
            FadeOut(hit_obj),
            FadeOut(double_obj),
            FadeOut(tangent),
            FadeOut(vertical),
            FadeOut(formula_double),
            run_time=1.0,
        )

        narrative_7 = Text(
            "El segundo caso especial ocurre con dos puntos opuestos.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_7))

        p2_x = 0.5
        p2 = (p2_x, curve_y(p2_x))
        neg_p2 = (p2_x, -curve_y(p2_x))

        p2_obj = add_point(p2, "P", YELLOW, UP + RIGHT)
        neg_obj = add_point(neg_p2, "-P", RED, DOWN + RIGHT)
        self.play(FadeIn(p2_obj), FadeIn(neg_obj), run_time=1.0)

        narrative_8 = Text(
            "La recta que los une es vertical, así que no aparece un tercer corte visible.",
            font="Cambria",
        ).scale(0.40).to_edge(UP)
        self.play(Transform(title, narrative_8))

        vertical_line = Line(
            axes.c2p(p2_x, -5.5),
            axes.c2p(p2_x, 5.5),
            color=GREEN,
            stroke_width=4,
        )
        self.play(Create(vertical_line), run_time=1.0)
        self.wait(0.8)

        infinity = Text("𝒪", font="Cambria Math", color=PURPLE).scale(1.25)
        infinity.move_to(axes.c2p(p2_x + 0.32, 4.85))

        narrative_9 = Text(
            "Ese tercer corte se interpreta como 𝒪, el punto al infinito.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_9))
        self.play(FadeIn(infinity, scale=0.6), Flash(infinity, color=PURPLE, flash_radius=0.8), run_time=1.1)

        formula_inf = make_formula(
            ["P", "+", "(-P)", "=", "𝒪"],
            [YELLOW, WHITE, RED, WHITE, PURPLE],
        )
        self.play(Write(formula_inf), run_time=1.0)
        self.wait(0.8)

        narrative_10 = Text(
            "Por eso 𝒪 actúa como elemento neutro: sumar el opuesto cancela el punto.",
            font="Cambria",
        ).scale(0.39).to_edge(UP)
        self.play(Transform(title, narrative_10))
        self.play(Indicate(formula_inf, color=PURPLE, scale_factor=1.05), run_time=1.0)
        self.wait(3)
