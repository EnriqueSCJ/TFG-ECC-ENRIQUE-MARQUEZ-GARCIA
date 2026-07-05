from manim import *


class CamposFinitos(Scene):
    def construct(self):
        a = 2
        b = 2
        p = 17

        title = Text("Curvas elípticas sobre campos finitos", font="Cambria").scale(0.46).to_edge(UP)
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

        formula_real = Text("y² = x³ + 2x + 2", font="Cambria Math", color=WHITE).scale(0.58)
        formula_real.move_to(DOWN * 3.45 + LEFT * 0.2)

        self.play(Create(axes), Create(curve), Write(formula_real), run_time=2)

        narrative_1 = Text(
            "Sobre los números reales, la curva es continua: hay infinitos puntos.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_1))
        self.wait(1.2)

        formula_mod = Text("y² ≡ x³ + 2x + 2   (mod 17)", font="Cambria Math", color=WHITE).scale(0.58)
        formula_mod.move_to(DOWN * 3.45)

        narrative_2 = Text(
            "En criptografía no trabajamos con todos los reales, sino con restos módulo p.",
            font="Cambria",
        ).scale(0.39).to_edge(UP)
        self.play(Transform(title, narrative_2))
        self.play(ReplacementTransform(formula_real, formula_mod), run_time=0.9)
        self.wait(1.0)

        field = self.make_field_grid(p)
        cloud = self.make_solution_cloud(p, a, b)

        narrative_3 = Text(
            "Módulo 17 significa que solo existen los valores 0, 1, ..., 16.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_3))
        self.play(
            FadeOut(axes),
            curve.animate.set_stroke(opacity=0.0),
            Create(field),
            run_time=1.4,
        )
        self.wait(0.6)

        narrative_4 = Text(
            "Ahora probamos esos restos: solo algunos pares (x, y) cumplen la ecuación.",
            font="Cambria",
        ).scale(0.39).to_edge(UP)
        self.play(Transform(title, narrative_4))
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in cloud], lag_ratio=0.035),
            run_time=2.0,
        )
        self.wait(1.0)

        count_label = Text("18 puntos + 𝒪", font="Cambria Math", color=BLUE).scale(0.48)
        count_label.move_to(DOWN * 2.92)

        narrative_5 = Text(
            "La curva no desaparece: se convierte en una nube finita de soluciones.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_5))
        self.play(FadeIn(count_label, shift=UP * 0.15), Indicate(cloud, color=BLUE), run_time=1.1)
        self.wait(1.0)

        marker = Dot(self.field_to_point(16, 4, p), color=YELLOW, radius=0.09).set_z_index(4)
        marker_label = Text("16", font="Cambria Math", color=YELLOW).scale(0.34)
        marker_label.next_to(marker, UP, buff=0.08)
        marker_group = VGroup(marker, marker_label)

        narrative_6 = Text(
            "El plano finito se envuelve: al pasar de 16 volvemos a 0.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_6))
        self.play(FadeIn(marker_group), run_time=0.6)
        step_label = Text("+ 1", font="Cambria Math", color=YELLOW).scale(0.34)
        step_label.next_to(marker, RIGHT, buff=0.14)
        self.play(Write(step_label), run_time=0.5)
        self.play(marker_group.animate.shift(RIGHT * 0.29), step_label.animate.shift(RIGHT * 0.29), run_time=0.8)

        zero_marker = Dot(self.field_to_point(0, 4, p), color=YELLOW, radius=0.09).set_z_index(4)
        zero_label = Text("0", font="Cambria Math", color=YELLOW).scale(0.34)
        zero_label.next_to(zero_marker, UP, buff=0.08)
        zero_group = VGroup(zero_marker, zero_label)
        wrap_arrow = DashedLine(
            self.field_to_point(17, 4, p),
            self.field_to_point(0, 4, p),
            color=YELLOW,
            stroke_width=2,
            dash_length=0.08,
        ).set_opacity(0.55)
        self.play(Create(wrap_arrow), FadeIn(zero_group), Flash(zero_marker, color=YELLOW, flash_radius=0.55), run_time=0.9)
        self.play(FadeOut(marker_group), FadeOut(step_label), FadeOut(wrap_arrow), run_time=0.5)

        wrap_formula = Text("16 + 1 ≡ 0   (mod 17)", font="Cambria Math", color=YELLOW).scale(0.42)
        wrap_formula.move_to(DOWN * 2.92 + LEFT * 1.18)
        self.play(count_label.animate.move_to(DOWN * 2.92 + RIGHT * 1.45), Write(wrap_formula), run_time=0.8)
        self.wait(1.0)

        narrative_7 = Text(
            "Esa aritmética finita es la base que permite usar curvas elípticas en computación.",
            font="Cambria",
        ).scale(0.38).to_edge(UP)
        self.play(Transform(title, narrative_7))
        self.play(Indicate(formula_mod, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.wait(3)

    def field_to_point(self, x, y, p):
        spacing = 0.29
        center = DOWN * 0.12
        return center + RIGHT * ((x - (p - 1) / 2) * spacing) + UP * ((y - (p - 1) / 2) * spacing)

    def make_field_grid(self, p):
        grid = VGroup()

        for x in range(p):
            for y in range(p):
                dot = Dot(self.field_to_point(x, y, p), color=GRAY, radius=0.014)
                dot.set_opacity(0.45)
                grid.add(dot)

        for value, direction in [(0, DOWN), (p - 1, DOWN)]:
            label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.25)
            label.next_to(self.field_to_point(value, 0, p), direction, buff=0.1)
            grid.add(label)

        for value, direction in [(0, LEFT), (p - 1, LEFT)]:
            label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.25)
            label.next_to(self.field_to_point(0, value, p), direction, buff=0.1)
            grid.add(label)

        return grid

    def make_solution_cloud(self, p, a, b):
        cloud = VGroup()
        for x in range(p):
            rhs = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y - rhs) % p == 0:
                    dot = Dot(self.field_to_point(x, y, p), color=BLUE, radius=0.055)
                    cloud.add(dot)
        return cloud
