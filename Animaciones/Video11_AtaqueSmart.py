from manim import *


class AtaqueSmart(ThreeDScene):
    def construct(self):
        title = self.top_text("Ataque de Smart", scale=0.64)
        self.show_fixed(title, Write(title), run_time=0.9)

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=7.2,
            y_length=5.1,
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.24, "stroke_width": 1},
            axis_config={"stroke_color": GRAY, "stroke_width": 2},
        ).shift(DOWN * 0.05)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        points = [
            (-3.1, -2.0),
            (-2.2, 1.1),
            (-1.3, -0.5),
            (-0.4, 1.9),
            (0.6, -1.4),
            (1.5, 0.6),
            (2.3, -2.2),
            (3.1, 1.5),
        ]
        background_cloud = VGroup(
            *[
                Dot(plane.c2p((i % 9) - 4, (i * 5 % 7) - 3), color=GRAY, radius=0.022).set_opacity(0.35)
                for i in range(45)
            ]
        )
        curve_points = VGroup(*[Dot(plane.c2p(x, y), color=BLUE, radius=0.055) for x, y in points])

        field_label = Text("E(𝔽ₚ)", font="Cambria Math", color=BLUE).scale(0.52)
        field_label.to_edge(LEFT, buff=0.30).shift(UP * 2.10)
        bottom = Text("Empezamos con una curva anómala: #E(𝔽ₚ) = p.", font="Cambria", color=WHITE).scale(0.47)
        bottom.move_to(DOWN * 3.35)
        self.add_fixed_in_frame_mobjects(field_label, bottom)
        self.play(Create(plane), FadeIn(background_cloud), FadeIn(curve_points), Write(field_label), Write(bottom), run_time=2.0)
        self.wait(2.0)

        p_dot = Dot(plane.c2p(-2.2, 1.1), color=YELLOW, radius=0.095)
        q_dot = Dot(plane.c2p(1.5, 0.6), color=RED, radius=0.095)
        p_label = Text("P", font="Cambria Math", slant=ITALIC, color=YELLOW).scale(0.44)
        q_label = Text("Q", font="Cambria Math", slant=ITALIC, color=RED).scale(0.44)
        p_label.next_to(p_dot, UP + LEFT, buff=0.10)
        q_label.next_to(q_dot, UP + RIGHT, buff=0.10)
        point_group = VGroup(p_dot, q_dot, p_label, q_label)

        narrative_1 = self.top_text("Como antes, el atacante conoce P y Q = kP, pero no conoce k.")
        bottom_1 = self.make_formula(
            ["Q", "=", "kP"],
            [RED, WHITE, YELLOW],
            scale=0.66,
        )
        title = self.replace_fixed(title, narrative_1)
        bottom = self.replace_fixed(bottom, bottom_1)
        self.play(FadeIn(point_group), run_time=0.8)
        self.play(Flash(q_dot.get_center(), color=RED, flash_radius=0.55), run_time=0.9)
        self.wait(2.4)

        self.play(FadeOut(p_label), FadeOut(q_label), run_time=0.4)

        layers = VGroup()
        for z in [0.70, 1.40, 2.10]:
            layer = plane.copy()
            layer.set_stroke(color=GRAY, width=1, opacity=0.22)
            layer.shift(OUT * z)
            layers.add(layer)

        lift_note = self.explain_box(
            ["p-ádico", "más precisión:", "mod p, p², p³..."],
            color=PURPLE,
        ).move_to(RIGHT * 4.05 + UP * 1.75)
        narrative_2 = self.top_text("Smart levanta la curva: no mira solo 𝔽ₚ, sino aproximaciones p-ádicas.")
        bottom_2 = VGroup(
            Text("p-ádico = estudiar la misma información con precisión p, p², p³, ...", font="Cambria", color=PURPLE).scale(0.41),
            Text("Es como pasar de una sombra modular a varias capas de detalle.", font="Cambria", color=WHITE).scale(0.36),
        ).arrange(DOWN, buff=0.10).move_to(DOWN * 3.22)
        title = self.replace_fixed(title, narrative_2)
        bottom = self.replace_fixed(bottom, bottom_2)
        self.show_fixed(lift_note, Write(lift_note), run_time=0.8)
        self.move_camera(phi=64 * DEGREES, theta=-42 * DEGREES, zoom=0.86, run_time=1.7)
        self.play(LaggedStart(*[Create(layer) for layer in layers], lag_ratio=0.25), run_time=1.9)
        self.wait(2.5)
        self.play(FadeOut(lift_note), run_time=0.35)
        self.remove(lift_note)

        lifted_p = Dot(plane.c2p(-2.2, 1.1) + OUT * 2.10, color=YELLOW, radius=0.080)
        lifted_q = Dot(plane.c2p(1.5, 0.6) + OUT * 2.10, color=RED, radius=0.080)
        lift_lines = VGroup(
            DashedLine(p_dot.get_center(), lifted_p.get_center(), color=YELLOW, stroke_width=3, dash_length=0.12),
            DashedLine(q_dot.get_center(), lifted_q.get_center(), color=RED, stroke_width=3, dash_length=0.12),
        )

        narrative_3 = self.top_text("Los puntos también se levantan y conservan información p-ádica.")
        bottom_3 = self.make_formula(
            ["P", ",", "Q", "→", "P̃", ",", "Q̃"],
            [YELLOW, WHITE, RED, WHITE, YELLOW, WHITE, RED],
            scale=0.58,
        )
        title = self.replace_fixed(title, narrative_3)
        bottom = self.replace_fixed(bottom, bottom_3)
        self.play(Create(lift_lines), FadeIn(lifted_p), FadeIn(lifted_q), run_time=1.4)
        self.wait(2.5)

        path_points = [
            plane.c2p(-2.2, 1.1) + OUT * 2.10,
            plane.c2p(-0.7, -1.2) + OUT * 1.35,
            plane.c2p(0.8, 1.8) + OUT * 0.78,
            plane.c2p(1.5, 0.6) + OUT * 2.10,
        ]
        crooked_path = VMobject(color=ORANGE, stroke_width=5).set_points_as_corners(path_points)
        straight_path = Line3D(path_points[0], path_points[-1], color=GREEN, thickness=0.035)

        narrative_4 = self.top_text("En una curva anómala, esa información extra convierte los saltos en una relación lineal.")
        bottom_4 = Text("salto discreto  →  relación lineal", font="Cambria Math", color=GREEN).scale(0.56)
        bottom_4.move_to(DOWN * 3.35)
        title = self.replace_fixed(title, narrative_4)
        bottom = self.replace_fixed(bottom, bottom_4)
        self.play(Create(crooked_path), run_time=1.1)
        self.play(ReplacementTransform(crooked_path, straight_path), Flash(straight_path.get_center(), color=GREEN), run_time=1.4)
        self.wait(2.5)

        psi_info = VGroup(
            Text("ψ es el logaritmo p-ádico:", font="Cambria Math", color=PURPLE).scale(0.43),
            Text("toma un punto levantado y devuelve un número p-ádico.", font="Cambria", color=WHITE).scale(0.37),
        ).arrange(DOWN, buff=0.08).move_to(DOWN * 2.14)
        relation = self.make_formula(
            ["ψ(Q̃)", "=", "k", "ψ(P̃)"],
            [RED, WHITE, YELLOW, YELLOW],
            scale=0.54,
        ).move_to(DOWN * 2.88)
        result = self.make_formula(
            ["k", "=", "ψ(Q̃)", "/", "ψ(P̃)"],
            [YELLOW, WHITE, RED, WHITE, YELLOW],
            scale=0.64,
        )
        narrative_5 = self.top_text("El mapa p-ádico deja a k como una división ordinaria.")
        title = self.replace_fixed(title, narrative_5)
        self.play(FadeOut(bottom), run_time=0.35)
        self.remove(bottom)
        self.show_fixed(psi_info, FadeIn(psi_info), run_time=0.7)
        self.show_fixed(relation, Write(relation), run_time=0.8)
        self.wait(1.5)
        self.show_fixed(result, Write(result), run_time=0.8)
        self.play(Indicate(result[0], color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.wait(2.5)

        warning_box = RoundedRectangle(
            corner_radius=0.08,
            width=4.95,
            height=0.90,
            color=RED,
            fill_color="#240B12",
            fill_opacity=0.90,
        ).move_to(DOWN * 2.05)
        warning_text = Text("no usar curvas con #E(𝔽ₚ)=p", font="Cambria Math", color=RED).scale(0.48)
        warning_text.move_to(warning_box)
        final_bottom = Text("criterio de seguridad: #E(𝔽ₚ) ≠ p", font="Cambria Math", color=GREEN).scale(0.58)
        final_bottom.move_to(DOWN * 3.35)
        final_narrative = Text(
            "Smart no rompe todas las curvas: rompe este caso especial.",
            font="Cambria",
        ).scale(0.56).to_edge(UP)
        title = self.replace_fixed(title, final_narrative)
        self.play(FadeOut(psi_info), run_time=0.35)
        self.remove(psi_info)
        self.play(FadeOut(relation), run_time=0.35)
        self.remove(relation)
        bottom = self.replace_fixed(result, final_bottom)
        self.show_fixed(warning_box, FadeIn(warning_box), run_time=0.5)
        self.show_fixed(warning_text, Write(warning_text), run_time=0.6)
        self.play(
            Flash(warning_box.get_center(), color=RED, flash_radius=0.80),
            run_time=0.9,
        )
        self.wait(4.0)

    def show_fixed(self, mob, animation, run_time=0.8):
        self.add_fixed_in_frame_mobjects(mob)
        self.play(animation, run_time=run_time)
        return mob

    def replace_fixed(self, old, new, run_time=0.45):
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), FadeIn(new), run_time=run_time)
        self.remove(old)
        return new

    def top_text(self, text, scale=0.55):
        mob = Text(text, font="Cambria").scale(scale)
        if mob.width > 12.4:
            mob.scale_to_fit_width(12.4)
        mob.to_edge(UP)
        return mob

    def explain_box(self, lines, color=PURPLE):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.65,
            height=1.02,
            color=color,
            fill_color="#15101F",
            fill_opacity=0.86,
        )
        text = VGroup(
            *[
                Text(line, font="Cambria Math" if index == 0 else "Cambria", color=color if index == 0 else WHITE).scale(
                    0.34 if index == 0 else 0.28
                )
                for index, line in enumerate(lines)
            ]
        ).arrange(DOWN, buff=0.05)
        text.move_to(box)
        return VGroup(box, text)

    def make_formula(self, parts, colors, scale=0.58):
        formula = VGroup(
            *[
                Text(
                    part,
                    font="Cambria Math",
                    slant=ITALIC if part not in ["=", "→", ",", "/"] else NORMAL,
                    color=color,
                )
                for part, color in zip(parts, colors)
            ]
        )
        formula.arrange(RIGHT, buff=0.14).scale(scale)
        formula.move_to(DOWN * 3.35)
        return formula
