from manim import *
import numpy as np


class PairingsBilineales(Scene):
    def construct(self):
        title = self.top_text("Pairings bilineales").scale(1.02)
        self.play(Write(title), run_time=0.9)

        left_group = self.make_source_group("G₁", BLUE).move_to(LEFT * 3.25 + UP * 0.65)
        right_group = self.make_source_group("G₂", RED).move_to(RIGHT * 3.25 + UP * 0.65)
        target_group = self.make_target_group().move_to(DOWN * 1.65)

        p_obj = self.group_point(left_group, "P", YELLOW, 0.35, self.curve_y(0.35))
        q_obj = self.group_point(right_group, "Q", RED, -0.35, self.curve_y(-0.35))
        bottom = self.bottom_text("Un pairing toma dos puntos de dos grupos y produce un valor en un tercer grupo.")

        self.play(Create(left_group), Create(right_group), FadeIn(p_obj), FadeIn(q_obj), Write(bottom), run_time=2.0)
        self.wait(4.5)

        output = Dot(target_group.get_center() + RIGHT * 0.55, color=PURPLE, radius=0.090)
        output_label = Text("e(P,Q)", font="Cambria Math", color=PURPLE).scale(0.42)
        output_label.next_to(output, RIGHT, buff=0.12)

        narrative_1 = self.top_text("El mapa se escribe e(P,Q): mezcla P y Q en un grupo multiplicativo.")
        bottom_1 = self.make_formula(["e", "(", "P", ",", "Q", ")", "∈", "Gₜ"], [PURPLE, WHITE, YELLOW, WHITE, RED, WHITE, WHITE, PURPLE], scale=0.58)
        self.play(Transform(title, narrative_1), ReplacementTransform(bottom, bottom_1), Create(target_group), run_time=1.1)
        funnel = VGroup(
            Arrow(p_obj[0].get_center(), target_group.get_center() + LEFT * 0.30 + UP * 0.35, buff=0.12, color=GREEN, stroke_width=4),
            Arrow(q_obj[0].get_center(), target_group.get_center() + RIGHT * 0.30 + UP * 0.35, buff=0.12, color=GREEN, stroke_width=4),
        )
        self.play(Create(funnel), run_time=0.8)
        self.play(FadeIn(output), Write(output_label), Flash(output.get_center(), color=PURPLE, flash_radius=0.65), run_time=1.0)
        self.wait(5.5)

        a_target = left_group[0].c2p(-0.55, -self.curve_y(-0.55))
        b_target = right_group[0].c2p(0.62, self.curve_y(0.62))
        a_label = Text("aP", font="Cambria Math", color=YELLOW).scale(0.42).next_to(a_target, UP, buff=0.12)
        b_label = Text("bQ", font="Cambria Math", color=RED).scale(0.42).next_to(b_target, UP, buff=0.12)
        p_path = CurvedArrow(p_obj[0].get_center(), a_target, angle=-TAU / 6, color=YELLOW, stroke_width=3, tip_length=0.16)
        q_path = CurvedArrow(q_obj[0].get_center(), b_target, angle=TAU / 6, color=RED, stroke_width=3, tip_length=0.16)
        scalar_a = self.scalar_stack("a veces", YELLOW).next_to(left_group, DOWN, buff=0.18)
        scalar_b = self.scalar_stack("b veces", RED).next_to(right_group, DOWN, buff=0.18)

        narrative_2 = self.top_text("Bilineal significa que escalar antes del pairing equivale a escalar el resultado.")
        bottom_2 = self.make_formula(["e", "(", "aP", ",", "bQ", ")", "=", "e(P,Q)", "^ab"], [PURPLE, WHITE, YELLOW, WHITE, RED, WHITE, WHITE, PURPLE, GREEN], scale=0.56)
        self.play(Transform(title, narrative_2), ReplacementTransform(bottom_1, bottom_2), FadeOut(output_label), FadeOut(output), run_time=1.2)
        self.wait(1.0)
        self.play(Create(p_path), Create(q_path), FadeIn(scalar_a), FadeIn(scalar_b), run_time=0.9)
        self.play(
            p_obj[0].animate.move_to(a_target),
            q_obj[0].animate.move_to(b_target),
            Transform(p_obj[1], a_label),
            Transform(q_obj[1], b_label),
            run_time=1.4,
            rate_func=smooth,
        )
        self.play(FadeOut(p_path), FadeOut(q_path), run_time=0.4)
        self.wait(5.8)

        exp_y = -0.35
        base_value = self.value_card("g = e(P,Q)", PURPLE).move_to(np.array([-2.15, exp_y, 0]))
        powered_value = self.value_card("g^ab", GREEN).move_to(np.array([1.90, exp_y, 0]))
        power_arrow = Arrow(base_value.get_right(), powered_value.get_left(), buff=0.16, color=GREEN, stroke_width=4)
        power_label = Text("elevar a ab", font="Cambria Math", color=GREEN).scale(0.36)
        power_label.next_to(power_arrow, UP, buff=0.16)
        exp_group = VGroup(base_value, power_arrow, power_label, powered_value)
        narrative_3 = self.top_text("Los factores a y b salen juntos como un exponente ab.")
        bottom_3 = self.bottom_text("en Gₜ multiplicar muchas veces se escribe como una potencia", color=GREEN, font="Cambria Math")
        self.play(Transform(title, narrative_3), ReplacementTransform(bottom_2, bottom_3), FadeIn(base_value), run_time=1.0)
        self.play(Create(power_arrow), Write(power_label), FadeIn(powered_value), run_time=1.0)
        self.play(Indicate(powered_value, color=GREEN, scale_factor=1.08), run_time=0.9)
        self.wait(5.5)

        left_check = self.check_card("e(aP,bQ)", PURPLE)
        right_check = self.check_card("e(P,Q)ᵃᵇ", GREEN)
        equals = Text("=", font="Cambria Math", color=WHITE).scale(0.68)
        check_group = VGroup(left_check, equals, right_check).arrange(RIGHT, buff=0.35)
        check_group.move_to(UP * 0.10)
        check_mark = self.check_mark(color=GREEN).scale(1.05)
        check_mark.next_to(check_group, RIGHT, buff=0.25)

        narrative_4 = self.top_text("Esto permite verificar relaciones algebraicas sin rehacer toda la cuenta punto a punto.")
        bottom_4 = self.bottom_text("si ambos lados coinciden, la relación entre secretos era correcta")
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            FadeOut(funnel),
            FadeOut(exp_group),
            FadeOut(scalar_a),
            FadeOut(scalar_b),
            FadeOut(left_group),
            FadeOut(right_group),
            FadeOut(target_group),
            FadeOut(p_obj),
            FadeOut(q_obj),
            FadeIn(check_group),
            run_time=1.4,
        )
        self.play(Create(check_mark), Flash(check_mark.get_center(), color=GREEN, flash_radius=0.70), run_time=0.9)
        self.wait(5.5)

        use_cases = VGroup(
            self.small_card("firmas BLS", "agregar muchas firmas", BLUE),
            self.small_card("zkSNARKs", "verificar pruebas cortas", PURPLE),
        ).arrange(RIGHT, buff=0.55)
        use_cases.move_to(UP * 0.15)
        narrative_5 = self.top_text("Por eso los pairings aparecen en firmas agregadas y pruebas de conocimiento cero.")
        final_bottom = self.bottom_text("pairing = puente algebraico entre puntos y verificaciones compactas", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, final_bottom),
            FadeOut(check_group),
            FadeOut(check_mark),
            FadeIn(use_cases),
            run_time=1.2,
        )
        self.play(Indicate(use_cases, color=GREEN, scale_factor=1.03), run_time=1.0)
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

    def make_source_group(self, label, color):
        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=2.6,
            y_length=2.6,
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.22, "stroke_width": 1},
            axis_config={"stroke_color": GRAY, "stroke_width": 2},
        )
        curve = plane.plot_implicit_curve(
            lambda x, y: y**2 - (x**3 - x + 0.55),
            color=color,
            stroke_width=3,
        )
        title = Text(label, font="Cambria Math", color=color).scale(0.45)
        title.next_to(plane, UP, buff=0.12)
        return VGroup(plane, curve, title)

    def make_target_group(self):
        rings = VGroup(*[Circle(radius=0.28 + 0.22 * i, color=GRAY, stroke_width=1, stroke_opacity=0.45) for i in range(4)])
        values = VGroup(
            self.target_value("g", RIGHT * 0.52, 0.28),
            self.target_value("g²", UP * 0.42 + LEFT * 0.18, 0.24),
            self.target_value("g³", DOWN * 0.30 + LEFT * 0.45, 0.24),
        )
        label = VGroup(
            Text("Gₜ", font="Cambria Math", color=PURPLE).scale(0.45),
            Text("grupo multiplicativo", font="Cambria", color=WHITE).scale(0.24),
        ).arrange(DOWN, buff=0.04)
        label.next_to(rings, DOWN, buff=0.12)
        return VGroup(rings, values, label)

    def target_value(self, text, position, scale):
        dot = Dot(position, color=PURPLE, radius=0.032)
        label = Text(text, font="Cambria Math", color=PURPLE).scale(scale)
        label.next_to(dot, RIGHT, buff=0.04)
        return VGroup(dot, label)

    def group_point(self, group, label, color, x, y):
        plane = group[0]
        dot = Dot(plane.c2p(x, y), color=color, radius=0.085)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(0.44)
        text.next_to(dot, UP, buff=0.08)
        return VGroup(dot, text)

    def curve_y(self, x):
        return np.sqrt(max(0, x**3 - x + 0.55))

    def make_formula(self, parts, colors, scale=0.58):
        formula = VGroup(
            *[
                Text(
                    part,
                    font="Cambria Math",
                    slant=ITALIC if part not in ["(", ")", ",", "=", "∈"] else NORMAL,
                    color=color,
                )
                for part, color in zip(parts, colors)
            ]
        )
        formula.arrange(RIGHT, buff=0.10).scale(scale)
        formula.move_to(DOWN * 3.12)
        return formula

    def scalar_stack(self, text, color):
        dots = VGroup(*[Dot(RIGHT * 0.18 * i, color=color, radius=0.035) for i in range(4)])
        label = Text(text, font="Cambria", color=color).scale(0.30)
        label.next_to(dots, DOWN, buff=0.08)
        return VGroup(dots, label)

    def check_card(self, text, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.25,
            height=0.86,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        label = Text(text, font="Cambria Math", color=color).scale(0.42)
        label.move_to(box)
        return VGroup(box, label)

    def value_card(self, text, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=1.95,
            height=0.78,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        label = Text(text, font="Cambria Math", color=color).scale(0.38)
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
            width=2.75,
            height=1.10,
            color=color,
            fill_color="#151515",
            fill_opacity=0.90,
        )
        text = VGroup(
            Text(title, font="Cambria Math", color=color).scale(0.42),
            Text(subtitle, font="Cambria", color=WHITE).scale(0.31),
        ).arrange(DOWN, buff=0.10)
        text.move_to(box)
        return VGroup(box, text)
