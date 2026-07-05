from manim import *


class CurvasAnomalas(Scene):
    def construct(self):
        p = 17
        normal_a, normal_b = 2, 2
        anomalous_a, anomalous_b = 1, 3
        normal_count = self.curve_order(p, normal_a, normal_b)
        anomalous_count = self.curve_order(p, anomalous_a, anomalous_b)

        left = LEFT * 2.55 + DOWN * 0.05
        right = RIGHT * 2.55 + DOWN * 0.05

        title = Text("Curvas anómalas", font="Cambria").scale(0.61).to_edge(UP)
        self.play(Write(title))

        normal_grid = self.make_field_grid(p, left)
        anomalous_grid = self.make_field_grid(p, right)
        normal_cloud = self.make_solution_cloud(p, normal_a, normal_b, left)
        anomalous_cloud = self.make_solution_cloud(p, anomalous_a, anomalous_b, right)

        normal_name = Text("curva no anómala", font="Cambria", color=BLUE).scale(0.42)
        anomalous_name = Text("curva anómala", font="Cambria", color=RED).scale(0.42)
        normal_name.move_to(left + UP * 2.05)
        anomalous_name.move_to(right + UP * 2.05)

        normal_formula = Text("y² ≡ x³ + 2x + 2", font="Cambria Math", color=BLUE).scale(0.38)
        anomalous_formula = Text("y² ≡ x³ + x + 3", font="Cambria Math", color=RED).scale(0.38)
        normal_formula.next_to(normal_name, DOWN, buff=0.12)
        anomalous_formula.next_to(anomalous_name, DOWN, buff=0.12)

        bottom_formula = Text("trabajamos en 𝔽₁₇", font="Cambria Math", color=WHITE).scale(0.58)
        bottom_formula.move_to(DOWN * 3.35)

        self.play(
            Create(normal_grid),
            Create(anomalous_grid),
            LaggedStart(*[GrowFromCenter(dot) for dot in normal_cloud], lag_ratio=0.02),
            LaggedStart(*[GrowFromCenter(dot) for dot in anomalous_cloud], lag_ratio=0.02),
            FadeIn(normal_name),
            FadeIn(anomalous_name),
            FadeIn(normal_formula),
            FadeIn(anomalous_formula),
            Write(bottom_formula),
            run_time=2.6,
        )
        self.wait(1.4)

        narrative_1 = Text(
            "La seguridad no depende solo de la fórmula: también importa cuántos puntos tiene la curva.",
            font="Cambria",
        ).scale(0.43).to_edge(UP)
        count_formula = VGroup(
            Text("#E(𝔽ₚ)", font="Cambria Math", color=WHITE).scale(0.48),
            Text("número de puntos de E sobre 𝔽ₚ, incluido 𝒪", font="Cambria Math", color=WHITE).scale(0.40),
        ).arrange(DOWN, buff=0.10)
        count_formula.move_to(DOWN * 3.25)
        self.play(Transform(title, narrative_1), ReplacementTransform(bottom_formula, count_formula), run_time=1.2)
        self.wait(4.0)

        normal_count_label = Text(f"#E(𝔽₁₇) = {normal_count}", font="Cambria Math", color=BLUE).scale(0.44)
        anomalous_count_label = Text(f"#E(𝔽₁₇) = {anomalous_count}", font="Cambria Math", color=RED).scale(0.44)
        normal_count_label.move_to(left + DOWN * 2.12)
        anomalous_count_label.move_to(right + DOWN * 2.12)

        narrative_2 = Text(
            "En una curva normal, el número de puntos no coincide exactamente con p.",
            font="Cambria",
        ).scale(0.50).to_edge(UP)
        normal_bottom = Text("#E(𝔽₁₇) = 19, pero p = 17", font="Cambria Math", color=BLUE).scale(0.56)
        normal_bottom.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_2), ReplacementTransform(count_formula, normal_bottom), run_time=1.2)
        self.play(FadeIn(normal_count_label), Indicate(normal_cloud, color=BLUE, scale_factor=1.03), run_time=1.2)
        self.wait(3.8)

        narrative_3 = Text(
            "Una curva anómala es el caso peligroso: su número de puntos es justo p.",
            font="Cambria",
        ).scale(0.49).to_edge(UP)
        anomalous_bottom = Text("#E(𝔽₁₇) = 17 = p", font="Cambria Math", color=RED).scale(0.62)
        anomalous_bottom.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_3), ReplacementTransform(normal_bottom, anomalous_bottom), run_time=1.2)
        self.play(FadeIn(anomalous_count_label), Indicate(anomalous_cloud, color=RED, scale_factor=1.04), run_time=1.2)
        self.wait(4.0)

        narrative_4 = Text(
            "La traza de Frobenius mide esa diferencia: t = p + 1 - #E(𝔽ₚ).",
            font="Cambria",
        ).scale(0.48).to_edge(UP)
        trace_normal = Text("t = 17 + 1 - 19 = -1", font="Cambria Math", color=BLUE).scale(0.34)
        trace_anomalous = Text("t = 17 + 1 - 17 = 1", font="Cambria Math", color=RED).scale(0.34)
        trace_normal.next_to(normal_count_label, DOWN, buff=0.20)
        trace_anomalous.next_to(anomalous_count_label, DOWN, buff=0.20)
        trace_group = VGroup(trace_normal, trace_anomalous)
        trace_bottom = Text("t = 1 marca la anomalía", font="Cambria Math", color=RED).scale(0.58)
        trace_bottom.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_4), ReplacementTransform(anomalous_bottom, trace_bottom), run_time=1.2)
        self.play(FadeIn(trace_group), run_time=1.1)
        self.wait(4.0)

        warning_box = RoundedRectangle(
            corner_radius=0.08,
            width=2.85,
            height=0.86,
            color=RED,
            fill_color="#240B12",
            fill_opacity=0.92,
        ).move_to(right + DOWN * 0.10)
        warning_text = Text("no usar en criptografía", font="Cambria Math", color=RED).scale(0.44)
        warning_text.move_to(warning_box)

        narrative_5 = Text(
            "Cuando #E(𝔽ₚ)=p, ataques especiales reducen el logaritmo discreto a un problema más fácil.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        attack_bottom = Text("curva anómala  →  atajo matemático", font="Cambria Math", color=RED).scale(0.56)
        attack_bottom.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_5), ReplacementTransform(trace_bottom, attack_bottom), run_time=1.2)
        self.play(FadeIn(warning_box), Write(warning_text), Flash(anomalous_count_label, color=RED, flash_radius=0.70), run_time=1.2)
        self.wait(4.2)

        narrative_6 = Text(
            "Por eso los estándares descartan curvas con #E(𝔽ₚ) = p antes de usarlas.",
            font="Cambria",
        ).scale(0.51).to_edge(UP)
        safe_box = SurroundingRectangle(normal_count_label, color=GREEN, buff=0.14)
        bad_box = SurroundingRectangle(anomalous_count_label, color=RED, buff=0.14)
        final_bottom = Text("criterio básico: #E(𝔽ₚ) ≠ p", font="Cambria Math", color=GREEN).scale(0.60)
        final_bottom.move_to(DOWN * 3.35)
        self.play(
            Transform(title, narrative_6),
            ReplacementTransform(attack_bottom, final_bottom),
            FadeOut(warning_box),
            FadeOut(warning_text),
            FadeOut(trace_group),
            run_time=1.2,
        )
        self.play(Create(safe_box), Create(bad_box), run_time=0.9)
        self.play(Indicate(final_bottom, color=GREEN, scale_factor=1.05), run_time=1.0)
        self.wait(4.5)

    def curve_order(self, p, a, b):
        count = 1
        for x in range(p):
            rhs = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y - rhs) % p == 0:
                    count += 1
        return count

    def field_to_point(self, x, y, p, offset):
        spacing = 0.18
        return offset + RIGHT * ((x - (p - 1) / 2) * spacing) + UP * ((y - (p - 1) / 2) * spacing)

    def make_field_grid(self, p, offset):
        grid = VGroup()
        for x in range(p):
            for y in range(p):
                dot = Dot(self.field_to_point(x, y, p, offset), color=GRAY, radius=0.010)
                dot.set_opacity(0.42)
                grid.add(dot)

        for value in [0, p - 1]:
            x_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.20)
            x_label.next_to(self.field_to_point(value, 0, p, offset), DOWN, buff=0.07)
            y_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.20)
            y_label.next_to(self.field_to_point(0, value, p, offset), LEFT, buff=0.07)
            grid.add(x_label, y_label)

        return grid

    def make_solution_cloud(self, p, a, b, offset):
        cloud = VGroup()
        for x in range(p):
            rhs = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y - rhs) % p == 0:
                    cloud.add(Dot(self.field_to_point(x, y, p, offset), color=BLUE, radius=0.036))
        return cloud
