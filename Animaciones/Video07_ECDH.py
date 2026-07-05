from manim import *


class ECDH(Scene):
    def construct(self):
        p = 17
        a = 2
        b = 2
        base = (5, 1)
        alice_k = 5
        bob_k = 7
        alice_public = self.ec_mul(alice_k, base, p, a)
        bob_public = self.ec_mul(bob_k, base, p, a)
        secret = self.ec_mul(alice_k, bob_public, p, a)

        left = LEFT * 3.0 + DOWN * 0.08
        right = RIGHT * 3.0 + DOWN * 0.08

        title = Text("Intercambio de claves ECDH", font="Cambria").scale(0.57).to_edge(UP)
        self.play(Write(title))

        alice_grid = self.make_field_grid(p, left)
        bob_grid = self.make_field_grid(p, right)
        alice_cloud = self.make_solution_cloud(p, a, b, left)
        bob_cloud = self.make_solution_cloud(p, a, b, right)

        alice_name = Text("Alice", font="Cambria", color=YELLOW).scale(0.50)
        bob_name = Text("Bob", font="Cambria", color=RED).scale(0.50)
        alice_name.move_to(left + UP * 2.0)
        bob_name.move_to(right + UP * 2.0)

        formula = Text("y² ≡ x³ + 2x + 2   (mod 17)", font="Cambria Math", color=WHITE).scale(0.58)
        formula.move_to(DOWN * 3.45)

        self.play(
            Create(alice_grid),
            Create(bob_grid),
            LaggedStart(*[GrowFromCenter(dot) for dot in alice_cloud], lag_ratio=0.02),
            LaggedStart(*[GrowFromCenter(dot) for dot in bob_cloud], lag_ratio=0.02),
            FadeIn(alice_name),
            FadeIn(bob_name),
            Write(formula),
            run_time=2.6,
        )

        narrative_1 = Text(
            "Alice y Bob usan la misma curva y el mismo punto público P.",
            font="Cambria",
        ).scale(0.51).to_edge(UP)
        base_alice = self.point_with_label(base, p, "P", GREEN, UP + LEFT, left, scale=0.38)
        base_bob = self.point_with_label(base, p, "P", GREEN, DOWN + RIGHT, right, scale=0.38)
        public_p = Text("P es público", font="Cambria Math", color=GREEN).scale(0.58)
        public_p.move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_1), run_time=1.2)
        self.play(FadeIn(base_alice), FadeIn(base_bob), ReplacementTransform(formula, public_p), run_time=1.4)
        self.play(Flash(base_alice[0], color=GREEN, flash_radius=0.36), Flash(base_bob[0], color=GREEN, flash_radius=0.36), run_time=1.0)
        self.wait(2.1)

        narrative_2 = Text(
            "Después cada uno elige un número secreto, que no se envía.",
            font="Cambria",
        ).scale(0.52).to_edge(UP)
        alice_secret = Text("a = 5", font="Cambria Math", color=YELLOW).scale(0.46)
        bob_secret = Text("b = 7", font="Cambria Math", color=RED).scale(0.46)
        alice_secret.next_to(alice_name, DOWN, buff=0.12)
        bob_secret.next_to(bob_name, DOWN, buff=0.12)
        secret_text = Text("a y b son privados", font="Cambria Math", color=WHITE).scale(0.58)
        secret_text.move_to(DOWN * 2.85)
        self.play(
            Transform(title, narrative_2),
            FadeIn(alice_secret),
            FadeIn(bob_secret),
            ReplacementTransform(public_p, secret_text),
            run_time=1.3,
        )
        self.wait(2.2)

        narrative_3 = Text(
            "Con esos secretos calculan puntos públicos: A = aP y B = bP.",
            font="Cambria",
        ).scale(0.50).to_edge(UP)
        alice_pub_obj = self.point_with_label(alice_public, p, "A", YELLOW, DOWN + RIGHT, left, scale=0.39)
        bob_pub_obj = self.point_with_label(bob_public, p, "B", RED, RIGHT, right, scale=0.39)
        public_keys = Text("A = aP          B = bP", font="Cambria Math", color=WHITE).scale(0.58)
        public_keys.move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_3), ReplacementTransform(secret_text, public_keys), run_time=1.3)
        self.play(
            TransformFromCopy(base_alice[0], alice_pub_obj[0]),
            TransformFromCopy(base_bob[0], bob_pub_obj[0]),
            FadeIn(alice_pub_obj[1]),
            FadeIn(bob_pub_obj[1]),
            run_time=1.4,
        )
        self.play(Flash(alice_pub_obj[0], color=YELLOW, flash_radius=0.4), Flash(bob_pub_obj[0], color=RED, flash_radius=0.4), run_time=1.0)
        self.wait(2.0)

        narrative_4 = Text(
            "Solo intercambian A y B; los secretos a y b se quedan en su lado.",
            font="Cambria",
        ).scale(0.50).to_edge(UP)
        exchange_text = Text("A y B viajan por el canal público", font="Cambria Math", color=WHITE).scale(0.54)
        exchange_text.move_to(DOWN * 2.85)
        send_a = Arrow(
            left + UP * 2.35,
            right + UP * 2.35,
            buff=0.24,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.04,
        )
        send_b = Arrow(
            right + DOWN * 2.15,
            left + DOWN * 2.15,
            buff=0.24,
            color=RED,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.04,
        )
        label_a = Text("A", font="Cambria Math", color=YELLOW).scale(0.44).next_to(send_a, UP, buff=0.06)
        label_b = Text("B", font="Cambria Math", color=RED).scale(0.44).next_to(send_b, UP, buff=0.06)
        self.play(Transform(title, narrative_4), ReplacementTransform(public_keys, exchange_text), run_time=1.3)
        self.play(Create(send_a), FadeIn(label_a), run_time=1.1)
        self.play(Create(send_b), FadeIn(label_b), run_time=1.1)
        self.wait(2.0)

        narrative_5 = Text(
            "Alice calcula aB y Bob calcula bA.",
            font="Cambria",
        ).scale(0.55).to_edge(UP)
        shared_formula = Text("aB = bA", font="Cambria Math", color=WHITE).scale(0.62)
        shared_formula.move_to(DOWN * 2.85)
        s_alice = self.point_with_label(secret, p, "S", PURPLE, UP + RIGHT, left, scale=0.40)
        s_bob = self.point_with_label(secret, p, "S", PURPLE, UP + RIGHT, right, scale=0.40)
        self.play(Transform(title, narrative_5), ReplacementTransform(exchange_text, shared_formula), run_time=1.3)
        self.play(
            TransformFromCopy(bob_pub_obj[0], s_alice[0]),
            TransformFromCopy(alice_pub_obj[0], s_bob[0]),
            FadeIn(s_alice[1]),
            FadeIn(s_bob[1]),
            run_time=1.5,
        )
        self.play(Flash(s_alice[0], color=PURPLE, flash_radius=0.45), Flash(s_bob[0], color=PURPLE, flash_radius=0.45), run_time=1.0)
        self.wait(2.0)

        narrative_6 = Text(
            "Los dos caminos llegan al mismo punto S sin revelar los números secretos.",
            font="Cambria",
        ).scale(0.48).to_edge(UP)
        final_formula = Text("aB = bA = abP = S", font="Cambria Math", color=PURPLE).scale(0.64)
        final_formula.move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_6), ReplacementTransform(shared_formula, final_formula), run_time=1.3)
        self.play(Indicate(final_formula, color=PURPLE, scale_factor=1.05), run_time=1.1)
        self.wait(3.5)

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

    def point_with_label(self, point, p, label, color, direction, offset, scale=0.34):
        dot = Dot(self.field_to_point(*point, p, offset), color=color, radius=0.065).set_z_index(5)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
        text.next_to(dot, direction, buff=0.07)
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
