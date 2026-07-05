from manim import *
import numpy as np


class ZkSNARKs(Scene):
    def construct(self):
        title = self.top_text("zkSNARKs").scale(1.08)
        self.play(Write(title), run_time=0.9)

        circuit = self.make_circuit().move_to(UP * 0.45)
        secret_box = self.secret_box("testigo secreto", "w").move_to(LEFT * 3.55 + UP * 0.40)
        public_box = self.secret_box("dato público", "x", color=BLUE).move_to(RIGHT * 3.55 + UP * 0.40)
        bottom = self.bottom_text("Queremos probar que conocemos w tal que el cálculo público sale bien.")

        self.play(FadeIn(secret_box), FadeIn(public_box), Create(circuit), Write(bottom), run_time=2.0)
        self.wait(4.5)

        narrative_1 = self.top_text("Un zkSNARK convierte ese cálculo en restricciones algebraicas.")
        card_a = self.constraint_card("A(w,x)", YELLOW)
        card_b = self.constraint_card("B(w,x)", RED)
        card_c = self.constraint_card("C(w,x)", PURPLE)
        constraints = VGroup(
            card_a,
            Text("·", font="Cambria Math", color=WHITE).scale(0.75),
            card_b,
            Text("=", font="Cambria Math", color=WHITE).scale(0.62),
            card_c,
        ).arrange(RIGHT, buff=0.14)
        constraints.move_to(DOWN * 0.18)
        bottom_1 = self.bottom_text("cada puerta del circuito se traduce a una igualdad", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_1),
            ReplacementTransform(bottom, bottom_1),
            FadeOut(circuit),
            FadeIn(constraints),
            run_time=1.2,
        )
        self.wait(5.0)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1.5, 3.0, 1],
            x_length=7.2,
            y_length=4.15,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        ).shift(UP * 0.15)
        grid = self.add_grid(axes)
        poly_a = axes.plot(lambda x: 0.18 * (x + 2.0) * (x - 0.35) * (x - 2.0) + 1.15, color=YELLOW, stroke_width=4)
        poly_b = axes.plot(lambda x: -0.14 * (x + 1.7) * (x - 0.20) * (x - 1.85) + 0.95, color=RED, stroke_width=4)
        poly_c = axes.plot(lambda x: 0.10 * (x + 2.2) * (x - 0.65) * (x - 1.7) + 0.25, color=PURPLE, stroke_width=4)
        poly_labels = VGroup(
            Text("A(t)", font="Cambria Math", color=YELLOW).scale(0.38).move_to(LEFT * 2.85 + UP * 1.95),
            Text("B(t)", font="Cambria Math", color=RED).scale(0.38).move_to(LEFT * 2.15 + UP * 1.35),
            Text("C(t)", font="Cambria Math", color=PURPLE).scale(0.38).move_to(LEFT * 1.45 + DOWN * 0.25),
        )

        narrative_2 = self.top_text("Las restricciones se agrupan en polinomios A(t), B(t) y C(t).")
        bottom_2 = self.bottom_text("el testigo queda codificado dentro de esos polinomios", color=WHITE)
        self.play(
            Transform(title, narrative_2),
            ReplacementTransform(bottom_1, bottom_2),
            FadeOut(secret_box),
            FadeOut(public_box),
            FadeOut(constraints[1]),
            FadeOut(constraints[3]),
            Create(grid),
            Create(axes),
            ReplacementTransform(card_a, poly_a),
            ReplacementTransform(card_b, poly_b),
            ReplacementTransform(card_c, poly_c),
            FadeIn(poly_labels),
            run_time=2.0,
        )
        self.wait(5.2)

        fog = self.make_fog().move_to(ORIGIN)
        hidden_label = Text("w permanece oculto", font="Cambria", color=WHITE).scale(0.48).move_to(UP * 2.05)
        narrative_3 = self.top_text("Cero conocimiento significa: se prueba la validez sin revelar el testigo.")
        bottom_3 = self.bottom_text("el verificador ve una prueba, no los valores secretos", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_3),
            ReplacementTransform(bottom_2, bottom_3),
            FadeIn(fog),
            Write(hidden_label),
            run_time=1.3,
        )
        self.wait(5.0)

        tau = 0.65
        probe_line = DashedLine(axes.c2p(tau, -1.25), axes.c2p(tau, 2.65), color=GREEN, stroke_width=4, dash_length=0.12)
        probe_label = self.tau_box().move_to(RIGHT * 2.95 + UP * 1.70)
        probe_arrow = Arrow(probe_label.get_left(), axes.c2p(tau, 2.35), buff=0.10, color=GREEN, stroke_width=3)
        sample_points = VGroup(
            Dot(axes.c2p(tau, 0.18 * (tau + 2.0) * (tau - 0.35) * (tau - 2.0) + 1.15), color=YELLOW, radius=0.065),
            Dot(axes.c2p(tau, -0.14 * (tau + 1.7) * (tau - 0.20) * (tau - 1.85) + 0.95), color=RED, radius=0.065),
            Dot(axes.c2p(tau, 0.10 * (tau + 2.2) * (tau - 0.65) * (tau - 1.7) + 0.25), color=PURPLE, radius=0.065),
        )
        proof_card = self.proof_card().move_to(RIGHT * 3.25 + DOWN * 0.75)

        narrative_4 = self.top_text("La prueba solo contiene evaluaciones comprometidas en un punto secreto τ.")
        bottom_4 = self.bottom_text("A(τ), B(τ), C(τ) viajan sellados dentro de la prueba π", color=WHITE)
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            Create(probe_line),
            FadeIn(probe_label),
            Create(probe_arrow),
            run_time=1.2,
        )
        self.play(FadeIn(sample_points), FadeIn(proof_card), run_time=1.0)
        self.wait(5.5)

        pairing_check = VGroup(
            self.check_card("e(A,B)", PURPLE),
            Text("=", font="Cambria Math", color=WHITE).scale(0.68),
            self.check_card("e(C,G)", GREEN),
        ).arrange(RIGHT, buff=0.32)
        pairing_check.move_to(UP * 0.20)
        check = self.check_mark(GREEN).scale(1.05)
        check.next_to(pairing_check, RIGHT, buff=0.22)

        narrative_5 = self.top_text("El verificador usa pairings para comprobar la igualdad sin abrir la prueba.")
        bottom_5 = self.bottom_text("aquí entra el video anterior: los pairings verifican relaciones compactas", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, bottom_5),
            FadeOut(grid),
            FadeOut(axes),
            FadeOut(poly_a),
            FadeOut(poly_b),
            FadeOut(poly_c),
            FadeOut(poly_labels),
            FadeOut(fog),
            FadeOut(hidden_label),
            FadeOut(probe_line),
            FadeOut(probe_label),
            FadeOut(probe_arrow),
            FadeOut(sample_points),
            FadeOut(proof_card),
            FadeIn(pairing_check),
            run_time=1.5,
        )
        self.play(Create(check), Flash(check.get_center(), color=GREEN, flash_radius=0.75), run_time=0.9)
        self.wait(5.5)

        final_cards = VGroup(
            self.small_card("succinct", "prueba corta", BLUE),
            self.small_card("non-interactive", "un solo mensaje", PURPLE),
            self.small_card("zero knowledge", "w oculto", GREEN),
        ).arrange(RIGHT, buff=0.32)
        final_cards.move_to(UP * 0.20)
        narrative_6 = self.top_text("SNARK: prueba corta, no interactiva y sin revelar el secreto.")
        final_bottom = self.bottom_text("el verificador queda convencido, pero no aprende w", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_6),
            ReplacementTransform(bottom_5, final_bottom),
            FadeOut(pairing_check),
            FadeOut(check),
            FadeIn(final_cards),
            run_time=1.2,
        )
        self.play(Indicate(final_cards, color=GREEN, scale_factor=1.03), run_time=1.0)
        self.wait(6.0)

    def top_text(self, text, scale=0.60):
        mob = Text(text, font="Cambria").scale(scale)
        if mob.width > 12.4:
            mob.scale_to_fit_width(12.4)
        mob.to_edge(UP)
        return mob

    def bottom_text(self, text, color=WHITE, font="Cambria", scale=0.52):
        mob = Text(text, font=font, color=color).scale(scale)
        if mob.width > 11.8:
            mob.scale_to_fit_width(11.8)
        mob.move_to(DOWN * 3.12)
        return mob

    def make_circuit(self):
        nodes = {
            "x": LEFT * 2.00 + UP * 0.80,
            "w": LEFT * 2.00 + DOWN * 0.20,
            "×": LEFT * 0.45 + UP * 0.30,
            "+": RIGHT * 0.90 + UP * 0.30,
            "y": RIGHT * 2.15 + UP * 0.30,
        }
        edges = VGroup(
            Arrow(nodes["x"], nodes["×"], buff=0.16, color=GRAY, stroke_width=3),
            Arrow(nodes["w"], nodes["×"], buff=0.16, color=GRAY, stroke_width=3),
            Arrow(nodes["×"], nodes["+"], buff=0.16, color=GRAY, stroke_width=3),
            Arrow(nodes["+"], nodes["y"], buff=0.16, color=GRAY, stroke_width=3),
        )
        node_group = VGroup()
        for label, position in nodes.items():
            color = GREEN if label in ["×", "+"] else (BLUE if label in ["x", "y"] else YELLOW)
            circle = Circle(radius=0.25, color=color, stroke_width=3).move_to(position)
            text = Text(label, font="Cambria Math", color=color).scale(0.38).move_to(circle)
            node_group.add(VGroup(circle, text))
        return VGroup(edges, node_group)

    def secret_box(self, title, symbol, color=YELLOW):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.15,
            height=1.00,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        text = VGroup(
            Text(title, font="Cambria", color=WHITE).scale(0.30),
            Text(symbol, font="Cambria Math", color=color).scale(0.58),
        ).arrange(DOWN, buff=0.08)
        text.move_to(box)
        return VGroup(box, text)

    def constraint_card(self, text, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=1.45,
            height=0.72,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        label = Text(text, font="Cambria Math", color=color).scale(0.36)
        label.move_to(box)
        return VGroup(box, label)

    def add_grid(self, axes):
        lines = VGroup()
        for x in np.arange(-3, 3.1, 1):
            lines.add(Line(axes.c2p(x, -1.3), axes.c2p(x, 2.8), color=GRAY, stroke_width=1, stroke_opacity=0.18))
        for y in np.arange(-1, 2.1, 1):
            lines.add(Line(axes.c2p(-3, y), axes.c2p(3, y), color=GRAY, stroke_width=1, stroke_opacity=0.18))
        return lines

    def make_fog(self):
        fog = VGroup()
        for index in range(24):
            radius = 0.50 + 0.05 * (index % 5)
            center = np.array([
                2.5 * np.sin(index * 1.7),
                1.10 * np.cos(index * 1.1),
                0,
            ])
            circle = Circle(radius=radius, color=GRAY, stroke_width=1, stroke_opacity=0.05)
            circle.set_fill(GRAY, opacity=0.06)
            circle.move_to(center)
            fog.add(circle)
        return fog

    def proof_card(self):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=1.55,
            height=0.92,
            color=GREEN,
            fill_color="#102013",
            fill_opacity=0.92,
        )
        text = VGroup(
            Text("π", font="Cambria Math", color=GREEN).scale(0.62),
            Text("prueba", font="Cambria", color=WHITE).scale(0.28),
        ).arrange(DOWN, buff=0.04)
        text.move_to(box)
        return VGroup(box, text)

    def tau_box(self):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.30,
            height=0.88,
            color=GREEN,
            fill_color="#102013",
            fill_opacity=0.92,
        )
        text = VGroup(
            Text("τ secreto", font="Cambria Math", color=GREEN).scale(0.38),
            Text("punto de evaluación", font="Cambria", color=WHITE).scale(0.27),
        ).arrange(DOWN, buff=0.06)
        text.move_to(box)
        return VGroup(box, text)

    def check_card(self, text, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.10,
            height=0.82,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        label = Text(text, font="Cambria Math", color=color).scale(0.42)
        label.move_to(box)
        return VGroup(box, label)

    def check_mark(self, color=GREEN):
        return VGroup(
            Line(LEFT * 0.22 + DOWN * 0.02, LEFT * 0.02 + DOWN * 0.22, color=color, stroke_width=7),
            Line(LEFT * 0.02 + DOWN * 0.22, RIGHT * 0.32 + UP * 0.25, color=color, stroke_width=7),
        )

    def small_card(self, title, subtitle, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.45,
            height=1.05,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        text = VGroup(
            Text(title, font="Cambria Math", color=color).scale(0.34),
            Text(subtitle, font="Cambria", color=WHITE).scale(0.30),
        ).arrange(DOWN, buff=0.09)
        text.move_to(box)
        return VGroup(box, text)
