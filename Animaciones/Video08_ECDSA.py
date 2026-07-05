from manim import *


class ECDSA(Scene):
    def construct(self):
        p = 17
        a = 2
        b = 2
        order = 19
        base = (5, 1)
        private_key = 5
        nonce = 3
        hash_value = 9
        public_key = self.ec_mul(private_key, base, p, a)
        nonce_point = self.ec_mul(nonce, base, p, a)
        r_value = nonce_point[0] % order
        s_value = (pow(nonce, -1, order) * (hash_value + r_value * private_key)) % order

        grid_offset = RIGHT * 2.15 + DOWN * 0.10
        message_center = LEFT * 3.10 + UP * 0.50

        title = Text("Firmas digitales con ECDSA", font="Cambria").scale(0.61).to_edge(UP)
        self.play(Write(title))

        grid = self.make_field_grid(p, grid_offset)
        cloud = self.make_solution_cloud(p, a, b, grid_offset)
        formula = Text("y² ≡ x³ + 2x + 2   (mod 17)", font="Cambria Math", color=WHITE).scale(0.58)
        formula.move_to(DOWN * 3.45)
        self.play(
            Create(grid),
            LaggedStart(*[GrowFromCenter(dot) for dot in cloud], lag_ratio=0.02),
            Write(formula),
            run_time=2.4,
        )

        narrative_1 = Text(
            "ECDSA permite firmar un mensaje sin publicar la clave privada.",
            font="Cambria",
        ).scale(0.55).to_edge(UP)
        message_box = RoundedRectangle(
            corner_radius=0.08,
            width=1.55,
            height=0.88,
            color=WHITE,
            fill_color="#182033",
            fill_opacity=0.90,
        ).move_to(message_center)
        message_label = Text("mensaje", font="Cambria", color=WHITE).scale(0.36).move_to(message_box)
        self.play(Transform(title, narrative_1), run_time=1.2)
        self.play(FadeIn(message_box), Write(message_label), run_time=1.1)
        self.wait(2.3)

        narrative_2 = Text(
            "Primero se resume el mensaje en un hash H(m).",
            font="Cambria",
        ).scale(0.58).to_edge(UP)
        hash_box = RoundedRectangle(
            corner_radius=0.08,
            width=1.25,
            height=0.82,
            color=GREEN,
            fill_color="#06170F",
            fill_opacity=0.90,
        ).move_to(LEFT * 1.35 + UP * 0.50)
        hash_box.set_z_index(1)
        hash_label = Text("H(m) = 9", font="Cambria Math", color=GREEN).scale(0.42).move_to(hash_box)
        hash_label.set_z_index(3)
        hash_arrow = Arrow(
            message_box.get_right(),
            hash_box.get_left(),
            buff=0.12,
            color=GREEN,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.08,
        )
        hash_formula = Text("H(m) = 9", font="Cambria Math", color=GREEN).scale(0.58).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_2), ReplacementTransform(formula, hash_formula), run_time=1.2)
        self.play(Create(hash_arrow), FadeIn(hash_box), ReplacementTransform(message_label.copy(), hash_label), run_time=1.3)
        self.wait(2.5)

        narrative_3 = Text(
            "El firmante guarda una clave privada d y publica Q = dG.",
            font="Cambria",
        ).scale(0.54).to_edge(UP)
        base_obj = self.point_with_label(base, p, "G", GREEN, DOWN + RIGHT, grid_offset, scale=0.40)
        public_obj = self.point_with_label(public_key, p, "Q", YELLOW, DOWN + RIGHT, grid_offset, scale=0.40)
        private_text = Text("d = 5 privado", font="Cambria Math", color=YELLOW).scale(0.48)
        private_text.move_to(LEFT * 3.10 + DOWN * 0.35)
        public_formula = Text("Q = dG", font="Cambria Math", color=YELLOW).scale(0.62).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_3), ReplacementTransform(hash_formula, public_formula), run_time=1.2)
        self.play(FadeIn(base_obj), FadeIn(private_text), run_time=1.0)
        self.play(TransformFromCopy(base_obj[0], public_obj[0]), FadeIn(public_obj[1]), run_time=1.3)
        self.play(Flash(public_obj[0], color=YELLOW, flash_radius=0.45), run_time=1.0)
        self.wait(2.5)

        narrative_4 = Text(
            "Para cada firma se elige un nonce k nuevo y se calcula R = kG.",
            font="Cambria",
        ).scale(0.53).to_edge(UP)
        nonce_text = Text("k = 3 nuevo", font="Cambria Math", color=PURPLE).scale(0.48)
        nonce_text.next_to(private_text, DOWN, buff=0.22)
        nonce_obj = self.point_with_label(nonce_point, p, "R", PURPLE, UP + RIGHT, grid_offset, scale=0.40)
        nonce_formula = Text("R = kG", font="Cambria Math", color=PURPLE).scale(0.62).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_4), ReplacementTransform(public_formula, nonce_formula), run_time=1.2)
        self.play(FadeIn(nonce_text), TransformFromCopy(base_obj[0], nonce_obj[0]), FadeIn(nonce_obj[1]), run_time=1.4)
        self.play(Flash(nonce_obj[0], color=PURPLE, flash_radius=0.45), run_time=1.0)
        self.wait(2.5)

        narrative_5 = Text(
            "La primera mitad de la firma es r, la coordenada x del punto R.",
            font="Cambria",
        ).scale(0.53).to_edge(UP)
        r_formula = Text(f"r = xR = {r_value}", font="Cambria Math", color=PURPLE).scale(0.62).move_to(DOWN * 2.85)
        r_marker = DashedLine(
            nonce_obj[0].get_center(),
            self.field_to_point(nonce_point[0], 0, p, grid_offset),
            color=PURPLE,
            stroke_width=3,
        )
        r_label = Text("xR", font="Cambria Math", color=PURPLE).scale(0.38)
        r_label.next_to(r_marker, RIGHT, buff=0.08).shift(UP * 0.18)
        self.play(Transform(title, narrative_5), ReplacementTransform(nonce_formula, r_formula), run_time=1.2)
        self.play(Create(r_marker), FadeIn(r_label), run_time=1.0)
        self.wait(2.5)

        narrative_6 = Text(
            "La segunda mitad mezcla el hash, d y k: si k se repite, la firma deja de ser segura.",
            font="Cambria",
        ).scale(0.46).to_edge(UP)
        s_formula = Text("s = k⁻¹(H(m) + r·d)", font="Cambria Math", color=WHITE).scale(0.58)
        s_formula.move_to(DOWN * 2.85)
        s_value_text = Text(f"s = {s_value}", font="Cambria Math", color=WHITE).scale(0.54)
        s_value_text.next_to(s_formula, DOWN, buff=0.20)
        self.play(Transform(title, narrative_6), ReplacementTransform(r_formula, s_formula), run_time=1.3)
        self.play(FadeIn(s_value_text), run_time=1.0)
        self.wait(2.9)

        narrative_7 = Text(
            "La firma que viaja junto al mensaje es solo el par (r, s).",
            font="Cambria",
        ).scale(0.55).to_edge(UP)
        signature_box = RoundedRectangle(
            corner_radius=0.08,
            width=1.90,
            height=0.90,
            color=PURPLE,
            fill_color="#221633",
            fill_opacity=0.90,
        ).move_to(LEFT * 3.10 + DOWN * 1.65)
        signature_label = Text(f"(r, s) = ({r_value}, {s_value})", font="Cambria Math", color=PURPLE).scale(0.38)
        signature_label.move_to(signature_box)
        signature_formula = Text(f"(r, s) = ({r_value}, {s_value})", font="Cambria Math", color=PURPLE).scale(0.58)
        signature_formula.move_to(DOWN * 2.85)
        self.play(
            Transform(title, narrative_7),
            ReplacementTransform(s_formula, signature_formula),
            FadeOut(s_value_text),
            run_time=1.3,
        )
        self.play(TransformFromCopy(VGroup(r_label, nonce_obj[1]), signature_box), FadeIn(signature_label), run_time=1.2)
        self.wait(2.5)

        narrative_8 = Text(
            "El verificador usa H(m), Q y (r,s), pero nunca necesita conocer d.",
            font="Cambria",
        ).scale(0.50).to_edge(UP)
        verify_formula = Text("H(m) + Q + (r,s)  →  válido", font="Cambria Math", color=GREEN).scale(0.54)
        verify_formula.move_to(DOWN * 2.85)
        verify_arrow = Arrow(
            signature_box.get_right(),
            RIGHT * 0.40 + DOWN * 1.65,
            buff=0.16,
            color=GREEN,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.08,
        )
        check = Text("válido", font="Cambria", color=GREEN).scale(0.50)
        check.move_to(RIGHT * 1.15 + DOWN * 1.65)
        self.play(Transform(title, narrative_8), ReplacementTransform(signature_formula, verify_formula), run_time=1.3)
        self.play(Create(verify_arrow), FadeIn(check), Indicate(public_obj[0], color=YELLOW, scale_factor=1.25), run_time=1.4)
        self.wait(2.7)

        narrative_9 = Text(
            "Así se demuestra autoría: cualquiera verifica la firma, solo quien conoce d puede crearla.",
            font="Cambria",
        ).scale(0.45).to_edge(UP)
        final_formula = Text("firma pública, clave privada", font="Cambria Math", color=WHITE).scale(0.58)
        final_formula.move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_9), ReplacementTransform(verify_formula, final_formula), run_time=1.3)
        self.play(Indicate(signature_box, color=PURPLE, scale_factor=1.05), Flash(public_obj[0], color=YELLOW, flash_radius=0.45), run_time=1.1)
        self.wait(3.5)

    def field_to_point(self, x, y, p, offset):
        spacing = 0.25
        return offset + RIGHT * ((x - (p - 1) / 2) * spacing) + UP * ((y - (p - 1) / 2) * spacing)

    def make_field_grid(self, p, offset):
        grid = VGroup()
        for x in range(p):
            for y in range(p):
                dot = Dot(self.field_to_point(x, y, p, offset), color=GRAY, radius=0.012)
                dot.set_opacity(0.42)
                grid.add(dot)

        for value in [0, p - 1]:
            x_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.22)
            x_label.next_to(self.field_to_point(value, 0, p, offset), DOWN, buff=0.08)
            y_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.22)
            y_label.next_to(self.field_to_point(0, value, p, offset), LEFT, buff=0.08)
            grid.add(x_label, y_label)

        return grid

    def make_solution_cloud(self, p, a, b, offset):
        cloud = VGroup()
        for x in range(p):
            rhs = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y - rhs) % p == 0:
                    cloud.add(Dot(self.field_to_point(x, y, p, offset), color=BLUE, radius=0.050))
        return cloud

    def point_with_label(self, point, p, label, color, direction, offset, scale=0.38):
        dot = Dot(self.field_to_point(*point, p, offset), color=color, radius=0.080).set_z_index(5)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
        text.next_to(dot, direction, buff=0.08)
        return VGroup(dot, text)

    def ec_add(self, point_1, point_2, p, a):
        if point_1 is None:
            return point_2
        if point_2 is None:
            return point_1

        x1, y1 = point_1
        x2, y2 = point_2
        if x1 == x2 and (y1 + y2) % p == 0:
            return None

        if point_1 == point_2:
            slope = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p
        else:
            slope = ((y2 - y1) * pow(x2 - x1, -1, p)) % p

        x3 = (slope * slope - x1 - x2) % p
        y3 = (slope * (x1 - x3) - y1) % p
        return (x3, y3)

    def ec_mul(self, scalar, point, p, a):
        result = None
        addend = point
        while scalar:
            if scalar & 1:
                result = self.ec_add(result, addend, p, a)
            addend = self.ec_add(addend, addend, p, a)
            scalar >>= 1
        return result
