from manim import *


class LogaritmoDiscreto(Scene):
    def construct(self):
        p = 17
        a = 2
        b = 2
        base = (5, 1)
        secret = 11
        target = self.ec_mul(secret, base, p, a)
        chain = [self.ec_mul(i, base, p, a) for i in range(1, secret + 1)]

        title = Text("El problema del logaritmo discreto", font="Cambria").scale(0.54).to_edge(UP)
        self.play(Write(title))

        field = self.make_field_grid(p)
        cloud = self.make_solution_cloud(p, a, b)
        formula = Text("y² ≡ x³ + 2x + 2   (mod 17)", font="Cambria Math", color=WHITE).scale(0.58)
        formula.move_to(DOWN * 3.45)

        self.play(Create(field), LaggedStart(*[GrowFromCenter(dot) for dot in cloud], lag_ratio=0.02), Write(formula), run_time=2.0)

        p_obj = self.point_with_label(base, p, "P", YELLOW, UP + LEFT)
        self.play(FadeIn(p_obj), Flash(p_obj[0], color=YELLOW, flash_radius=0.45), run_time=0.8)

        narrative_1 = Text(
            "Partimos de un punto público P sobre la curva.",
            font="Cambria",
        ).scale(0.53).to_edge(UP)
        self.play(Transform(title, narrative_1))
        self.wait(1.5)

        forward_formula = Text("Q = kP", font="Cambria Math", color=WHITE).scale(0.58)
        forward_formula.move_to(DOWN * 2.9)
        known_k = Text("k = 11", font="Cambria Math", color=YELLOW).scale(0.5)
        known_k.next_to(forward_formula, DOWN, buff=0.28)

        narrative_2 = Text(
            "Si conocemos k, calcular Q = kP es repetir la suma de P.",
            font="Cambria",
        ).scale(0.50).to_edge(UP)
        self.play(Transform(title, narrative_2), ReplacementTransform(formula, forward_formula), FadeIn(known_k), run_time=0.9)
        self.wait(1.35)

        path = self.path_from_points(chain, p, GREEN, stroke_width=3)
        q_obj = self.point_with_label(target, p, "Q", RED, UP + RIGHT)
        q_obj[1].shift(RIGHT * 0.08 + UP * 0.03)
        self.play(Create(path), run_time=2.3)
        self.play(FadeIn(q_obj), Flash(q_obj[0], color=RED, flash_radius=0.55), run_time=0.8)
        self.wait(0.8)

        narrative_3 = Text(
            "Hacia delante es fácil: hacemos 11 saltos y llegamos a Q.",
            font="Cambria",
        ).scale(0.52).to_edge(UP)
        self.play(Transform(title, narrative_3))
        self.wait(1.8)

        inverse_formula = Text("? · P = Q", font="Cambria Math", color=WHITE).scale(0.58)
        inverse_formula.move_to(DOWN * 2.72)
        inverse_question = Text("¿Cuál es k?", font="Cambria Math", color=YELLOW).scale(0.5)
        inverse_question.next_to(inverse_formula, DOWN, buff=0.22)

        narrative_4 = Text(
            "El problema inverso pregunta: si solo conocemos P y Q, ¿cuál era k?",
            font="Cambria",
        ).scale(0.47).to_edge(UP)
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(forward_formula, inverse_formula),
            ReplacementTransform(known_k, inverse_question),
            run_time=1.0,
        )
        self.wait(1.8)

        self.play(path.animate.set_opacity(0.25), run_time=0.6)
        guesses = self.make_guess_paths(p)
        narrative_5 = Text(
            "Probar hacia atrás no revela una dirección clara: muchos caminos parecen posibles.",
            font="Cambria",
        ).scale(0.44).to_edge(UP)
        self.play(Transform(title, narrative_5))
        self.wait(0.5)
        self.play(LaggedStart(*[Create(route) for route in guesses], lag_ratio=0.12), run_time=2.0)
        self.wait(1.35)

        highlight = SurroundingRectangle(inverse_formula, color=RED, buff=0.18)
        hard_label = Text("Difícil de invertir", font="Cambria Math", color=RED).scale(0.46)
        hard_label.next_to(inverse_question, DOWN, buff=0.14)

        narrative_6 = Text(
            "En campos enormes, encontrar k por prueba y error deja de ser viable.",
            font="Cambria",
        ).scale(0.49).to_edge(UP)
        self.play(Transform(title, narrative_6))
        self.wait(0.6)
        self.play(Create(highlight), FadeIn(hard_label), run_time=0.9)
        self.wait(1.6)

        narrative_7 = Text(
            "Esa asimetría, fácil en un sentido y difícil en el otro, sostiene la seguridad de ECC.",
            font="Cambria",
        ).scale(0.44).to_edge(UP)
        self.play(Transform(title, narrative_7))
        self.wait(0.6)
        self.play(Indicate(inverse_formula, color=RED, scale_factor=1.06), Flash(q_obj[0], color=RED, flash_radius=0.55), run_time=1.1)
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

    def point_with_label(self, point, p, label, color, direction, scale=0.36):
        dot = Dot(self.field_to_point(*point, p), color=color, radius=0.09).set_z_index(5)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
        text.next_to(dot, direction, buff=0.08)
        return VGroup(dot, text)

    def path_from_points(self, points, p, color, stroke_width=3, opacity=1.0):
        path = VGroup()
        for start, end in zip(points, points[1:]):
            segment = Line(
                self.field_to_point(*start, p),
                self.field_to_point(*end, p),
                color=color,
                stroke_width=stroke_width,
            ).set_opacity(opacity)
            path.add(segment)
        return path

    def make_guess_paths(self, p):
        routes = [
            [(5, 1), (9, 16), (0, 6), (7, 11), (13, 10)],
            [(5, 1), (3, 16), (10, 11), (13, 7), (13, 10)],
            [(5, 1), (16, 13), (7, 6), (9, 1), (13, 10)],
            [(5, 1), (10, 6), (16, 4), (3, 1), (13, 10)],
        ]
        return VGroup(
            *[
                self.path_from_points(route, p, GRAY, stroke_width=2, opacity=0.28)
                for route in routes
            ]
        )

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
