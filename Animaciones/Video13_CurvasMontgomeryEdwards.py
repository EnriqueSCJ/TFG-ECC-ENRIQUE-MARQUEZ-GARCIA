from manim import *
import numpy as np


class CurvasMontgomeryEdwards(Scene):
    def construct(self):
        title = self.top_text("Curvas Montgomery y Edwards").scale(1.02)
        self.play(Write(title), run_time=0.9)

        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.0, 3.0, 1],
            x_length=7.2,
            y_length=5.2,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        ).shift(UP * 0.10)
        grid = self.add_grid(axes)

        weierstrass = axes.plot_implicit_curve(
            lambda x, y: y**2 - x**3 + x - 1,
            color=BLUE,
            stroke_width=4,
        )
        weierstrass_label = Text("Weierstrass", font="Cambria", color=BLUE).scale(0.42)
        weierstrass_label.move_to(LEFT * 3.45 + UP * 2.15)
        bottom = Text("La forma y² = x³ + ax + b es muy buena para explicar la geometría.", font="Cambria").scale(0.45)
        bottom.move_to(DOWN * 3.35)

        self.play(Create(grid), Create(axes), Create(weierstrass), Write(weierstrass_label), Write(bottom), run_time=2.0)
        self.wait(3.0)

        p = (-1.1, self.weierstrass_y(-1.1))
        q = (0.05, self.weierstrass_y(0.05))
        p_obj = self.point_on_axes(axes, p, "P", YELLOW, UP + LEFT)
        q_obj = self.point_on_axes(axes, q, "Q", RED, UP + RIGHT)
        hit, r, slope = self.third_intersection(p, q)
        secant = Line(
            axes.c2p(-2.9, slope * (-2.9 - p[0]) + p[1]),
            axes.c2p(2.9, slope * (2.9 - p[0]) + p[1]),
            color=GREEN,
            stroke_width=4,
        )
        r_obj = self.point_on_axes(axes, r, "P+Q", PURPLE, DOWN + RIGHT, scale=0.33)
        r_obj[1].next_to(r_obj[0], RIGHT, buff=0.18).shift(DOWN * 0.12)

        narrative_1 = self.top_text("Pero al implementar, la forma de la ecuación afecta al coste y a las excepciones.")
        bottom_1 = self.make_formula(["P", "+", "Q", "=", "R"], [YELLOW, WHITE, RED, WHITE, PURPLE], scale=0.60)
        self.play(Transform(title, narrative_1), ReplacementTransform(bottom, bottom_1), FadeIn(p_obj), FadeIn(q_obj), run_time=1.2)
        self.wait(1.4)
        self.play(Create(secant), run_time=0.8)
        self.play(FadeIn(r_obj), Flash(r_obj[0].get_center(), color=PURPLE, flash_radius=0.55), run_time=0.9)
        self.wait(3.0)

        montgomery = axes.plot_implicit_curve(
            lambda x, y: y**2 - (x**3 + 1.35 * x**2 + x),
            color=GREEN,
            stroke_width=4,
        )
        mont_label = Text("Montgomery", font="Cambria", color=GREEN).scale(0.42)
        mont_label.move_to(LEFT * 3.35 + UP * 2.15)
        narrative_2 = self.top_text("Montgomery reorganiza la curva para hacer más rápida la multiplicación escalar.")
        bottom_2 = Text("forma típica: By² = x³ + Ax² + x", font="Cambria Math", color=GREEN).scale(0.58)
        bottom_2.move_to(DOWN * 3.35)
        self.play(
            Transform(title, narrative_2),
            ReplacementTransform(bottom_1, bottom_2),
            ReplacementTransform(weierstrass, montgomery),
            ReplacementTransform(weierstrass_label, mont_label),
            FadeOut(p_obj),
            FadeOut(q_obj),
            FadeOut(r_obj),
            FadeOut(secant),
            run_time=1.5,
        )
        self.wait(3.2)

        ladder = self.make_ladder()
        ladder.move_to(RIGHT * 2.75 + DOWN * 0.35)
        ladder_note = self.info_box(
            ["escalera Montgomery", "usa solo coordenadas x", "patrón regular"],
            GREEN,
        ).move_to(LEFT * 2.75 + DOWN * 0.15)
        narrative_3 = self.top_text("La escalera de Montgomery ayuda a usar un patrón uniforme para kP.")
        bottom_3 = Text("misma estructura de pasos  →  mejor para resistir canales laterales", font="Cambria Math", color=GREEN).scale(0.52)
        bottom_3.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_3), ReplacementTransform(bottom_2, bottom_3), FadeIn(ladder_note), run_time=1.0)
        self.wait(1.3)
        self.play(LaggedStart(*[Create(part) for part in ladder], lag_ratio=0.12), run_time=1.8)
        self.wait(3.5)

        edwards = ParametricFunction(
            lambda t: axes.c2p(
                2.05 * np.cos(t) / (1 + 0.38 * np.sin(t) ** 2),
                2.05 * np.sin(t) / (1 + 0.38 * np.cos(t) ** 2),
            ),
            t_range=[0, TAU],
            color=BLUE,
            stroke_width=4,
        )
        edwards_label = Text("Edwards", font="Cambria", color=BLUE).scale(0.42)
        edwards_label.move_to(LEFT * 3.55 + UP * 2.15)
        narrative_4 = self.top_text("Edwards busca fórmulas de suma más simétricas y con menos casos especiales.")
        bottom_4 = Text("forma típica: x² + y² = 1 + d x²y²", font="Cambria Math", color=BLUE).scale(0.58)
        bottom_4.move_to(DOWN * 3.35)
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            ReplacementTransform(montgomery, edwards),
            ReplacementTransform(mont_label, edwards_label),
            FadeOut(ladder),
            FadeOut(ladder_note),
            run_time=1.5,
        )
        self.wait(4.4)

        sample_points = [0.25, 1.25, 2.15, 3.30, 4.35, 5.35]
        moving_dot = Dot(self.edwards_point(axes, sample_points[0]), color=YELLOW, radius=0.080)
        trace = VMobject(color=GREEN, stroke_width=4)
        trace.set_points_as_corners([self.edwards_point(axes, sample_points[0])])
        self.add(trace)

        narrative_5 = self.top_text("En implementaciones reales, cada caso especial puede convertirse en una rama del programa.")
        bottom_5 = Text("si el código cambia de camino, puede cambiar tiempo, memoria o consumo", font="Cambria", color=WHITE).scale(0.48)
        bottom_5.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_5), ReplacementTransform(bottom_4, bottom_5), FadeIn(moving_dot), run_time=1.1)
        self.wait(2.0)

        trace_points = [self.edwards_point(axes, sample_points[0])]
        for t in sample_points[1:]:
            trace_points.append(self.edwards_point(axes, t))
            new_trace = VMobject(color=GREEN, stroke_width=4).set_points_as_corners(trace_points)
            self.play(moving_dot.animate.move_to(trace_points[-1]), ReplacementTransform(trace, new_trace), run_time=0.45)
            trace = new_trace

        branch_box = self.info_box(
            ["casos especiales", "P = Q", "P = -Q", "P = 𝒪"],
            RED,
            width=2.70,
            height=1.58,
        ).move_to(RIGHT * 2.65 + UP * 0.75)
        narrative_6 = self.top_text("Esas ramas son justo lo que queríamos evitar en el video de canales laterales.")
        bottom_6 = Text("rama visible  →  posible filtración", font="Cambria Math", color=RED).scale(0.56)
        bottom_6.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_6), ReplacementTransform(bottom_5, bottom_6), FadeIn(branch_box), run_time=1.1)
        self.play(Indicate(branch_box, color=RED, scale_factor=1.04), run_time=0.9)
        self.wait(3.3)

        branch_cross = Cross(branch_box, stroke_color=RED, stroke_width=5)
        complete_box = self.info_box(
            ["fórmula completa", "misma receta", "para casi todos los casos"],
            GREEN,
            width=3.05,
            height=1.36,
        ).move_to(RIGHT * 2.65 + UP * 0.75)
        narrative_7 = self.top_text("Las formas Edwards permiten fórmulas de suma completas: menos excepciones, menos ramas.")
        bottom_7 = Text("mismo algoritmo para más entradas  →  menos ramas dependientes del secreto", font="Cambria Math", color=GREEN).scale(0.50)
        bottom_7.move_to(DOWN * 3.35)
        self.play(Create(branch_cross), Flash(branch_box.get_center(), color=RED, flash_radius=0.75), run_time=0.8)
        self.play(
            Transform(title, narrative_7),
            ReplacementTransform(bottom_6, bottom_7),
            FadeOut(branch_box),
            FadeOut(branch_cross),
            FadeIn(complete_box),
            run_time=1.1,
        )
        self.play(Indicate(complete_box, color=GREEN, scale_factor=1.04), run_time=0.9)
        self.wait(3.4)

        narrative_8 = self.top_text("Por eso Curve25519 y Ed25519 usan estas formas en implementaciones reales.")
        final_cards = VGroup(
            self.small_card("Curve25519", "Montgomery", GREEN),
            self.small_card("Ed25519", "Edwards", BLUE),
        ).arrange(RIGHT, buff=0.55)
        final_cards.move_to(DOWN * 0.28)
        final_bottom = Text("misma ECC, formas elegidas para calcular mejor y filtrar menos", font="Cambria Math", color=GREEN).scale(0.50)
        final_bottom.move_to(DOWN * 3.35)
        self.play(
            Transform(title, narrative_8),
            ReplacementTransform(bottom_7, final_bottom),
            FadeOut(moving_dot),
            FadeOut(trace),
            FadeOut(complete_box),
            FadeIn(final_cards),
            run_time=1.2,
        )
        self.play(Indicate(final_cards, color=GREEN, scale_factor=1.03), run_time=1.0)
        self.wait(5.0)

    def top_text(self, text, scale=0.54):
        mob = Text(text, font="Cambria").scale(scale)
        if mob.width > 12.4:
            mob.scale_to_fit_width(12.4)
        mob.to_edge(UP)
        return mob

    def make_formula(self, parts, colors, scale=0.58):
        formula = VGroup(
            *[
                Text(
                    part,
                    font="Cambria Math",
                    slant=ITALIC if part not in ["+", "="] else NORMAL,
                    color=color,
                )
                for part, color in zip(parts, colors)
            ]
        )
        formula.arrange(RIGHT, buff=0.14).scale(scale)
        formula.move_to(DOWN * 3.35)
        return formula

    def add_grid(self, axes):
        lines = VGroup()
        for x in np.arange(-3, 3.1, 1):
            lines.add(Line(axes.c2p(x, -2.8), axes.c2p(x, 2.8), color=GRAY, stroke_width=1, stroke_opacity=0.20))
        for y in np.arange(-2, 2.1, 1):
            lines.add(Line(axes.c2p(-3.3, y), axes.c2p(3.3, y), color=GRAY, stroke_width=1, stroke_opacity=0.20))
        return lines

    def weierstrass_y(self, x):
        return np.sqrt(max(0, x**3 - x + 1))

    def third_intersection(self, p, q):
        x1, y1 = p
        x2, y2 = q
        slope = (y2 - y1) / (x2 - x1)
        x3 = slope**2 - x1 - x2
        y3 = slope * (x3 - x1) + y1
        return (x3, y3), (x3, -y3), slope

    def point_on_axes(self, axes, point, label, color, direction, scale=0.38):
        dot = Dot(axes.c2p(*point), color=color, radius=0.075)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
        text.next_to(dot, direction, buff=0.08)
        return VGroup(dot, text)

    def make_ladder(self):
        group = VGroup()
        left_x = -0.90
        right_x = 0.90
        ys = [1.25, 0.65, 0.05, -0.55, -1.15]
        for i, y in enumerate(ys):
            color = GREEN if i % 2 == 0 else RED
            group.add(Line(np.array([left_x, y, 0]), np.array([right_x, y, 0]), color=color, stroke_width=4))
            group.add(Dot(np.array([left_x, y, 0]), color=YELLOW, radius=0.05))
            group.add(Dot(np.array([right_x, y, 0]), color=PURPLE, radius=0.05))
            if i < len(ys) - 1:
                group.add(Line(np.array([right_x, y, 0]), np.array([left_x, ys[i + 1], 0]), color=GRAY, stroke_width=2))
        label = Text("kP", font="Cambria Math", color=PURPLE).scale(0.42)
        label.next_to(group, DOWN, buff=0.12)
        group.add(label)
        return group

    def info_box(self, lines, color, width=3.25, height=1.32):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=height,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        text = VGroup(
            *[
                Text(line, font="Cambria Math" if index == 0 else "Cambria", color=color if index == 0 else WHITE).scale(
                    0.36 if index == 0 else 0.30
                )
                for index, line in enumerate(lines)
            ]
        ).arrange(DOWN, buff=0.07)
        text.move_to(box)
        return VGroup(box, text)

    def edwards_point(self, axes, t):
        return axes.c2p(
            2.05 * np.cos(t) / (1 + 0.38 * np.sin(t) ** 2),
            2.05 * np.sin(t) / (1 + 0.38 * np.cos(t) ** 2),
        )

    def small_card(self, title, subtitle, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.55,
            height=1.12,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        text = VGroup(
            Text(title, font="Cambria Math", color=color).scale(0.42),
            Text(subtitle, font="Cambria", color=WHITE).scale(0.34),
        ).arrange(DOWN, buff=0.10)
        text.move_to(box)
        return VGroup(box, text)
