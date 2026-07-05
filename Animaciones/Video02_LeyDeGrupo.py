from manim import *
import numpy as np


class LeyDeGrupo(Scene):
    def construct(self):
        # Curva base: y^2 = x^3 - x + 1
        a = -1
        b = 1

        title = Text("Ley de Grupo: sumar puntos en una curva", font="Cambria").scale(0.46).to_edge(UP)
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

        def add_point(point, label, color, direction):
            dot = Dot(axes.c2p(*point), color=color, radius=0.08)
            text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(0.42)
            text.next_to(dot, direction, buff=0.1)
            return VGroup(dot, text)

        def third_intersection(p, q):
            x1, y1 = p
            x2, y2 = q
            slope = (y2 - y1) / (x2 - x1)
            x3 = slope**2 - x1 - x2
            y3 = slope * (x3 - x1) + y1
            return (x3, y3), (x3, -y3), slope

        def curve_y(x):
            return np.sqrt(x**3 + a * x + b)

        p = (-1.2, curve_y(-1.2))
        q = (-0.2, curve_y(-0.2))
        hit, r, slope = third_intersection(p, q)

        p_obj = add_point(p, "P", YELLOW, UP + LEFT)
        q_obj = add_point(q, "Q", RED, UP + RIGHT)
        q_obj[1].shift(LEFT * 0.35 + UP * 0.05)

        narrative_1 = Text(
            "Para sumar dos puntos, elegimos P y Q sobre la misma curva.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_1))
        self.play(FadeIn(p_obj), FadeIn(q_obj), run_time=0.9)
        self.wait(1)

        narrative_2 = Text(
            "Trazamos la recta secante que pasa por P y Q.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_2))

        x_left, x_right = -3.5, 4.5
        secant = Line(
            axes.c2p(x_left, slope * (x_left - p[0]) + p[1]),
            axes.c2p(x_right, slope * (x_right - p[0]) + p[1]),
            color=GREEN,
            stroke_width=4,
        )
        self.play(Create(secant), run_time=1.2)
        self.wait(1)

        hit_obj = add_point(hit, "R", ORANGE, UP)

        narrative_3 = Text(
            "La secante corta la curva una tercera vez: ese punto es R.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_3))
        self.play(FadeIn(hit_obj), Flash(axes.c2p(*hit), color=ORANGE, flash_radius=0.55), run_time=1.0)
        self.wait(1)

        relation = VGroup(
            Text("P", font="Cambria Math", slant=ITALIC, color=YELLOW),
            Text("+", font="Cambria Math", color=WHITE),
            Text("Q", font="Cambria Math", slant=ITALIC, color=RED),
            Text("+", font="Cambria Math", color=WHITE),
            Text("R", font="Cambria Math", slant=ITALIC, color=ORANGE),
            Text("=", font="Cambria Math", color=WHITE),
            Text("𝒪", font="Cambria Math", color=WHITE),
        ).arrange(RIGHT, buff=0.15).scale(0.54)
        relation.move_to(DOWN * 3.32 + LEFT * 0.25)

        narrative_4 = Text(
            "Los tres puntos de corte cumplen P + Q + R = 𝒪, donde 𝒪 es el punto al infinito.",
            font="Cambria",
        ).scale(0.36).to_edge(UP)
        self.play(Transform(title, narrative_4))
        self.play(Write(relation), run_time=1.0)
        self.wait(1.2)

        narrative_5 = Text(
            "Por eso P + Q = -R: reflejamos R respecto del eje X.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_5))

        vertical = DashedLine(
            axes.c2p(hit[0], hit[1]),
            axes.c2p(r[0], r[1]),
            color=PURPLE,
            stroke_width=3,
            dash_length=0.12,
        )
        r_obj = add_point(r, "-R", PURPLE, DOWN + RIGHT)
        r_obj[1].shift(UP * 0.42 + RIGHT * 0.08)
        self.play(Create(vertical), run_time=0.9)
        self.play(TransformFromCopy(hit_obj[0], r_obj[0]), Write(r_obj[1]), run_time=1.0)
        self.play(Flash(axes.c2p(*r), color=PURPLE, flash_radius=0.55))

        formula = VGroup(
            Text("P", font="Cambria Math", slant=ITALIC, color=YELLOW),
            Text("+", font="Cambria Math", color=WHITE),
            Text("Q", font="Cambria Math", slant=ITALIC, color=RED),
            Text("=", font="Cambria Math", color=WHITE),
            Text("-R", font="Cambria Math", slant=ITALIC, color=PURPLE),
        ).arrange(RIGHT, buff=0.18).scale(0.58)
        formula.move_to(DOWN * 3.32 + LEFT * 0.25)

        self.play(
            ReplacementTransform(relation, formula),
            run_time=1.0,
        )
        self.play(
            Indicate(formula[4], color=PURPLE, scale_factor=1.15),
            run_time=0.8,
        )
        self.wait(0.5)

        final_narrative = Text(
            "El reflejo -R es el punto que llamamos suma P + Q.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, final_narrative))
        self.play(Indicate(formula, color=PURPLE, scale_factor=1.05), run_time=1.0)
        self.wait(3)
